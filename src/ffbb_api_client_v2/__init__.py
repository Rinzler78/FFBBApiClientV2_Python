"""
FFBB API Client V2.

A Python client library for the French Basketball Federation (FFBB) API,
providing access to clubs, competitions, matches, and other basketball data.
"""

from .directus.exceptions import (
    DirectusAuthError,
    DirectusError,
    DirectusNotFoundError,
    DirectusRateLimitError,
    DirectusServerError,
)
from .directus.models.field_set import FieldSet
from .directus_ffbb.client import ApiFFBBAppClient
from .directus_ffbb.models.get_communes_response import GetCommunesResponse
from .directus_ffbb.models.get_engagements_response import GetEngagementsResponse
from .directus_ffbb.models.get_entraineurs_response import GetEntraineursResponse
from .directus_ffbb.models.get_formations_response import GetFormationsResponse
from .directus_ffbb.models.get_officiels_response import GetOfficielsResponse
from .directus_ffbb.models.get_pratiques_response import GetPratiquesResponse
from .directus_ffbb.models.get_rencontres_response import GetRencontresResponse
from .directus_ffbb.models.get_salles_response import GetSallesResponse
from .directus_ffbb.models.get_terrains_response import GetTerrainsResponse
from .directus_ffbb.models.get_tournois_response import GetTournoisResponse
from .exceptions import (
    FFBBApiError,
    FFBBAuthError,
    FFBBNetworkError,
    FFBBNotFoundError,
    FFBBRateLimitError,
    FFBBServerError,
    FFBBValidationError,
)
from .facade.client import FFBBAPIClientV2
from .facade.token_manager import FFBBTokens, TokenManager
from .meilisearch.client import MeilisearchClient
from .meilisearch.client_extension import MeilisearchClientExtension
from .meilisearch.exceptions import (
    MeilisearchError,
    MeilisearchIndexNotFoundError,
    MeilisearchInvalidFilterError,
)
from .meilisearch.models.federated_search_result import (
    FederatedHit,
    FederatedSearchResult,
    FederationInfo,
)
from .meilisearch.models.meilisearch_index_settings import MeilisearchIndexSettings
from .meilisearch.models.multi_search_query import MultiSearchQuery
from .meilisearch_ffbb.client import MeilisearchFFBBClient
from .meilisearch_ffbb.geo_sort_order import GeoSortOrder
from .meilisearch_ffbb.models.competitions_facet_distribution import (
    CompetitionsFacetDistribution,
)
from .meilisearch_ffbb.models.competitions_facet_stats import CompetitionsFacetStats
from .meilisearch_ffbb.models.competitions_hit import CompetitionsHit
from .meilisearch_ffbb.models.engagements_facet_distribution import (
    EngagementsFacetDistribution,
)
from .meilisearch_ffbb.models.engagements_facet_stats import EngagementsFacetStats
from .meilisearch_ffbb.models.engagements_hit import EngagementsHit
from .meilisearch_ffbb.models.formations_facet_distribution import (
    FormationsFacetDistribution,
)
from .meilisearch_ffbb.models.formations_facet_stats import FormationsFacetStats
from .meilisearch_ffbb.models.formations_hit import FormationsHit
from .meilisearch_ffbb.models.multi_search_result_competitions import (
    CompetitionsMultiSearchResult,
)
from .meilisearch_ffbb.models.multi_search_result_engagements import (
    EngagementsMultiSearchResult,
)
from .meilisearch_ffbb.models.multi_search_result_formations import (
    FormationsMultiSearchResult,
)
from .meilisearch_ffbb.models.multi_search_result_organismes import (
    OrganismesMultiSearchResult,
)
from .meilisearch_ffbb.models.multi_search_result_pratiques import (
    PratiquesMultiSearchResult,
)
from .meilisearch_ffbb.models.multi_search_result_rencontres import (
    RencontresMultiSearchResult,
)
from .meilisearch_ffbb.models.multi_search_result_salles import SallesMultiSearchResult
from .meilisearch_ffbb.models.multi_search_result_terrains import (
    TerrainsMultiSearchResult,
)
from .meilisearch_ffbb.models.multi_search_result_tournois import (
    TournoisMultiSearchResult,
)
from .meilisearch_ffbb.models.organismes_facet_distribution import (
    OrganismesFacetDistribution,
)
from .meilisearch_ffbb.models.organismes_facet_stats import OrganismesFacetStats
from .meilisearch_ffbb.models.organismes_hit import OrganismesHit
from .meilisearch_ffbb.models.pratiques_facet_distribution import (
    PratiquesFacetDistribution,
)
from .meilisearch_ffbb.models.pratiques_facet_stats import PratiquesFacetStats
from .meilisearch_ffbb.models.pratiques_hit import PratiquesHit
from .meilisearch_ffbb.models.rencontres_facet_stats import RencontresFacetStats
from .meilisearch_ffbb.models.rencontres_hit import RencontresHit
from .meilisearch_ffbb.models.salles_facet_distribution import SallesFacetDistribution
from .meilisearch_ffbb.models.salles_facet_stats import SallesFacetStats
from .meilisearch_ffbb.models.salles_hit import SallesHit
from .meilisearch_ffbb.models.terrains_facet_distribution import (
    TerrainsFacetDistribution,
)
from .meilisearch_ffbb.models.terrains_facet_stats import TerrainsFacetStats
from .meilisearch_ffbb.models.terrains_hit import TerrainsHit
from .meilisearch_ffbb.models.tournois_facet_stats import TournoisFacetStats
from .meilisearch_ffbb.models.tournois_hit import TournoisHit
from .meilisearch_ffbb.query_helper import generate_queries
from .models.club_contacts import ClubContacts
from .models.contact_info import ContactInfo
from .models.engagement_contacts import EngagementContacts

