"""Tests for the structured exception hierarchy."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.directus_exceptions import (
    DirectusAuthError,
    DirectusError,
    DirectusNotFoundError,
    DirectusRateLimitError,
    DirectusServerError,
)
from ffbb_api_client_v2.exceptions import (
    FFBBApiError,
    FFBBAuthError,
    FFBBNetworkError,
    FFBBNotFoundError,
    FFBBRateLimitError,
    FFBBServerError,
    FFBBValidationError,
)
from ffbb_api_client_v2.meilisearch_exceptions import (
    MeilisearchError,
    MeilisearchIndexNotFoundError,
    MeilisearchInvalidFilterError,
)


class Test213BaseExceptions(unittest.TestCase):
    """Tests for the shared base exception classes."""

    def test_000_ffbb_api_error_basic(self) -> None:
        err = FFBBApiError("test error")
        self.assertEqual(str(err), "test error")
        self.assertEqual(err.message, "test error")
        self.assertIsNone(err.status_code)
        self.assertIsNone(err.response_body)

    def test_001_ffbb_api_error_with_status(self) -> None:
        err = FFBBApiError("test", status_code=400, response_body={"key": "val"})
        self.assertEqual(err.status_code, 400)
        self.assertEqual(err.response_body, {"key": "val"})

    def test_002_ffbb_api_error_is_exception(self) -> None:
        err = FFBBApiError("test")
        self.assertIsInstance(err, Exception)

    def test_003_ffbb_network_error(self) -> None:
        original = ConnectionError("refused")
        err = FFBBNetworkError("Network failed", original_exception=original)
        self.assertEqual(err.message, "Network failed")
        self.assertIs(err.original_exception, original)
        self.assertIsInstance(err, FFBBApiError)

    def test_004_ffbb_auth_error(self) -> None:
        err = FFBBAuthError(status_code=401)
        self.assertEqual(err.message, "Authentication failed")
        self.assertEqual(err.status_code, 401)
        self.assertIsInstance(err, FFBBApiError)

    def test_005_ffbb_not_found_error(self) -> None:
        err = FFBBNotFoundError()
        self.assertEqual(err.status_code, 404)
        self.assertIsInstance(err, FFBBApiError)

    def test_006_ffbb_rate_limit_error(self) -> None:
        err = FFBBRateLimitError(retry_after=30.0)
        self.assertEqual(err.status_code, 429)
        self.assertEqual(err.retry_after, 30.0)
        self.assertIsInstance(err, FFBBApiError)

    def test_007_ffbb_validation_error(self) -> None:
        err = FFBBValidationError("bad filter")
        self.assertEqual(err.message, "bad filter")
        self.assertIsInstance(err, FFBBApiError)

    def test_008_ffbb_server_error(self) -> None:
        err = FFBBServerError(status_code=502)
        self.assertEqual(err.status_code, 502)
        self.assertIsInstance(err, FFBBApiError)


class Test213DirectusExceptions(unittest.TestCase):
    """Tests for Directus-specific exceptions."""

    def test_000_directus_error_basic(self) -> None:
        err = DirectusError("test", error_code="FORBIDDEN")
        self.assertEqual(err.error_code, "FORBIDDEN")
        self.assertIsInstance(err, FFBBApiError)

    def test_001_directus_error_from_response_401(self) -> None:
        body: dict[str, Any] = {
            "errors": [
                {
                    "message": "You don't have permission",
                    "extensions": {"code": "FORBIDDEN"},
                }
            ]
        }
        err = DirectusError.from_response(body, status_code=403)
        self.assertIsInstance(err, DirectusAuthError)
        self.assertEqual(err.message, "You don't have permission")
        self.assertEqual(err.error_code, "FORBIDDEN")
        self.assertEqual(err.status_code, 403)

    def test_002_directus_error_from_response_404(self) -> None:
        body: dict[str, Any] = {
            "errors": [
                {"message": "Item not found", "extensions": {"code": "ITEM_NOT_FOUND"}}
            ]
        }
        err = DirectusError.from_response(body, status_code=404)
        self.assertIsInstance(err, DirectusNotFoundError)

    def test_003_directus_error_from_response_429(self) -> None:
        body: dict[str, Any] = {"errors": [{"message": "Rate limited"}]}
        err = DirectusError.from_response(body, status_code=429)
        self.assertIsInstance(err, DirectusRateLimitError)

    def test_004_directus_error_from_response_500(self) -> None:
        body: dict[str, Any] = {"errors": [{"message": "Internal error"}]}
        err = DirectusError.from_response(body, status_code=500)
        self.assertIsInstance(err, DirectusServerError)

    def test_005_directus_error_from_response_generic(self) -> None:
        body: dict[str, Any] = {"errors": [{"message": "Bad request"}]}
        err = DirectusError.from_response(body, status_code=400)
        self.assertIsInstance(err, DirectusError)
        self.assertNotIsInstance(err, DirectusAuthError)

    def test_006_directus_error_no_errors_key(self) -> None:
        body: dict[str, Any] = {"message": "Something went wrong"}
        err = DirectusError.from_response(body, status_code=400)
        self.assertEqual(err.message, "Something went wrong")

    def test_007_directus_hierarchy_isolation(self) -> None:
        """Directus errors should NOT be instances of Meilisearch errors."""
        err = DirectusAuthError("test")
        self.assertNotIsInstance(err, MeilisearchError)


class Test213MeilisearchExceptions(unittest.TestCase):
    """Tests for Meilisearch-specific exceptions."""

    def test_000_meilisearch_error_basic(self) -> None:
        err = MeilisearchError("test", error_code="invalid_api_key")
        self.assertEqual(err.error_code, "invalid_api_key")
        self.assertIsInstance(err, FFBBApiError)

    def test_001_meilisearch_error_from_response_index_not_found(self) -> None:
        body: dict[str, Any] = {
            "message": "Index `foobar` not found.",
            "code": "index_not_found",
            "type": "invalid_request",
            "link": "https://docs.meilisearch.com/errors#index_not_found",
        }
        err = MeilisearchError.from_response(body, status_code=404)
        self.assertIsInstance(err, MeilisearchIndexNotFoundError)
        self.assertEqual(err.error_code, "index_not_found")
        self.assertIn("foobar", err.message)

    def test_002_meilisearch_error_from_response_invalid_filter(self) -> None:
        body: dict[str, Any] = {
            "message": "Attribute `foo` is not filterable.",
            "code": "invalid_search_filter",
            "type": "invalid_request",
            "link": "https://docs.meilisearch.com/errors#invalid_search_filter",
        }
        err = MeilisearchError.from_response(body, status_code=400)
        self.assertIsInstance(err, MeilisearchInvalidFilterError)

    def test_003_meilisearch_error_from_response_generic(self) -> None:
        body: dict[str, Any] = {
            "message": "Something went wrong",
            "code": "internal",
            "type": "internal",
        }
        err = MeilisearchError.from_response(body)
        self.assertIsInstance(err, MeilisearchError)
        self.assertNotIsInstance(err, MeilisearchIndexNotFoundError)

    def test_004_meilisearch_hierarchy_isolation(self) -> None:
        """Meilisearch errors should NOT be instances of Directus errors."""
        err = MeilisearchIndexNotFoundError("test")
        self.assertNotIsInstance(err, DirectusError)

    def test_005_meilisearch_error_link(self) -> None:
        err = MeilisearchError(
            "test",
            error_link="https://docs.meilisearch.com/errors#test",
        )
        self.assertEqual(err.error_link, "https://docs.meilisearch.com/errors#test")


class Test213ExceptionCatchability(unittest.TestCase):
    """Tests that exception hierarchy supports proper try/except patterns."""

    def test_000_catch_directus_auth_as_ffbb_api_error(self) -> None:
        with self.assertRaises(FFBBApiError):
            raise DirectusAuthError("test")

    def test_001_catch_meilisearch_as_ffbb_api_error(self) -> None:
        with self.assertRaises(FFBBApiError):
            raise MeilisearchIndexNotFoundError("test")

    def test_002_catch_directus_auth_as_directus_error(self) -> None:
        with self.assertRaises(DirectusError):
            raise DirectusAuthError("test")

    def test_003_meilisearch_not_caught_by_directus(self) -> None:
        """Meilisearch errors should NOT be caught by DirectusError."""
        with self.assertRaises(MeilisearchError):
            try:
                raise MeilisearchIndexNotFoundError("test")
            except DirectusError:
                self.fail("Should not catch MeilisearchError as DirectusError")

    def test_004_directus_not_caught_by_meilisearch(self) -> None:
        """Directus errors should NOT be caught by MeilisearchError."""
        with self.assertRaises(DirectusError):
            try:
                raise DirectusAuthError("test")
            except MeilisearchError:
                self.fail("Should not catch DirectusError as MeilisearchError")

    def test_005_network_error_wraps_original(self) -> None:
        original = TimeoutError("timed out")
        err = FFBBNetworkError("failed", original_exception=original)
        self.assertIs(err.original_exception, original)


if __name__ == "__main__":
    unittest.main()
