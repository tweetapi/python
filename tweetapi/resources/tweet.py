from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI
    from ..types import (
        TweetResponse,
        TweetsPaginatedResponse,
        TweetTranslationResponse,
        UserPaginatedResponse,
    )


class TweetResource:
    def __init__(self, client: TweetAPI) -> None:
        self._client = client

    def get_details_and_conversation(self, *, tweet_id: str, cursor: Optional[str] = None, sort_by: Optional[str] = None) -> TweetsPaginatedResponse:
        """Get tweet details and conversation thread."""
        return self._client._get("/tw-v2/tweet/details", {"tweetId": tweet_id, "cursor": cursor, "sortBy": sort_by})

    def get_details_by_ids(self, *, ids: str) -> dict[str, Any]:
        """Get details for multiple tweets by IDs (comma-separated, max 200)."""
        return self._client._get("/tw-v2/tweet/details-by-ids", {"ids": ids})

    def get_retweets(self, *, tweet_id: str, cursor: Optional[str] = None) -> UserPaginatedResponse:
        """Get users who retweeted a tweet."""
        return self._client._get("/tw-v2/tweet/retweets", {"tweetId": tweet_id, "cursor": cursor})

    def get_quotes(self, *, tweet_id: str, cursor: Optional[str] = None) -> TweetsPaginatedResponse:
        """Get quote tweets for a tweet."""
        return self._client._get("/tw-v2/tweet/quotes", {"tweetId": tweet_id, "cursor": cursor})

    def translate(self, *, tweet_id: str, dst_lang: str) -> TweetTranslationResponse:
        """Translate a tweet to a different language."""
        return self._client._post("/tw-v2/tweet/translate", {"tweetId": tweet_id, "dstLang": dst_lang})
