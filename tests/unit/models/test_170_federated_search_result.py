"""Unit tests for federated search result to_dict branch coverage."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.meilisearch.models.federated_search_result import (
    FederatedHit,
    FederatedSearchResult,
    FederationInfo,
)


class TestFederationInfoToDict(unittest.TestCase):
    def test_all_none_returns_empty_dict(self) -> None:
        info = FederationInfo()
        self.assertEqual(info.to_dict(), {})

    def test_partial_fields(self) -> None:
        info = FederationInfo(index_uid="organismes")
        self.assertEqual(info.to_dict(), {"indexUid": "organismes"})

    def test_all_fields(self) -> None:
        info = FederationInfo(
            index_uid="idx", queries_position=0, weighted_ranking_score=0.9
        )
        d = info.to_dict()
        self.assertEqual(d["indexUid"], "idx")
        self.assertEqual(d["queriesPosition"], 0)
        self.assertAlmostEqual(d["weightedRankingScore"], 0.9)


class TestFederatedHitToDict(unittest.TestCase):
    def test_none_data_returns_empty_dict(self) -> None:
        hit = FederatedHit(data=None, federation=None)
        self.assertEqual(hit.to_dict(), {})

    def test_empty_data_returns_empty_dict(self) -> None:
        hit = FederatedHit(data={}, federation=None)
        self.assertEqual(hit.to_dict(), {})

    def test_with_data_and_federation(self) -> None:
        hit = FederatedHit(
            data={"id": "1", "nom": "Club"},
            federation=FederationInfo(index_uid="organismes"),
        )
        d = hit.to_dict()
        self.assertEqual(d["id"], "1")
        self.assertEqual(d["nom"], "Club")
        self.assertEqual(d["_federation"], {"indexUid": "organismes"})

    def test_from_dict_without_federation(self) -> None:
        hit = FederatedHit.from_dict({"id": "1", "nom": "Club"})
        self.assertIsNone(hit.federation)
        assert hit.data is not None
        self.assertEqual(hit.data["id"], "1")

    def test_from_dict_with_non_dict_federation(self) -> None:
        hit = FederatedHit.from_dict({"id": "1", "_federation": "invalid"})
        self.assertIsNone(hit.federation)


class TestFederatedSearchResultToDict(unittest.TestCase):
    def test_all_none_returns_empty_dict(self) -> None:
        result = FederatedSearchResult()
        self.assertEqual(result.to_dict(), {})

    def test_partial_fields(self) -> None:
        result = FederatedSearchResult(processing_time_ms=5, offset=0, limit=20)
        d = result.to_dict()
        self.assertEqual(d, {"processingTimeMs": 5, "offset": 0, "limit": 20})
        self.assertNotIn("hits", d)
        self.assertNotIn("estimatedTotalHits", d)
        self.assertNotIn("facetDistribution", d)
        self.assertNotIn("facetStats", d)

    def test_all_fields(self) -> None:
        hit = FederatedHit(data={"id": "1"})
        result = FederatedSearchResult(
            hits=[hit],
            processing_time_ms=3,
            offset=0,
            limit=10,
            estimated_total_hits=100,
            facet_distribution={"type": {"club": 5}},
            facet_stats={"score": {"min": 0.1}},
        )
        d = result.to_dict()
        self.assertEqual(len(d["hits"]), 1)
        self.assertEqual(d["processingTimeMs"], 3)
        self.assertEqual(d["offset"], 0)
        self.assertEqual(d["limit"], 10)
        self.assertEqual(d["estimatedTotalHits"], 100)
        self.assertEqual(d["facetDistribution"], {"type": {"club": 5}})
        self.assertEqual(d["facetStats"], {"score": {"min": 0.1}})

    def test_from_dict_empty_hits(self) -> None:
        result = FederatedSearchResult.from_dict({"hits": []})
        self.assertIsNone(result.hits)

    def test_from_dict_no_hits_key(self) -> None:
        result = FederatedSearchResult.from_dict({})
        self.assertIsNone(result.hits)


if __name__ == "__main__":
    unittest.main()
