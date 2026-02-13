from __future__ import annotations

from ...meilisearch.models.multi_search_results import MultiSearchResult
from .terrains_facet_distribution import TerrainsFacetDistribution
from .terrains_facet_stats import TerrainsFacetStats
from .terrains_hit import TerrainsHit


class TerrainsMultiSearchResult(
    MultiSearchResult[TerrainsHit, TerrainsFacetDistribution, TerrainsFacetStats]
):
    """MultiSearchResult for Terrains."""
