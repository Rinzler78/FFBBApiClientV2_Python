from typing import Any

from .multi_search_result_organismes import (
    OrganismesFacetDistribution,
    OrganismesFacetStats,
    OrganismesHit,
)
from .multi_search_results import MultiSearchResult


class MultiSearchResultOrganismes(
    MultiSearchResult[OrganismesHit, OrganismesFacetDistribution, OrganismesFacetStats]
):

    @staticmethod
    def from_dict(obj: Any) -> "MultiSearchResultOrganismes":
        return MultiSearchResult.from_dict(
            obj,
            OrganismesHit,
            OrganismesFacetDistribution,
            OrganismesFacetStats,
            MultiSearchResultOrganismes,
        )
