from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI


class CommunityResource:
    def __init__(self, client: TweetAPI) -> None:
        self._client = client

    def get_details(self, *, community_id: str) -> dict[str, Any]:
        """Get community details."""
        return self._client._get("/tw-v2/community/details", {"communityId": community_id})

    def get_tweets(self, *, community_id: str, sort_by: str, cursor: Optional[str] = None) -> dict[str, Any]:
        """Get tweets in a community."""
        return self._client._get("/tw-v2/community/tweets", {"communityId": community_id, "sortBy": sort_by, "cursor": cursor})

    def get_members(self, *, community_id: str, cursor: Optional[str] = None) -> dict[str, Any]:
        """Get community members."""
        return self._client._get("/tw-v2/community/members", {"communityId": community_id, "cursor": cursor})

    def search(self, *, query: str, cursor: Optional[str] = None) -> dict[str, Any]:
        """Search communities."""
        return self._client._get("/tw-v2/community/search", {"query": query, "cursor": cursor})

    def create_post(self, *, auth_token: str, text: str, community_id: str, proxy: str, disable_link_preview: Optional[bool] = None) -> dict[str, Any]:
        """Create a post in a community."""
        return self._client._post("/tw-v2/interaction/create-community-post", {
            "authToken": auth_token, "text": text, "communityId": community_id,
            "proxy": proxy, "disableLinkPreview": disable_link_preview,
        })

    def create_post_with_media(self, *, auth_token: str, text: str, community_id: str, media: list[Any], proxy: str, disable_link_preview: Optional[bool] = None) -> dict[str, Any]:
        """Create a post with media in a community."""
        return self._client._post("/tw-v2/interaction/create-community-post-with-media", {
            "authToken": auth_token, "text": text, "communityId": community_id,
            "media": media, "proxy": proxy, "disableLinkPreview": disable_link_preview,
        })

    def reply_post(self, *, auth_token: str, text: str, tweet_id: str, community_id: str, proxy: str, disable_link_preview: Optional[bool] = None) -> dict[str, Any]:
        """Reply to a community post."""
        return self._client._post("/tw-v2/interaction/reply-community-post", {
            "authToken": auth_token, "text": text, "tweetId": tweet_id,
            "communityId": community_id, "proxy": proxy, "disableLinkPreview": disable_link_preview,
        })

    def reply_post_with_media(self, *, auth_token: str, text: str, tweet_id: str, community_id: str, media: list[Any], proxy: str, disable_link_preview: Optional[bool] = None) -> dict[str, Any]:
        """Reply to a community post with media."""
        return self._client._post("/tw-v2/interaction/reply-community-post-with-media", {
            "authToken": auth_token, "text": text, "tweetId": tweet_id,
            "communityId": community_id, "media": media, "proxy": proxy,
            "disableLinkPreview": disable_link_preview,
        })

    def join(self, *, auth_token: str, community_id: str, proxy: Optional[str] = None) -> dict[str, Any]:
        """Join a community."""
        return self._client._post("/tw-v2/interaction/join-community", {
            "authToken": auth_token, "communityId": community_id, "proxy": proxy,
        })

    def leave(self, *, auth_token: str, community_id: str, proxy: Optional[str] = None) -> dict[str, Any]:
        """Leave a community."""
        return self._client._post("/tw-v2/interaction/leave-community", {
            "authToken": auth_token, "communityId": community_id, "proxy": proxy,
        })
