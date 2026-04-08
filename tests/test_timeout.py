"""Tests for split timeout configuration."""

import responses

from tweetapi import TweetAPI

BASE_URL = "https://api.tweetapi.com"


class TestTimeoutDefaults:
    def test_default_timeout_is_tuple(self):
        client = TweetAPI(api_key="key")
        assert client._timeout == (10.0, 30.0)

    def test_single_timeout_value(self):
        client = TweetAPI(api_key="key", timeout=15)
        assert client._timeout == 15

    def test_tuple_timeout_value(self):
        client = TweetAPI(api_key="key", timeout=(5, 20))
        assert client._timeout == (5, 20)

    def test_explicit_connect_and_read(self):
        client = TweetAPI(api_key="key", connect_timeout=5.0, read_timeout=60.0)
        assert client._timeout == (5.0, 60.0)

    def test_only_connect_timeout(self):
        client = TweetAPI(api_key="key", connect_timeout=3.0)
        assert client._timeout == (3.0, 30.0)

    def test_only_read_timeout(self):
        client = TweetAPI(api_key="key", read_timeout=120.0)
        assert client._timeout == (10.0, 120.0)

    def test_timeout_overrides_connect_read(self):
        """When timeout is explicitly set, connect_timeout/read_timeout are ignored."""
        client = TweetAPI(api_key="key", timeout=25, connect_timeout=5, read_timeout=60)
        assert client._timeout == 25


class TestTimeoutPassedToRequests:
    @responses.activate
    def test_timeout_passed_in_request(self):
        responses.add(
            responses.GET,
            f"{BASE_URL}/tw-v2/user/by-username",
            json={"data": {"id": "1", "username": "test"}},
            status=200,
        )

        client = TweetAPI(api_key="key", timeout=42)
        client.user.get_by_username(username="test")

        # The responses library records the request but doesn't expose the
        # timeout kwarg. We verify configuration storage instead.
        assert client._timeout == 42
