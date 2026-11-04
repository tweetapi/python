from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI
    from ..types import (
        ActionResponse,
        FollowRequestsResponse,
        NotificationPaginatedResponse,
        TweetsPaginatedResponse,
        UserAnalyticsResponse,
        UserPaginatedResponse,
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

    def vote_poll(self, *, auth_token: str, tweet_id: str, choice: int, proxy: Optional[str] = None) -> ActionResponse:
        """Vote in the poll on a tweet.

        ``choice`` is the option number, 1 to 4, in the order x.com shows the options.
        """
        return self._client._post("/tw-v2/interaction/vote-poll", {
            "authToken": auth_token, "tweetId": tweet_id, "choice": choice, "proxy": proxy,
        })

    def follow(self, *, auth_token: str, user_id: str, username: Optional[str] = None, proxy: Optional[str] = None) -> ActionResponse:
        """Follow a user. ``username`` is the optional username of the target account."""
        return self._client._post("/tw-v2/interaction/follow", {
            "authToken": auth_token, "userId": user_id, "username": username, "proxy": proxy,
        })

    def unfollow(self, *, auth_token: str, user_id: str, username: Optional[str] = None, proxy: Optional[str] = None) -> ActionResponse:
        """Unfollow a user. ``username`` is the optional username of the target account."""
        return self._client._post("/tw-v2/interaction/unfollow", {
            "authToken": auth_token, "userId": user_id, "username": username, "proxy": proxy,
        })

    def remove_follower(self, *, auth_token: str, user_id: str, username: Optional[str] = None, proxy: Optional[str] = None) -> ActionResponse:
        """Make a user stop following you. ``username`` is the optional username of the follower."""
        return self._client._post("/tw-v2/interaction/remove-follower", {
            "authToken": auth_token, "userId": user_id, "username": username, "proxy": proxy,
        })

    def block(self, *, auth_token: str, user_id: str, username: Optional[str] = None, proxy: Optional[str] = None) -> ActionResponse:
        """Block a user. ``username`` is the optional username of the target account."""
        return self._client._post("/tw-v2/interaction/block", {
            "authToken": auth_token, "userId": user_id, "username": username, "proxy": proxy,
        })

    def unblock(self, *, auth_token: str, user_id: str, username: Optional[str] = None, proxy: Optional[str] = None) -> ActionResponse:
        """Unblock a user. ``username`` is the optional username of the target account."""
        return self._client._post("/tw-v2/interaction/unblock", {
            "authToken": auth_token, "userId": user_id, "username": username, "proxy": proxy,
        })

    def mute(self, *, auth_token: str, user_id: str, username: Optional[str] = None, proxy: Optional[str] = None) -> ActionResponse:
        """Mute a user. ``username`` is the optional username of the target account."""
        return self._client._post("/tw-v2/interaction/mute", {
            "authToken": auth_token, "userId": user_id, "username": username, "proxy": proxy,
        })

    def unmute(self, *, auth_token: str, user_id: str, username: Optional[str] = None, proxy: Optional[str] = None) -> ActionResponse:
        """Unmute a user. ``username`` is the optional username of the target account."""
        return self._client._post("/tw-v2/interaction/unmute", {
            "authToken": auth_token, "userId": user_id, "username": username, "proxy": proxy,
        })

    def get_follow_requests(self, *, auth_token: str, proxy: Optional[str] = None, cursor: Optional[str] = None, count: Optional[int] = None) -> FollowRequestsResponse:
        """List pending requester IDs for the supplied session's account.

        Omit cursor/count for server defaults ("-1"/100). Count must be an
        integer from 1 to 100. Terminal cursors are returned as None.
        """
        return self._client._get("/tw-v2/interaction/follow-requests", {
            "authToken": auth_token, "proxy": proxy, "cursor": cursor, "count": count,
        })

    def accept_follow_request(self, *, auth_token: str, user_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Accept a pending request from a digit-only user ID string.

        Automatic retries are disabled. A timeout leaves the outcome uncertain;
        reconcile the account state before retrying manually.
        """
        return self._client._post("/tw-v2/interaction/accept-follow-request", {
            "authToken": auth_token, "userId": user_id, "proxy": proxy,
        }, retry=False)

    def deny_follow_request(self, *, auth_token: str, user_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Deny a pending request from a digit-only user ID string.

        Automatic retries are disabled. A timeout leaves the outcome uncertain;
        reconcile the account state before retrying manually.
        """
        return self._client._post("/tw-v2/interaction/deny-follow-request", {
            "authToken": auth_token, "userId": user_id, "proxy": proxy,
        }, retry=False)

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

    def get_bookmarks(self, *, auth_token: str, cursor: Optional[str] = None, proxy: Optional[str] = None) -> TweetsPaginatedResponse:
        """Get the posts bookmarked by the ``auth_token`` account."""
        return self._client._get("/tw-v2/interaction/bookmarks", {
            "authToken": auth_token, "cursor": cursor, "proxy": proxy,
        })

    def get_likes(self, *, auth_token: str, user_id: str, cursor: Optional[str] = None, proxy: Optional[str] = None) -> TweetsPaginatedResponse:
        """Get the posts liked by the ``auth_token`` account.

        ``user_id`` must be the numeric ID of that same account.
        """
        return self._client._get("/tw-v2/interaction/likes", {
            "authToken": auth_token, "userId": user_id, "cursor": cursor, "proxy": proxy,
        })

    def get_blocked_accounts(self, *, auth_token: str, cursor: Optional[str] = None, proxy: Optional[str] = None) -> UserPaginatedResponse:
        """Get the accounts blocked by the ``auth_token`` account."""
        return self._client._get("/tw-v2/interaction/blocked-accounts", {
            "authToken": auth_token, "cursor": cursor, "proxy": proxy,
        })

    def get_muted_accounts(self, *, auth_token: str, cursor: Optional[str] = None, proxy: Optional[str] = None) -> UserPaginatedResponse:
        """Get the accounts muted by the ``auth_token`` account."""
        return self._client._get("/tw-v2/interaction/muted-accounts", {
            "authToken": auth_token, "cursor": cursor, "proxy": proxy,
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
