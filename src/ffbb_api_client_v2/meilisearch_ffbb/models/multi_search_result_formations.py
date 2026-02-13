from __future__ import annotations

from ...meilisearch.models.multi_search_results import MultiSearchResult
from .formations_facet_distribution import FormationsFacetDistribution
from .formations_facet_stats import FormationsFacetStats
from .formations_hit import FormationsHit


class FormationsMultiSearchResult(
    MultiSearchResult[FormationsHit, FormationsFacetDistribution, FormationsFacetStats]
):
    """MultiSearchResult for Formations."""
