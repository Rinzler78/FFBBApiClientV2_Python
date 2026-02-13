"""Tests for geo-search methods in MeilisearchFFBBClient."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from ffbb_api_client_v2.meilisearch.models.multi_search_results_class import (
    MultiSearchResults,
)
from ffbb_api_client_v2.meilisearch_ffbb.client import MeilisearchFFBBClient
from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_organismes import (
    OrganismesMultiSearchResult,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_salles import (
    SallesMultiSearchResult,
)


class Test217GeoSearchOrganismes(unittest.TestCase):
    """Tests for search_organismes_by_geo."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.meilisearch.client_extension.CacheManager"):
            self.client = MeilisearchFFBBClient(bearer_token="test-token")

    @patch.object(MeilisearchFFBBClient, "smart_multi_search")
    def test_000_geo_search_organismes_builds_correct_filter(
        self, mock_search: MagicMock
    ) -> None:
        mock_result = MagicMock(spec=OrganismesMultiSearchResult)
        results = MagicMock(spec=MultiSearchResults)
        results.results = [mock_result]
        mock_search.return_value = results

        self.client.search_organismes_by_geo(lat=48.8566, lng=2.3522, radius_km=10.0)

        mock_search.assert_called_once()
        queries = mock_search.call_args[0][0]
        self.assertEqual(len(queries), 1)
        query = queries[0]
        # Check filter contains _geoRadius
        self.assertIsNotNone(query.filter)
        self.assertEqual(len(query.filter), 1)
        self.assertIn("_geoRadius", query.filter[0])
        self.assertIn("48.8566", query.filter[0])
        self.assertIn("2.3522", query.filter[0])
        self.assertIn("10000", query.filter[0])

    @patch.object(MeilisearchFFBBClient, "smart_multi_search")
    def test_001_geo_search_organismes_default_sort(
        self, mock_search: MagicMock
    ) -> None:
        mock_result = MagicMock(spec=OrganismesMultiSearchResult)
        results = MagicMock(spec=MultiSearchResults)
        results.results = [mock_result]
        mock_search.return_value = results

        self.client.search_organismes_by_geo(lat=48.8566, lng=2.3522)

        query = mock_search.call_args[0][0][0]
        self.assertIsNotNone(query.sort)
        self.assertIn("_geoPoint", query.sort[0])
        self.assertIn("asc", query.sort[0])

    @patch.object(MeilisearchFFBBClient, "smart_multi_search")
    def test_002_geo_search_organismes_custom_sort(
        self, mock_search: MagicMock
    ) -> None:
        mock_result = MagicMock(spec=OrganismesMultiSearchResult)
        results = MagicMock(spec=MultiSearchResults)
        results.results = [mock_result]
        mock_search.return_value = results

        self.client.search_organismes_by_geo(lat=48.8566, lng=2.3522, sort=["nom:asc"])

        query = mock_search.call_args[0][0][0]
        self.assertEqual(query.sort, ["nom:asc"])

    @patch.object(MeilisearchFFBBClient, "smart_multi_search")
    def test_003_geo_search_organismes_with_query(self, mock_search: MagicMock) -> None:
        mock_result = MagicMock(spec=OrganismesMultiSearchResult)
        results = MagicMock(spec=MultiSearchResults)
        results.results = [mock_result]
        mock_search.return_value = results

        self.client.search_organismes_by_geo(lat=48.8566, lng=2.3522, q="basket")

        query = mock_search.call_args[0][0][0]
        self.assertEqual(query.q, "basket")

    @patch.object(MeilisearchFFBBClient, "smart_multi_search")
    def test_004_geo_search_organismes_returns_none_on_empty(
        self, mock_search: MagicMock
    ) -> None:
        mock_search.return_value = None
        result = self.client.search_organismes_by_geo(lat=48.8566, lng=2.3522)
        self.assertIsNone(result)

    @patch.object(MeilisearchFFBBClient, "smart_multi_search")
    def test_005_geo_search_radius_conversion(self, mock_search: MagicMock) -> None:
        """Verify km to meters conversion."""
        mock_result = MagicMock(spec=OrganismesMultiSearchResult)
        results = MagicMock(spec=MultiSearchResults)
        results.results = [mock_result]
        mock_search.return_value = results

        self.client.search_organismes_by_geo(lat=0, lng=0, radius_km=5.5)

        query = mock_search.call_args[0][0][0]
        self.assertIn("5500", query.filter[0])


class Test217GeoSearchSalles(unittest.TestCase):
    """Tests for search_salles_by_geo."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.meilisearch.client_extension.CacheManager"):
            self.client = MeilisearchFFBBClient(bearer_token="test-token")

    @patch.object(MeilisearchFFBBClient, "smart_multi_search")
    def test_000_geo_search_salles_builds_correct_filter(
        self, mock_search: MagicMock
    ) -> None:
        mock_result = MagicMock(spec=SallesMultiSearchResult)
        results = MagicMock(spec=MultiSearchResults)
        results.results = [mock_result]
        mock_search.return_value = results

        self.client.search_salles_by_geo(lat=43.2965, lng=5.3698, radius_km=15.0)

        mock_search.assert_called_once()
        query = mock_search.call_args[0][0][0]
        self.assertIn("_geoRadius", query.filter[0])
        self.assertIn("43.2965", query.filter[0])
        self.assertIn("15000", query.filter[0])

    @patch.object(MeilisearchFFBBClient, "smart_multi_search")
    def test_001_geo_search_salles_returns_none_on_empty(
        self, mock_search: MagicMock
    ) -> None:
        mock_search.return_value = None
        result = self.client.search_salles_by_geo(lat=43.2965, lng=5.3698)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
