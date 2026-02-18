"""Unit tests for MeilisearchClient base methods.

Tests cover init validation, list_indexes, and search_index methods.
"""

from __future__ import annotations

import unittest
from unittest.mock import Mock, patch

from requests_cache import CachedSession

from ffbb_api_client_v2.meilisearch.client import MeilisearchClient


class TestMeilisearchClientInit(unittest.TestCase):
    """Tests for MeilisearchClient.__init__ token validation."""

    def test_init_empty_token_raises(self) -> None:
        with self.assertRaises(ValueError):
            MeilisearchClient(bearer_token="")

    def test_init_whitespace_token_raises(self) -> None:
        with self.assertRaises(ValueError):
            MeilisearchClient(bearer_token="   ")


class TestMeilisearchClientListIndexes(unittest.TestCase):
    """Tests for MeilisearchClient.list_indexes."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.meilisearch.client.CacheManager"):
            self.client = MeilisearchClient(
                bearer_token="test-token",
                cached_session=Mock(spec=CachedSession),
            )

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_list_indexes_success(self, mock_get: Mock) -> None:
        mock_get.return_value = {
            "results": [{"uid": "movies", "primaryKey": "id"}],
            "offset": 0,
            "limit": 20,
            "total": 1,
        }
        result = self.client.list_indexes()
        self.assertIsNotNone(result)
        self.assertEqual(result["total"], 1)

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_list_indexes_with_params(self, mock_get: Mock) -> None:
        mock_get.return_value = {
            "results": [],
            "offset": 5,
            "limit": 10,
            "total": 0,
        }
        result = self.client.list_indexes(offset=5, limit=10)
        self.assertIsNotNone(result)
        call_url = mock_get.call_args[0][0]
        self.assertIn("offset=5", call_url)
        self.assertIn("limit=10", call_url)


class TestMeilisearchClientSearchIndex(unittest.TestCase):
    """Tests for MeilisearchClient.search_index."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.meilisearch.client.CacheManager"):
            self.client = MeilisearchClient(
                bearer_token="test-token",
                cached_session=Mock(spec=CachedSession),
            )

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_post_json")
    def test_search_index_basic(self, mock_post: Mock) -> None:
        mock_post.return_value = {
            "hits": [{"id": 1, "title": "Test"}],
            "estimatedTotalHits": 1,
        }
        result = self.client.search_index("movies", query="Test")
        self.assertIsNotNone(result)
        self.assertEqual(len(result["hits"]), 1)
        body = mock_post.call_args[0][2]
        self.assertEqual(body["q"], "Test")
        self.assertNotIn("filter", body)
        self.assertNotIn("facets", body)
        self.assertNotIn("sort", body)
        self.assertNotIn("attributesToRetrieve", body)

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_post_json")
    def test_search_index_with_filter(self, mock_post: Mock) -> None:
        mock_post.return_value = {"hits": [], "estimatedTotalHits": 0}
        self.client.search_index("movies", filter="genre = action")
        body = mock_post.call_args[0][2]
        self.assertEqual(body["filter"], "genre = action")

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_post_json")
    def test_search_index_with_facets(self, mock_post: Mock) -> None:
        mock_post.return_value = {"hits": [], "facetDistribution": {"genre": {}}}
        self.client.search_index("movies", facets=["genre"])
        body = mock_post.call_args[0][2]
        self.assertEqual(body["facets"], ["genre"])

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_post_json")
    def test_search_index_with_sort(self, mock_post: Mock) -> None:
        mock_post.return_value = {"hits": []}
        self.client.search_index("movies", sort=["price:asc"])
        body = mock_post.call_args[0][2]
        self.assertEqual(body["sort"], ["price:asc"])

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_post_json")
    def test_search_index_with_attributes_to_retrieve(self, mock_post: Mock) -> None:
        mock_post.return_value = {"hits": []}
        self.client.search_index("movies", attributes_to_retrieve=["title", "id"])
        body = mock_post.call_args[0][2]
        self.assertEqual(body["attributesToRetrieve"], ["title", "id"])

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_post_json")
    def test_search_index_all_options(self, mock_post: Mock) -> None:
        mock_post.return_value = {"hits": [{"id": 1}]}
        result = self.client.search_index(
            "movies",
            query="action",
            offset=10,
            limit=5,
            filter="year > 2020",
            facets=["genre", "year"],
            sort=["year:desc"],
            attributes_to_retrieve=["id", "title", "year"],
        )
        self.assertIsNotNone(result)
        body = mock_post.call_args[0][2]
        self.assertEqual(body["q"], "action")
        self.assertEqual(body["offset"], 10)
        self.assertEqual(body["limit"], 5)
        self.assertEqual(body["filter"], "year > 2020")
        self.assertEqual(body["facets"], ["genre", "year"])
        self.assertEqual(body["sort"], ["year:desc"])
        self.assertEqual(body["attributesToRetrieve"], ["id", "title", "year"])

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_post_json")
    def test_search_index_returns_none_on_empty(self, mock_post: Mock) -> None:
        """Returns None when server returns empty body."""
        import json

        mock_post.side_effect = json.decoder.JSONDecodeError("Expecting value", "", 0)
        result = self.client.search_index("movies")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
