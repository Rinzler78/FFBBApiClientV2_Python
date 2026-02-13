"""Tests for HTTP response error handling in http_requests_utils."""

from __future__ import annotations

import json
import unittest
from unittest.mock import MagicMock

from ffbb_api_client_v2.directus_exceptions import DirectusAuthError, DirectusError
from ffbb_api_client_v2.exceptions import (
    FFBBAuthError,
    FFBBNetworkError,
    FFBBNotFoundError,
    FFBBRateLimitError,
    FFBBServerError,
    FFBBValidationError,
)
from ffbb_api_client_v2.helpers.http_requests_helper import catch_result
from ffbb_api_client_v2.helpers.http_requests_utils import _check_response_errors
from ffbb_api_client_v2.meilisearch_exceptions import (
    MeilisearchError,
    MeilisearchIndexNotFoundError,
)


class Test218CheckResponseErrors(unittest.TestCase):
    """Tests for _check_response_errors function."""

    def _make_response(self, status_code: int, body: dict | None = None) -> MagicMock:
        response = MagicMock()
        response.status_code = status_code
        response.headers = {}
        if body is not None:
            response.json.return_value = body
        else:
            response.json.side_effect = json.JSONDecodeError("", "", 0)
        return response

    def test_000_2xx_no_error(self) -> None:
        response = self._make_response(200)
        # Should not raise
        _check_response_errors(response)

    def test_001_directus_401_raises_directus_auth_error(self) -> None:
        body = {
            "errors": [
                {"message": "Unauthorized", "extensions": {"code": "UNAUTHORIZED"}}
            ]
        }
        response = self._make_response(401, body)
        with self.assertRaises(DirectusAuthError) as ctx:
            _check_response_errors(response)
        self.assertEqual(ctx.exception.status_code, 401)

    def test_002_directus_403_raises_directus_auth_error(self) -> None:
        body = {"errors": [{"message": "Forbidden"}]}
        response = self._make_response(403, body)
        with self.assertRaises(DirectusAuthError):
            _check_response_errors(response)

    def test_003_directus_404_raises_directus_not_found(self) -> None:
        body = {"errors": [{"message": "Item not found"}]}
        response = self._make_response(404, body)
        with self.assertRaises(DirectusError):
            _check_response_errors(response)

    def test_004_directus_500_raises_directus_server_error(self) -> None:
        body = {"errors": [{"message": "Internal error"}]}
        response = self._make_response(500, body)
        with self.assertRaises(DirectusError):
            _check_response_errors(response)

    def test_005_meilisearch_error_format(self) -> None:
        body = {
            "message": "Index not found",
            "code": "index_not_found",
            "type": "invalid_request",
            "link": "https://docs.meilisearch.com/errors#index_not_found",
        }
        response = self._make_response(404, body)
        with self.assertRaises(MeilisearchIndexNotFoundError):
            _check_response_errors(response)

    def test_006_meilisearch_invalid_filter(self) -> None:
        body = {
            "message": "Attribute `foo` is not filterable",
            "code": "invalid_search_filter",
            "type": "invalid_request",
            "link": "https://docs.meilisearch.com/errors#invalid_search_filter",
        }
        response = self._make_response(400, body)
        with self.assertRaises(MeilisearchError):
            _check_response_errors(response)

    def test_007_generic_401_without_body(self) -> None:
        response = self._make_response(401, body=None)
        with self.assertRaises(FFBBAuthError):
            _check_response_errors(response)

    def test_008_generic_404_without_body(self) -> None:
        response = self._make_response(404, body=None)
        with self.assertRaises(FFBBNotFoundError):
            _check_response_errors(response)

    def test_009_generic_429_without_body(self) -> None:
        response = self._make_response(429, body=None)
        with self.assertRaises(FFBBRateLimitError):
            _check_response_errors(response)

    def test_010_429_with_retry_after_header(self) -> None:
        response = self._make_response(429, body=None)
        response.headers = {"Retry-After": "30"}
        with self.assertRaises(FFBBRateLimitError) as ctx:
            _check_response_errors(response)
        self.assertEqual(ctx.exception.retry_after, 30.0)

    def test_011_generic_500(self) -> None:
        response = self._make_response(500, body=None)
        with self.assertRaises(FFBBServerError):
            _check_response_errors(response)

    def test_012_generic_502(self) -> None:
        response = self._make_response(502, body=None)
        with self.assertRaises(FFBBServerError):
            _check_response_errors(response)

    def test_013_generic_400_raises_validation_error(self) -> None:
        response = self._make_response(400, body={"message": "Bad request"})
        with self.assertRaises(FFBBValidationError):
            _check_response_errors(response)

    def test_014_204_no_error(self) -> None:
        response = self._make_response(204)
        _check_response_errors(response)


class Test218CatchResultWithExceptions(unittest.TestCase):
    """Tests for catch_result with the new exception handling."""

    def test_000_catch_result_propagates_ffbb_api_error(self) -> None:
        """FFBBApiError should propagate through catch_result."""

        def raise_api_error():
            raise FFBBAuthError("test")

        with self.assertRaises(FFBBAuthError):
            catch_result(raise_api_error)

    def test_001_catch_result_propagates_directus_error(self) -> None:
        def raise_directus_error():
            raise DirectusAuthError("test")

        with self.assertRaises(DirectusAuthError):
            catch_result(raise_directus_error)

    def test_002_catch_result_propagates_meilisearch_error(self) -> None:
        def raise_meili_error():
            raise MeilisearchIndexNotFoundError("test")

        with self.assertRaises(MeilisearchIndexNotFoundError):
            catch_result(raise_meili_error)

    def test_003_catch_result_returns_none_on_empty_json(self) -> None:
        def raise_empty_json():
            raise json.JSONDecodeError("Expecting value", "", 0)

        result = catch_result(raise_empty_json)
        self.assertIsNone(result)

    def test_004_catch_result_wraps_network_error(self) -> None:
        """ConnectionError should be wrapped in FFBBNetworkError after retry."""
        call_count = 0

        def raise_connection_error():
            nonlocal call_count
            call_count += 1
            raise ConnectionError("refused")

        with self.assertRaises(FFBBNetworkError) as ctx:
            catch_result(raise_connection_error)

        self.assertIsInstance(ctx.exception.original_exception, ConnectionError)
        # Should have tried twice (original + retry)
        self.assertEqual(call_count, 2)

    def test_005_catch_result_returns_value_on_success(self) -> None:
        result = catch_result(lambda: {"data": [1, 2, 3]})
        self.assertEqual(result, {"data": [1, 2, 3]})


if __name__ == "__main__":
    unittest.main()
