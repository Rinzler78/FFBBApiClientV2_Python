from typing import List

from requests_cache import CachedSession

from .api_ffbb_app_client import ApiFFBBAppClient
from .http_requests_helper import default_cached_session
from .lives import Live
from .meilisearch_ffbb_client import MeilisearchFFBBClient
from .MultiSearchResultCompetitions import CompetitionsMultiSearchResult
from .MultiSearchResultOrganismes import OrganismesMultiSearchResult
from .MultiSearchResultPratiques import PratiquesMultiSearchResult
from .MultiSearchResultRencontres import RencontresMultiSearchResult
from .MultiSearchResultSalles import SallesMultiSearchResult
from .MultiSearchResultTerrains import TerrainsMultiSearchResult
from .MultiSearchResultTournois import TournoisMultiSearchResult


class FFBBAPIClientV2:
    def __init__(
        self,
        api_ffbb_client: ApiFFBBAppClient,
        meilisearch_ffbb_app_client_helper: MeilisearchFFBBClient,
    ):
        self.api_ffbb_client = api_ffbb_client
        self.meilisearch_ffbb_app_client = meilisearch_ffbb_app_client_helper

    @staticmethod
    def create(
        meilisearch_bearer_token: str,
        api_bearer_token: str,
        debug: bool = False,
        cached_session: CachedSession = default_cached_session,
    ):

        api_ffbb_client = ApiFFBBAppClient(
            api_bearer_token, debug=debug, cached_session=cached_session
        )
        meilisearch_ffbb_client: MeilisearchFFBBClient = MeilisearchFFBBClient(
            meilisearch_bearer_token, debug=debug, cached_session=cached_session
        )

        return FFBBAPIClientV2(api_ffbb_client, meilisearch_ffbb_client)

    def get_lives(self, cached_session: CachedSession = None) -> List[Live]:
        return self.api_ffbb_client.get_lives(cached_session)

    def search_organismes(
        self, name: str = None, cached_session: CachedSession = None
    ) -> OrganismesMultiSearchResult:
        return self.meilisearch_ffbb_app_client.search_organismes(name, cached_session)

    def search_multiple_organismes(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[OrganismesMultiSearchResult]:
        return self.meilisearch_ffbb_app_client.search_multiple_organismes(
            names, cached_session
        )

    def search_rencontres(
        self, name: str = None, cached_session: CachedSession = None
    ) -> RencontresMultiSearchResult:
        return self.meilisearch_ffbb_app_client.search_rencontres(name, cached_session)

    def search_multiple_rencontres(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[RencontresMultiSearchResult]:
        return self.meilisearch_ffbb_app_client.search_multiple_rencontres(
            names, cached_session
        )

    def search_terrains(
        self, name: str = None, cached_session: CachedSession = None
    ) -> TerrainsMultiSearchResult:
        return self.meilisearch_ffbb_app_client.search_terrains(name, cached_session)

    def search_multiple_terrains(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[TerrainsMultiSearchResult]:
        return self.meilisearch_ffbb_app_client.search_multiple_terrains(
            names, cached_session
        )

    def search_competitions(
        self, name: str = None, cached_session: CachedSession = None
    ) -> CompetitionsMultiSearchResult:
        return self.meilisearch_ffbb_app_client.search_competitions(
            name, cached_session
        )

    def search_multiple_competitions(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[CompetitionsMultiSearchResult]:
        return self.meilisearch_ffbb_app_client.search_multiple_competitions(
            names, cached_session
        )

    def search_salles(
        self, name: str = None, cached_session: CachedSession = None
    ) -> SallesMultiSearchResult:
        return self.meilisearch_ffbb_app_client.search_salles(name, cached_session)

    def search_multiple_salles(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[SallesMultiSearchResult]:
        return self.meilisearch_ffbb_app_client.search_multiple_salles(
            names, cached_session
        )

    def search_tournois(
        self, name: str = None, cached_session: CachedSession = None
    ) -> TournoisMultiSearchResult:
        return self.meilisearch_ffbb_app_client.search_tournois(name, cached_session)

    def search_multiple_tournois(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[TournoisMultiSearchResult]:
        return self.meilisearch_ffbb_app_client.search_multiple_tournois(
            names, cached_session
        )

    def search_pratiques(
        self, name: str = None, cached_session: CachedSession = None
    ) -> PratiquesMultiSearchResult:
        return self.meilisearch_ffbb_app_client.search_pratiques(name, cached_session)

    def search_multiple_pratiques(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[PratiquesMultiSearchResult]:
        return self.meilisearch_ffbb_app_client.search_multiple_pratiques(
            names, cached_session
        )
