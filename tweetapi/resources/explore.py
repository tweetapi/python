from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI


class ExploreResource:
    def __init__(self, client: TweetAPI) -> None:
        self._client = client

    def search(self, *, query: str, type: str, cursor: Optional[str] = None) -> dict[str, Any]:
        """Search for tweets, users, photos, or videos.

        Args:
            query: Search query string. Supports Twitter search operators.
            type: Type of search results — "Latest", "Top", "People", "Photos", or "Videos".
            cursor: Pagination cursor for fetching next page.
        """
        return self._client._get("/tw-v2/search", {"query": query, "type": type, "cursor": cursor})
