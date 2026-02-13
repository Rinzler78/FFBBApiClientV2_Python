"""Model for Meilisearch federated multi-search responses.

When using federation in multi-search, Meilisearch returns a single merged
list of hits across all indexes, ranked by relevance, instead of separate
results per index.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class FederationInfo:
    """Federation metadata attached to each hit in federated results."""

    index_uid: str | None = None
    queries_position: int | None = None
    weighted_ranking_score: float | None = None

    @staticmethod
    def from_dict(obj: Any) -> FederationInfo:
        assert isinstance(obj, dict)
        return FederationInfo(
            index_uid=obj.get("indexUid"),
            queries_position=obj.get("queriesPosition"),
            weighted_ranking_score=obj.get("weightedRankingScore"),
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.index_uid is not None:
            result["indexUid"] = self.index_uid
        if self.queries_position is not None:
            result["queriesPosition"] = self.queries_position
        if self.weighted_ranking_score is not None:
            result["weightedRankingScore"] = self.weighted_ranking_score
        return result


@dataclass
class FederatedHit:
    """A single hit from a federated multi-search response.

    Contains the raw document data plus federation metadata.
    """

    data: dict[str, Any] | None = None
    federation: FederationInfo | None = None

    @staticmethod
    def from_dict(obj: Any) -> FederatedHit:
        assert isinstance(obj, dict)
        federation_raw = obj.get("_federation")
        federation = (
            FederationInfo.from_dict(federation_raw)
            if isinstance(federation_raw, dict)
            else None
        )
        # Everything except _federation is the document data
        data = {k: v for k, v in obj.items() if k != "_federation"}
        return FederatedHit(data=data, federation=federation)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.data:
            result.update(self.data)
        if self.federation is not None:
            result["_federation"] = self.federation.to_dict()
        return result


@dataclass
class FederatedSearchResult:
    """Response from a federated multi-search request.

    Meilisearch federated multi-search merges results from multiple indexes
    into a single list ranked by relevance.
    """

    hits: list[FederatedHit] | None = None
    processing_time_ms: int | None = None
    offset: int | None = None
    limit: int | None = None
    estimated_total_hits: int | None = None
    facet_distribution: dict[str, Any] | None = None
    facet_stats: dict[str, Any] | None = None

    @staticmethod
    def from_dict(obj: Any) -> FederatedSearchResult:
        assert isinstance(obj, dict)
        hits_raw = obj.get("hits", [])
        hits = [FederatedHit.from_dict(h) for h in hits_raw] if hits_raw else None
        return FederatedSearchResult(
            hits=hits,
            processing_time_ms=obj.get("processingTimeMs"),
            offset=obj.get("offset"),
            limit=obj.get("limit"),
            estimated_total_hits=obj.get("estimatedTotalHits"),
            facet_distribution=obj.get("facetDistribution"),
            facet_stats=obj.get("facetStats"),
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.hits is not None:
            result["hits"] = [h.to_dict() for h in self.hits]
        if self.processing_time_ms is not None:
            result["processingTimeMs"] = self.processing_time_ms
        if self.offset is not None:
            result["offset"] = self.offset
        if self.limit is not None:
            result["limit"] = self.limit
        if self.estimated_total_hits is not None:
            result["estimatedTotalHits"] = self.estimated_total_hits
        if self.facet_distribution is not None:
            result["facetDistribution"] = self.facet_distribution
        if self.facet_stats is not None:
            result["facetStats"] = self.facet_stats
        return result
