import sys

from .api_ffbb_app_client import ApiFFBBAppClient  # noqa
from .ffbb_api_client_v2 import FFBBAPIClientV2  # noqa
from .meilisearch_client import MeilisearchClient  # noqa
from .meilisearch_client_extension import MeilisearchClientExtension  # noqa
from .meilisearch_ffbb_client import MeilisearchFFBBClient  # noqa
from .multi_search_query import MultiSearchQuery  # noqa
from .multi_search_query_helper import generate_queries  # noqa
from .multi_search_result_competitions import CompetitionsFacetDistribution  # noqa
from .multi_search_result_competitions import CompetitionsFacetStats  # noqa
from .multi_search_result_competitions import CompetitionsHit  # noqa
from .multi_search_result_organismes import OrganismesFacetDistribution  # noqa
from .multi_search_result_organismes import OrganismesFacetStats  # noqa
from .multi_search_result_organismes import OrganismesHit  # noqa
from .multi_search_result_pratiques import PratiquesFacetDistribution  # noqa
from .multi_search_result_pratiques import PratiquesFacetStats  # noqa
from .multi_search_result_pratiques import PratiquesHit  # noqa
from .multi_search_result_rencontres import RencontresFacetDistribution  # noqa
from .multi_search_result_rencontres import RencontresFacetStats  # noqa
from .multi_search_result_rencontres import RencontresHit  # noqa
from .multi_search_result_salles import SallesFacetDistribution  # noqa
from .multi_search_result_salles import SallesFacetStats  # noqa
from .multi_search_result_salles import SallesHit  # noqa
from .multi_search_result_terrains import TerrainsFacetDistribution  # noqa
from .multi_search_result_terrains import TerrainsFacetStats  # noqa
from .multi_search_result_terrains import TerrainsHit  # noqa
from .multi_search_result_tournois import TournoisFacetDistribution  # noqa
from .multi_search_result_tournois import TournoisFacetStats  # noqa
from .multi_search_result_tournois import TournoisHit  # noqa
from .MultiSearchResultCompetitions import CompetitionsMultiSearchResult  # noqa
from .MultiSearchResultOrganismes import OrganismesMultiSearchResult  # noqa
from .MultiSearchResultPratiques import PratiquesMultiSearchResult  # noqa
from .MultiSearchResultRencontres import RencontresMultiSearchResult  # noqa
from .MultiSearchResultSalles import SallesMultiSearchResult  # noqa
from .MultiSearchResultTerrains import TerrainsMultiSearchResult  # noqa
from .MultiSearchResultTournois import TournoisMultiSearchResult  # noqa

if sys.version_info[:2] >= (3, 8):
    # T-238 Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "ffbb_api_client_v2"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
