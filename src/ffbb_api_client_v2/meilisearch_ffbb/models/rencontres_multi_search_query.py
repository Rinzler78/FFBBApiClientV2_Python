from __future__ import annotations

from ...meilisearch.models.multi_search_query import MultiSearchQuery
from ...meilisearch.models.multi_search_results import MultiSearchResult
from ..config import MEILISEARCH_FACETS_RENCONTRES, MEILISEARCH_INDEX_RENCONTRES
from .competitions_facet_distribution import CompetitionsFacetDistribution
from .multi_search_result_rencontres import RencontresMultiSearchResult
from .rencontres_facet_stats import RencontresFacetStats


class RencontresMultiSearchQuery(MultiSearchQuery):
    def __init__(
        self,
        q: str | None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
    ):
        super().__init__(
            index_uid=MEILISEARCH_INDEX_RENCONTRES,
            q=q,
            facets=MEILISEARCH_FACETS_RENCONTRES,
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
        )

    def is_valid_result(self, result: MultiSearchResult):
        return result and (
            isinstance(result, RencontresMultiSearchResult)
            and (
                result.facet_distribution is None
                or isinstance(result.facet_distribution, CompetitionsFacetDistribution)
            )
            and (
                result.facet_stats is None
                or isinstance(result.facet_stats, RencontresFacetStats)
            )
        )
