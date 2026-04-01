from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI


class SpaceResource:
    def __init__(self, client: TweetAPI) -> None:
        self._client = client

    def get_by_id(self, *, space_id: str) -> dict[str, Any]:
        """Get Space details by ID."""
        return self._client._get("/tw-v2/space/by-id", {"spaceId": space_id})

    def get_stream_url(self, *, media_key: str) -> dict[str, Any]:
        """Get the HLS stream URL for a Space."""
        return self._client._get("/tw-v2/space/stream-url", {"mediaKey": media_key})
