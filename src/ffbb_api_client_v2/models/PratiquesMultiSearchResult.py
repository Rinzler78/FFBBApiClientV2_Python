from typing import Any

from .multi_search_result import MultiSearchResult
from .multi_search_result_pratiques import (
    PratiquesFacetDistribution,
    PratiquesFacetStats,
    PratiquesHit,
)


class PratiquesMultiSearchResult(
    MultiSearchResult[PratiquesHit, PratiquesFacetDistribution, PratiquesFacetStats]
):
    @staticmethod
    def from_dict(obj: Any) -> "PratiquesMultiSearchResult":
        return MultiSearchResult.from_dict(
            obj,
            PratiquesHit,
            PratiquesFacetDistribution,
            PratiquesFacetStats,
            PratiquesMultiSearchResult,
        )
