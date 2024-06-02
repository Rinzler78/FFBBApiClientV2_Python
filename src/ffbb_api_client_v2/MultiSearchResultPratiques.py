from typing import Any

from ffbb_api_client_v2.multi_search_result_pratiques import (
    PratiquesFacetDistribution,
    PratiquesFacetStats,
    PratiquesHit,
)

from .multi_search_results import MultiSearchResult


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
