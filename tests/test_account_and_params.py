"""Offline contracts for account usage and the optional parameters added in 2.6.0."""

import inspect
import json
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

import pytest
import responses

from tweetapi import ServerError, TweetAPI
from tweetapi.resources.account import AccountResource
from tweetapi.types import AccountUsage

BASE = "https://api.tweetapi.com/tw-v2"
USAGE_URL = f"{BASE}/account/usage"
AUTH = "test-auth-token"

USAGE: AccountUsage = {
    "availableUnits": 120500,
    "plan": {
        "active": True,
        "requestLimit": 100000,
        "usedUnits": 4500,
        "remainingUnits": 95500,
        "periodEnd": "2026-11-21T00:00:00.000Z",
    },
    "payg": {"availableUnits": 25000, "expiresAt": "2027-10-21T00:00:00.000Z"},
    "rateLimit": {"requestsPerMinute": 120},
}


def make_client(**kwargs):
    defaults = {"api_key": "test-key", "initial_retry_delay": 0.01, "max_retry_delay": 0.1}
    defaults.update(kwargs)
    return TweetAPI(**defaults)


def body(call):
    return json.loads(call.request.body)


def test_get_usage_takes_no_arguments():
    assert list(inspect.signature(AccountResource.get_usage).parameters) == ["self"]


@responses.activate
def test_get_usage_sends_get_without_query():
    responses.add(responses.GET, USAGE_URL, json={"data": USAGE})
    result = make_client().account.get_usage()

    request = responses.calls[0].request
    assert request.method == "GET"
    assert request.url == USAGE_URL
    assert request.headers["X-API-Key"] == "test-key"
    assert result == {"data": USAGE}


@responses.activate
def test_get_usage_keeps_null_plan_and_payg():
    payg_only = {**USAGE, "plan": None, "payg": None}
    responses.add(responses.GET, USAGE_URL, json={"data": payg_only})
    assert make_client().account.get_usage()["data"] == payg_only


@responses.activate
def test_get_usage_retries_after_503_with_retry_after():
    responses.add(responses.GET, USAGE_URL, status=503, headers={"Retry-After": "1"},
                  json={"statusCode": 503, "message": "unavailable"})
    responses.add(responses.GET, USAGE_URL, json={"data": USAGE})
    with patch("tweetapi.client.time.sleep"):
        assert make_client().account.get_usage()["data"] == USAGE
    assert len(responses.calls) == 2


@responses.activate
def test_get_usage_raises_server_error_without_retries():
    responses.add(responses.GET, USAGE_URL, status=503,
                  json={"statusCode": 503, "message": "unavailable"})
    with pytest.raises(ServerError):
        make_client(max_retries=0).account.get_usage()


@responses.activate
def test_community_tweets_sort_by_is_optional():
    url = f"{BASE}/community/tweets"
    responses.add(responses.GET, url, json={"data": [], "pagination": {"nextCursor": None, "prevCursor": None}})
    client = make_client()

    client.community.get_tweets(community_id="1493446837214187523")
    assert parse_qs(urlsplit(responses.calls[0].request.url).query) == {"communityId": ["1493446837214187523"]}

    client.community.get_tweets(community_id="1493446837214187523", sort_by="Recency")
    assert parse_qs(urlsplit(responses.calls[1].request.url).query)["sortBy"] == ["Recency"]


@pytest.mark.parametrize("action", ["follow", "unfollow"])
@responses.activate
def test_follow_sends_username_only_when_set(action):
    responses.add(responses.POST, f"{BASE}/interaction/{action}", json={"data": {"success": True}})
    method = getattr(make_client().interaction, action)

    method(auth_token=AUTH, user_id="44196397", username="elonmusk")
    assert body(responses.calls[0]) == {"authToken": AUTH, "userId": "44196397", "username": "elonmusk"}

    method(auth_token=AUTH, user_id="44196397")
    assert body(responses.calls[1]) == {"authToken": AUTH, "userId": "44196397"}


@responses.activate
def test_xchat_send_conversation_fields_only_when_set():
    responses.add(responses.POST, f"{BASE}/xchat/send", json={"data": {}})
    client = make_client()
    base = {"authToken": AUTH, "recipientId": "44196397", "message": "hi"}

    client.xchat.send(auth_token=AUTH, recipient_id="44196397", message="hi",
                      conversation_token="TOKEN", conversation_key_version="1",
                      encrypted_conversation_key="KEY")
    assert body(responses.calls[0]) == {
        **base, "conversationToken": "TOKEN", "conversationKeyVersion": "1",
        "encryptedConversationKey": "KEY",
    }

    client.xchat.send(auth_token=AUTH, recipient_id="44196397", message="hi")
    assert body(responses.calls[1]) == base
