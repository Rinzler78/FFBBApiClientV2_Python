"""Tests for MeilisearchClient settings methods (get_index_settings, etc.)."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from ffbb_api_client_v2.clients.meilisearch_client import MeilisearchClient
from ffbb_api_client_v2.models.meilisearch_index_settings import (
    MeilisearchIndexSettings,
)
from ffbb_api_client_v2.models.multi_search_results_class import MultiSearchResults


class Test207MeilisearchSettings(unittest.TestCase):
    """Tests for MeilisearchClient get_index_settings and related methods."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.clients.meilisearch_client.CacheManager"):
            self.client = MeilisearchClient(bearer_token="test-token")

    def test_001_get_json_success(self) -> None:
        """Test _get_json makes authenticated GET request."""
        expected = {"filterableAttributes": ["type"]}
        with patch(
            "ffbb_api_client_v2.clients.meilisearch_client.http_get_json",
            return_value=expected,
        ):
            result = self.client._get_json("indexes/test/settings")
            self.assertEqual(result, expected)

    def test_002_get_json_failure_json_decode(self) -> None:
        """Test _get_json returns None on JSONDecodeError."""
        import json

        with patch(
            "ffbb_api_client_v2.clients.meilisearch_client.http_get_json",
            side_effect=json.JSONDecodeError("Expecting value", "", 0),
        ):
            result = self.client._get_json("indexes/test/settings")
            self.assertIsNone(result)

    def test_002b_get_json_returns_error_response(self) -> None:
        """Test _get_json returns error dict for 403 responses."""
        error_response = {
            "message": "The provided API key is invalid.",
            "code": "invalid_api_key",
            "type": "auth",
        }
        with patch(
            "ffbb_api_client_v2.clients.meilisearch_client.http_get_json",
            return_value=error_response,
        ):
            result = self.client._get_json("indexes/test/settings")
            self.assertIsNotNone(result)
            assert result is not None
            self.assertIn("code", result)

    def test_002c_get_index_settings_error_response_triggers_fallback(self) -> None:
        """Test get_index_settings falls back when API returns error with 'code' key."""
        error_response = {
            "message": "The provided API key is invalid.",
            "code": "invalid_api_key",
            "type": "auth",
        }
        with (
            patch.object(self.client, "_get_json", return_value=error_response),
            patch.object(
                self.client, "_discover_filterable_via_facets", return_value=["type"]
            ),
        ):
            settings = self.client.get_index_settings("ffbbserver_salles")
            self.assertIsNotNone(settings)
            assert settings is not None
            self.assertEqual(settings.filterable_attributes, ["type"])

    def test_003_get_index_settings_success(self) -> None:
        """Test get_index_settings returns settings from API."""
        api_response = {
            "filterableAttributes": ["type", "commune.codePostal"],
            "sortableAttributes": ["nom"],
            "searchableAttributes": ["nom"],
            "displayedAttributes": ["*"],
            "rankingRules": ["words", "typo"],
            "stopWords": [],
            "synonyms": {},
            "distinctAttribute": None,
            "pagination": {},
            "faceting": {},
        }
        with patch.object(self.client, "_get_json", return_value=api_response):
            settings = self.client.get_index_settings("ffbbserver_salles")
            self.assertIsNotNone(settings)
            assert settings is not None
            self.assertIsInstance(settings, MeilisearchIndexSettings)
            self.assertEqual(
                settings.filterable_attributes, ["type", "commune.codePostal"]
            )
            self.assertEqual(settings.sortable_attributes, ["nom"])

    def test_004_get_index_settings_fallback_to_facets(self) -> None:
        """Test get_index_settings falls back to facet discovery."""
        mock_result = MagicMock()
        mock_result.facet_distribution = {
            "type": {"salle": 100},
            "commune.codePostal": {"75000": 5},
        }

        mock_results = MagicMock(spec=MultiSearchResults)
        mock_results.results = [mock_result]

        with (
            patch.object(self.client, "_get_json", return_value=None),
            patch.object(self.client, "multi_search", return_value=mock_results),
        ):
            settings = self.client.get_index_settings("ffbbserver_salles")
            self.assertIsNotNone(settings)
            assert settings is not None
            self.assertIn("commune.codePostal", settings.filterable_attributes)
            self.assertIn("type", settings.filterable_attributes)

    def test_005_get_index_settings_both_fail(self) -> None:
        """Test get_index_settings returns None when both methods fail."""
        with (
            patch.object(self.client, "_get_json", return_value=None),
            patch.object(self.client, "multi_search", return_value=None),
        ):
            settings = self.client.get_index_settings("ffbbserver_salles")
            self.assertIsNone(settings)

    def test_006_get_filterable_attributes(self) -> None:
        """Test get_filterable_attributes returns list."""
        mock_settings = MeilisearchIndexSettings(filterable_attributes=["type", "_geo"])
        with patch.object(
            self.client, "get_index_settings", return_value=mock_settings
        ):
            result = self.client.get_filterable_attributes("ffbbserver_salles")
            self.assertEqual(result, ["type", "_geo"])

    def test_007_get_filterable_attributes_none(self) -> None:
        """Test get_filterable_attributes returns None when settings unavailable."""
        with patch.object(self.client, "get_index_settings", return_value=None):
            result = self.client.get_filterable_attributes("ffbbserver_salles")
            self.assertIsNone(result)

    def test_008_get_sortable_attributes(self) -> None:
        """Test get_sortable_attributes returns list."""
        mock_settings = MeilisearchIndexSettings(sortable_attributes=["nom", "code"])
        with patch.object(
            self.client, "get_index_settings", return_value=mock_settings
        ):
            result = self.client.get_sortable_attributes("ffbbserver_salles")
            self.assertEqual(result, ["nom", "code"])

    def test_009_get_sortable_attributes_none(self) -> None:
        """Test get_sortable_attributes returns None when settings unavailable."""
        with patch.object(self.client, "get_index_settings", return_value=None):
            result = self.client.get_sortable_attributes("ffbbserver_salles")
            self.assertIsNone(result)

    def test_010_discover_filterable_via_facets_empty_results(self) -> None:
        """Test _discover_filterable_via_facets with empty results."""
        mock_results = MagicMock(spec=MultiSearchResults)
        mock_results.results = []
        with patch.object(self.client, "multi_search", return_value=mock_results):
            result = self.client._discover_filterable_via_facets("test_index")
            self.assertIsNone(result)

    def test_011_discover_filterable_via_facets_no_distribution(self) -> None:
        """Test _discover_filterable_via_facets when no facet_distribution."""
        mock_result = MagicMock()
        mock_result.facet_distribution = None
        mock_results = MagicMock(spec=MultiSearchResults)
        mock_results.results = [mock_result]
        with patch.object(self.client, "multi_search", return_value=mock_results):
            result = self.client._discover_filterable_via_facets("test_index")
            self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
