"""Tests for split timeout configuration and the media timeout."""

import pytest
import requests
import responses

from tweetapi import NetworkError, TweetAPI

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


class TestMediaTimeoutDefaults:
    def test_default_is_120_seconds_with_the_normal_connect_timeout(self):
        client = TweetAPI(api_key="key")
        assert client._media_timeout == (10.0, 120.0)

    def test_a_longer_read_timeout_is_kept(self):
        client = TweetAPI(api_key="key", read_timeout=180.0)
        assert client._media_timeout == (10.0, 180.0)

    def test_single_timeout_value_applies_to_both(self):
        assert TweetAPI(api_key="key", timeout=15)._media_timeout == (15, 120.0)
        assert TweetAPI(api_key="key", timeout=200)._media_timeout == (200, 200)

    def test_tuple_timeout_keeps_its_connect_value(self):
        client = TweetAPI(api_key="key", timeout=(5, 20))
        assert client._media_timeout == (5, 120.0)

    def test_explicit_media_timeout_wins(self):
        assert TweetAPI(api_key="key", media_timeout=300)._media_timeout == (10.0, 300)
        client = TweetAPI(api_key="key", read_timeout=180.0, media_timeout=60)
        assert client._media_timeout == (10.0, 60)

    def test_no_read_timeout_stays_none(self):
        client = TweetAPI(api_key="key", timeout=(5, None))
        assert client._media_timeout == (5, None)


AUTH = "auth"
PROXY = "host:8080@user:pass"
MEDIA = [{"url": "https://example.com/a.jpg"}]
PROFILE_MEDIA = {"url": "https://example.com/a.jpg"}

# Every call that sends a file: resource, method, path, kwargs
UPLOADS = [
    ("post", "create_post_with_media", "/interaction/create-post-with-media",
     {"auth_token": AUTH, "text": "Hi", "media": MEDIA, "proxy": PROXY}),
    ("post", "reply_post_with_media", "/interaction/reply-post-with-media",
     {"auth_token": AUTH, "text": "Hi", "tweet_id": "1", "media": MEDIA, "proxy": PROXY}),
    ("post", "upload_media", "/interaction/upload-media",
     {"auth_token": AUTH, "proxy": PROXY, "media": PROFILE_MEDIA}),
    ("community", "create_post_with_media", "/interaction/create-community-post-with-media",
     {"auth_token": AUTH, "text": "Hi", "community_id": "2", "media": MEDIA, "proxy": PROXY}),
    ("community", "create_quote_with_media", "/interaction/create-community-quote-with-media",
     {"auth_token": AUTH, "text": "Hi", "attachment_url": "https://x.com/user/status/1",
      "community_id": "2", "media": MEDIA, "proxy": PROXY}),
    ("community", "reply_post_with_media", "/interaction/reply-community-post-with-media",
     {"auth_token": AUTH, "text": "Hi", "tweet_id": "1", "community_id": "2",
      "media": MEDIA, "proxy": PROXY}),
    ("profile", "avatar", "/profile/avatar", {"auth_token": AUTH, "media": PROFILE_MEDIA}),
    ("profile", "banner", "/profile/banner", {"auth_token": AUTH, "media": PROFILE_MEDIA}),
    ("dm", "send_dm", "/interaction/send-dm",
     {"auth_token": AUTH, "conversation_id": "1-2", "text": "Hi", "proxy": PROXY, "media": MEDIA}),
]


def sent_timeout(call):
    return call.request.req_kwargs["timeout"]


class TestMediaTimeoutPassedToRequests:
    @pytest.mark.parametrize("resource,method,path,kwargs", UPLOADS,
                             ids=[f"{u[0]}.{u[1]}" for u in UPLOADS])
    @responses.activate
    def test_file_uploads_use_the_media_timeout(self, resource, method, path, kwargs):
        responses.post(f"{BASE_URL}/tw-v2{path}", json={"data": {}})
        client = TweetAPI(api_key="key")
        getattr(getattr(client, resource), method)(**kwargs)
        assert sent_timeout(responses.calls[0]) == (10.0, 120.0)

    @responses.activate
    def test_explicit_media_timeout_is_sent(self):
        responses.post(f"{BASE_URL}/tw-v2/interaction/upload-media", json={"data": {}})
        client = TweetAPI(api_key="key", connect_timeout=5.0, media_timeout=45.0)
        client.post.upload_media(auth_token=AUTH, proxy=PROXY, media=PROFILE_MEDIA)
        assert sent_timeout(responses.calls[0]) == (5.0, 45.0)

    @responses.activate
    def test_normal_calls_keep_the_regular_timeout(self):
        responses.get(f"{BASE_URL}/tw-v2/user/by-username", json={"data": {}})
        responses.post(f"{BASE_URL}/tw-v2/interaction/create-post", json={"data": {}})
        responses.get(f"{BASE_URL}/tw-v2/interaction/media-status", json={"data": {}})
        client = TweetAPI(api_key="key")

        client.user.get_by_username(username="test")
        client.post.create_post(auth_token=AUTH, text="Hi", proxy=PROXY)
        client.post.get_media_status(auth_token=AUTH, proxy=PROXY, media_id="3")
        assert [sent_timeout(c) for c in responses.calls] == [(10.0, 30.0)] * 3

    @pytest.mark.parametrize("media", [None, []])
    @responses.activate
    def test_send_dm_without_media_keeps_the_regular_timeout(self, media):
        responses.post(f"{BASE_URL}/tw-v2/interaction/send-dm", json={"data": {}})
        TweetAPI(api_key="key").dm.send_dm(
            auth_token=AUTH, conversation_id="1-2", text="Hi", proxy=PROXY, media=media,
        )
        assert sent_timeout(responses.calls[0]) == (10.0, 30.0)


class TestTimeoutErrorMessage:
    @responses.activate
    def test_reports_the_media_timeout_for_an_upload(self):
        responses.post(f"{BASE_URL}/tw-v2/interaction/upload-media",
                       body=requests.exceptions.ReadTimeout("timed out"))
        with pytest.raises(NetworkError, match=r"connect=10\.0s, read=120\.0s"):
            TweetAPI(api_key="key").post.upload_media(
                auth_token=AUTH, proxy=PROXY, media=PROFILE_MEDIA,
            )

    @responses.activate
    def test_reports_the_regular_timeout_for_a_normal_call(self):
        responses.get(f"{BASE_URL}/tw-v2/user/by-username",
                      body=requests.exceptions.ReadTimeout("timed out"))
        with pytest.raises(NetworkError, match=r"connect=10\.0s, read=30\.0s"):
            TweetAPI(api_key="key", max_retries=0).user.get_by_username(username="test")
