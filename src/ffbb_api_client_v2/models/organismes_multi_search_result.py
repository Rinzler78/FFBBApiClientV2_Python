from typing import Any

from .multi_search_result import MultiSearchResult
from .multi_search_result_organismes import (
    OrganismesFacetDistribution,
    OrganismesFacetStats,
    OrganismesHit,
)


class OrganismesMultiSearchResult(
    MultiSearchResult[OrganismesHit, OrganismesFacetDistribution, OrganismesFacetStats]
):
    @staticmethod
    def from_dict(obj: Any) -> "OrganismesMultiSearchResult":
        return MultiSearchResult.from_dict(
            obj,
            OrganismesHit,
            OrganismesFacetDistribution,
            OrganismesFacetStats,
            OrganismesMultiSearchResult,
        )
