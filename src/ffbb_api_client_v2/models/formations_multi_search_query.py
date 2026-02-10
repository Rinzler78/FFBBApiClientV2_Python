from __future__ import annotations

from ..config import MEILISEARCH_FACETS_FORMATIONS, MEILISEARCH_INDEX_FORMATIONS
from .formations_facet_distribution import FormationsFacetDistribution
from .formations_facet_stats import FormationsFacetStats
from .multi_search_query import MultiSearchQuery
from .multi_search_result_formations import FormationsMultiSearchResult
from .multi_search_results import MultiSearchResult


class FormationsMultiSearchQuery(MultiSearchQuery):
    def __init__(
        self,
        q: str | None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
    ):
        super().__init__(
            index_uid=MEILISEARCH_INDEX_FORMATIONS,
            q=q,
            facets=MEILISEARCH_FACETS_FORMATIONS,
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
        )

    def is_valid_result(self, result: MultiSearchResult):
        return result and (
            isinstance(result, FormationsMultiSearchResult)
            and (
                result.facet_distribution is None
                or isinstance(result.facet_distribution, FormationsFacetDistribution)
            )
            and (
                result.facet_stats is None
                or isinstance(result.facet_stats, FormationsFacetStats)
            )
        )
