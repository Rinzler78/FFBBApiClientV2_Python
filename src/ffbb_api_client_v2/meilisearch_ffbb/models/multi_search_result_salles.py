from __future__ import annotations

from ...meilisearch.models.multi_search_results import MultiSearchResult
from .salles_facet_distribution import SallesFacetDistribution
from .salles_facet_stats import SallesFacetStats
from .salles_hit import SallesHit


class SallesMultiSearchResult(
    MultiSearchResult[SallesHit, SallesFacetDistribution, SallesFacetStats]
):
    """MultiSearchResult for Salles."""
