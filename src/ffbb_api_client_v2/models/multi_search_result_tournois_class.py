from typing import Any

from .multi_search_result_tournois import (
    TournoisFacetDistribution,
    TournoisFacetStats,
    TournoisHit,
)
from .multi_search_results import MultiSearchResult


class TournoisMultiSearchResult(
    MultiSearchResult[TournoisHit, TournoisFacetDistribution, TournoisFacetStats]
):
    @staticmethod
    def from_dict(obj: Any) -> "TournoisMultiSearchResult":
        return MultiSearchResult.from_dict(
            obj,
            TournoisHit,
            TournoisFacetDistribution,
            TournoisFacetStats,
            TournoisMultiSearchResult,
        )
