"""Unit tests for DirectusClient base class.

Tests cover error handling, single-item retrieval, list retrieval,
pagination, and schema discovery methods.
"""

from __future__ import annotations

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

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_get_json_success(self, mock_get: Mock) -> None:
        """Successful GET returns dict."""
        mock_get.return_value = {"data": {"id": 1}}
        result = self.client._get_json("https://example.com/items/1")
        self.assertEqual(result, {"data": {"id": 1}})


class TestDirectusClientGetItem(unittest.TestCase):
    """Tests for DirectusClient._get_item."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.directus.client.CacheManager"):
            self.client = DirectusClient(
                bearer_token="test-token",
                url="https://example.com/",
                cached_session=Mock(spec=CachedSession),
            )

    @patch.object(DirectusClient, "_get_json")
    def test_get_item_success(self, mock_json: Mock) -> None:
        mock_json.return_value = {"data": {"id": 42, "name": "test"}}
        result = self.client._get_item("items/42")
        self.assertEqual(result, {"id": 42, "name": "test"})

    @patch.object(DirectusClient, "_get_json")
    def test_get_item_returns_none_on_non_dict(self, mock_json: Mock) -> None:
        """When response data is not a dict, returns None."""
        mock_json.return_value = "not a dict"
        result = self.client._get_item("items/42")
        self.assertIsNone(result)

    @patch.object(DirectusClient, "_get_json")
    def test_get_item_with_fields_and_params(self, mock_json: Mock) -> None:
        mock_json.return_value = {"data": {"id": 1}}
        result = self.client._get_item(
            "items/1",
            fields=["id", "name"],
            params={"deep[translations][_limit]": "-1"},
        )
        self.assertEqual(result, {"id": 1})
        call_url = mock_json.call_args[0][0]
        self.assertIn("fields%5B%5D=id", call_url)
        self.assertIn("fields%5B%5D=name", call_url)

    @patch.object(DirectusClient, "_get_json")
    def test_get_item_returns_none_on_catch(self, mock_json: Mock) -> None:
        """When _get_json raises a non-API exception, catch_result returns None."""
        import json

        mock_json.side_effect = json.decoder.JSONDecodeError("Expecting value", "", 0)
        result = self.client._get_item("items/42")
        self.assertIsNone(result)


class TestDirectusClientListItems(unittest.TestCase):
    """Tests for DirectusClient._list_items."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.directus.client.CacheManager"):
            self.client = DirectusClient(
                bearer_token="test-token",
                url="https://example.com/",
                cached_session=Mock(spec=CachedSession),
            )

    @patch.object(DirectusClient, "_get_json")
    def test_list_items_success(self, mock_json: Mock) -> None:
        mock_json.return_value = {"data": [{"id": 1}, {"id": 2}]}
        result = self.client._list_items("items")
        self.assertEqual(result, [{"id": 1}, {"id": 2}])

    @patch.object(DirectusClient, "_get_json")
    def test_list_items_returns_empty_on_non_list(self, mock_json: Mock) -> None:
        """When data is not a list, returns empty list."""
        mock_json.return_value = {"data": "not a list"}
        result = self.client._list_items("items")
        self.assertEqual(result, [])

    @patch.object(DirectusClient, "_get_json")
    def test_list_items_with_offset_and_fields(self, mock_json: Mock) -> None:
        mock_json.return_value = {"data": [{"id": 3}]}
        result = self.client._list_items(
            "items", fields=["id", "name"], limit=5, offset=10
        )
        self.assertEqual(result, [{"id": 3}])
        call_url = mock_json.call_args[0][0]
        self.assertIn("limit=5", call_url)
        self.assertIn("offset=10", call_url)
        self.assertIn("fields%5B%5D=id", call_url)

    @patch.object(DirectusClient, "_get_json")
    def test_list_items_returns_empty_on_none(self, mock_json: Mock) -> None:
        """When catch_result returns None, returns empty list."""
        import json

        mock_json.side_effect = json.decoder.JSONDecodeError("Expecting value", "", 0)
        result = self.client._list_items("items")
        self.assertEqual(result, [])


