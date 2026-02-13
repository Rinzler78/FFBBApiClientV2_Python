"""Tests for pagination guard-rails in MeilisearchClientExtension and _fetch_all_pages."""

from __future__ import annotations

import logging
import unittest
from unittest.mock import MagicMock, patch

from ffbb_api_client_v2.helpers.meilisearch_client_extension import (
    DEFAULT_MAX_ITERATIONS,
    DEFAULT_MAX_TOTAL_HITS,
    MeilisearchClientExtension,
)
from ffbb_api_client_v2.models.multi_search_query import MultiSearchQuery
from ffbb_api_client_v2.models.multi_search_results import MultiSearchResult
from ffbb_api_client_v2.models.multi_search_results_class import MultiSearchResults


class Test215RecursivePaginationGuardrails(unittest.TestCase):
    """Tests for max_iterations and max_total_hits guard-rails."""

    def setUp(self) -> None:
        with patch(
            "ffbb_api_client_v2.helpers.meilisearch_client_extension.CacheManager"
        ):
            self.client = MeilisearchClientExtension(
                bearer_token="test-token", url="https://test/"
            )

    def test_000_default_constants(self) -> None:
        """Verify default guard-rail constants."""
        self.assertEqual(DEFAULT_MAX_TOTAL_HITS, 1000)
        self.assertEqual(DEFAULT_MAX_ITERATIONS, 20)

    def test_001_max_iterations_parameter_accepted(self) -> None:
        """recursive_smart_multi_search accepts max_iterations parameter."""
        with patch.object(self.client, "smart_multi_search", return_value=None):
            result = self.client.recursive_smart_multi_search(
                queries=None, max_iterations=5
            )
            self.assertIsNone(result)

    def test_002_max_total_hits_parameter_accepted(self) -> None:
        """recursive_smart_multi_search accepts max_total_hits parameter."""
        with patch.object(self.client, "smart_multi_search", return_value=None):
            result = self.client.recursive_smart_multi_search(
                queries=None, max_total_hits=500
            )
            self.assertIsNone(result)

    @patch.object(MeilisearchClientExtension, "smart_multi_search")
    def test_003_stops_at_max_iterations(self, mock_search: MagicMock) -> None:
        """Recursive pagination stops when max_iterations is reached."""
        # Create a result that always asks for more pages
        mock_result = MagicMock(spec=MultiSearchResult)
        mock_result.hits = [MagicMock()] * 5
        mock_result.estimated_total_hits = (
            100  # More than limit, but under max_total_hits
        )
        mock_result.index_uid = "test"

        results = MagicMock(spec=MultiSearchResults)
        results.results = [mock_result]

        mock_search.return_value = results

        query = MultiSearchQuery(index_uid="test", q="", limit=5, offset=0)

        with self.assertLogs(
            "ffbb_api_client_v2.helpers.meilisearch_client_extension",
            level=logging.WARNING,
        ) as cm:
            self.client.recursive_smart_multi_search(
                queries=[query],
                max_iterations=1,
                max_total_hits=100000,  # High enough to not interfere
            )

        # Should have logged max_iterations warning
        self.assertTrue(
            any("max_iterations" in msg for msg in cm.output),
            f"Expected max_iterations warning in logs: {cm.output}",
        )

    @patch.object(MeilisearchClientExtension, "smart_multi_search")
    def test_004_stops_at_max_total_hits(self, mock_search: MagicMock) -> None:
        """Recursive pagination stops when offset exceeds max_total_hits."""
        mock_result = MagicMock(spec=MultiSearchResult)
        mock_result.hits = [MagicMock()] * 20
        mock_result.estimated_total_hits = 5000
        mock_result.index_uid = "test"

        results = MagicMock(spec=MultiSearchResults)
        results.results = [mock_result]

        mock_search.return_value = results

        # Start near the limit
        query = MultiSearchQuery(index_uid="test", q="", limit=20, offset=990)

        with self.assertLogs(
            "ffbb_api_client_v2.helpers.meilisearch_client_extension",
            level=logging.WARNING,
        ) as cm:
            self.client.recursive_smart_multi_search(
                queries=[query], max_total_hits=1000
            )

        # Should have logged max_total_hits warning
        self.assertTrue(
            any("max_total_hits" in msg for msg in cm.output),
            f"Expected max_total_hits warning in logs: {cm.output}",
        )

    def test_005_backward_compat_recursive_multi_search(self) -> None:
        """recursive_multi_search alias should accept new parameters."""
        with patch.object(self.client, "smart_multi_search", return_value=None):
            result = self.client.recursive_multi_search(
                queries=None, max_iterations=3, max_total_hits=500
            )
            self.assertIsNone(result)


class Test215FetchAllPagesWarning(unittest.TestCase):
    """Tests for max_items warning in ApiFFBBAppClient._fetch_all_pages."""

    def test_000_warning_logged_when_max_items_reached(self) -> None:
        """_fetch_all_pages should log warning when max_items is hit."""
        from ffbb_api_client_v2.clients.api_ffbb_app_client import ApiFFBBAppClient
        from ffbb_api_client_v2.utils.secure_logging import get_secure_logger

        with patch(
            "ffbb_api_client_v2.clients.api_ffbb_app_client.catch_result"
        ) as mock_catch:
            # Simulate a response with more items available than max_items
            mock_catch.return_value = {
                "data": [{"id": i} for i in range(100)],
                "meta": {"total_count": 50000, "filter_count": 50000},
            }

            client = ApiFFBBAppClient.__new__(ApiFFBBAppClient)
            client.url = "https://test/"
            client.headers = {"Authorization": "Bearer test"}
            client.debug = False
            client.cached_session = None
            client.logger = get_secure_logger("test_fetch_all")

            with self.assertLogs("test_fetch_all", level=logging.WARNING) as cm:
                client._fetch_all_pages(
                    endpoint="items/test",
                    fields=["id"],
                    from_list_fn=lambda x: x,
                    max_items=100,
                )

            self.assertTrue(
                any("max_items" in msg for msg in cm.output),
                f"Expected max_items warning in logs: {cm.output}",
            )


if __name__ == "__main__":
    unittest.main()
