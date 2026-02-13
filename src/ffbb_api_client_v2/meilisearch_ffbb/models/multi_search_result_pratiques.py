from __future__ import annotations

from ...meilisearch.models.multi_search_results import MultiSearchResult
from .pratiques_facet_distribution import PratiquesFacetDistribution
from .pratiques_facet_stats import PratiquesFacetStats
from .pratiques_hit import PratiquesHit


class PratiquesMultiSearchResult(
    MultiSearchResult[PratiquesHit, PratiquesFacetDistribution, PratiquesFacetStats]
):
    """MultiSearchResult for Pratiques."""
