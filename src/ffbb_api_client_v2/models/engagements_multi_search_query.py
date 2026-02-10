from __future__ import annotations

from ..config import MEILISEARCH_FACETS_ENGAGEMENTS, MEILISEARCH_INDEX_ENGAGEMENTS
from .engagements_facet_distribution import EngagementsFacetDistribution
from .engagements_facet_stats import EngagementsFacetStats
from .multi_search_query import MultiSearchQuery
from .multi_search_result_engagements import EngagementsMultiSearchResult
from .multi_search_results import MultiSearchResult


class EngagementsMultiSearchQuery(MultiSearchQuery):
    def __init__(
        self,
        q: str | None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
    ):
        super().__init__(
            index_uid=MEILISEARCH_INDEX_ENGAGEMENTS,
            q=q,
            facets=MEILISEARCH_FACETS_ENGAGEMENTS,
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
        )

    def is_valid_result(self, result: MultiSearchResult):
        return result and (
            isinstance(result, EngagementsMultiSearchResult)
            and (
                result.facet_distribution is None
                or isinstance(result.facet_distribution, EngagementsFacetDistribution)
            )
            and (
                result.facet_stats is None
                or isinstance(result.facet_stats, EngagementsFacetStats)
            )
        )
