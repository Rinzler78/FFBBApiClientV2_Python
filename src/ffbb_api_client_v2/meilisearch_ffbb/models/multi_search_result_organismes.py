from __future__ import annotations

from ...meilisearch.models.multi_search_results import MultiSearchResult
from .organismes_facet_distribution import OrganismesFacetDistribution
from .organismes_facet_stats import OrganismesFacetStats
from .organismes_hit import OrganismesHit


class OrganismesMultiSearchResult(
    MultiSearchResult[OrganismesHit, OrganismesFacetDistribution, OrganismesFacetStats]
):
    """MultiSearchResult for Organismes."""
