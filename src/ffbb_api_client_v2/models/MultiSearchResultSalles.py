from typing import Any

from .multi_search_result_salles import (
    SallesFacetDistribution,
    SallesFacetStats,
    SallesHit,
)
from .multi_search_results import MultiSearchResult


class SallesMultiSearchResult(
    MultiSearchResult[SallesHit, SallesFacetDistribution, SallesFacetStats]
):
    @staticmethod
    def from_dict(obj: Any) -> "SallesMultiSearchResult":
        return MultiSearchResult.from_dict(
            obj,
            SallesHit,
            SallesFacetDistribution,
            SallesFacetStats,
            SallesMultiSearchResult,
        )
