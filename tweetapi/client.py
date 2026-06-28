from __future__ import annotations

import random
import time
from typing import Any, Optional, Union

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
        timeout: Request timeout in seconds. Pass a tuple ``(connect, read)`` for
            split timeouts. Default: ``(10, 30)``.
        connect_timeout: Connection timeout in seconds (used when *timeout* is not set).
        read_timeout: Read timeout in seconds (used when *timeout* is not set).
        max_retries: Maximum retry attempts on transient errors (default: 3, set 0 to disable).
        backoff_multiplier: Multiplier for exponential backoff (default: 2.0).
        initial_retry_delay: Initial retry delay in seconds (default: 1.0).
        max_retry_delay: Maximum retry delay cap in seconds (default: 30.0).
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.tweetapi.com",
        timeout: Optional[Union[float, tuple[float, float]]] = None,
        connect_timeout: Optional[float] = None,
        read_timeout: Optional[float] = None,
        max_retries: int = 3,
        backoff_multiplier: float = 2.0,
        initial_retry_delay: float = 1.0,
        max_retry_delay: float = 30.0,
    ) -> None:
        if not api_key:
            raise ValueError("TweetAPI: api_key is required")

        self._base_url = base_url.rstrip("/")

        # Timeout resolution
        if timeout is not None:
            self._timeout: Union[float, tuple[float, float]] = timeout
        elif connect_timeout is not None or read_timeout is not None:
            self._timeout = (
                connect_timeout if connect_timeout is not None else 10.0,
                read_timeout if read_timeout is not None else 30.0,
            )
        else:
            self._timeout = (10.0, 30.0)

        # Retry configuration
        self._max_retries = max_retries
        self._backoff_multiplier = backoff_multiplier
        self._initial_retry_delay = initial_retry_delay
        self._max_retry_delay = max_retry_delay
        self._rate_limit_info: Optional[dict[str, Any]] = None

        self._session = requests.Session()
        self._session.headers.update({"X-API-Key": api_key})

        # Lazy imports to avoid circular dependencies
        from .resources.user import UserResource
        from .resources.tweet import TweetResource
        from .resources.post import PostResource
        from .resources.interaction import InteractionResource
        from .resources.list_ import ListResource
        from .resources.profile import ProfileResource
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
        self.profile = ProfileResource(self)
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

    @property
    def rate_limit_info(self) -> Optional[dict[str, Any]]:
        """Last known rate limit info from a 429 response, or ``None``."""
        return self._rate_limit_info

    # ── internal helpers ─────────────────────────────────────────────────

    @property
    def _timeout_desc(self) -> str:
        if isinstance(self._timeout, tuple):
            return f"connect={self._timeout[0]}s, read={self._timeout[1]}s"
        return f"{self._timeout}s"

    def _is_retryable(self, error: TweetAPIError) -> bool:
        if isinstance(error, ConnectionError_):
            return True
        return error.status_code == 429 or error.status_code >= 500

    def _calculate_retry_delay(self, error: Optional[TweetAPIError], attempt: int) -> float:
        if isinstance(error, RateLimitError) and error.retry_after > 0:
            return min(float(error.retry_after), self._max_retry_delay)
        base = self._initial_retry_delay * (self._backoff_multiplier ** attempt)
        capped = min(base, self._max_retry_delay)
        return capped + random.random() * capped * 0.25

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> Any:
        url = f"{self._base_url}{path}"
        last_error: Optional[TweetAPIError] = None

        for attempt in range(self._max_retries + 1):
            try:
                response = self._session.request(
                    method,
                    url,
                    params=params,
                    json=json,
                    timeout=self._timeout,
                )
            except requests.exceptions.Timeout as e:
                last_error = ConnectionError_(
                    f"Request timed out ({self._timeout_desc})", e
                )
                if attempt < self._max_retries:
                    time.sleep(self._calculate_retry_delay(last_error, attempt))
                    continue
                raise last_error from e
            except requests.exceptions.ConnectionError as e:
                last_error = ConnectionError_(f"Network error: {e}", e)
                if attempt < self._max_retries:
                    time.sleep(self._calculate_retry_delay(last_error, attempt))
                    continue
                raise last_error from e
            except requests.exceptions.RequestException as e:
                last_error = ConnectionError_(f"Request failed: {e}", e)
                if attempt < self._max_retries:
                    time.sleep(self._calculate_retry_delay(last_error, attempt))
                    continue
                raise last_error from e

            if not response.ok:
                try:
                    self._handle_error_response(response)
                except TweetAPIError as err:
                    last_error = err
                    if isinstance(err, RateLimitError):
                        self._rate_limit_info = {
                            "retry_after": err.retry_after,
                            "timestamp": time.time(),
                        }
                    if attempt < self._max_retries and self._is_retryable(err):
                        time.sleep(self._calculate_retry_delay(err, attempt))
                        continue
                    raise

            return response.json()

        raise last_error  # type: ignore[misc]

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
