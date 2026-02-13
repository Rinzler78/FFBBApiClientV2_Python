from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ...utils.converter_utils import (
    from_int,
    from_list,
    from_str,
)
from .facet_distribution import FacetDistribution
from .facet_stats import FacetStats
from .hit import Hit
from .multi_search_results import MultiSearchResult


@dataclass
class MultiSearchQuery:
    index_uid: str | None = None
    q: str | None = None
    facets: list[str] | None = None
    limit: int | None = 20
    offset: int | None = 0
    filter: list[Any] | None = None
    sort: list[Any] | None = None
    # Meilisearch advanced search parameters
    matching_strategy: str | None = None
    attributes_to_highlight: list[str] | None = None
    highlight_pre_tag: str | None = None
    highlight_post_tag: str | None = None
    attributes_to_crop: list[str] | None = None
    crop_length: int | None = None
    crop_marker: str | None = None
    show_matches_position: bool | None = None
    show_ranking_score: bool | None = None
    show_ranking_score_details: bool | None = None
    ranking_score_threshold: float | None = None
    attributes_to_search_on: list[str] | None = None
    attributes_to_retrieve: list[str] | None = None
    distinct: str | None = None
    # Internal
    lower_q: str | None = field(init=False, default=None, repr=False)

    def __post_init__(self) -> None:
        self.lower_q = self.q.lower() if self.q else None

    @staticmethod
    def from_dict(obj: Any) -> MultiSearchQuery:
        assert isinstance(obj, dict)
        index_uid = from_str(obj, "indexUid")
        q = from_str(obj, "q")
        facets = from_list(str, obj, "facets")
        limit = from_int(obj, "limit")
        offset = from_int(obj, "offset")
        filter = from_list(lambda x: x, obj, "filter")
        sort = from_list(lambda x: x, obj, "sort")
        matching_strategy = from_str(obj, "matchingStrategy")
        attributes_to_highlight = from_list(str, obj, "attributesToHighlight")
        highlight_pre_tag = from_str(obj, "highlightPreTag")
        highlight_post_tag = from_str(obj, "highlightPostTag")
        attributes_to_crop = from_list(str, obj, "attributesToCrop")
        crop_length = from_int(obj, "cropLength")
        crop_marker = from_str(obj, "cropMarker")
        show_ranking_score = obj.get("showRankingScore")
        show_ranking_score_details = obj.get("showRankingScoreDetails")
        ranking_score_threshold = obj.get("rankingScoreThreshold")
        attributes_to_search_on = from_list(str, obj, "attributesToSearchOn")
        attributes_to_retrieve = from_list(str, obj, "attributesToRetrieve")
        distinct = from_str(obj, "distinct")
        return MultiSearchQuery(
            index_uid=index_uid,
            q=q,
            facets=facets,
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
            matching_strategy=matching_strategy,
            attributes_to_highlight=attributes_to_highlight,
            highlight_pre_tag=highlight_pre_tag,
            highlight_post_tag=highlight_post_tag,
            attributes_to_crop=attributes_to_crop,
            crop_length=crop_length,
            crop_marker=crop_marker,
            show_ranking_score=show_ranking_score,
            show_ranking_score_details=show_ranking_score_details,
            ranking_score_threshold=ranking_score_threshold,
            attributes_to_search_on=attributes_to_search_on,
            attributes_to_retrieve=attributes_to_retrieve,
            distinct=distinct,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.index_uid is not None:
            result["indexUid"] = self.index_uid
        if self.q is not None:
            result["q"] = self.q
        if self.facets is not None:
            result["facets"] = self.facets
        if self.limit is not None:
            result["limit"] = self.limit
        if self.offset is not None:
            result["offset"] = self.offset
        if self.filter is not None:
            result["filter"] = self.filter
        if self.sort is not None:
            result["sort"] = self.sort
        if self.matching_strategy is not None:
            result["matchingStrategy"] = self.matching_strategy
        if self.attributes_to_highlight is not None:
            result["attributesToHighlight"] = self.attributes_to_highlight
        if self.highlight_pre_tag is not None:
            result["highlightPreTag"] = self.highlight_pre_tag
        if self.highlight_post_tag is not None:
            result["highlightPostTag"] = self.highlight_post_tag
        if self.attributes_to_crop is not None:
            result["attributesToCrop"] = self.attributes_to_crop
        if self.crop_length is not None:
            result["cropLength"] = self.crop_length
        if self.crop_marker is not None:
            result["cropMarker"] = self.crop_marker
        if self.show_matches_position is not None:
            result["showMatchesPosition"] = self.show_matches_position
        if self.show_ranking_score is not None:
            result["showRankingScore"] = self.show_ranking_score
        if self.show_ranking_score_details is not None:
            result["showRankingScoreDetails"] = self.show_ranking_score_details
        if self.ranking_score_threshold is not None:
            result["rankingScoreThreshold"] = self.ranking_score_threshold
        if self.attributes_to_search_on is not None:
            result["attributesToSearchOn"] = self.attributes_to_search_on
        if self.attributes_to_retrieve is not None:
            result["attributesToRetrieve"] = self.attributes_to_retrieve
        if self.distinct is not None:
            result["distinct"] = self.distinct
        return result

    def is_valid_result(self, result: MultiSearchResult):
        return result and (
            isinstance(result, MultiSearchResult)
            and (
                result.facet_distribution is None
                or isinstance(result.facet_distribution, FacetDistribution)
            )
            and (
                result.facet_stats is None or isinstance(result.facet_stats, FacetStats)
            )
        )

    def is_valid_hit(self, _hit: Hit):
        return True

    def filter_result(self, result: MultiSearchResult) -> MultiSearchResult:
        if self.lower_q and result.hits:
            invalid_hits = [
                hit for hit in result.hits if not hit.is_valid_for_query(self.lower_q)
            ]

            if invalid_hits:
                if result.estimated_total_hits is not None:
                    result.estimated_total_hits -= len(invalid_hits)

                for hit in invalid_hits:
                    result.hits.remove(hit)
        return result
