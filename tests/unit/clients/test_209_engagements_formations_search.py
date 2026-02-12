"""Tests for MeilisearchFFBBClient search_engagements and search_formations."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from ffbb_api_client_v2.clients.meilisearch_ffbb_client import MeilisearchFFBBClient
from ffbb_api_client_v2.models.engagements_multi_search_query import (
    EngagementsMultiSearchQuery,
)
from ffbb_api_client_v2.models.formations_multi_search_query import (
    FormationsMultiSearchQuery,
)
from ffbb_api_client_v2.models.multi_search_result_engagements import (
    EngagementsMultiSearchResult,
)
from ffbb_api_client_v2.models.multi_search_result_formations import (
    FormationsMultiSearchResult,
)
from ffbb_api_client_v2.models.multi_search_results_class import MultiSearchResults


class Test209EngagementsFormationsSearch(unittest.TestCase):
    """Tests for engagements and formations search in MeilisearchFFBBClient."""

    def setUp(self) -> None:
        with patch(
            "ffbb_api_client_v2.helpers.meilisearch_client_extension.CacheManager"
        ):
            self.client = MeilisearchFFBBClient(bearer_token="test-token")

    def _make_mock_results(self, result_mock: MagicMock) -> MultiSearchResults:
        results = MagicMock(spec=MultiSearchResults)
        results.results = [result_mock]
        return results

    # --- Engagements ---

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_000_search_engagements_basic(self, mock_search: MagicMock) -> None:
        """Test search_engagements calls recursive_multi_search."""
        mock_result = MagicMock(spec=EngagementsMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        result = self.client.search_engagements(name="Mantes")
        self.assertIsNotNone(result)
        mock_search.assert_called_once()

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_001_search_engagements_with_filter(self, mock_search: MagicMock) -> None:
        """Test search_engagements passes filter."""
        mock_result = MagicMock(spec=EngagementsMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_engagements(
            name=None,
            filter=['idCompetition.sexe = "Féminin"'],
        )

        queries = mock_search.call_args[0][0]
        self.assertEqual(len(queries), 1)
        self.assertIsInstance(queries[0], EngagementsMultiSearchQuery)
        self.assertEqual(queries[0].filter, ['idCompetition.sexe = "Féminin"'])

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_002_search_engagements_with_sort(self, mock_search: MagicMock) -> None:
        """Test search_engagements passes sort."""
        mock_result = MagicMock(spec=EngagementsMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_engagements(name=None, sort=["nom:asc"])
        queries = mock_search.call_args[0][0]
        self.assertEqual(queries[0].sort, ["nom:asc"])

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_003_search_multiple_engagements(self, mock_search: MagicMock) -> None:
        """Test search_multiple_engagements."""
        mock_result = MagicMock(spec=EngagementsMultiSearchResult)
        mock_results = MagicMock(spec=MultiSearchResults)
        mock_results.results = [mock_result, mock_result]
        mock_search.return_value = mock_results

        result = self.client.search_multiple_engagements(
            names=["Team A", "Team B"],
            filter=["clubPro = true"],
            limit=20,
        )
        self.assertIsNotNone(result)
        queries = mock_search.call_args[0][0]
        self.assertEqual(len(queries), 2)
        for q in queries:
            self.assertEqual(q.filter, ["clubPro = true"])
            self.assertEqual(q.limit, 20)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_004_search_multiple_engagements_none(self, mock_search: MagicMock) -> None:
        """Test search_multiple_engagements with None names."""
        result = self.client.search_multiple_engagements(names=None)
        self.assertIsNone(result)
        mock_search.assert_not_called()

    # --- Formations ---

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_005_search_formations_basic(self, mock_search: MagicMock) -> None:
        """Test search_formations calls recursive_multi_search."""
        mock_result = MagicMock(spec=FormationsMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        result = self.client.search_formations(name="Technicien")
        self.assertIsNotNone(result)
        mock_search.assert_called_once()

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_006_search_formations_with_filter(self, mock_search: MagicMock) -> None:
        """Test search_formations passes filter."""
        mock_result = MagicMock(spec=FormationsMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_formations(
            name=None,
            filter=['domain = "Technicien"'],
        )

        queries = mock_search.call_args[0][0]
        self.assertIsInstance(queries[0], FormationsMultiSearchQuery)
        self.assertEqual(queries[0].filter, ['domain = "Technicien"'])

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_007_search_formations_with_sort(self, mock_search: MagicMock) -> None:
        """Test search_formations passes sort."""
        mock_result = MagicMock(spec=FormationsMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_formations(name=None, sort=["title:asc"])
        queries = mock_search.call_args[0][0]
        self.assertEqual(queries[0].sort, ["title:asc"])

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_008_search_multiple_formations(self, mock_search: MagicMock) -> None:
        """Test search_multiple_formations."""
        mock_result = MagicMock(spec=FormationsMultiSearchResult)
        mock_results = MagicMock(spec=MultiSearchResults)
        mock_results.results = [mock_result, mock_result]
        mock_search.return_value = mock_results

        result = self.client.search_multiple_formations(
            names=["DEFB", "Bénévole"],
            filter=['type = "formation"'],
        )
        self.assertIsNotNone(result)
        queries = mock_search.call_args[0][0]
        self.assertEqual(len(queries), 2)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_009_search_multiple_formations_none(self, mock_search: MagicMock) -> None:
        """Test search_multiple_formations with None names."""
        result = self.client.search_multiple_formations(names=None)
        self.assertIsNone(result)
        mock_search.assert_not_called()

    # --- Default limit ---

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_010_default_limit_engagements(self, mock_search: MagicMock) -> None:
        """Test default limit is 10 for engagements."""
        mock_result = MagicMock(spec=EngagementsMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_engagements(name="test")
        queries = mock_search.call_args[0][0]
        self.assertEqual(queries[0].limit, 10)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_011_default_limit_formations(self, mock_search: MagicMock) -> None:
        """Test default limit is 10 for formations."""
        mock_result = MagicMock(spec=FormationsMultiSearchResult)
        mock_search.return_value = self._make_mock_results(mock_result)

        self.client.search_formations(name="test")
        queries = mock_search.call_args[0][0]
        self.assertEqual(queries[0].limit, 10)


if __name__ == "__main__":
    unittest.main()
