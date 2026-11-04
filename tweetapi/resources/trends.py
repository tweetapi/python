from __future__ import annotations

from typing import Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI
    from ..types import TrendLocationsResponse, TrendsByPlaceResponse


class TrendsResource:
    def __init__(self, client: TweetAPI) -> None:
        self._client = client

    def get(self, *, country: Optional[str] = None, woeid: Optional[Union[str, int]] = None) -> TrendsByPlaceResponse:
        """Get the trending topics worldwide, in a country, or at a WOEID.

        Pass ``country`` (a two-letter code such as "US") or ``woeid``, not both.
        Omit both for worldwide trends. ``tweetVolume`` is ``None`` when X reports no volume.
        """
        return self._client._get("/tw-v2/trends", {"country": country, "woeid": woeid})

    def get_locations(self) -> TrendLocationsResponse:
        """List the locations X serves trends for, with the WOEID to pass to ``get``."""
        return self._client._get("/tw-v2/trends/locations")
