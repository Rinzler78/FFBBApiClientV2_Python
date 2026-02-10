from __future__ import annotations

from .engagements_facet_distribution import EngagementsFacetDistribution
from .engagements_facet_stats import EngagementsFacetStats
from .engagements_hit import EngagementsHit
from .multi_search_results import MultiSearchResult


class EngagementsMultiSearchResult(
    MultiSearchResult[
        EngagementsHit, EngagementsFacetDistribution, EngagementsFacetStats
    ]
):
    """MultiSearchResult for Engagements."""
