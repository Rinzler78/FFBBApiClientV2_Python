"""
Structured exception hierarchy for FFBB API Client V2.

This module contains only the shared base exceptions.
Client-specific exceptions are in their own modules:
- directus_exceptions.py for Directus API errors
- meilisearch_exceptions.py for Meilisearch API errors
"""

from __future__ import annotations

from typing import Any


class FFBBApiError(Exception):
    """Base exception for all FFBB API errors.

    Attributes:
        message: Human-readable error description.
        status_code: HTTP status code if applicable.
        response_body: Raw response body if available.
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message)


class FFBBNetworkError(FFBBApiError):
    """Raised on network-level failures (timeout, connection refused, DNS)."""

    def __init__(
        self,
        message: str,
        original_exception: Exception | None = None,
    ) -> None:
        self.original_exception = original_exception
        super().__init__(message)


class FFBBAuthError(FFBBApiError):
    """Raised on authentication/authorization failures (HTTP 401, 403)."""

    def __init__(
        self,
        message: str = "Authentication failed",
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=status_code, response_body=response_body)


class FFBBNotFoundError(FFBBApiError):
    """Raised when a requested resource is not found (HTTP 404)."""

    def __init__(
        self,
        message: str = "Resource not found",
        status_code: int | None = 404,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=status_code, response_body=response_body)


class FFBBRateLimitError(FFBBApiError):
    """Raised when rate limited (HTTP 429) after all retries are exhausted."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        status_code: int | None = 429,
        response_body: dict[str, Any] | None = None,
        retry_after: float | None = None,
    ) -> None:
        self.retry_after = retry_after
        super().__init__(message, status_code=status_code, response_body=response_body)


class FFBBValidationError(FFBBApiError):
    """Raised on invalid request parameters (bad filter, unknown field, etc.)."""

    def __init__(
        self,
        message: str = "Validation error",
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=status_code, response_body=response_body)


class FFBBServerError(FFBBApiError):
    """Raised on server-side errors (HTTP 500, 502, 503, 504)."""

    def __init__(
        self,
        message: str = "Server error",
        status_code: int | None = 500,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=status_code, response_body=response_body)
