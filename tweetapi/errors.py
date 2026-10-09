from __future__ import annotations

from typing import Any, Optional


class ErrorCode:
    """Error codes the API returns in ``TweetAPIError.code``.

    Errors without a specific code use ``UNKNOWN_ERROR``; newer API versions may add codes.
    """

    RATE_LIMITED = "RATE_LIMITED"
    """Per-minute limit reached. ``RateLimitError.retry_after`` says when it resets."""
    QUOTA_EXHAUSTED = "QUOTA_EXHAUSTED"
    """Plan allowance or prepaid balance used up. Retrying does not help."""
    SUBSCRIPTION_INACTIVE = "SUBSCRIPTION_INACTIVE"
    """Plan expired or inactive. Retrying does not help."""
    ACCOUNT_SUSPENDED = "ACCOUNT_SUSPENDED"
    """The Twitter account behind ``auth_token`` is suspended."""
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    """The Twitter account behind ``auth_token`` is locked."""
    PROXY_ERROR = "PROXY_ERROR"
    """Your ``proxy`` refused or could not be reached."""
    PROXY_TIMEOUT = "PROXY_TIMEOUT"
    """Your ``proxy`` timed out."""
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    """Login: wrong username or password."""
    TWO_FACTOR_REQUIRED = "TWO_FACTOR_REQUIRED"
    """Login: the account needs ``two_factor_secret``."""
    INVALID_TWO_FACTOR_CODE = "INVALID_TWO_FACTOR_CODE"
    """Login: the two-factor code was rejected."""
    EMAIL_VERIFICATION_REQUIRED = "EMAIL_VERIFICATION_REQUIRED"
    """Login: the account must verify its email first."""
    LOGIN_RUNTIME_UNAVAILABLE = "LOGIN_RUNTIME_UNAVAILABLE"
    """Login: X could not be reached; try again later."""
    CONNECTION_ERROR = "CONNECTION_ERROR"
    """No response was received (network failure or timeout)."""
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    """The response did not include a specific code."""


class TweetAPIError(Exception):
    """Base error for all TweetAPI errors.

    Contains the API error code, HTTP status, and optional details.
    """

    def __init__(
        self,
        message: str,
        code: str,
        status_code: int,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code={self.code!r}, status_code={self.status_code}, message={self.message!r})"


class AuthenticationError(TweetAPIError):
    """Thrown when the API key or auth token is invalid or missing (HTTP 401)."""

    def __init__(
        self,
        message: str,
        code: str,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, code, 401, details)


class ForbiddenError(TweetAPIError):
    """Thrown when the request is forbidden (HTTP 403)."""

    def __init__(
        self,
        message: str,
        code: str,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, code, 403, details)


class NotFoundError(TweetAPIError):
    """Thrown when the requested resource is not found (HTTP 404)."""

    def __init__(
        self,
        message: str,
        code: str,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, code, 404, details)


class ValidationError(TweetAPIError):
    """Thrown when the request parameters are invalid (HTTP 400)."""

    def __init__(
        self,
        message: str,
        code: str,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, code, 400, details)


class RateLimitError(TweetAPIError):
    """Thrown on HTTP 429.

    Check ``code``: ``RATE_LIMITED`` clears after ``retry_after`` seconds, while
    ``QUOTA_EXHAUSTED`` and ``SUBSCRIPTION_INACTIVE`` need a plan change.
    ``retry_after`` is the API's ``Retry-After``, or 60 when it sends none.
    """

    def __init__(
        self,
        message: str,
        code: str,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, code, 429, details)
        self.retry_after: int = (details or {}).get("retryAfter", 60)


class ServerError(TweetAPIError):
    """Thrown when the API encounters a server error (HTTP 5xx)."""

    def __init__(
        self,
        message: str,
        code: str,
        status_code: int,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, code, status_code, details)


class ConnectionError_(TweetAPIError):
    """Thrown when a network error occurs (DNS failure, timeout, connection refused).

    Named ``ConnectionError_`` to avoid shadowing the built-in ``ConnectionError``.
    Also importable as ``NetworkError``.
    """

    def __init__(self, message: str, cause: Optional[Exception] = None) -> None:
        super().__init__(message, ErrorCode.CONNECTION_ERROR, 0, None)
        self.__cause__ = cause


# Alias for cleaner imports
NetworkError = ConnectionError_
