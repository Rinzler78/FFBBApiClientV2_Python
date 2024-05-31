from typing import Any

from ffbb_api_client_v2.multi_search_results import MultiSearchResult

from .multi_search_result_competitions import (
    CompetitionsFacetDistribution,
    CompetitionsFacetStats,
    CompetitionsHit,
)


class MultiSearchResultCompetitions(
    MultiSearchResult[
        CompetitionsHit, CompetitionsFacetDistribution, CompetitionsFacetStats
    ]
):

    @staticmethod
    def from_dict(obj: Any) -> "MultiSearchResultCompetitions":
        return MultiSearchResult.from_dict(
            obj,
            CompetitionsHit,
            CompetitionsFacetDistribution,
            CompetitionsFacetStats,
            MultiSearchResultCompetitions,
        )
