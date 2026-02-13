"""Tests for federated multi-search functionality."""

from __future__ import annotations

import unittest
from typing import Any
from unittest.mock import MagicMock, patch

from ffbb_api_client_v2.clients.meilisearch_client import MeilisearchClient
from ffbb_api_client_v2.clients.meilisearch_ffbb_client import MeilisearchFFBBClient
from ffbb_api_client_v2.models.federated_search_result import (
    FederatedHit,
    FederatedSearchResult,
    FederationInfo,
)
from ffbb_api_client_v2.models.multi_search_query import MultiSearchQuery


class Test216FederationInfo(unittest.TestCase):
    """Tests for FederationInfo model."""

    def test_000_from_dict(self) -> None:
        raw: dict[str, Any] = {
            "indexUid": "ffbbserver_organismes",
            "queriesPosition": 0,
            "weightedRankingScore": 0.95,
        }
        info = FederationInfo.from_dict(raw)
        self.assertEqual(info.index_uid, "ffbbserver_organismes")
        self.assertEqual(info.queries_position, 0)
        self.assertAlmostEqual(info.weighted_ranking_score, 0.95, places=2)

    def test_001_to_dict(self) -> None:
        info = FederationInfo(
            index_uid="test", queries_position=1, weighted_ranking_score=0.8
        )
        d = info.to_dict()
        self.assertEqual(d["indexUid"], "test")
        self.assertEqual(d["queriesPosition"], 1)

    def test_002_empty_from_dict(self) -> None:
        info = FederationInfo.from_dict({})
        self.assertIsNone(info.index_uid)
        self.assertIsNone(info.queries_position)
        self.assertIsNone(info.weighted_ranking_score)


class Test216FederatedHit(unittest.TestCase):
    """Tests for FederatedHit model."""

    def test_000_from_dict_with_federation(self) -> None:
        raw: dict[str, Any] = {
            "id": 123,
            "nom": "Club de Paris",
            "_federation": {
                "indexUid": "ffbbserver_organismes",
                "queriesPosition": 0,
                "weightedRankingScore": 0.9,
            },
        }
        hit = FederatedHit.from_dict(raw)
        self.assertEqual(hit.data, {"id": 123, "nom": "Club de Paris"})
        self.assertIsNotNone(hit.federation)
        self.assertEqual(hit.federation.index_uid, "ffbbserver_organismes")

    def test_001_from_dict_without_federation(self) -> None:
        raw: dict[str, Any] = {"id": 1, "name": "test"}
        hit = FederatedHit.from_dict(raw)
        self.assertEqual(hit.data, {"id": 1, "name": "test"})
        self.assertIsNone(hit.federation)

    def test_002_to_dict_roundtrip(self) -> None:
        hit = FederatedHit(
            data={"id": 1},
            federation=FederationInfo(index_uid="test", queries_position=0),
        )
        d = hit.to_dict()
        self.assertEqual(d["id"], 1)
        self.assertIn("_federation", d)
        self.assertEqual(d["_federation"]["indexUid"], "test")


class Test216FederatedSearchResult(unittest.TestCase):
    """Tests for FederatedSearchResult model."""

    def test_000_from_dict_full(self) -> None:
        raw: dict[str, Any] = {
            "hits": [
                {
                    "id": 1,
                    "nom": "Club A",
                    "_federation": {
                        "indexUid": "ffbbserver_organismes",
                        "queriesPosition": 0,
                    },
                },
                {
                    "id": 2,
                    "nom": "Salle B",
                    "_federation": {
                        "indexUid": "ffbbserver_salles",
                        "queriesPosition": 1,
                    },
                },
            ],
            "processingTimeMs": 5,
            "offset": 0,
            "limit": 20,
            "estimatedTotalHits": 100,
        }
        result = FederatedSearchResult.from_dict(raw)
        self.assertEqual(len(result.hits), 2)
        self.assertEqual(result.processing_time_ms, 5)
        self.assertEqual(result.estimated_total_hits, 100)
        self.assertEqual(result.hits[0].federation.index_uid, "ffbbserver_organismes")
        self.assertEqual(result.hits[1].federation.index_uid, "ffbbserver_salles")

    def test_001_from_dict_empty_hits(self) -> None:
        raw: dict[str, Any] = {"hits": [], "processingTimeMs": 1}
        result = FederatedSearchResult.from_dict(raw)
        self.assertIsNone(result.hits)

    def test_002_to_dict(self) -> None:
        result = FederatedSearchResult(
            hits=[FederatedHit(data={"id": 1})],
            processing_time_ms=10,
            offset=0,
            limit=20,
            estimated_total_hits=50,
        )
        d = result.to_dict()
        self.assertEqual(len(d["hits"]), 1)
        self.assertEqual(d["processingTimeMs"], 10)
        self.assertEqual(d["estimatedTotalHits"], 50)


