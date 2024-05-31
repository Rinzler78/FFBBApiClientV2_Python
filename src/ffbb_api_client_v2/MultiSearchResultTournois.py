from typing import Any

from .multi_search_result_tournois import (
    TournoisFacetDistribution,
    TournoisFacetStats,
    TournoisHit,
)
from .multi_search_results import MultiSearchResult


class MultiSearchResultTournois(
    MultiSearchResult[TournoisHit, TournoisFacetDistribution, TournoisFacetStats]
):

    @staticmethod
    def from_dict(obj: Any) -> "MultiSearchResultTournois":
        return MultiSearchResult.from_dict(
            obj,
            TournoisHit,
            TournoisFacetDistribution,
            TournoisFacetStats,
            MultiSearchResultTournois,
        )
