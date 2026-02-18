"""Unit tests for DirectusClient base class.

Tests cover error handling paths that require mocks — scenarios impossible
to reproduce with the real API (JSON decode errors, non-dict/non-list
responses, Directus error enrichment).
"""

from __future__ import annotations

import json
import unittest
from unittest.mock import Mock, patch

from requests_cache import CachedSession

from ffbb_api_client_v2.directus.client import DirectusClient
from ffbb_api_client_v2.directus.exceptions import DirectusError
from ffbb_api_client_v2.exceptions import FFBBApiError


class TestDirectusClientGetJson(unittest.TestCase):
    """Tests for DirectusClient._get_json error handling."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.directus.client.CacheManager"):
            self.client = DirectusClient(
                bearer_token="test-token",
                url="https://example.com/",
                cached_session=Mock(spec=CachedSession),
            )

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_get_json_raises_ffbb_error_non_directus(self, mock_get: Mock) -> None:
        """FFBBApiError without Directus body is re-raised as-is."""
        mock_get.side_effect = FFBBApiError(
            "Server error", status_code=500, response_body=None
        )
        with self.assertRaises(FFBBApiError) as ctx:
            self.client._get_json("https://example.com/items")
        self.assertNotIsInstance(ctx.exception, DirectusError)

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_get_json_raises_directus_error(self, mock_get: Mock) -> None:
        """FFBBApiError with Directus error body is enriched to DirectusError."""
        directus_body = {
            "errors": [
                {
                    "message": "Forbidden",
                    "extensions": {"code": "FORBIDDEN"},
                }
            ]
        }
        mock_get.side_effect = FFBBApiError(
            "Forbidden", status_code=403, response_body=directus_body
        )
        with self.assertRaises(DirectusError):
            self.client._get_json("https://example.com/items")


class TestDirectusClientGetItem(unittest.TestCase):
    """Tests for DirectusClient._get_item error paths."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.directus.client.CacheManager"):
            self.client = DirectusClient(
                bearer_token="test-token",
                url="https://example.com/",
                cached_session=Mock(spec=CachedSession),
            )

    @patch.object(DirectusClient, "_get_json")
    def test_get_item_returns_none_on_non_dict(self, mock_json: Mock) -> None:
        """When response data is not a dict, returns None."""
        mock_json.return_value = "not a dict"
        result = self.client._get_item("items/42")
        self.assertIsNone(result)

    @patch.object(DirectusClient, "_get_json")
    def test_get_item_returns_none_on_catch(self, mock_json: Mock) -> None:
        """When _get_json raises a non-API exception, catch_result returns None."""
        mock_json.side_effect = json.decoder.JSONDecodeError("Expecting value", "", 0)
        result = self.client._get_item("items/42")
        self.assertIsNone(result)


class TestDirectusClientListItems(unittest.TestCase):
    """Tests for DirectusClient._list_items error paths."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.directus.client.CacheManager"):
            self.client = DirectusClient(
                bearer_token="test-token",
                url="https://example.com/",
                cached_session=Mock(spec=CachedSession),
            )

    @patch.object(DirectusClient, "_get_json")
    def test_list_items_returns_empty_on_non_list(self, mock_json: Mock) -> None:
        """When data is not a list, returns empty list."""
        mock_json.return_value = {"data": "not a list"}
        result = self.client._list_items("items")
        self.assertEqual(result, [])

    @patch.object(DirectusClient, "_get_json")
    def test_list_items_returns_empty_on_none(self, mock_json: Mock) -> None:
        """When catch_result returns None, returns empty list."""
        mock_json.side_effect = json.decoder.JSONDecodeError("Expecting value", "", 0)
        result = self.client._list_items("items")
        self.assertEqual(result, [])


class TestDirectusClientFetchAllPages(unittest.TestCase):
    """Tests for DirectusClient._fetch_all_pages error and limit paths."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.directus.client.CacheManager"):
            self.client = DirectusClient(
                bearer_token="test-token",
                url="https://example.com/",
                cached_session=Mock(spec=CachedSession),
            )

    @patch.object(DirectusClient, "_get_json")
    def test_fetch_all_pages_stops_on_empty_data(self, mock_json: Mock) -> None:
        """Stops when data is None or not a dict."""
        mock_json.side_effect = json.decoder.JSONDecodeError("Expecting value", "", 0)
        result = self.client._fetch_all_pages(
            "items",
            fields=["id"],
            from_list_fn=lambda items: items,
        )
        self.assertEqual(result, [])

    @patch.object(DirectusClient, "_get_json")
    def test_fetch_all_pages_stops_on_max_items(self, mock_json: Mock) -> None:
        """Stops when max_items limit is reached."""
        page = [{"id": i} for i in range(10)]
        mock_json.return_value = {
            "data": page,
            "meta": {"total_count": 1000, "filter_count": 1000},
        }
        result = self.client._fetch_all_pages(
            "items",
            fields=["id"],
            from_list_fn=lambda items: items,
            page_size=10,
            max_items=10,
        )
        self.assertEqual(len(result), 10)


class TestDirectusClientGetCollections(unittest.TestCase):
    """Tests for DirectusClient.get_collections error paths."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.directus.client.CacheManager"):
            self.client = DirectusClient(
                bearer_token="test-token",
                url="https://example.com/",
                cached_session=Mock(spec=CachedSession),
            )

    @patch.object(DirectusClient, "_get_json")
    def test_get_collections_returns_empty_on_error(self, mock_json: Mock) -> None:
        """Returns empty list when catch_result returns None."""
        mock_json.side_effect = json.decoder.JSONDecodeError("Expecting value", "", 0)
        result = self.client.get_collections()
        self.assertEqual(result, [])

    @patch.object(DirectusClient, "_get_json")
    def test_get_collections_returns_empty_on_non_list(self, mock_json: Mock) -> None:
        mock_json.return_value = {"data": "not a list"}
        result = self.client.get_collections()
        self.assertEqual(result, [])


class TestDirectusClientGetFields(unittest.TestCase):
    """Tests for DirectusClient.get_fields error paths."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.directus.client.CacheManager"):
            self.client = DirectusClient(
                bearer_token="test-token",
                url="https://example.com/",
                cached_session=Mock(spec=CachedSession),
            )

    @patch.object(DirectusClient, "_get_json")
    def test_get_fields_returns_empty(self, mock_json: Mock) -> None:
        mock_json.side_effect = json.decoder.JSONDecodeError("Expecting value", "", 0)
        result = self.client.get_fields()
        self.assertEqual(result, [])

    @patch.object(DirectusClient, "_get_json")
    def test_get_fields_returns_empty_on_non_list(self, mock_json: Mock) -> None:
        mock_json.return_value = {"data": "not a list"}
        result = self.client.get_fields()
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
