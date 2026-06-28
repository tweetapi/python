from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI
    from ..types import ProfileMediaInput, UserResponse


class ProfileResource:
    def __init__(self, client: TweetAPI) -> None:
        self._client = client

    def update(self, *, auth_token: str, name: Optional[str] = None, bio: Optional[str] = None, location: Optional[str] = None, website: Optional[str] = None, proxy: Optional[str] = None) -> UserResponse:
        """Update the authenticated user's profile."""
        return self._client._post("/tw-v2/profile/update", {
            "authToken": auth_token, "name": name, "bio": bio,
            "location": location, "website": website, "proxy": proxy,
        })

    def avatar(self, *, auth_token: str, media: ProfileMediaInput, proxy: Optional[str] = None) -> UserResponse:
        """Update the authenticated user's avatar."""
        return self._client._post("/tw-v2/profile/avatar", {
            "authToken": auth_token, "media": media, "proxy": proxy,
        })

    def banner(self, *, auth_token: str, media: ProfileMediaInput, proxy: Optional[str] = None) -> UserResponse:
        """Update the authenticated user's banner."""
        return self._client._post("/tw-v2/profile/banner", {
            "authToken": auth_token, "media": media, "proxy": proxy,
        })
