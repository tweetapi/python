"""Tests for retry with exponential backoff."""

from unittest.mock import patch

import pytest
import responses

from tweetapi import (
    TweetAPI,
    RateLimitError,
    ServerError,
    NetworkError,
    ValidationError,
    AuthenticationError,
    NotFoundError,
)

BASE_URL = "https://api.tweetapi.com"


def make_client(**kwargs):
    defaults = {"api_key": "test-key", "initial_retry_delay": 0.01, "max_retry_delay": 0.1}
    defaults.update(kwargs)
    return TweetAPI(**defaults)


class TestRetryOnTransientErrors:
    @responses.activate
    def test_retries_on_500_and_succeeds(self):
        responses.add(responses.GET, f"{BASE_URL}/tw-v2/user/by-username",
                      json={"error": {"code": "SERVER_ERROR", "message": "fail", "details": None}}, status=500)
        responses.add(responses.GET, f"{BASE_URL}/tw-v2/user/by-username",
                      json={"data": {"id": "1", "username": "test"}}, status=200)

        client = make_client(max_retries=3)
        result = client.user.get_by_username(username="test")
        assert result["data"]["id"] == "1"
        assert len(responses.calls) == 2

    @responses.activate
    def test_retries_on_429_with_retry_after(self):
        responses.add(responses.GET, f"{BASE_URL}/tw-v2/user/by-username",
                      json={"error": {"code": "RATE_LIMIT", "message": "rate limited",
                                       "details": {"retryAfter": 1}}}, status=429)
        responses.add(responses.GET, f"{BASE_URL}/tw-v2/user/by-username",
                      json={"data": {"id": "1"}}, status=200)

        client = make_client(max_retries=1, max_retry_delay=2.0)
        with patch("tweetapi.client.time.sleep") as mock_sleep:
            result = client.user.get_by_username(username="test")
            assert result["data"]["id"] == "1"
            assert len(responses.calls) == 2
            # Should have slept for the retryAfter duration (1 second)
            mock_sleep.assert_called_once()
            delay = mock_sleep.call_args[0][0]
            assert 0.9 <= delay <= 2.0  # retryAfter=1, capped at max_retry_delay

    @responses.activate
    def test_exhausts_retries_and_raises(self):
        for _ in range(4):
            responses.add(responses.GET, f"{BASE_URL}/tw-v2/user/by-username",
                          json={"error": {"code": "SERVER_ERROR", "message": "fail", "details": None}}, status=500)

        client = make_client(max_retries=2)
        with pytest.raises(ServerError):
            client.user.get_by_username(username="test")
        assert len(responses.calls) == 3  # 1 initial + 2 retries


class TestNoRetryOnClientErrors:
    @responses.activate
    def test_no_retry_on_400(self):
        responses.add(responses.GET, f"{BASE_URL}/tw-v2/user/by-username",
                      json={"error": {"code": "BAD_REQUEST", "message": "bad", "details": None}}, status=400)

        client = make_client(max_retries=3)
        with pytest.raises(ValidationError):
            client.user.get_by_username(username="test")
        assert len(responses.calls) == 1

    @responses.activate
    def test_no_retry_on_401(self):
        responses.add(responses.GET, f"{BASE_URL}/tw-v2/user/by-username",
                      json={"error": {"code": "UNAUTHORIZED", "message": "bad key", "details": None}}, status=401)

        client = make_client(max_retries=3)
        with pytest.raises(AuthenticationError):
            client.user.get_by_username(username="test")
        assert len(responses.calls) == 1

    @responses.activate
    def test_no_retry_on_404(self):
        responses.add(responses.GET, f"{BASE_URL}/tw-v2/user/by-username",
                      json={"error": {"code": "NOT_FOUND", "message": "nope", "details": None}}, status=404)

        client = make_client(max_retries=3)
        with pytest.raises(NotFoundError):
            client.user.get_by_username(username="test")
        assert len(responses.calls) == 1


class TestRetryOnNetworkErrors:
    @responses.activate
    def test_retries_on_connection_error(self):
        import requests as req
        responses.add(responses.GET, f"{BASE_URL}/tw-v2/user/by-username",
                      body=req.exceptions.ConnectionError("connection refused"))
        responses.add(responses.GET, f"{BASE_URL}/tw-v2/user/by-username",
                      json={"data": {"id": "1"}}, status=200)

        client = make_client(max_retries=1)
        result = client.user.get_by_username(username="test")
        assert result["data"]["id"] == "1"
        assert len(responses.calls) == 2


class TestRetryDisabled:
    @responses.activate
    def test_max_retries_zero(self):
        responses.add(responses.GET, f"{BASE_URL}/tw-v2/user/by-username",
                      json={"error": {"code": "SERVER_ERROR", "message": "fail", "details": None}}, status=500)

        client = make_client(max_retries=0)
        with pytest.raises(ServerError):
            client.user.get_by_username(username="test")
        assert len(responses.calls) == 1


class TestRateLimitInfo:
    @responses.activate
    def test_rate_limit_info_initially_none(self):
        client = make_client()
        assert client.rate_limit_info is None

    @responses.activate
    def test_rate_limit_info_populated_after_429(self):
        responses.add(responses.GET, f"{BASE_URL}/tw-v2/user/by-username",
                      json={"error": {"code": "RATE_LIMIT", "message": "rate limited",
                                       "details": {"retryAfter": 30}}}, status=429)
        responses.add(responses.GET, f"{BASE_URL}/tw-v2/user/by-username",
                      json={"data": {"id": "1"}}, status=200)

        client = make_client(max_retries=1)
        client.user.get_by_username(username="test")

        assert client.rate_limit_info is not None
        assert client.rate_limit_info["retry_after"] == 30
        assert client.rate_limit_info["timestamp"] > 0
