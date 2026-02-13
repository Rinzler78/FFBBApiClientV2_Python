from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, TypeVar, get_args

from ...utils.converter_utils import (
    from_int,
    from_list,
    from_str,
)
from .facet_distribution import FacetDistribution
from .facet_stats import FacetStats
from .hit import Hit

HitType = TypeVar("HitType", bound=Hit)
FacetDistributionType = TypeVar("FacetDistributionType", bound=FacetDistribution)
FacetStatsType = TypeVar("FacetStatsType", bound=FacetStats)


@dataclass
class MultiSearchResult(Generic[HitType, FacetDistributionType, FacetStatsType]):
    index_uid: str | None = None
    hits: list[HitType] | None = None
    query: str | None = None
    processing_time_ms: int | None = None
    limit: int | None = None
    offset: int | None = None
    estimated_total_hits: int | None = None
    facet_distribution: FacetDistributionType | None = None
    facet_stats: FacetStatsType | None = None

    @classmethod
    def from_dict(
        cls,
        obj: Any,
    ) -> MultiSearchResult[HitType, FacetDistributionType, FacetStatsType]:
        """
        Parse dict into the concrete MultiSearchResult subclass.
        Types are extracted from the class's generic parameters.
        """
        assert isinstance(obj, dict)

        # Extract generic type arguments from class definition
        # e.g., OrganismesMultiSearchResult inherits from
        # MultiSearchResult[OrganismesHit, OrganismesFacetDistribution, OrganismesFacetStats]
        orig_bases = getattr(cls, "__orig_bases__", ())
        if not orig_bases:
            raise TypeError(f"{cls.__name__} must be a generic subclass")
        type_args = get_args(orig_bases[0])
        hit_type: type[HitType] = type_args[0]
        facet_distribution_type: type[FacetDistributionType] = type_args[1]
        facet_stats_type: type[FacetStatsType] = type_args[2]

        index_uid = from_str(obj, "indexUid")
        hits = from_list(hit_type.from_dict, obj, "hits")
        query = from_str(obj, "query")
        processing_time_ms = from_int(obj, "processingTimeMs")
        limit = from_int(obj, "limit")
        offset = from_int(obj, "offset")
        estimated_total_hits = from_int(obj, "estimatedTotalHits")
        fd_val = obj.get("facetDistribution")
        facet_distribution = (
            facet_distribution_type.from_dict(fd_val)
            if isinstance(fd_val, dict)
            else None
        )
        fs_val = obj.get("facetStats")
        facet_stats = (
            facet_stats_type.from_dict(fs_val) if isinstance(fs_val, dict) else None
        )
        return cls(
            index_uid=index_uid,
            hits=hits,  # type: ignore[arg-type]  # from_dict returns Hit base type
            query=query,
            processing_time_ms=processing_time_ms,
            limit=limit,
            offset=offset,
            estimated_total_hits=estimated_total_hits,
            facet_distribution=facet_distribution,  # type: ignore[arg-type]  # dynamic type from generics
            facet_stats=facet_stats,  # type: ignore[arg-type]  # dynamic type from generics
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.index_uid is not None:
            result["indexUid"] = self.index_uid
        if self.hits is not None:
            result["hits"] = [hit.to_dict() for hit in self.hits]
        if self.query is not None:
            result["query"] = self.query
        if self.processing_time_ms is not None:
            result["processingTimeMs"] = self.processing_time_ms
        if self.limit is not None:
            result["limit"] = self.limit
        if self.offset is not None:
            result["offset"] = self.offset
        if self.estimated_total_hits is not None:
            result["estimatedTotalHits"] = self.estimated_total_hits
        if self.facet_distribution is not None:
            result["facetDistribution"] = self.facet_distribution.to_dict()
        if self.facet_stats is not None:
            result["facetStats"] = self.facet_stats.to_dict()
        return result
