"""Offline contracts for pending follow requests and single-attempt decisions."""

import inspect
import json
from typing import get_type_hints
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

import pytest
import requests
import responses

from tweetapi import (
    AuthenticationError, ForbiddenError, NetworkError, NotFoundError,
    RateLimitError, ServerError, TweetAPI, TweetAPIError, ValidationError,
    paginate, paginate_pages,
)
from tweetapi.resources.interaction import InteractionResource
from tweetapi.types import FollowRequestsResponse, Pagination

BASE = "https://api.tweetapi.com/tw-v2/interaction"
LONG_ID = "9007199254740993123"
AUTH = "test-auth-token"
PROXY = "host:8080@user:pass"
DECISIONS = ("accept", "deny")


def page(ids=None, next_cursor=None, prev_cursor=None):
    return {"data": ids if ids is not None else [LONG_ID], "pagination": {
        "nextCursor": next_cursor, "prevCursor": prev_cursor,
    }}


def action(decision):
    return {"data": {"id": LONG_ID, "action": f"{decision}_follow_request",
                     "timestamp": "2026-09-14T00:00:00.000Z", "success": True,
                     "metadata": {"user_id": LONG_ID}}}


def query(call):
    return parse_qs(urlsplit(call.request.url).query)


@pytest.mark.parametrize("method,required,optional", [
    ("get_follow_requests", {"auth_token"}, {"proxy", "cursor", "count"}),
    ("accept_follow_request", {"auth_token", "user_id"}, {"proxy"}),
    ("deny_follow_request", {"auth_token", "user_id"}, {"proxy"}),
])
def test_keyword_only_contract(method, required, optional):
    params = dict(inspect.signature(getattr(InteractionResource, method)).parameters)
    params.pop("self")
    assert set(params) == required | optional
    assert all(p.kind == inspect.Parameter.KEYWORD_ONLY for p in params.values())
    assert all(params[k].default is inspect.Parameter.empty for k in required)
    assert all(params[k].default is None for k in optional)


def test_concrete_ids_page_type():
    assert get_type_hints(FollowRequestsResponse) == {
        "data": list[str], "pagination": Pagination,
    }
    assert FollowRequestsResponse.__required_keys__ == {"data", "pagination"}


@pytest.mark.parametrize("options,expected", [
    ({}, {}),
    ({"proxy": None, "cursor": None, "count": None}, {}),
    ({"proxy": PROXY, "cursor": "-1", "count": 100},
     {"proxy": [PROXY], "cursor": ["-1"], "count": ["100"]}),
    ({"cursor": "opaque+/=cursor", "count": 1},
     {"cursor": ["opaque+/=cursor"], "count": ["1"]}),
])
@responses.activate
def test_list_query_and_precise_response(options, expected):
    payload = page()
    responses.get(f"{BASE}/follow-requests", json=payload)
    result = TweetAPI(api_key="test-key").interaction.get_follow_requests(
        auth_token=AUTH, **options,
    )
    assert result == payload
    assert isinstance(result["data"][0], str)
    assert query(responses.calls[0]) == {"authToken": [AUTH], **expected}
    assert responses.calls[0].request.body is None
    assert responses.calls[0].request.headers["X-API-Key"] == "test-key"
    assert len(responses.calls) == 1


@pytest.mark.parametrize("helper", [paginate, paginate_pages])
@responses.activate
def test_empty_page_is_valid_and_stops(helper):
    responses.get(f"{BASE}/follow-requests", json=page([]))
    client = TweetAPI(api_key="test-key")
    result = list(helper(lambda cursor: client.interaction.get_follow_requests(
        auth_token=AUTH, cursor=cursor,
    )))
    assert result == ([] if helper is paginate else [page([])])
    assert len(responses.calls) == 1


@pytest.mark.parametrize("helper", [paginate, paginate_pages])
@responses.activate
def test_multiple_pages_keep_ids_and_opaque_cursors(helper):
    pages = [page(next_cursor="opaque+/="), page([], "next", "previous"),
             page(["18446744073709551615"], None, "opaque+/=")]
    for payload in pages:
        responses.get(f"{BASE}/follow-requests", json=payload)
    client = TweetAPI(api_key="test-key")
    result = list(helper(lambda cursor: client.interaction.get_follow_requests(
        auth_token=AUTH, cursor=cursor, count=1, proxy=PROXY,
    )))
    assert result == ([LONG_ID, "18446744073709551615"] if helper is paginate else pages)
    assert [query(c).get("cursor") for c in responses.calls] == [None, ["opaque+/="], ["next"]]
    assert all(query(c)["count"] == ["1"] for c in responses.calls)
    assert all(query(c)["proxy"] == [PROXY] for c in responses.calls)
    assert len(responses.calls) == 3


@pytest.mark.parametrize("decision", DECISIONS)
@pytest.mark.parametrize("options,extra", [({}, {}), ({"proxy": None}, {}),
                                         ({"proxy": PROXY}, {"proxy": PROXY})])
@responses.activate
def test_action_body_and_response(decision, options, extra):
    payload = action(decision)
    responses.post(f"{BASE}/{decision}-follow-request", json=payload)
    method = getattr(TweetAPI(api_key="test-key").interaction, f"{decision}_follow_request")
    assert method(auth_token=AUTH, user_id=LONG_ID, **options) == payload
    request = responses.calls[0].request
    assert json.loads(request.body) == {"authToken": AUTH, "userId": LONG_ID, **extra}
    assert urlsplit(request.url).query == ""
    assert len(responses.calls) == 1


