from typing import Any

from .multi_search_result import MultiSearchResult
from .multi_search_result_competitions import (
    CompetitionsFacetDistribution,
    CompetitionsFacetStats,
    CompetitionsHit,
)


class CompetitionsMultiSearchResult(
    MultiSearchResult[
        CompetitionsHit, CompetitionsFacetDistribution, CompetitionsFacetStats
    ]
):
    @staticmethod
    def from_dict(obj: Any) -> "CompetitionsMultiSearchResult":
        return MultiSearchResult.from_dict(
            obj,
            CompetitionsHit,
            CompetitionsFacetDistribution,
            CompetitionsFacetStats,
            CompetitionsMultiSearchResult,
        )
