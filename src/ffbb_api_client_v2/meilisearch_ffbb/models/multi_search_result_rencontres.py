from __future__ import annotations

from ...meilisearch.models.multi_search_results import MultiSearchResult
from .competitions_facet_distribution import CompetitionsFacetDistribution
from .rencontres_facet_stats import RencontresFacetStats
from .rencontres_hit import RencontresHit


class RencontresMultiSearchResult(
    MultiSearchResult[
        RencontresHit, CompetitionsFacetDistribution, RencontresFacetStats
    ]
):
    """MultiSearchResult for Rencontres."""
