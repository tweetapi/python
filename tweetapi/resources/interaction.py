from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI
    from ..types import (
        ActionResponse,
        NotificationPaginatedResponse,
        UserAnalyticsResponse,
    )


class InteractionResource:
    def __init__(self, client: TweetAPI) -> None:
        self._client = client

    def favorite_post(self, *, auth_token: str, tweet_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Like a tweet."""
        return self._client._post("/tw-v2/interaction/like-post", {
            "authToken": auth_token, "tweetId": tweet_id, "proxy": proxy,
        })

    def unfavorite_post(self, *, auth_token: str, tweet_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Unlike a tweet."""
        return self._client._post("/tw-v2/interaction/unlike-post", {
            "authToken": auth_token, "tweetId": tweet_id, "proxy": proxy,
        })

    def retweet(self, *, auth_token: str, tweet_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Retweet a tweet."""
        return self._client._post("/tw-v2/interaction/retweet", {
            "authToken": auth_token, "tweetId": tweet_id, "proxy": proxy,
        })

    def delete_retweet(self, *, auth_token: str, tweet_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Remove a retweet."""
        return self._client._post("/tw-v2/interaction/delete-retweet", {
            "authToken": auth_token, "tweetId": tweet_id, "proxy": proxy,
        })

    def bookmark(self, *, auth_token: str, tweet_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Bookmark a tweet."""
        return self._client._post("/tw-v2/interaction/bookmark", {
            "authToken": auth_token, "tweetId": tweet_id, "proxy": proxy,
        })

    def delete_bookmark(self, *, auth_token: str, tweet_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Remove a bookmark."""
        return self._client._post("/tw-v2/interaction/delete-bookmark", {
            "authToken": auth_token, "tweetId": tweet_id, "proxy": proxy,
        })

    def follow(self, *, auth_token: str, user_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Follow a user."""
        return self._client._post("/tw-v2/interaction/follow", {
            "authToken": auth_token, "userId": user_id, "proxy": proxy,
        })

    def unfollow(self, *, auth_token: str, user_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Unfollow a user."""
        return self._client._post("/tw-v2/interaction/unfollow", {
            "authToken": auth_token, "userId": user_id, "proxy": proxy,
        })

    def add_member_to_list(self, *, auth_token: str, list_id: str, user_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Add a user to a list."""
        return self._client._post("/tw-v2/interaction/add-to-list", {
            "authToken": auth_token, "listId": list_id, "userId": user_id, "proxy": proxy,
        })

    def remove_member_from_list(self, *, auth_token: str, list_id: str, user_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Remove a user from a list."""
        return self._client._post("/tw-v2/interaction/remove-from-list", {
            "authToken": auth_token, "listId": list_id, "userId": user_id, "proxy": proxy,
        })

    def get_notifications(self, *, auth_token: str, timeline_type: Optional[str] = None, count: Optional[int] = None, cursor: Optional[str] = None, proxy: Optional[str] = None) -> NotificationPaginatedResponse:
        """Get your notifications."""
        return self._client._get("/tw-v2/interaction/notifications", {
            "authToken": auth_token, "timelineType": timeline_type,
            "count": count, "cursor": cursor, "proxy": proxy,
        })

    def get_user_analytics(self, *, auth_token: str, to_time: Optional[str] = None, from_time: Optional[str] = None, granularity: Optional[str] = None, show_verified_followers: Optional[bool] = None, proxy: Optional[str] = None) -> UserAnalyticsResponse:
        """Get your account analytics."""
        return self._client._get("/tw-v2/interaction/user-analytics", {
            "authToken": auth_token, "toTime": to_time, "fromTime": from_time,
            "granularity": granularity, "showVerifiedFollowers": show_verified_followers,
            "proxy": proxy,
        })
