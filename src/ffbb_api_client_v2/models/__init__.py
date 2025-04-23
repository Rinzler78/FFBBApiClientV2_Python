"""
Models package for ffbb_api_client_v2
"""

from .multi_search_query import MultiSearchQuery
from .multi_search_query_helper import generate_queries
from .MultiSearchResultCompetitions import (
    CompetitionsFacetDistribution,
    CompetitionsFacetStats,
    CompetitionsHit,
    CompetitionsMultiSearchResult,
)
from .MultiSearchResultOrganismes import (
    OrganismesFacetDistribution,
    OrganismesFacetStats,
    OrganismesHit,
    OrganismesMultiSearchResult,
)
from .MultiSearchResultPratiques import (
    PratiquesFacetDistribution,
    PratiquesFacetStats,
    PratiquesHit,
    PratiquesMultiSearchResult,
)
from .MultiSearchResultRencontres import (
    RencontresFacetDistribution,
    RencontresFacetStats,
    RencontresHit,
    RencontresMultiSearchResult,
)
from .MultiSearchResultSalles import (
    SallesFacetDistribution,
    SallesFacetStats,
    SallesHit,
    SallesMultiSearchResult,
)
from .MultiSearchResultTerrains import (
    TerrainsFacetDistribution,
    TerrainsFacetStats,
    TerrainsHit,
    TerrainsMultiSearchResult,
)
from .MultiSearchResultTournois import (
    TournoisFacetDistribution,
    TournoisFacetStats,
    TournoisHit,
    TournoisMultiSearchResult,
)

__all__ = [
    "MultiSearchQuery",
    "generate_queries",
    "CompetitionsFacetDistribution",
    "CompetitionsFacetStats",
    "CompetitionsHit",
    "CompetitionsMultiSearchResult",
    "OrganismesFacetDistribution",
    "OrganismesFacetStats",
    "OrganismesHit",
    "OrganismesMultiSearchResult",
    "PratiquesFacetDistribution",
    "PratiquesFacetStats",
    "PratiquesHit",
    "PratiquesMultiSearchResult",
    "RencontresFacetDistribution",
    "RencontresFacetStats",
    "RencontresHit",
    "RencontresMultiSearchResult",
    "SallesFacetDistribution",
    "SallesFacetStats",
    "SallesHit",
    "SallesMultiSearchResult",
    "TerrainsFacetDistribution",
    "TerrainsFacetStats",
    "TerrainsHit",
    "TerrainsMultiSearchResult",
    "TournoisFacetDistribution",
    "TournoisFacetStats",
    "TournoisHit",
    "TournoisMultiSearchResult",
]