class TestDirectusClientFetchAllPages(unittest.TestCase):
    """Tests for DirectusClient._fetch_all_pages."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.directus.client.CacheManager"):
            self.client = DirectusClient(
                bearer_token="test-token",
                url="https://example.com/",
                cached_session=Mock(spec=CachedSession),
            )

    @patch.object(DirectusClient, "_get_json")
    def test_fetch_all_pages_stops_on_short_page(self, mock_json: Mock) -> None:
        """Stops when page has fewer items than page_size."""
        mock_json.return_value = {
            "data": [{"id": 1}, {"id": 2}],
            "meta": {"total_count": 100, "filter_count": 100},
        }
        result = self.client._fetch_all_pages(
            "items",
            fields=["id"],
            from_list_fn=lambda items: items,
            page_size=10,
        )
        self.assertEqual(len(result), 2)
        mock_json.assert_called_once()

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

    @patch.object(DirectusClient, "_get_json")
    def test_fetch_all_pages_with_filter_sort_search(self, mock_json: Mock) -> None:
        """Verifies filter, sort, and search params are passed."""
        mock_json.return_value = {
            "data": [{"id": 1}],
            "meta": {"total_count": 1},
        }
        result = self.client._fetch_all_pages(
            "items",
            fields=["id"],
            from_list_fn=lambda items: items,
            filter_criteria='{"status": {"_eq": "active"}}',
            sort=["name"],
            search="test",
        )
        self.assertEqual(len(result), 1)
        call_url = mock_json.call_args[0][0]
        self.assertIn("filter=", call_url)
        self.assertIn("sort%5B%5D=name", call_url)
        self.assertIn("search=test", call_url)

    @patch.object(DirectusClient, "_get_json")
    def test_fetch_all_pages_multiple_pages(self, mock_json: Mock) -> None:
        """Fetches multiple pages until total is reached."""
        page1 = [{"id": i} for i in range(5)]
        page2 = [{"id": i} for i in range(5, 8)]
        mock_json.side_effect = [
            {"data": page1, "meta": {"total_count": 8, "filter_count": 8}},
            {"data": page2, "meta": {"total_count": 8, "filter_count": 8}},
        ]
        result = self.client._fetch_all_pages(
            "items",
            fields=["id"],
            from_list_fn=lambda items: items,
            page_size=5,
        )
        self.assertEqual(len(result), 8)
        self.assertEqual(mock_json.call_count, 2)

    @patch.object(DirectusClient, "_get_json")
    def test_fetch_all_pages_stops_on_empty_data(self, mock_json: Mock) -> None:
        """Stops when data is None or not a dict."""
        import json

        mock_json.side_effect = json.decoder.JSONDecodeError("Expecting value", "", 0)
        result = self.client._fetch_all_pages(
            "items",
            fields=["id"],
            from_list_fn=lambda items: items,
        )
        self.assertEqual(result, [])


class TestDirectusClientGetCollections(unittest.TestCase):
    """Tests for DirectusClient.get_collections."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.directus.client.CacheManager"):
            self.client = DirectusClient(
                bearer_token="test-token",
                url="https://example.com/",
                cached_session=Mock(spec=CachedSession),
            )

    @patch.object(DirectusClient, "_get_json")
    def test_get_collections_success(self, mock_json: Mock) -> None:
        mock_json.return_value = {
            "data": [
                {"collection": "articles", "schema": {}},
                {"collection": "users", "schema": {}},
            ]
        }
        result = self.client.get_collections()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["collection"], "articles")

    @patch.object(DirectusClient, "_get_json")
    def test_get_collections_returns_empty_on_error(self, mock_json: Mock) -> None:
        """Returns empty list when catch_result returns None."""
        import json

        mock_json.side_effect = json.decoder.JSONDecodeError("Expecting value", "", 0)
        result = self.client.get_collections()
        self.assertEqual(result, [])

    @patch.object(DirectusClient, "_get_json")
    def test_get_collections_returns_empty_on_non_list(self, mock_json: Mock) -> None:
        mock_json.return_value = {"data": "not a list"}
        result = self.client.get_collections()
        self.assertEqual(result, [])


class TestDirectusClientGetFields(unittest.TestCase):
    """Tests for DirectusClient.get_fields and get_collection_fields."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.directus.client.CacheManager"):
            self.client = DirectusClient(
                bearer_token="test-token",
                url="https://example.com/",
                cached_session=Mock(spec=CachedSession),
            )

    @patch.object(DirectusClient, "_get_json")
    def test_get_fields_all(self, mock_json: Mock) -> None:
        mock_json.return_value = {"data": [{"field": "id", "type": "integer"}]}
        result = self.client.get_fields()
        self.assertEqual(len(result), 1)
        call_url = mock_json.call_args[0][0]
        self.assertTrue(call_url.endswith("fields"))

    @patch.object(DirectusClient, "_get_json")
    def test_get_fields_for_collection(self, mock_json: Mock) -> None:
        mock_json.return_value = {"data": [{"field": "name", "type": "string"}]}
        result = self.client.get_fields(collection="articles")
        self.assertEqual(len(result), 1)
        call_url = mock_json.call_args[0][0]
        self.assertIn("fields/articles", call_url)

    @patch.object(DirectusClient, "_get_json")
    def test_get_fields_returns_empty(self, mock_json: Mock) -> None:
        import json

        mock_json.side_effect = json.decoder.JSONDecodeError("Expecting value", "", 0)
        result = self.client.get_fields()
        self.assertEqual(result, [])

    @patch.object(DirectusClient, "_get_json")
    def test_get_fields_returns_empty_on_non_list(self, mock_json: Mock) -> None:
        mock_json.return_value = {"data": "not a list"}
        result = self.client.get_fields()
        self.assertEqual(result, [])

    @patch.object(DirectusClient, "_get_json")
    def test_get_collection_fields_delegates(self, mock_json: Mock) -> None:
        mock_json.return_value = {"data": [{"field": "id", "type": "integer"}]}
        result = self.client.get_collection_fields("users")
        self.assertEqual(len(result), 1)
        call_url = mock_json.call_args[0][0]
        self.assertIn("fields/users", call_url)


if __name__ == "__main__":
    unittest.main()