class Test216MeilisearchClientFederated(unittest.TestCase):
    """Tests for MeilisearchClient.federated_multi_search."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.clients.meilisearch_client.CacheManager"):
            self.client = MeilisearchClient(
                bearer_token="test-token", url="https://test/"
            )

    @patch("ffbb_api_client_v2.clients.meilisearch_client.catch_result")
    def test_000_federated_search_returns_result(self, mock_catch: MagicMock) -> None:
        mock_catch.return_value = {
            "hits": [
                {
                    "id": 1,
                    "_federation": {"indexUid": "test", "queriesPosition": 0},
                }
            ],
            "processingTimeMs": 5,
            "estimatedTotalHits": 1,
        }
        queries = [MultiSearchQuery(index_uid="test", q="hello")]
        result = self.client.federated_multi_search(queries=queries)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, FederatedSearchResult)
        self.assertEqual(len(result.hits), 1)

    @patch("ffbb_api_client_v2.clients.meilisearch_client.catch_result")
    def test_001_federated_search_with_options(self, mock_catch: MagicMock) -> None:
        mock_catch.return_value = {"hits": [], "processingTimeMs": 1}
        self.client.federated_multi_search(
            queries=[MultiSearchQuery(index_uid="test", q="")],
            federation_options={"limit": 50},
        )
        # Verify http_post_json was called with federation in body
        call_args = mock_catch.call_args
        self.assertIsNotNone(call_args)

    @patch("ffbb_api_client_v2.clients.meilisearch_client.catch_result")
    def test_002_federated_search_none_on_empty(self, mock_catch: MagicMock) -> None:
        mock_catch.return_value = None
        result = self.client.federated_multi_search(queries=[])
        self.assertIsNone(result)


class Test216MeilisearchFFBBFederatedSearch(unittest.TestCase):
    """Tests for MeilisearchFFBBClient.federated_search_all."""

    def setUp(self) -> None:
        with patch(
            "ffbb_api_client_v2.helpers.meilisearch_client_extension.CacheManager"
        ):
            self.client = MeilisearchFFBBClient(bearer_token="test-token")

    @patch.object(MeilisearchFFBBClient, "federated_multi_search")
    def test_000_federated_search_all_calls_federated(
        self, mock_fed: MagicMock
    ) -> None:
        mock_fed.return_value = FederatedSearchResult(hits=[], processing_time_ms=1)
        self.client.federated_search_all(q="Paris")
        mock_fed.assert_called_once()
        # Should pass 9 queries (one per FFBB index)
        args, kwargs = mock_fed.call_args
        queries = kwargs.get("queries") or args[0]
        self.assertEqual(len(queries), 9)

    @patch.object(MeilisearchFFBBClient, "federated_multi_search")
    def test_001_federated_search_all_passes_limit(self, mock_fed: MagicMock) -> None:
        mock_fed.return_value = None
        self.client.federated_search_all(q="test", limit=50)
        _, kwargs = mock_fed.call_args
        options = kwargs.get("federation_options", {})
        self.assertEqual(options.get("limit"), 50)


if __name__ == "__main__":
    unittest.main()
