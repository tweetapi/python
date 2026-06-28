from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI
    from ..types import ActionResponse, ReplyOption, TweetMediaInput


class PostResource:
    def __init__(self, client: TweetAPI) -> None:
        self._client = client

    def create_post(self, *, auth_token: str, text: str, proxy: str, disable_link_preview: Optional[bool] = None, reply_option: Optional[ReplyOption] = None) -> ActionResponse:
        """Create a new tweet."""
        return self._client._post("/tw-v2/interaction/create-post", {
            "authToken": auth_token, "text": text, "proxy": proxy,
            "disableLinkPreview": disable_link_preview, "replyOption": reply_option,
        })

    def create_post_quote(self, *, auth_token: str, text: str, attachment_url: str, proxy: str, disable_link_preview: Optional[bool] = None, reply_option: Optional[ReplyOption] = None) -> ActionResponse:
        """Create a quote tweet."""
        return self._client._post("/tw-v2/interaction/create-post-quote", {
            "authToken": auth_token, "text": text, "attachmentUrl": attachment_url,
            "proxy": proxy, "disableLinkPreview": disable_link_preview,
            "replyOption": reply_option,
        })

    def create_post_with_media(self, *, auth_token: str, text: str, media: list[TweetMediaInput], proxy: str, disable_link_preview: Optional[bool] = None, reply_option: Optional[ReplyOption] = None) -> ActionResponse:
        """Create a tweet with media attachments.

        ``media`` accepts items shaped as ``{"media_id": str}``,
        ``{"url": str, "type": str | None}``, or ``{"data": str, "type": str}``.
        """
        return self._client._post("/tw-v2/interaction/create-post-with-media", {
            "authToken": auth_token, "text": text, "media": media,
            "proxy": proxy, "disableLinkPreview": disable_link_preview,
            "replyOption": reply_option,
        })

    def reply_post(self, *, auth_token: str, text: str, tweet_id: str, proxy: str, disable_link_preview: Optional[bool] = None) -> ActionResponse:
        """Reply to a tweet."""
        return self._client._post("/tw-v2/interaction/reply-post", {
            "authToken": auth_token, "text": text, "tweetId": tweet_id,
            "proxy": proxy, "disableLinkPreview": disable_link_preview,
        })

    def reply_post_with_media(self, *, auth_token: str, text: str, tweet_id: str, media: list[Any], proxy: str, disable_link_preview: Optional[bool] = None) -> ActionResponse:
        """Reply to a tweet with media attachments."""
        return self._client._post("/tw-v2/interaction/reply-post-with-media", {
            "authToken": auth_token, "text": text, "tweetId": tweet_id,
            "media": media, "proxy": proxy, "disableLinkPreview": disable_link_preview,
        })

    def delete_post(self, *, auth_token: str, tweet_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Delete a tweet."""
        return self._client._post("/tw-v2/interaction/delete-post", {
            "authToken": auth_token, "tweetId": tweet_id, "proxy": proxy,
        })
