"""Offline contracts for the profile tab methods and sort_by added in 2.9.0."""

import inspect
from typing import Literal, Optional, get_type_hints
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

import pytest
import responses

from tweetapi import ForbiddenError, NotFoundError, TweetAPI, ValidationError, paginate, types
from tweetapi.resources.user import UserResource

BASE = "https://api.tweetapi.com/tw-v2"
USER_ID = "44196397"
EMPTY = {"data": [], "pagination": {"nextCursor": None, "prevCursor": None}}

PATHS = {
    "get_posts": "/user/posts",
    "get_replies": "/user/replies",
    "get_reposts": "/user/reposts",
    "get_tweets_and_replies": "/user/tweets-and-replies",
    "get_highlights": "/user/highlights",
}
SORTABLE = ["get_posts", "get_tweets_and_replies", "get_highlights"]


def make_client():
    return TweetAPI(api_key="test-key", max_retries=0)


def query(call):
    return parse_qs(urlsplit(call.request.url).query)


def page(*ids, next_cursor=None):
    return {
        "data": [{"id": i, "text": f"post {i}", "author": {"id": USER_ID}} for i in ids],
        "pagination": {"nextCursor": next_cursor, "prevCursor": None},
    }


@pytest.mark.parametrize("method", list(PATHS))
def test_signature(method):
    params = dict(inspect.signature(getattr(UserResource, method)).parameters)
    params.pop("self")
    optional = {"cursor", "sort_by"} if method in SORTABLE else {"cursor"}
    assert set(params) == {"user_id"} | optional
    assert all(p.kind is inspect.Parameter.KEYWORD_ONLY for p in params.values())
    assert params["user_id"].default is inspect.Parameter.empty
    assert all(params[name].default is None for name in optional)


@pytest.mark.parametrize("method", SORTABLE)
def test_sort_by_is_recent_or_most_liked(method):
    hints = get_type_hints(getattr(UserResource, method), vars(types))
    assert hints["sort_by"] == Optional[Literal["Recent", "MostLiked"]]
    assert hints["return"] is types.TweetsPaginatedResponse


@pytest.mark.parametrize("method", list(PATHS))
@responses.activate
def test_sends_only_user_id_by_default(method):
    responses.get(f"{BASE}{PATHS[method]}", json=EMPTY)
    assert getattr(make_client().user, method)(user_id=USER_ID) == EMPTY

    request = responses.calls[0].request
    assert request.method == "GET"
    assert urlsplit(request.url).path == f"/tw-v2{PATHS[method]}"
    assert query(responses.calls[0]) == {"userId": [USER_ID]}
    assert request.body is None


@pytest.mark.parametrize("method", list(PATHS))
@responses.activate
def test_sends_cursor_when_set(method):
    responses.get(f"{BASE}{PATHS[method]}", json=EMPTY)
    getattr(make_client().user, method)(user_id=USER_ID, cursor="c1")
    assert query(responses.calls[0]) == {"userId": [USER_ID], "cursor": ["c1"]}


@pytest.mark.parametrize("sort_by", ["Recent", "MostLiked"])
@pytest.mark.parametrize("method", SORTABLE)
@responses.activate
def test_sends_sort_by_when_set(method, sort_by):
    responses.get(f"{BASE}{PATHS[method]}", json=EMPTY)
    getattr(make_client().user, method)(user_id=USER_ID, cursor="c1", sort_by=sort_by)
    assert query(responses.calls[0]) == {"userId": [USER_ID], "cursor": ["c1"], "sortBy": [sort_by]}


@responses.activate
def test_paginate_keeps_sort_by_and_goes_past_short_pages():
    url = f"{BASE}/user/posts"
    responses.get(url, json=page("3", next_cursor="c2"))
    responses.get(url, json=page(next_cursor="c3"))
    responses.get(url, json=page("1"))
    client = make_client()

    posts = paginate(lambda cursor: client.user.get_posts(user_id=USER_ID, sort_by="MostLiked", cursor=cursor))

    assert [post["id"] for post in posts] == ["3", "1"]
    assert [query(call) for call in responses.calls] == [
        {"userId": [USER_ID], "sortBy": ["MostLiked"]},
        {"userId": [USER_ID], "sortBy": ["MostLiked"], "cursor": ["c2"]},
        {"userId": [USER_ID], "sortBy": ["MostLiked"], "cursor": ["c3"]},
    ]


@responses.activate
def test_get_reposts_keeps_the_original_post():
    repost = {
        "id": "1900000000000000002", "type": "retweet", "text": "RT @nasa: Liftoff",
        "author": {"id": USER_ID, "username": "elonmusk"},
        "retweetedTweet": {"id": "1900000000000000001", "type": "tweet", "text": "Liftoff",
                           "author": {"id": "11348282", "username": "nasa"}},
    }
    result = {"data": [repost], "pagination": {"nextCursor": "c2", "prevCursor": "c0"}}
    responses.get(f"{BASE}/user/reposts", json=result)
    assert make_client().user.get_reposts(user_id=USER_ID) == result


@responses.activate
def test_get_replies_keeps_reply_to_when_the_answered_post_is_missing():
    reply = {
        "id": "1900000000000000004", "type": "reply", "text": "Agreed",
        "author": {"id": USER_ID, "username": "elonmusk"},
        "replyTo": {"tweetId": "1900000000000000003", "userId": "11348282", "username": "nasa"},
    }
    result = {"data": [reply], "pagination": {"nextCursor": None, "prevCursor": None}}
    responses.get(f"{BASE}/user/replies", json=result)
    data = make_client().user.get_replies(user_id=USER_ID)["data"]
    assert data[0]["replyTo"]["tweetId"] == "1900000000000000003"


@pytest.mark.parametrize("status,error", [(400, ValidationError), (403, ForbiddenError), (404, NotFoundError)])
@responses.activate
def test_client_errors_are_raised_without_a_retry(status, error):
    responses.get(f"{BASE}/user/posts", status=status, json={"statusCode": status, "message": "Request failed"})
    with patch("tweetapi.client.time.sleep") as sleep, pytest.raises(error):
        TweetAPI(api_key="test-key").user.get_posts(user_id=USER_ID, sort_by="MostLiked")
    assert len(responses.calls) == 1
    sleep.assert_not_called()
