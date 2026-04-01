from __future__ import annotations

from typing import Any, Optional

import requests

from .errors import (
    TweetAPIError,
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
    ConnectionError_,
)


class TweetAPI:
    """TweetAPI Python SDK client.

    Args:
        api_key: Your TweetAPI API key.
        base_url: Base URL for the API (default: https://api.tweetapi.com).
        timeout: Request timeout in seconds (default: 30).
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.tweetapi.com",
        timeout: int = 30,
    ) -> None:
        if not api_key:
            raise ValueError("TweetAPI: api_key is required")

        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"X-API-Key": api_key})

        # Lazy imports to avoid circular dependencies
        from .resources.user import UserResource
        from .resources.tweet import TweetResource
        from .resources.post import PostResource
        from .resources.interaction import InteractionResource
        from .resources.list_ import ListResource
        from .resources.community import CommunityResource
        from .resources.space import SpaceResource
        from .resources.explore import ExploreResource
        from .resources.auth import AuthResource
        from .resources.xchat import XChatResource
        from .resources.unencrypted_dm import UnencryptedDMResource

        self.user = UserResource(self)
        self.tweet = TweetResource(self)
        self.post = PostResource(self)
        self.interaction = InteractionResource(self)
        self.list = ListResource(self)
        self.community = CommunityResource(self)
        self.space = SpaceResource(self)
        self.explore = ExploreResource(self)
        self.auth = AuthResource(self)
        self.xchat = XChatResource(self)
        self.dm = UnencryptedDMResource(self)

    def _get(self, path: str, params: Optional[dict[str, Any]] = None) -> Any:
        """Send a GET request to the API."""
        clean_params = None
        if params:
            clean_params = {
                k: v for k, v in params.items() if v is not None
            }
        return self._request("GET", path, params=clean_params)

    def _post(self, path: str, body: Optional[dict[str, Any]] = None) -> Any:
        """Send a POST request to the API."""
        clean_body = None
        if body:
            clean_body = {k: v for k, v in body.items() if v is not None}
        return self._request("POST", path, json=clean_body)

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> Any:
        url = f"{self._base_url}{path}"

        try:
            response = self._session.request(
                method,
                url,
                params=params,
                json=json,
                timeout=self._timeout,
            )
        except requests.exceptions.Timeout as e:
            raise ConnectionError_(
                f"Request timed out after {self._timeout}s", e
            ) from e
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError_(f"Network error: {e}", e) from e
        except requests.exceptions.RequestException as e:
            raise ConnectionError_(f"Request failed: {e}", e) from e

        if not response.ok:
            self._handle_error_response(response)

        return response.json()

    def _handle_error_response(self, response: requests.Response) -> None:
        """Parse error response and raise the appropriate exception."""
        try:
            body = response.json()
        except (ValueError, requests.exceptions.JSONDecodeError):
            body = None

        code = "UNKNOWN_ERROR"
        message = f"HTTP {response.status_code}"
        details = None

        if body and isinstance(body.get("error"), dict):
            error = body["error"]
            code = error.get("code", code)
            message = error.get("message", message)
            details = error.get("details")

        status = response.status_code

        if status == 400:
            raise ValidationError(message, code, details)
        elif status == 401:
            raise AuthenticationError(message, code, details)
        elif status == 403:
            raise ForbiddenError(message, code, details)
        elif status == 404:
            raise NotFoundError(message, code, details)
        elif status == 429:
            raise RateLimitError(message, code, details)
        elif status >= 500:
            raise ServerError(message, code, status, details)
        else:
            raise TweetAPIError(message, code, status, details)
