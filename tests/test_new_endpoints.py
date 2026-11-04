"""Offline contracts for the endpoints added in 2.7.0."""

import inspect
import json
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

import pytest
import responses

from tweetapi import ServerError, TweetAPI
from tweetapi.resources.trends import TrendsResource

BASE = "https://api.tweetapi.com/tw-v2"
AUTH = "test-auth-token"
PROXY = "host:8080@user:pass"
USER_ID = "44196397"
TWEET_ID = "1971008286821380096"
LIST_ID = "1585430245762441216"
PAGE = {"data": [], "pagination": {"nextCursor": None, "prevCursor": None}}


def make_client():
    return TweetAPI(api_key="test-key", max_retries=0)


def query(call):
    return parse_qs(urlsplit(call.request.url).query)


def body(call):
    return json.loads(call.request.body)


def method_of(client, resource, method):
    return getattr(getattr(client, resource), method)


# resource, method, path, required kwargs and their query, optional kwargs and their query
READS = [
    ("user", "get_photos", "/user/photos",
     {"user_id": USER_ID}, {"userId": USER_ID}, {"cursor": "c1"}, {"cursor": "c1"}),
    ("user", "get_videos", "/user/videos",
     {"user_id": USER_ID}, {"userId": USER_ID}, {"cursor": "c1"}, {"cursor": "c1"}),
    ("user", "get_affiliates", "/user/affiliates",
     {"user_id": USER_ID}, {"userId": USER_ID}, {"cursor": "c1"}, {"cursor": "c1"}),
    ("user", "get_lists", "/user/lists",
     {"user_id": USER_ID}, {"userId": USER_ID}, {"cursor": "c1"}, {"cursor": "c1"}),
    ("user", "get_list_memberships", "/user/list-memberships",
     {"user_id": USER_ID}, {"userId": USER_ID}, {"cursor": "c1"}, {"cursor": "c1"}),
    ("user", "get_highlights", "/user/highlights",
     {"user_id": USER_ID}, {"userId": USER_ID}, {"cursor": "c1"}, {"cursor": "c1"}),
    ("user", "get_articles", "/user/articles",
     {"user_id": USER_ID}, {"userId": USER_ID}, {"cursor": "c1"}, {"cursor": "c1"}),
    ("user", "get_similar_accounts", "/user/similar-accounts",
     {"user_id": USER_ID}, {"userId": USER_ID}, {}, {}),
    ("tweet", "get_hidden_replies", "/tweet/hidden-replies",
     {"tweet_id": TWEET_ID}, {"tweetId": TWEET_ID}, {"cursor": "c1"}, {"cursor": "c1"}),
    ("list", "search", "/list/search",
     {"query": "crypto news"}, {"query": "crypto news"}, {"cursor": "c1"}, {"cursor": "c1"}),
    ("community", "get_media", "/community/media",
     {"community_id": "1493446837214187523"}, {"communityId": "1493446837214187523"},
     {"cursor": "c1"}, {"cursor": "c1"}),
    ("interaction", "get_bookmarks", "/interaction/bookmarks",
     {"auth_token": AUTH}, {"authToken": AUTH},
     {"cursor": "c1", "proxy": PROXY}, {"cursor": "c1", "proxy": PROXY}),
    ("interaction", "get_likes", "/interaction/likes",
     {"auth_token": AUTH, "user_id": USER_ID}, {"authToken": AUTH, "userId": USER_ID},
     {"cursor": "c1", "proxy": PROXY}, {"cursor": "c1", "proxy": PROXY}),
    ("interaction", "get_blocked_accounts", "/interaction/blocked-accounts",
     {"auth_token": AUTH}, {"authToken": AUTH},
     {"cursor": "c1", "proxy": PROXY}, {"cursor": "c1", "proxy": PROXY}),
    ("interaction", "get_muted_accounts", "/interaction/muted-accounts",
     {"auth_token": AUTH}, {"authToken": AUTH},
     {"cursor": "c1", "proxy": PROXY}, {"cursor": "c1", "proxy": PROXY}),
]
READ_IDS = [f"{r[0]}.{r[1]}" for r in READS]


