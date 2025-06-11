"""Public API exports for :mod:`ffbb_api_client_v2`."""

from importlib.metadata import PackageNotFoundError, version

from dotenv import load_dotenv

from .api_ffbb_app_client import ApiFFBBAppClient
from .ffbb_api_client_v2 import FFBBAPIClientV2
from .helpers import (
    catch_result,
    create_cache_key,
    default_cached_session,
    encode_params,
    generate_queries,
    http_get,
    http_get_json,
    http_post,
    http_post_json,
    to_json_from_response,
    url_with_params,
)
from .meilisearch_client import MeilisearchClient
from .meilisearch_client_extension import MeilisearchClientExtension
from .meilisearch_ffbb_client import MeilisearchFFBBClient
from .models import (
    CompetitionsFacetDistribution,
    CompetitionsFacetStats,
    CompetitionsHit,
    CompetitionsMultiSearchResult,
    MultiSearchQuery,
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
)
from .utils import (
    from_bool,
    from_datetime,
    from_float,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
    to_enum,
    to_float,
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

__all__ = [
    "ApiFFBBAppClient",
    "FFBBAPIClientV2",
    "MeilisearchClient",
    "MeilisearchClientExtension",
    "MeilisearchFFBBClient",
    "catch_result",
    "create_cache_key",
    "default_cached_session",
    "encode_params",
    "generate_queries",
    "http_get",
    "http_get_json",
    "http_post",
    "http_post_json",
    "to_json_from_response",
    "url_with_params",
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
    "CompetitionsFacetDistribution",
    "CompetitionsFacetStats",
    "CompetitionsHit",
    "CompetitionsMultiSearchResult",
    "MultiSearchQuery",
    "from_bool",
    "from_datetime",
    "from_float",
    "from_int",
    "from_list",
    "from_none",
    "from_str",
    "from_union",
    "is_type",
    "to_class",
    "to_enum",
    "to_float",
]

load_dotenv()
