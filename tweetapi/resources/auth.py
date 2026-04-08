from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI
    from ..types import LoginApiResponse


class AuthResource:
    def __init__(self, client: TweetAPI) -> None:
        self._client = client

    def login(self, *, username: str, password: str, proxy: str, two_factor_secret: Optional[str] = None) -> LoginApiResponse:
        """Log in to a Twitter account and get auth tokens."""
        return self._client._post("/tw-v2/auth/login", {
            "username": username, "password": password,
            "proxy": proxy, "twoFactorSecret": two_factor_secret,
        })
