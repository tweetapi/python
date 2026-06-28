import json

import pytest
import responses

from tweetapi import (
    TweetAPI,
    TweetAPIError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    NetworkError,
)

BASE_URL = "https://api.tweetapi.com"


def make_client(**kwargs) -> TweetAPI:
    defaults = {"api_key": "test-api-key", "max_retries": 0}
    defaults.update(kwargs)
    return TweetAPI(**defaults)


class TestClientInit:
    def test_raises_on_empty_api_key(self):
        with pytest.raises(ValueError, match="api_key is required"):
            TweetAPI(api_key="")

    def test_creates_with_valid_key(self):
        client = TweetAPI(api_key="key")
        assert client is not None

    def test_all_resources_exist(self):
        client = make_client()
        for attr in ["user", "tweet", "post", "interaction", "list", "community",
                      "profile", "space", "explore", "auth", "xchat", "dm"]:
            assert hasattr(client, attr), f"Missing resource: {attr}"


class TestGetRequests:
    @responses.activate
    def test_sends_api_key_header(self):
        responses.add(
            responses.GET,
            f"{BASE_URL}/tw-v2/user/by-username",
            json={"data": {"id": "123", "username": "testuser", "name": "Test"}},
            status=200,
        )

        client = make_client()
        client.user.get_by_username(username="testuser")

        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers["X-API-Key"] == "test-api-key"

    @responses.activate
    def test_sends_query_params(self):
        responses.add(
            responses.GET,
            f"{BASE_URL}/tw-v2/user/by-username",
            json={"data": {"id": "123", "username": "elonmusk"}},
            status=200,
        )

        client = make_client()
        client.user.get_by_username(username="elonmusk")

        assert "username=elonmusk" in responses.calls[0].request.url

    @responses.activate
    def test_omits_none_params(self):
        responses.add(
            responses.GET,
            f"{BASE_URL}/tw-v2/user/followers",
            json={"data": [], "pagination": {"nextCursor": None, "prevCursor": None}},
            status=200,
        )

        client = make_client()
        client.user.get_followers(user_id="123")

        assert "cursor" not in responses.calls[0].request.url
        assert "userId=123" in responses.calls[0].request.url

    @responses.activate
    def test_parses_json_response(self):
        responses.add(
            responses.GET,
            f"{BASE_URL}/tw-v2/user/by-username",
            json={"data": {"id": "123", "username": "elonmusk", "followerCount": 180000000}},
            status=200,
        )

        client = make_client()
        result = client.user.get_by_username(username="elonmusk")

        assert result["data"]["username"] == "elonmusk"
        assert result["data"]["followerCount"] == 180000000


class TestPostRequests:
    @responses.activate
    def test_sends_json_body(self):
        responses.add(
            responses.POST,
            f"{BASE_URL}/tw-v2/interaction/like-post",
            json={"data": {"id": "789", "action": "like", "timestamp": "2025-01-01", "success": True}},
            status=200,
        )

        client = make_client()
        client.interaction.favorite_post(auth_token="auth123", tweet_id="789", proxy="h:p@u:p")

        body = json.loads(responses.calls[0].request.body)
        assert body["authToken"] == "auth123"
        assert body["tweetId"] == "789"

    @responses.activate
    def test_strips_none_from_body(self):
        responses.add(
            responses.POST,
            f"{BASE_URL}/tw-v2/interaction/create-post",
            json={"data": {"id": "1", "action": "create_tweet", "success": True}},
            status=200,
        )

        client = make_client()
        client.post.create_post(auth_token="auth", text="Hello", proxy="h:p@u:p")

        body = json.loads(responses.calls[0].request.body)
        assert "disableLinkPreview" not in body

    @responses.activate
    def test_create_post_serializes_reply_option(self):
        responses.add(
            responses.POST,
            f"{BASE_URL}/tw-v2/interaction/create-post",
            json={"data": {"id": "1", "action": "create_tweet", "success": True}},
            status=200,
        )

        client = make_client()
        client.post.create_post(
            auth_token="auth",
            text="Hello",
            proxy="h:p@u:p",
            reply_option={"mode": "followers", "regions": ["US"]},
        )

        body = json.loads(responses.calls[0].request.body)
        assert body["replyOption"] == {"mode": "followers", "regions": ["US"]}

    @responses.activate
    def test_create_post_with_media_preserves_media_id(self):
        responses.add(
            responses.POST,
            f"{BASE_URL}/tw-v2/interaction/create-post-with-media",
            json={"data": {"id": "1", "action": "create_tweet", "success": True}},
            status=200,
        )

        client = make_client()
        client.post.create_post_with_media(
            auth_token="auth",
            text="Hello",
            media=[{"media_id": "1971008286821380096"}],
            proxy="h:p@u:p",
        )

        body = json.loads(responses.calls[0].request.body)
        assert body["media"] == [{"media_id": "1971008286821380096"}]


