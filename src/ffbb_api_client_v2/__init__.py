from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

from .api_ffbb_app_client import ApiFFBBAppClient
from .ffbb_api_client_v2 import FFBBAPIClientV2
from .meilisearch_client import MeilisearchClient
from .meilisearch_client_extension import MeilisearchClientExtension
from .meilisearch_ffbb_client import MeilisearchFFBBClient
from .models.competitions_multi_search_result import (
    CompetitionsFacetDistribution,
    CompetitionsFacetStats,
    CompetitionsHit,
    CompetitionsMultiSearchResult,
)
from .models.multi_search_query import MultiSearchQuery
from .models.multi_search_query_helper import generate_queries
from .models.organismes_multi_search_result import (
    OrganismesFacetDistribution,
    OrganismesFacetStats,
    OrganismesHit,
    OrganismesMultiSearchResult,
)
from .models.pratiques_multi_search_result import (
    PratiquesFacetDistribution,
    PratiquesFacetStats,
    PratiquesHit,
    PratiquesMultiSearchResult,
)
from .models.rencontres_multi_search_result import (
    RencontresFacetDistribution,
    RencontresFacetStats,
    RencontresHit,
    RencontresMultiSearchResult,
)
from .models.salles_multi_search_result import (
    SallesFacetDistribution,
    SallesFacetStats,
    SallesHit,
    SallesMultiSearchResult,
)
from .models.terrains_multi_search_result import (
    TerrainsFacetDistribution,
    TerrainsFacetStats,
    TerrainsHit,
    TerrainsMultiSearchResult,
)
from .models.tournois_multi_search_result import (
    TournoisFacetDistribution,
    TournoisFacetStats,
    TournoisHit,
    TournoisMultiSearchResult,
)

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

# Liste des objets exportés (types/classes/fonctions)
EXPORTED_TYPES = [
    ApiFFBBAppClient,
    FFBBAPIClientV2,
    MeilisearchClient,
    MeilisearchClientExtension,
    MeilisearchFFBBClient,
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
