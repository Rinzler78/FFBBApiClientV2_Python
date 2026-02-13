from __future__ import annotations

from ...meilisearch.models.multi_search_query import MultiSearchQuery
from ...meilisearch.models.multi_search_results import MultiSearchResult
from ..config import MEILISEARCH_FACETS_COMPETITIONS, MEILISEARCH_INDEX_COMPETITIONS
from .competitions_facet_distribution import CompetitionsFacetDistribution
from .competitions_facet_stats import CompetitionsFacetStats
from .multi_search_result_competitions import CompetitionsMultiSearchResult


class CompetitionsMultiSearchQuery(MultiSearchQuery):
    def __init__(
        self,
        q: str | None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
    ):
        super().__init__(
            index_uid=MEILISEARCH_INDEX_COMPETITIONS,
            q=q,
            facets=MEILISEARCH_FACETS_COMPETITIONS,
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
        )

    def is_valid_result(self, result: MultiSearchResult):
        return result and (
            isinstance(result, CompetitionsMultiSearchResult)
            and (
                result.facet_distribution is None
                or isinstance(result.facet_distribution, CompetitionsFacetDistribution)
            )
            and (
                result.facet_stats is None
                or isinstance(result.facet_stats, CompetitionsFacetStats)
            )
        )
