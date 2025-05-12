from typing import Any

from .multi_search_result_rencontres import (
    RencontresFacetDistribution,
    RencontresFacetStats,
    RencontresHit,
)
from .multi_search_results import MultiSearchResult


class RencontresMultiSearchResult(
    MultiSearchResult[RencontresHit, RencontresFacetDistribution, RencontresFacetStats]
):
    @staticmethod
    def from_dict(obj: Any) -> "RencontresMultiSearchResult":
        return MultiSearchResult.from_dict(
            obj,
            RencontresHit,
            RencontresFacetDistribution,
            RencontresFacetStats,
            RencontresMultiSearchResult,
        )
