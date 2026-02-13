from __future__ import annotations

from ...meilisearch.models.multi_search_results import MultiSearchResult
from .terrains_facet_distribution import TerrainsFacetDistribution
from .tournois_facet_stats import TournoisFacetStats
from .tournois_hit import TournoisHit


class TournoisMultiSearchResult(
    MultiSearchResult[TournoisHit, TerrainsFacetDistribution, TournoisFacetStats]
):
    """MultiSearchResult for Tournois."""
