from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI
    from ..types import (
        UserResponse,
        UsersResponse,
        UserPaginatedResponse,
        UserRelationshipResponse,
        TweetsPaginatedResponse,
        PaginatedResponse,
        ApiResponse,
    )


class UserResource:
    def __init__(self, client: TweetAPI) -> None:
        self._client = client

    def get_by_username(self, *, username: str) -> UserResponse:
        """Get a user profile by username."""
        return self._client._get("/tw-v2/user/by-username", {"username": username})

    def get_by_usernames(self, *, usernames: str) -> UsersResponse:
        """Get multiple user profiles by usernames (comma-separated)."""
        return self._client._get("/tw-v2/user/by-usernames", {"usernames": usernames})

    def get_by_user_id(self, *, user_id: str) -> UserResponse:
        """Get a user profile by user ID."""
        return self._client._get("/tw-v2/user/by-id", {"userId": user_id})

    def get_by_user_ids(self, *, user_ids: list[str]) -> UsersResponse:
        """Get multiple user profiles by user IDs (list of ID strings, max 50)."""
        return self._client._get("/tw-v2/user/by-ids", {"userIds": user_ids})

    def get_tweets(self, *, user_id: str, cursor: Optional[str] = None) -> TweetsPaginatedResponse:
        """Get a user's tweets."""
        return self._client._get("/tw-v2/user/tweets", {"userId": user_id, "cursor": cursor})

    def get_tweets_and_replies(self, *, user_id: str, cursor: Optional[str] = None) -> TweetsPaginatedResponse:
        """Get a user's tweets and replies."""
        return self._client._get("/tw-v2/user/tweets-and-replies", {"userId": user_id, "cursor": cursor})

    def get_following(self, *, user_id: str, cursor: Optional[str] = None) -> UserPaginatedResponse:
        """Get who a user follows (v2 — full user objects)."""
        return self._client._get("/tw-v2/user/following", {"userId": user_id, "cursor": cursor})

    def get_followers(self, *, user_id: str, cursor: Optional[str] = None) -> UserPaginatedResponse:
        """Get a user's followers (v2 — full user objects)."""
        return self._client._get("/tw-v2/user/followers", {"userId": user_id, "cursor": cursor})

    def get_verified_followers(self, *, user_id: str, cursor: Optional[str] = None) -> UserPaginatedResponse:
        """Get a user's verified followers."""
        return self._client._get("/tw-v2/user/verified-followers", {"userId": user_id, "cursor": cursor})

    def get_subscriptions(self, *, user_id: str, cursor: Optional[str] = None) -> UserPaginatedResponse:
        """Get a user's subscriptions."""
        return self._client._get("/tw-v2/user/subscriptions", {"userId": user_id, "cursor": cursor})

    def get_following_v1(self, *, user_id: str, count: Optional[str] = None, cursor: Optional[str] = None) -> UserPaginatedResponse:
        """Get who a user follows (v1 — supports count)."""
        return self._client._get("/tw-v2/user/following-list", {"userId": user_id, "count": count, "cursor": cursor})

    def get_followers_v1(self, *, user_id: str, count: Optional[str] = None, cursor: Optional[str] = None) -> UserPaginatedResponse:
        """Get a user's followers (v1 — supports count)."""
        return self._client._get("/tw-v2/user/followers-list", {"userId": user_id, "count": count, "cursor": cursor})

    def get_following_ids(self, *, user_id: str, count: Optional[str] = None, cursor: Optional[str] = None) -> PaginatedResponse:
        """Get IDs of accounts a user is following."""
        return self._client._get("/tw-v2/user/following-ids", {"userId": user_id, "count": count, "cursor": cursor})

    def get_followers_ids(self, *, user_id: str, count: Optional[str] = None, cursor: Optional[str] = None) -> PaginatedResponse:
        """Get IDs of a user's followers."""
        return self._client._get("/tw-v2/user/followers-ids", {"userId": user_id, "count": count, "cursor": cursor})

    def check_follow(self, *, subject_id: str, target_id: str) -> UserRelationshipResponse:
        """Check the follow relationship between two users."""
        return self._client._get("/tw-v2/user/friendship", {"subjectId": subject_id, "targetId": target_id})

    def about_account(self, *, username: str) -> ApiResponse:
        """Get account creation details and transparency information."""
        return self._client._get("/tw-v2/user/about-account", {"username": username})