@pytest.mark.parametrize("resource,method,path,required,_q,optional,_oq", READS, ids=READ_IDS)
def test_read_signature(resource, method, path, required, _q, optional, _oq):
    params = dict(inspect.signature(method_of(make_client(), resource, method)).parameters)
    assert set(params) == set(required) | set(optional)
    assert all(p.kind == inspect.Parameter.KEYWORD_ONLY for p in params.values())
    assert all(params[k].default is inspect.Parameter.empty for k in required)
    assert all(params[k].default is None for k in optional)


@pytest.mark.parametrize("resource,method,path,required,expected,_o,_oq", READS, ids=READ_IDS)
@responses.activate
def test_read_sends_get_and_drops_unset_optionals(resource, method, path, required, expected, _o, _oq):
    responses.get(f"{BASE}{path}", json=PAGE)
    assert method_of(make_client(), resource, method)(**required) == PAGE

    request = responses.calls[0].request
    assert request.method == "GET"
    assert urlsplit(request.url).path == f"/tw-v2{path}"
    assert query(responses.calls[0]) == {k: [v] for k, v in expected.items()}
    assert request.body is None


@pytest.mark.parametrize("resource,method,path,required,expected,optional,extra", READS, ids=READ_IDS)
@responses.activate
def test_read_sends_optionals_when_set(resource, method, path, required, expected, optional, extra):
    responses.get(f"{BASE}{path}", json=PAGE)
    method_of(make_client(), resource, method)(**required, **optional)
    assert query(responses.calls[0]) == {k: [v] for k, v in {**expected, **extra}.items()}


# ─── Actions ─────────────────────────────────────────────────────────────────

ON_TWEET = ({"auth_token": AUTH, "tweet_id": TWEET_ID}, {"authToken": AUTH, "tweetId": TWEET_ID},
            {"proxy": PROXY}, {"proxy": PROXY})
ON_USER = ({"auth_token": AUTH, "user_id": USER_ID}, {"authToken": AUTH, "userId": USER_ID},
           {"username": "elonmusk", "proxy": PROXY}, {"username": "elonmusk", "proxy": PROXY})

# resource, method, path, action, then required kwargs and their body, optional kwargs and their body
ACTIONS = [
    ("post", "pin_post", "/interaction/pin-post", "pin_tweet", *ON_TWEET),
    ("post", "unpin_post", "/interaction/unpin-post", "unpin_tweet", *ON_TWEET),
    ("post", "hide_reply", "/interaction/hide-reply", "hide_reply", *ON_TWEET),
    ("post", "unhide_reply", "/interaction/unhide-reply", "unhide_reply", *ON_TWEET),
    ("interaction", "block", "/interaction/block", "block", *ON_USER),
    ("interaction", "unblock", "/interaction/unblock", "unblock", *ON_USER),
    ("interaction", "mute", "/interaction/mute", "mute", *ON_USER),
    ("interaction", "unmute", "/interaction/unmute", "unmute", *ON_USER),
    ("interaction", "remove_follower", "/interaction/remove-follower", "remove_follower", *ON_USER),
    ("list", "delete", "/list/delete", "delete_list",
     {"auth_token": AUTH, "list_id": LIST_ID}, {"authToken": AUTH, "listId": LIST_ID},
     {"proxy": PROXY}, {"proxy": PROXY}),
]
ACTION_IDS = [f"{a[0]}.{a[1]}" for a in ACTIONS]


def action_response(action):
    return {"data": {"id": "1", "action": action, "timestamp": "2026-11-04T00:00:00.000Z",
                     "success": True, "message": "ok", "metadata": {}}}


@pytest.mark.parametrize("resource,method,path,_a,required,_b,optional,_ob", ACTIONS, ids=ACTION_IDS)
def test_action_signature(resource, method, path, _a, required, _b, optional, _ob):
    params = dict(inspect.signature(method_of(make_client(), resource, method)).parameters)
    assert set(params) == set(required) | set(optional)
    assert all(p.kind == inspect.Parameter.KEYWORD_ONLY for p in params.values())
    assert all(params[k].default is inspect.Parameter.empty for k in required)
    assert all(params[k].default is None for k in optional)


