from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI
    from ..types import (
        ActionResponse,
        MediaStatusResponse,
        MediaUploadInput,
        PollInput,
        ReplyOption,
        TweetMediaInput,
        UploadedMediaResponse,
    )


class PostResource:
    def __init__(self, client: TweetAPI) -> None:
        self._client = client

    def create_post(self, *, auth_token: str, text: str, proxy: str, disable_link_preview: Optional[bool] = None, reply_option: Optional[ReplyOption] = None, poll: Optional[PollInput] = None) -> ActionResponse:
        """Create a new tweet.

        ``poll`` adds a poll: ``{"choices": [...], "durationMinutes": int}`` with 2 to 4
        choices of up to 25 characters, open for 5 to 10080 minutes. A poll can't be
        combined with ``disable_link_preview``, and a post with a poll is limited to
        280 characters.
        """
        return self._client._post("/tw-v2/interaction/create-post", {
            "authToken": auth_token, "text": text, "proxy": proxy,
            "disableLinkPreview": disable_link_preview, "replyOption": reply_option,
            "poll": poll,
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
        }, upload=True)

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
        }, upload=True)

    def delete_post(self, *, auth_token: str, tweet_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Delete a tweet."""
        return self._client._post("/tw-v2/interaction/delete-post", {
            "authToken": auth_token, "tweetId": tweet_id, "proxy": proxy,
        })

    def upload_media(self, *, auth_token: str, proxy: str, media: MediaUploadInput) -> UploadedMediaResponse:
        """Upload one photo, GIF or video to use in a later post.

        ``media`` is one object, not a list: ``{"url": str, "type": str | None}`` or
        ``{"data": str, "type": str}`` (base64 plus MIME type). The API waits up to
        30 seconds for X to process the file, then returns the media ID and its state.

        Pass ``mediaId`` as ``media_id`` in the ``media`` list of a ``*_with_media``
        method with the same ``auth_token``. If ``state`` is ``"pending"`` or
        ``"in_progress"``, call ``get_media_status`` after ``checkAfterSecs`` seconds;
        each status check costs one unit. X discards an unused upload after
        ``expiresAfterSecs`` seconds.
        """
        return self._client._post("/tw-v2/interaction/upload-media", {
            "authToken": auth_token, "proxy": proxy, "media": media,
        }, upload=True)

    def get_media_status(self, *, auth_token: str, proxy: str, media_id: str) -> MediaStatusResponse:
        """Check whether an uploaded video or GIF has finished processing.

        Use the ``auth_token`` that uploaded it and wait ``checkAfterSecs`` seconds
        between checks. Each check costs one unit. When ``state`` is ``"failed"``,
        ``error`` holds X's reason.
        """
        return self._client._get("/tw-v2/interaction/media-status", {
            "authToken": auth_token, "proxy": proxy, "mediaId": media_id,
        })

    def pin_post(self, *, auth_token: str, tweet_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Pin one of your tweets to the top of your profile.

        ``metadata.added_to_highlights`` says whether X also added it to the Highlights tab.
        """
        return self._client._post("/tw-v2/interaction/pin-post", {
            "authToken": auth_token, "tweetId": tweet_id, "proxy": proxy,
        })

    def unpin_post(self, *, auth_token: str, tweet_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Unpin a tweet from the top of your profile."""
        return self._client._post("/tw-v2/interaction/unpin-post", {
            "authToken": auth_token, "tweetId": tweet_id, "proxy": proxy,
        })

    def hide_reply(self, *, auth_token: str, tweet_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Hide a reply to one of your tweets. ``tweet_id`` is the reply."""
        return self._client._post("/tw-v2/interaction/hide-reply", {
            "authToken": auth_token, "tweetId": tweet_id, "proxy": proxy,
        })

    def unhide_reply(self, *, auth_token: str, tweet_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Show a hidden reply to one of your tweets again. ``tweet_id`` is the reply."""
        return self._client._post("/tw-v2/interaction/unhide-reply", {
            "authToken": auth_token, "tweetId": tweet_id, "proxy": proxy,
        })
