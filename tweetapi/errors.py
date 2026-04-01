from __future__ import annotations

from typing import Any, Optional


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
    """Thrown when you've exceeded rate limits (HTTP 429).

    Check ``retry_after`` for seconds until you can retry.
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
        super().__init__(message, "CONNECTION_ERROR", 0, None)
        self.__cause__ = cause


# Alias for cleaner imports
NetworkError = ConnectionError_
