"""Offline contracts for explore.search and its response types."""

from typing import Literal, Union, get_type_hints
from urllib.parse import parse_qs, urlsplit

import responses

from tweetapi import TweetAPI, types

SEARCH_URL = "https://api.tweetapi.com/tw-v2/search"

# The API answers a search with data and pagination only.
PAGE = {"data": [], "pagination": {"nextCursor": "NEXT", "prevCursor": None}}


def make_client():
    return TweetAPI(api_key="test-key", initial_retry_delay=0.01, max_retry_delay=0.1)


def query(call):
    return {k: v[0] for k, v in parse_qs(urlsplit(call.request.url).query).items()}


@responses.activate
def test_search_sends_query_type_and_cursor():
    responses.get(SEARCH_URL, json=PAGE)
    result = make_client().explore.search(query="bitcoin", type="Latest", cursor="C1")

    assert responses.calls[0].request.method == "GET"
    assert query(responses.calls[0]) == {"query": "bitcoin", "type": "Latest", "cursor": "C1"}
    assert result == PAGE


@responses.activate
def test_search_leaves_out_an_unset_cursor():
    responses.get(SEARCH_URL, json=PAGE)
    make_client().explore.search(query="bitcoin", type="Top")

    assert query(responses.calls[0]) == {"query": "bitcoin", "type": "Top"}


def test_search_response_has_only_data_and_pagination():
    assert set(get_type_hints(types.SearchResponse, vars(types))) == {"data", "pagination"}


def test_top_results_are_labelled_tweets_or_users():
    assert types.SearchTopResult == Union[types.SearchTopTweetResult, types.SearchTopUserResult]

    tweet = get_type_hints(types.SearchTopTweetResult, vars(types))
    user = get_type_hints(types.SearchTopUserResult, vars(types))
    assert tweet == {"type": Literal["tweet"], "content": types.Tweet}
    assert user == {"type": Literal["user"], "content": types.User}
