"""Directus-specific exceptions for the Directus client."""

from __future__ import annotations

from typing import Any

from ..exceptions import FFBBApiError


class DirectusError(FFBBApiError):
    """Base exception for Directus API errors.

    Attributes:
        error_code: Directus error code (from extensions.code in the response).
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
        error_code: str | None = None,
    ) -> None:
        self.error_code = error_code
        super().__init__(message, status_code=status_code, response_body=response_body)

    @classmethod
    def from_response(
        cls, response_body: dict[str, Any], status_code: int
    ) -> DirectusError:
        """Create a DirectusError from a Directus error response body.

        Directus errors follow the format:
        {"errors": [{"message": "...", "extensions": {"code": "..."}}]}
        """
        errors = response_body.get("errors", [])
        if errors and isinstance(errors, list):
            first_error = errors[0]
            message = first_error.get("message", "Unknown Directus error")
            error_code = first_error.get("extensions", {}).get("code")
        else:
            message = response_body.get("message", f"HTTP {status_code}")
            error_code = None

        if status_code in (401, 403):
            return DirectusAuthError(
                message=message,
                status_code=status_code,
                response_body=response_body,
                error_code=error_code,
            )
        if status_code == 404:
            return DirectusNotFoundError(
                message=message,
                status_code=status_code,
                response_body=response_body,
                error_code=error_code,
            )
        if status_code == 429:
            return DirectusRateLimitError(
                message=message,
                status_code=status_code,
                response_body=response_body,
                error_code=error_code,
            )
        if status_code >= 500:
            return DirectusServerError(
                message=message,
                status_code=status_code,
                response_body=response_body,
                error_code=error_code,
            )

        return cls(
            message=message,
            status_code=status_code,
            response_body=response_body,
            error_code=error_code,
        )


class DirectusAuthError(DirectusError):
    """Raised on Directus authentication/authorization failures (401, 403)."""


class DirectusNotFoundError(DirectusError):
    """Raised when a Directus item/collection is not found (404)."""


class DirectusRateLimitError(DirectusError):
    """Raised when Directus rate limits requests (429)."""


class DirectusServerError(DirectusError):
    """Raised on Directus server errors (500+)."""
