"""Tests for MeilisearchFFBBClient with filter/sort/limit parameters."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from ffbb_api_client_v2.clients.meilisearch_ffbb_client import MeilisearchFFBBClient
from ffbb_api_client_v2.models.competitions_multi_search_query import (
    CompetitionsMultiSearchQuery,
)
from ffbb_api_client_v2.models.meilisearch_index_settings import (
    MeilisearchIndexSettings,
)
from ffbb_api_client_v2.models.multi_search_result_competitions import (
    CompetitionsMultiSearchResult,
)
from ffbb_api_client_v2.models.multi_search_result_organismes import (
    OrganismesMultiSearchResult,
)
from ffbb_api_client_v2.models.multi_search_result_pratiques import (
    PratiquesMultiSearchResult,
)
from ffbb_api_client_v2.models.multi_search_result_rencontres import (
    RencontresMultiSearchResult,
)
from ffbb_api_client_v2.models.multi_search_result_salles import (
    SallesMultiSearchResult,
)
from ffbb_api_client_v2.models.multi_search_result_terrains import (
    TerrainsMultiSearchResult,
)
from ffbb_api_client_v2.models.multi_search_result_tournois import (
    TournoisMultiSearchResult,
)
from ffbb_api_client_v2.models.multi_search_results_class import MultiSearchResults


class Test208MeilisearchEnhancedSearch(unittest.TestCase):
    """Tests for filter/sort/limit in MeilisearchFFBBClient search methods."""

    def setUp(self) -> None:
        with patch(
            "ffbb_api_client_v2.helpers.meilisearch_client_extension.CacheManager"
        ):
            self.client = MeilisearchFFBBClient(bearer_token="test-token")

    def _make_mock_results(self, result_mock: MagicMock) -> MultiSearchResults:
        results = MagicMock(spec=MultiSearchResults)
        results.results = [result_mock]
        return results

    # --- Competitions with filter/sort ---

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_000_search_competitions_with_filter(self, mock_search: MagicMock) -> None:
        """Test search_competitions passes filter to query."""
        mock_result = MagicMock(spec=CompetitionsMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_competitions(
            name="Nationale",
            filter=['sexe = "M"'],
        )

        mock_search.assert_called_once()
        queries = mock_search.call_args[0][0]
        self.assertEqual(len(queries), 1)
        query = queries[0]
        self.assertIsInstance(query, CompetitionsMultiSearchQuery)
        self.assertEqual(query.filter, ['sexe = "M"'])

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_001_search_competitions_with_sort(self, mock_search: MagicMock) -> None:
        """Test search_competitions passes sort to query."""
        mock_result = MagicMock(spec=CompetitionsMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_competitions(
            name="Nationale",
            sort=["nom:asc"],
        )

        queries = mock_search.call_args[0][0]
        self.assertEqual(queries[0].sort, ["nom:asc"])

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_002_search_competitions_with_limit(self, mock_search: MagicMock) -> None:
        """Test search_competitions passes limit to query."""
        mock_result = MagicMock(spec=CompetitionsMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_competitions(name="Nationale", limit=50)

        queries = mock_search.call_args[0][0]
        self.assertEqual(queries[0].limit, 50)

    # --- Organismes with filter/sort ---

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_003_search_organismes_with_filter(self, mock_search: MagicMock) -> None:
        """Test search_organismes passes filter to query."""
        mock_result = MagicMock(spec=OrganismesMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_organismes(
            name="Paris",
            filter=['type = "CLUB"'],
        )

        queries = mock_search.call_args[0][0]
        self.assertEqual(queries[0].filter, ['type = "CLUB"'])

    # --- Rencontres with filter ---

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_004_search_rencontres_with_filter(self, mock_search: MagicMock) -> None:
        """Test search_rencontres passes filter."""
        mock_result = MagicMock(spec=RencontresMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_rencontres(
            name=None,
            filter=["joue = true"],
        )

        queries = mock_search.call_args[0][0]
        self.assertEqual(queries[0].filter, ["joue = true"])

    # --- Salles with filter ---

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_005_search_salles_with_filter(self, mock_search: MagicMock) -> None:
        """Test search_salles passes filter."""
        mock_result = MagicMock(spec=SallesMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_salles(
            name=None,
            filter=['type = "salle"'],
        )

        queries = mock_search.call_args[0][0]
        self.assertEqual(queries[0].filter, ['type = "salle"'])

    # --- Terrains with filter ---

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_006_search_terrains_with_filter(self, mock_search: MagicMock) -> None:
        """Test search_terrains passes filter."""
        mock_result = MagicMock(spec=TerrainsMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_terrains(
            name=None,
            filter=["accesLibre = true"],
        )

        queries = mock_search.call_args[0][0]
        self.assertEqual(queries[0].filter, ["accesLibre = true"])

    # --- Tournois with filter ---

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_007_search_tournois_with_filter(self, mock_search: MagicMock) -> None:
        """Test search_tournois passes filter."""
        mock_result = MagicMock(spec=TournoisMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_tournois(
            name=None,
            filter=['sexe = "M"'],
        )

        queries = mock_search.call_args[0][0]
        self.assertEqual(queries[0].filter, ['sexe = "M"'])

    # --- Pratiques with filter ---

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_008_search_pratiques_with_filter(self, mock_search: MagicMock) -> None:
        """Test search_pratiques passes filter."""
        mock_result = MagicMock(spec=PratiquesMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_pratiques(
            name=None,
            filter=['type = "basketball"'],
        )

        queries = mock_search.call_args[0][0]
        self.assertEqual(queries[0].filter, ['type = "basketball"'])

    # --- search_multiple_* with filter/sort ---

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_009_search_multiple_competitions_with_filter(
        self, mock_search: MagicMock
    ) -> None:
        """Test search_multiple_competitions creates queries with filter."""
        mock_result = MagicMock(spec=CompetitionsMultiSearchResult)
        mock_results = MagicMock(spec=MultiSearchResults)
        mock_results.results = [mock_result, mock_result]
        mock_search.return_value = mock_results

        self.client.search_multiple_competitions(
            names=["NM1", "NM2"],
            filter=['sexe = "M"'],
            sort=["nom:asc"],
            limit=20,
        )

        queries = mock_search.call_args[0][0]
        self.assertEqual(len(queries), 2)
        for q in queries:
            self.assertEqual(q.filter, ['sexe = "M"'])
            self.assertEqual(q.sort, ["nom:asc"])
            self.assertEqual(q.limit, 20)

    # --- Default limit ---

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_010_default_limit_is_10(self, mock_search: MagicMock) -> None:
        """Test that default limit is 10."""
        mock_result = MagicMock(spec=CompetitionsMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_competitions(name="test")

        queries = mock_search.call_args[0][0]
        self.assertEqual(queries[0].limit, 10)

    # --- None filter/sort doesn't change query ---

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_011_none_filter_sort(self, mock_search: MagicMock) -> None:
        """Test that None filter/sort results in None on query."""
        mock_result = MagicMock(spec=CompetitionsMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_competitions(name="test", filter=None, sort=None)

        queries = mock_search.call_args[0][0]
        self.assertIsNone(queries[0].filter)
        self.assertIsNone(queries[0].sort)

    # --- get_all_index_settings ---

    def test_012_get_all_index_settings(self) -> None:
        """Test get_all_index_settings calls get_index_settings for each index."""
        mock_settings = MeilisearchIndexSettings(filterable_attributes=["type"])
        with patch.object(
            self.client, "get_index_settings", return_value=mock_settings
        ):
            result = self.client.get_all_index_settings()
            self.assertIsInstance(result, dict)
            self.assertTrue(len(result) > 0)
            for uid, settings in result.items():
                self.assertIsInstance(settings, MeilisearchIndexSettings)

    def test_013_get_all_index_settings_some_fail(self) -> None:
        """Test get_all_index_settings handles None results gracefully."""
        call_count = 0

        def mock_get_settings(uid, cached_session=None):
            nonlocal call_count
            call_count += 1
            if call_count % 2 == 0:
                return None
            return MeilisearchIndexSettings(filterable_attributes=[uid])

        with patch.object(
            self.client, "get_index_settings", side_effect=mock_get_settings
        ):
            result = self.client.get_all_index_settings()
            # Should only include successful results
            for settings in result.values():
                self.assertIsNotNone(settings)


if __name__ == "__main__":
    unittest.main()
