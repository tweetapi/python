"""Offline contract for list.create and its optional proxy."""

import inspect
import json

import responses

from tweetapi import TweetAPI
from tweetapi.resources.list_ import ListResource

URL = "https://api.tweetapi.com/tw-v2/list/create"
PROXY = "host:port@user:pass"


def make_client():
    return TweetAPI(api_key="test-key", initial_retry_delay=0.01, max_retry_delay=0.1)


def body(call):
    return json.loads(call.request.body)


@responses.activate
def test_list_create_sends_proxy_only_when_set():
    responses.post(URL, json={"data": {"id": "1234567890", "name": "Research"}})
    client = make_client()
    expected = {"authToken": "AUTH_TOKEN", "name": "Research", "description": "", "isPrivate": True}

    client.list.create(auth_token="AUTH_TOKEN", name="Research", proxy=PROXY)
    assert body(responses.calls[0]) == {**expected, "proxy": PROXY}

    client.list.create(auth_token="AUTH_TOKEN", name="Research")
    assert body(responses.calls[1]) == expected


def test_list_create_takes_proxy_as_an_optional_keyword():
    parameter = inspect.signature(ListResource.create).parameters["proxy"]
    assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
    assert parameter.default is None