# Public API exports
__all__ = [
    # Clients
    "ApiFFBBAppClient",
    "FFBBAPIClientV2",
    "MeilisearchClient",
    "MeilisearchFFBBClient",
    # Exceptions
    "FFBBApiError",
    "FFBBNetworkError",
    "FFBBAuthError",
    "FFBBNotFoundError",
    "FFBBRateLimitError",
    "FFBBValidationError",
    "FFBBServerError",
    "DirectusError",
    "DirectusAuthError",
    "DirectusNotFoundError",
    "DirectusRateLimitError",
    "DirectusServerError",
    "MeilisearchError",
    "MeilisearchIndexNotFoundError",
    "MeilisearchInvalidFilterError",
    # Helpers
    "MeilisearchClientExtension",
    "generate_queries",
    # Geo
    "GeoSortOrder",
    # Models
    "ClubContacts",
    "ContactInfo",
    "EngagementContacts",
    "FieldSet",
    "MeilisearchIndexSettings",
    # Federated search
    "FederatedSearchResult",
    "FederatedHit",
    "FederationInfo",
    # Directus Response Models
    "GetCommunesResponse",
    "GetEngagementsResponse",
    "GetEntraineursResponse",
    "GetFormationsResponse",
    "GetOfficielsResponse",
    "GetPratiquesResponse",
    "GetRencontresResponse",
    "GetSallesResponse",
    "GetTerrainsResponse",
    "GetTournoisResponse",
    # Query
    "MultiSearchQuery",
    # Engagements
    "EngagementsFacetDistribution",
    "EngagementsFacetStats",
    "EngagementsHit",
    "EngagementsMultiSearchResult",
    # Formations
    "FormationsFacetDistribution",
    "FormationsFacetStats",
    "FormationsHit",
    "FormationsMultiSearchResult",
    # Competitions
    "CompetitionsFacetDistribution",
    "CompetitionsFacetStats",
    "CompetitionsHit",
    "CompetitionsMultiSearchResult",
    # Organismes
    "OrganismesFacetDistribution",
    "OrganismesFacetStats",
    "OrganismesHit",
    "OrganismesMultiSearchResult",
    # Pratiques
    "PratiquesFacetDistribution",
    "PratiquesFacetStats",
    "PratiquesHit",
    "PratiquesMultiSearchResult",
    # Rencontres
    "RencontresFacetStats",
    "RencontresHit",
    "RencontresMultiSearchResult",
    # Salles
    "SallesFacetDistribution",
    "SallesFacetStats",
    "SallesHit",
    "SallesMultiSearchResult",
    # Terrains
    "TerrainsFacetDistribution",
    "TerrainsFacetStats",
    "TerrainsHit",
    "TerrainsMultiSearchResult",
    # Tournois
    "TournoisFacetStats",
    "TournoisHit",
    "TournoisMultiSearchResult",
    # Token management
    "FFBBTokens",
    "TokenManager",
]

from importlib.metadata import PackageNotFoundError, version

try:
    DIST_NAME = __name__
    __version__ = version(DIST_NAME)
except PackageNotFoundError:
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