class TestListParity:
    @responses.activate
    def test_create_sends_camel_case_body(self):
        responses.add(
            responses.POST,
            f"{BASE_URL}/tw-v2/list/create",
            json={"data": {"id": "list-1", "name": "Research"}},
            status=200,
        )

        client = make_client()
        client.list.create(
            auth_token="auth",
            name="Research",
            description="Signals",
            is_private=False,
        )

        body = json.loads(responses.calls[0].request.body)
        assert body == {
            "authToken": "auth",
            "name": "Research",
            "description": "Signals",
            "isPrivate": False,
        }

    @responses.activate
    def test_add_member_sends_camel_case_body_and_strips_none(self):
        responses.add(
            responses.POST,
            f"{BASE_URL}/tw-v2/list/add-member",
            json={"data": {"success": True}},
            status=200,
        )

        client = make_client()
        client.list.add_member(auth_token="auth", list_id="list-1", user_id="user-1")

        body = json.loads(responses.calls[0].request.body)
        assert body == {
            "authToken": "auth",
            "listId": "list-1",
            "userId": "user-1",
        }
        assert "proxy" not in body

    @responses.activate
    def test_remove_member_sends_camel_case_body(self):
        responses.add(
            responses.POST,
            f"{BASE_URL}/tw-v2/list/remove-member",
            json={"data": {"success": True}},
            status=200,
        )

        client = make_client()
        client.list.remove_member(
            auth_token="auth",
            list_id="list-1",
            user_id="user-1",
            proxy="h:p@u:p",
        )

        body = json.loads(responses.calls[0].request.body)
        assert body == {
            "authToken": "auth",
            "listId": "list-1",
            "userId": "user-1",
            "proxy": "h:p@u:p",
        }


class TestProfileParity:
    @responses.activate
    def test_update_sends_body_and_strips_none(self):
        responses.add(
            responses.POST,
            f"{BASE_URL}/tw-v2/profile/update",
            json={"data": {"id": "user-1", "name": "New Name"}},
            status=200,
        )

        client = make_client()
        client.profile.update(
            auth_token="auth",
            name="New Name",
            bio=None,
            location="Bangkok",
        )

        body = json.loads(responses.calls[0].request.body)
        assert body == {
            "authToken": "auth",
            "name": "New Name",
            "location": "Bangkok",
        }
        assert "bio" not in body
        assert "website" not in body
        assert "proxy" not in body

    @responses.activate
    def test_avatar_sends_media_body(self):
        responses.add(
            responses.POST,
            f"{BASE_URL}/tw-v2/profile/avatar",
            json={"data": {"id": "user-1", "avatar": "https://example.com/a.jpg"}},
            status=200,
        )

        client = make_client()
        client.profile.avatar(
            auth_token="auth",
            media={"url": "https://example.com/a.jpg"},
            proxy="h:p@u:p",
        )

        body = json.loads(responses.calls[0].request.body)
        assert body == {
            "authToken": "auth",
            "media": {"url": "https://example.com/a.jpg"},
            "proxy": "h:p@u:p",
        }

    @responses.activate
    def test_banner_sends_media_body(self):
        responses.add(
            responses.POST,
            f"{BASE_URL}/tw-v2/profile/banner",
            json={"data": {"id": "user-1", "banner": "https://example.com/b.jpg"}},
            status=200,
        )

        client = make_client()
        client.profile.banner(
            auth_token="auth",
            media={"data": "base64", "type": "image/png"},
        )

        body = json.loads(responses.calls[0].request.body)
        assert body == {
            "authToken": "auth",
            "media": {"data": "base64", "type": "image/png"},
        }