@pytest.mark.parametrize("resource,method,path,action,required,expected,_o,_ob", ACTIONS, ids=ACTION_IDS)
@responses.activate
def test_action_sends_post_and_drops_unset_optionals(resource, method, path, action, required, expected, _o, _ob):
    responses.post(f"{BASE}{path}", json=action_response(action))
    assert method_of(make_client(), resource, method)(**required) == action_response(action)

    request = responses.calls[0].request
    assert request.method == "POST"
    assert request.url == f"{BASE}{path}"
    assert body(responses.calls[0]) == expected


@pytest.mark.parametrize("resource,method,path,action,required,expected,optional,extra", ACTIONS, ids=ACTION_IDS)
@responses.activate
def test_action_sends_optionals_when_set(resource, method, path, action, required, expected, optional, extra):
    responses.post(f"{BASE}{path}", json=action_response(action))
    method_of(make_client(), resource, method)(**required, **optional)
    assert body(responses.calls[0]) == {**expected, **extra}


@pytest.mark.parametrize("resource,method,path,action,required,_b,_o,_ob", ACTIONS, ids=ACTION_IDS)
@responses.activate
def test_action_is_not_repeated_after_a_failure(resource, method, path, action, required, _b, _o, _ob):
    responses.post(f"{BASE}{path}", status=502, json={"statusCode": 502, "message": "Not confirmed"})
    with patch("tweetapi.client.time.sleep"), pytest.raises(ServerError):
        method_of(TweetAPI(api_key="test-key"), resource, method)(**required)
    assert len(responses.calls) == 1


@pytest.mark.parametrize("resource,method,path,action,required,_b,_o,_ob", ACTIONS, ids=ACTION_IDS)
@responses.activate
def test_action_is_retried_when_retry_after_says_it_never_reached_x(resource, method, path, action, required, _b, _o, _ob):
    responses.post(f"{BASE}{path}", status=503, headers={"Retry-After": "1"},
                   json={"statusCode": 503, "message": "unavailable"})
    responses.post(f"{BASE}{path}", json=action_response(action))
    with patch("tweetapi.client.time.sleep"):
        method_of(TweetAPI(api_key="test-key"), resource, method)(**required)
    assert len(responses.calls) == 2


# ─── Trends ──────────────────────────────────────────────────────────────────

TRENDS = {
    "location": {"woeid": 23424977, "name": "United States"},
    "asOf": "2026-11-04T10:00:00.000Z",
    "createdAt": "2026-11-04T09:55:00.000Z",
    "trends": [
        {"name": "#Example", "query": "%23Example", "url": None, "promoted": False, "tweetVolume": None},
    ],
}
LOCATIONS = [
    {"woeid": 1, "name": "Worldwide", "placeType": {"code": 19, "name": "Supername"},
     "country": None, "countryCode": None, "parentId": 0},
]


def test_trends_resource_is_wired():
    assert isinstance(make_client().trends, TrendsResource)


def test_trends_get_takes_optional_country_or_woeid():
    params = dict(inspect.signature(TrendsResource.get).parameters)
    params.pop("self")
    assert set(params) == {"country", "woeid"}
    assert all(p.kind == inspect.Parameter.KEYWORD_ONLY and p.default is None for p in params.values())


@responses.activate
def test_trends_get_without_arguments_asks_for_worldwide():
    responses.get(f"{BASE}/trends", json={"data": TRENDS})
    assert make_client().trends.get() == {"data": TRENDS}
    assert responses.calls[0].request.url == f"{BASE}/trends"


@responses.activate
def test_trends_get_with_country():
    responses.get(f"{BASE}/trends", json={"data": TRENDS})
    make_client().trends.get(country="US")
    assert query(responses.calls[0]) == {"country": ["US"]}


@pytest.mark.parametrize("woeid", [23424977, "23424977"])
@responses.activate
def test_trends_get_with_woeid_as_number_or_string(woeid):
    responses.get(f"{BASE}/trends", json={"data": TRENDS})
    make_client().trends.get(woeid=woeid)
    assert query(responses.calls[0]) == {"woeid": ["23424977"]}


@responses.activate
def test_trends_get_locations_sends_no_query_string():
    responses.get(f"{BASE}/trends/locations", json={"data": LOCATIONS})
    assert make_client().trends.get_locations() == {"data": LOCATIONS}

    request = responses.calls[0].request
    assert request.method == "GET"
    assert request.url == f"{BASE}/trends/locations"
    assert list(inspect.signature(TrendsResource.get_locations).parameters) == ["self"]
