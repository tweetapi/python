from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI
    from ..types import (
        ListResponse,
        TweetsPaginatedResponse,
        UserPaginatedResponse,
    )


class ListResource:
    def __init__(self, client: TweetAPI) -> None:
        self._client = client

    def get_details(self, *, list_id: str) -> ListResponse:
        """Get list details."""
        return self._client._get("/tw-v2/list/details", {"listId": list_id})

    def get_tweets(self, *, list_id: str, cursor: Optional[str] = None) -> TweetsPaginatedResponse:
        """Get tweets in a list."""
        return self._client._get("/tw-v2/list/tweets", {"listId": list_id, "cursor": cursor})

    def get_members(self, *, list_id: str, cursor: Optional[str] = None) -> UserPaginatedResponse:
        """Get members of a list."""
        return self._client._get("/tw-v2/list/members", {"listId": list_id, "cursor": cursor})

    def get_followers(self, *, list_id: str, cursor: Optional[str] = None) -> UserPaginatedResponse:
        """Get followers of a list."""
        return self._client._get("/tw-v2/list/followers", {"listId": list_id, "cursor": cursor})