class TestCommunityParity:
    @responses.activate
    def test_create_quote_sends_path_and_body(self):
        responses.add(
            responses.POST,
            f"{BASE_URL}/tw-v2/interaction/create-community-quote",
            json={"data": {"id": "tweet-1", "success": True}},
            status=200,
        )

        client = make_client()
        client.community.create_quote(
            auth_token="auth",
            text="Quote",
            attachment_url="https://x.com/user/status/1",
            community_id="community-1",
            proxy="h:p@u:p",
            disable_link_preview=True,
        )

        body = json.loads(responses.calls[0].request.body)
        assert body == {
            "authToken": "auth",
            "text": "Quote",
            "attachmentUrl": "https://x.com/user/status/1",
            "communityId": "community-1",
            "proxy": "h:p@u:p",
            "disableLinkPreview": True,
        }

    @responses.activate
    def test_create_quote_with_media_sends_path_and_body(self):
        responses.add(
            responses.POST,
            f"{BASE_URL}/tw-v2/interaction/create-community-quote-with-media",
            json={"data": {"id": "tweet-1", "success": True}},
            status=200,
        )

        client = make_client()
        client.community.create_quote_with_media(
            auth_token="auth",
            text="Quote",
            attachment_url="https://x.com/user/status/1",
            community_id="community-1",
            media=[{"media_id": "1971008286821380096"}],
            proxy="h:p@u:p",
        )

        body = json.loads(responses.calls[0].request.body)
        assert body == {
            "authToken": "auth",
            "text": "Quote",
            "attachmentUrl": "https://x.com/user/status/1",
            "communityId": "community-1",
            "media": [{"media_id": "1971008286821380096"}],
            "proxy": "h:p@u:p",
        }


class TestErrorHandling:
    @responses.activate
    def test_validation_error_on_400(self):
        responses.add(
            responses.GET,
            f"{BASE_URL}/tw-v2/user/by-username",
            json={"error": {"code": "VALIDATION_ERROR", "message": "Required - username", "details": None}},
            status=400,
        )

        client = make_client()
        with pytest.raises(ValidationError) as exc_info:
            client.user.get_by_username(username="")

        assert exc_info.value.code == "VALIDATION_ERROR"
        assert exc_info.value.status_code == 400

    @responses.activate
    def test_authentication_error_on_401(self):
        responses.add(
            responses.GET,
            f"{BASE_URL}/tw-v2/user/by-username",
            json={"error": {"code": "UNAUTHORIZED", "message": "Invalid token", "details": None}},
            status=401,
        )

        client = make_client()
        with pytest.raises(AuthenticationError) as exc_info:
            client.user.get_by_username(username="test")

        assert exc_info.value.code == "UNAUTHORIZED"

    @responses.activate
    def test_not_found_error_on_404(self):
        responses.add(
            responses.GET,
            f"{BASE_URL}/tw-v2/user/by-username",
            json={"error": {"code": "NOT_FOUND", "message": "User not found", "details": None}},
            status=404,
        )

        client = make_client()
        with pytest.raises(NotFoundError) as exc_info:
            client.user.get_by_username(username="nonexistent")

        assert exc_info.value.code == "NOT_FOUND"
        assert exc_info.value.status_code == 404
        assert exc_info.value.message == "User not found"

    @responses.activate
    def test_rate_limit_error_with_retry_after(self):
        responses.add(
            responses.GET,
            f"{BASE_URL}/tw-v2/user/by-username",
            json={"error": {"code": "RATE_LIMIT", "message": "Rate limit exceeded", "details": {"retryAfter": 30}}},
            status=429,
        )

        client = make_client()
        with pytest.raises(RateLimitError) as exc_info:
            client.user.get_by_username(username="test")

        assert exc_info.value.retry_after == 30

    @responses.activate
    def test_server_error_on_500(self):
        responses.add(
            responses.GET,
            f"{BASE_URL}/tw-v2/user/by-username",
            json={"error": {"code": "INTERNAL_SERVER_ERROR", "message": "Something went wrong", "details": None}},
            status=500,
        )

        client = make_client()
        with pytest.raises(ServerError):
            client.user.get_by_username(username="test")

    @responses.activate
    def test_malformed_error_response(self):
        responses.add(
            responses.GET,
            f"{BASE_URL}/tw-v2/user/by-username",
            body="not json",
            status=500,
            content_type="text/plain",
        )

        client = make_client()
        with pytest.raises(ServerError) as exc_info:
            client.user.get_by_username(username="test")

        assert exc_info.value.code == "UNKNOWN_ERROR"

    @responses.activate
    def test_preserves_api_error_code(self):
        responses.add(
            responses.GET,
            f"{BASE_URL}/tw-v2/user/by-username",
            json={"error": {"code": "ACCOUNT_SUSPENDED", "message": "Account suspended", "details": None}},
            status=403,
        )

        client = make_client()
        with pytest.raises(TweetAPIError) as exc_info:
            client.user.get_by_username(username="suspended")

        assert exc_info.value.code == "ACCOUNT_SUSPENDED"

    def test_network_error_on_connection_failure(self):
        client = TweetAPI(api_key="key", base_url="http://localhost:1", max_retries=0)
        with pytest.raises(NetworkError):
            client.user.get_by_username(username="test")