@pytest.mark.parametrize("decision", DECISIONS)
@pytest.mark.parametrize("status,error_type", [(429, RateLimitError), (500, ServerError),
                                               (502, ServerError), (503, ServerError),
                                               (504, ServerError)])
@responses.activate
def test_decisions_never_retry_transient_status_with_default_config(decision, status, error_type):
    url = f"{BASE}/{decision}-follow-request"
    responses.post(url, json={"statusCode": status, "message": "Upstream failure"}, status=status)
    success = responses.post(url, json=action(decision))
    client = TweetAPI(api_key="test-key")
    with patch("tweetapi.client.time.sleep") as sleep, pytest.raises(error_type) as exc:
        getattr(client.interaction, f"{decision}_follow_request")(auth_token=AUTH, user_id=LONG_ID)
    assert exc.value.message == "Upstream failure"
    assert exc.value.status_code == status
    sleep.assert_not_called()
    assert len(responses.calls) == 1
    assert success.call_count == 0


@pytest.mark.parametrize("decision", DECISIONS)
@pytest.mark.parametrize("failure", [requests.exceptions.Timeout, requests.exceptions.ConnectTimeout,
                                    requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError])
@responses.activate
def test_decisions_never_retry_network_failure_with_default_config(decision, failure):
    url = f"{BASE}/{decision}-follow-request"
    responses.post(url, body=failure("synthetic failure"))
    success = responses.post(url, json=action(decision))
    client = TweetAPI(api_key="test-key")
    with patch("tweetapi.client.time.sleep") as sleep, pytest.raises(NetworkError) as exc:
        getattr(client.interaction, f"{decision}_follow_request")(auth_token=AUTH, user_id=LONG_ID)
    assert isinstance(exc.value.__cause__, failure)
    sleep.assert_not_called()
    assert len(responses.calls) == 1
    assert success.call_count == 0


@pytest.mark.parametrize("failure", [429, 503, requests.exceptions.Timeout("timeout"),
                                    requests.exceptions.ConnectionError("connection")])
@responses.activate
def test_reads_keep_normal_retries(failure):
    if isinstance(failure, int):
        responses.get(f"{BASE}/follow-requests", json={"statusCode": failure, "message": "Retry"}, status=failure)
    else:
        responses.get(f"{BASE}/follow-requests", body=failure)
    responses.get(f"{BASE}/follow-requests", json=page())
    with patch("tweetapi.client.time.sleep") as sleep:
        assert TweetAPI(api_key="test-key").interaction.get_follow_requests(auth_token=AUTH) == page()
    sleep.assert_called_once()
    assert len(responses.calls) == 2


@pytest.mark.parametrize("method", ["get_follow_requests", "accept_follow_request", "deny_follow_request"])
@pytest.mark.parametrize("status,error_type", [(400, ValidationError), (401, AuthenticationError),
                                               (403, ForbiddenError), (404, NotFoundError),
                                               (422, TweetAPIError)])
@responses.activate
def test_actual_tw_v2_error_envelope(method, status, error_type):
    # error.middleware.ts sends {statusCode, message} for /tw-v2 routes.
    is_read = method == "get_follow_requests"
    path = "follow-requests" if is_read else method.replace("_", "-")
    responses.add(responses.GET if is_read else responses.POST, f"{BASE}/{path}",
                  json={"statusCode": status, "message": "Invalid follow request"}, status=status)
    options = {"auth_token": AUTH} if is_read else {"auth_token": AUTH, "user_id": LONG_ID}
    with pytest.raises(error_type) as exc:
        getattr(TweetAPI(api_key="test-key").interaction, method)(**options)
    assert exc.value.message == "Invalid follow request"
    assert exc.value.code == "UNKNOWN_ERROR"
    assert exc.value.status_code == status
    assert exc.value.details is None
    assert len(responses.calls) == 1


@responses.activate
def test_nested_error_parsing_still_takes_precedence():
    responses.post(f"{BASE}/accept-follow-request", status=400, json={
        "message": "legacy fallback", "error": {
            "code": "VALIDATION_ERROR", "message": "Invalid ID", "details": {"field": "userId"},
        },
    })
    with pytest.raises(ValidationError) as exc:
        TweetAPI(api_key="test-key").interaction.accept_follow_request(auth_token=AUTH, user_id="bad")
    assert exc.value.message == "Invalid ID"
    assert exc.value.code == "VALIDATION_ERROR"
    assert exc.value.details == {"field": "userId"}


@pytest.mark.parametrize("payload", [[], ["unexpected"], "unexpected", 42, None, {"message": []}])
@responses.activate
def test_malformed_error_json_remains_http_error(payload):
    responses.post(f"{BASE}/deny-follow-request", body=json.dumps(payload), status=502,
                   content_type="application/json")
    with pytest.raises(ServerError) as exc:
        TweetAPI(api_key="test-key").interaction.deny_follow_request(auth_token=AUTH, user_id=LONG_ID)
    assert exc.value.message == "HTTP 502"
    assert exc.value.code == "UNKNOWN_ERROR"
    assert len(responses.calls) == 1


@pytest.mark.parametrize("status", [200, 502])
@responses.activate
def test_invalid_json_never_becomes_success(status):
    responses.post(f"{BASE}/accept-follow-request", body="not JSON", status=status)
    with pytest.raises(ValueError if status == 200 else ServerError):
        TweetAPI(api_key="test-key").interaction.accept_follow_request(auth_token=AUTH, user_id=LONG_ID)
    assert len(responses.calls) == 1
