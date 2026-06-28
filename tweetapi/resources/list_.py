from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI
    from ..types import (
        ActionResponse,
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

    def create(self, *, auth_token: str, name: str, description: str = "", is_private: bool = True) -> ListResponse:
        """Create a list."""
        return self._client._post("/tw-v2/list/create", {
            "authToken": auth_token, "name": name, "description": description,
            "isPrivate": is_private,
        })

    def add_member(self, *, auth_token: str, list_id: str, user_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Add a user to a list."""
        return self._client._post("/tw-v2/list/add-member", {
            "authToken": auth_token, "listId": list_id, "userId": user_id,
            "proxy": proxy,
        })

    def remove_member(self, *, auth_token: str, list_id: str, user_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Remove a user from a list."""
        return self._client._post("/tw-v2/list/remove-member", {
            "authToken": auth_token, "listId": list_id, "userId": user_id,
            "proxy": proxy,
        })
