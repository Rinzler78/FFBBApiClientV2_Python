"""
FFBB API Client V2.

A Python client library for the French Basketball Federation (FFBB) API,
providing access to clubs, competitions, matches, and other basketball data.
"""

from .clients.api_ffbb_app_client import ApiFFBBAppClient
from .clients.ffbb_api_client_v2 import FFBBAPIClientV2
from .clients.meilisearch_client import MeilisearchClient
from .clients.meilisearch_ffbb_client import MeilisearchFFBBClient
from .helpers.meilisearch_client_extension import MeilisearchClientExtension
from .helpers.multi_search_query_helper import generate_queries
from .models.competitions_facet_distribution import CompetitionsFacetDistribution
from .models.competitions_facet_stats import CompetitionsFacetStats
from .models.competitions_hit import CompetitionsHit
from .models.engagements_facet_distribution import EngagementsFacetDistribution
from .models.engagements_facet_stats import EngagementsFacetStats
from .models.engagements_hit import EngagementsHit
from .models.field_set import FieldSet
from .models.formations_facet_distribution import FormationsFacetDistribution
from .models.formations_facet_stats import FormationsFacetStats
from .models.formations_hit import FormationsHit
from .models.meilisearch_index_settings import MeilisearchIndexSettings
from .models.multi_search_query import MultiSearchQuery
from .models.multi_search_result_competitions import CompetitionsMultiSearchResult
from .models.multi_search_result_engagements import EngagementsMultiSearchResult
from .models.multi_search_result_formations import FormationsMultiSearchResult
from .models.multi_search_result_organismes import OrganismesMultiSearchResult
from .models.multi_search_result_pratiques import PratiquesMultiSearchResult
from .models.multi_search_result_rencontres import RencontresMultiSearchResult
from .models.multi_search_result_salles import SallesMultiSearchResult
from .models.multi_search_result_terrains import TerrainsMultiSearchResult
from .models.multi_search_result_tournois import TournoisMultiSearchResult
from .models.organismes_facet_distribution import OrganismesFacetDistribution
from .models.organismes_facet_stats import OrganismesFacetStats
from .models.organismes_hit import OrganismesHit
from .models.pratiques_facet_distribution import PratiquesFacetDistribution
from .models.pratiques_facet_stats import PratiquesFacetStats
from .models.pratiques_hit import PratiquesHit
from .models.rencontres_facet_distribution import RencontresFacetDistribution
from .models.rencontres_facet_stats import RencontresFacetStats
from .models.rencontres_hit import RencontresHit
from .models.salles_facet_distribution import SallesFacetDistribution
from .models.salles_facet_stats import SallesFacetStats
from .models.salles_hit import SallesHit
from .models.terrains_facet_distribution import TerrainsFacetDistribution
from .models.terrains_facet_stats import TerrainsFacetStats
from .models.terrains_hit import TerrainsHit
from .models.tournois_facet_distribution import TournoisFacetDistribution
from .models.tournois_facet_stats import TournoisFacetStats
from .models.tournois_hit import TournoisHit
from .utils.token_manager import FFBBTokens, TokenManager

# Public API exports
__all__ = [
    # Clients
    "ApiFFBBAppClient",
    "FFBBAPIClientV2",
    "MeilisearchClient",
    "MeilisearchFFBBClient",
    # Helpers
    "MeilisearchClientExtension",
    "generate_queries",
    # Models
    "FieldSet",
    "MeilisearchIndexSettings",
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
    "RencontresFacetDistribution",
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
    "TournoisFacetDistribution",
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
