"""Tests for retry with exponential backoff."""

from unittest.mock import patch

import pytest
import responses

from tweetapi import (
    TweetAPI,
    TweetAPIError,
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

    @responses.activate
    def test_update_username_does_not_retry_transient_failure(self):
        responses.add(
            responses.POST,
            f"{BASE_URL}/tw-v2/profile/username",
            json={"error": {"code": "SERVER_ERROR", "message": "fail", "details": None}},
            status=500,
        )
        queued_success = responses.add(
            responses.POST,
            f"{BASE_URL}/tw-v2/profile/username",
            json={"data": {"username": "new_username"}},
            status=200,
        )

        client = make_client(max_retries=3)
        with pytest.raises(ServerError):
            client.profile.update_username(
                auth_token="auth",
                password="password",
                username="new_username",
            )

        assert len(responses.calls) == 1
        assert queued_success.call_count == 0


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


USER_URL = f"{BASE_URL}/tw-v2/user/by-username"
POST_URL = f"{BASE_URL}/tw-v2/interaction/create-post"
POST_PARAMS = {"auth_token": "AUTH_TOKEN", "text": "hello", "proxy": "host:8080@user:pass"}


def v2_error(status, code=None, headers=None):
    """The /tw-v2 error envelope, with optional response headers."""
    body = {"statusCode": status, "message": "synthetic"}
    if code:
        body["code"] = code
    return {"json": body, "status": status, "headers": headers or {}}


class TestRetryRules:
    @responses.activate
    def test_no_retry_when_the_callers_proxy_failed(self):
        for status, code in [(502, "PROXY_ERROR"), (504, "PROXY_TIMEOUT")]:
            responses.reset()
            responses.add(responses.GET, USER_URL, **v2_error(status, code))
            with pytest.raises(ServerError) as exc_info:
                make_client(max_retries=3).user.get_by_username(username="test")
            assert exc_info.value.code == code
            assert len(responses.calls) == 1

    @responses.activate
    def test_no_retry_for_a_used_up_or_expired_plan(self):
        for code in ["QUOTA_EXHAUSTED", "SUBSCRIPTION_INACTIVE"]:
            responses.reset()
            responses.add(responses.GET, USER_URL, **v2_error(429, code))
            with pytest.raises(RateLimitError) as exc_info:
                make_client(max_retries=3).user.get_by_username(username="test")
            assert exc_info.value.code == code
            assert len(responses.calls) == 1

    @responses.activate
    def test_waits_for_retry_after_before_retrying(self):
        for status, code in [(429, "RATE_LIMITED"), (503, None)]:
            responses.reset()
            responses.add(responses.GET, USER_URL, **v2_error(status, code, {"Retry-After": "2"}))
            responses.add(responses.GET, USER_URL, json={"data": {"id": "1"}}, status=200)
            client = make_client(max_retries=1, max_retry_delay=5.0)
            with patch("tweetapi.client.time.sleep") as mock_sleep:
                client.user.get_by_username(username="test")
            assert len(responses.calls) == 2
            mock_sleep.assert_called_once_with(2.0)

    @responses.activate
    def test_still_retries_a_429_without_a_code_as_older_api_versions_send(self):
        responses.add(responses.GET, USER_URL, **v2_error(429))
        responses.add(responses.GET, USER_URL, json={"data": {"id": "1"}}, status=200)

        make_client(max_retries=1).user.get_by_username(username="test")
        assert len(responses.calls) == 2

    @responses.activate
    def test_does_not_repeat_a_write_after_a_failure_that_may_have_gone_through(self):
        import requests as req
        failures = [v2_error(status) for status in (500, 502, 503, 504)] + [
            {"body": req.exceptions.ConnectionError("connection reset")},
            {"body": req.exceptions.ReadTimeout("read timed out")},
        ]
        for failure in failures:
            responses.reset()
            responses.add(responses.POST, POST_URL, **failure)
            responses.add(responses.POST, POST_URL, json={"data": {"id": "1"}}, status=200)
            with pytest.raises(TweetAPIError):
                make_client(max_retries=3).post.create_post(**POST_PARAMS)
            assert len(responses.calls) == 1

    @responses.activate
    def test_repeats_a_write_when_retry_after_says_it_never_reached_x(self):
        for status, code in [(429, "RATE_LIMITED"), (503, None)]:
            responses.reset()
            responses.add(responses.POST, POST_URL, **v2_error(status, code, {"Retry-After": "0"}))
            responses.add(responses.POST, POST_URL, json={"data": {"id": "1"}}, status=200)
            make_client(max_retries=3).post.create_post(**POST_PARAMS)
            assert len(responses.calls) == 2

    @responses.activate
    def test_does_not_repeat_a_login_that_x_itself_rate_limited(self):
        responses.add(responses.POST, f"{BASE_URL}/tw-v2/auth/login", **v2_error(429, "RATE_LIMITED"))
        with pytest.raises(RateLimitError):
            make_client(max_retries=3).auth.login(
                username="user", password="pass", proxy="host:8080@user:pass", country="US"
            )
        assert len(responses.calls) == 1

    @responses.activate
    def test_retries_reads_sent_as_post(self):
        url = f"{BASE_URL}/tw-v2/xchat/history"
        responses.add(responses.POST, url, **v2_error(500))
        responses.add(responses.POST, url, json={"data": {}}, status=200)

        make_client(max_retries=3).xchat.get_history(auth_token="AUTH_TOKEN", conversation_id="1-2")
        assert len(responses.calls) == 2

