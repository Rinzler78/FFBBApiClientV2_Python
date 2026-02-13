"""Meilisearch-specific exceptions for the MeilisearchClient."""

from __future__ import annotations

from typing import Any

from ..exceptions import FFBBApiError


class MeilisearchError(FFBBApiError):
    """Base exception for Meilisearch API errors.

    Attributes:
        error_code: Meilisearch error code (e.g., 'invalid_search_filter').
        error_type: Meilisearch error type (e.g., 'invalid_request').
        error_link: Link to Meilisearch documentation for this error.
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
        error_code: str | None = None,
        error_type: str | None = None,
        error_link: str | None = None,
    ) -> None:
        self.error_code = error_code
        self.error_type = error_type
        self.error_link = error_link
        super().__init__(message, status_code=status_code, response_body=response_body)

    @classmethod
    def from_response(
        cls, response_body: dict[str, Any], status_code: int | None = None
    ) -> MeilisearchError:
        """Create a MeilisearchError from a Meilisearch error response body.

        Meilisearch errors follow the format:
        {"message": "...", "code": "...", "type": "...", "link": "..."}
        """
        message = response_body.get("message", "Unknown Meilisearch error")
        error_code = response_body.get("code")
        error_type = response_body.get("type")
        error_link = response_body.get("link")

        if error_code == "index_not_found":
            return MeilisearchIndexNotFoundError(
                message=message,
                status_code=status_code,
                response_body=response_body,
                error_code=error_code,
                error_type=error_type,
                error_link=error_link,
            )
        if error_code and error_code.startswith("invalid_search"):
            return MeilisearchInvalidFilterError(
                message=message,
                status_code=status_code,
                response_body=response_body,
                error_code=error_code,
                error_type=error_type,
                error_link=error_link,
            )

        return cls(
            message=message,
            status_code=status_code,
            response_body=response_body,
            error_code=error_code,
            error_type=error_type,
            error_link=error_link,
        )


class MeilisearchIndexNotFoundError(MeilisearchError):
    """Raised when a Meilisearch index does not exist."""


class MeilisearchInvalidFilterError(MeilisearchError):
    """Raised when a Meilisearch search filter or parameter is invalid."""
