from __future__ import annotations

from ...meilisearch.models.multi_search_results import MultiSearchResult
from .engagements_facet_distribution import EngagementsFacetDistribution
from .engagements_facet_stats import EngagementsFacetStats
from .engagements_hit import EngagementsHit


class EngagementsMultiSearchResult(
    MultiSearchResult[
        EngagementsHit, EngagementsFacetDistribution, EngagementsFacetStats
    ]
):
    """MultiSearchResult for Engagements."""
