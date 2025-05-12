"""
Models package for ffbb_api_client_v2
"""

from .CompetitionsMultiSearchResult import (
    CompetitionsFacetDistribution,
    CompetitionsFacetStats,
    CompetitionsHit,
    CompetitionsMultiSearchResult,
)
from .multi_search_query import MultiSearchQuery
from .multi_search_query_helper import generate_queries
from .OrganismesMultiSearchResult import (
    OrganismesFacetDistribution,
    OrganismesFacetStats,
    OrganismesHit,
    OrganismesMultiSearchResult,
)
from .PratiquesMultiSearchResult import (
    PratiquesFacetDistribution,
    PratiquesFacetStats,
    PratiquesHit,
    PratiquesMultiSearchResult,
)
from .RencontresMultiSearchResult import (
    RencontresFacetDistribution,
    RencontresFacetStats,
    RencontresHit,
    RencontresMultiSearchResult,
)
from .SallesMultiSearchResult import (
    SallesFacetDistribution,
    SallesFacetStats,
    SallesHit,
    SallesMultiSearchResult,
)
from .TerrainsMultiSearchResult import (
    TerrainsFacetDistribution,
    TerrainsFacetStats,
    TerrainsHit,
    TerrainsMultiSearchResult,
)
from .TournoisMultiSearchResult import (
    TournoisFacetDistribution,
    TournoisFacetStats,
    TournoisHit,
    TournoisMultiSearchResult,
)

# Liste des objets exportés (types/classes/fonctions)
EXPORTED_TYPES = [
    MultiSearchQuery,
    generate_queries,
    CompetitionsFacetDistribution,
    CompetitionsFacetStats,
    CompetitionsHit,
    CompetitionsMultiSearchResult,
    OrganismesFacetDistribution,
    OrganismesFacetStats,
    OrganismesHit,
    OrganismesMultiSearchResult,
    PratiquesFacetDistribution,
    PratiquesFacetStats,
    PratiquesHit,
    PratiquesMultiSearchResult,
    RencontresFacetDistribution,
    RencontresFacetStats,
    RencontresHit,
    RencontresMultiSearchResult,
    SallesFacetDistribution,
    SallesFacetStats,
    SallesHit,
    SallesMultiSearchResult,
    TerrainsFacetDistribution,
    TerrainsFacetStats,
    TerrainsHit,
    TerrainsMultiSearchResult,
    TournoisFacetDistribution,
    TournoisFacetStats,
    TournoisHit,
    TournoisMultiSearchResult,
]

__all__ = [typ.__name__ for typ in EXPORTED_TYPES]
