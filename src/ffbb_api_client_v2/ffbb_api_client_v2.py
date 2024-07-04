from typing import List

from requests_cache import CachedSession

from ffbb_api_client_v2 import (
    MultiSearchResultCompetitions,
    MultiSearchResultOrganismes,
    MultiSearchResultPratiques,
    MultiSearchResultRencontres,
    MultiSearchResultSalles,
    MultiSearchResultTerrains,
    MultiSearchResultTournois,
)
from ffbb_api_client_v2.lives import Live

from .api_ffbb_app_client import ApiFFBBAppClient
from .meilisearch_ffbb_app_client_helper import MeilisearchFFBBAPPClientHelper


class FFBBAPIClientV2:
    def __init__(
        self,
        api_ffbb_client: ApiFFBBAppClient,
        meilisearch_ffbb_app_client_helper: MeilisearchFFBBAPPClientHelper,
    ):
        self.api_ffbb_client = api_ffbb_client
        self.meilisearch_ffbb_app_client = meilisearch_ffbb_app_client_helper

    def get_lives(self, cached_session: CachedSession = None) -> List[Live]:
        return self.api_ffbb_client.get_lives(cached_session)

    def search_organismes(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResultOrganismes:
        return self.meilisearch_ffbb_app_client.search_organismes(name, cached_session)

    def search_multiple_organismes(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResultOrganismes:
        return self.meilisearch_ffbb_app_client.search_multiple_organismes(
            names, cached_session
        )

    def search_rencontres(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResultRencontres:
        return self.meilisearch_ffbb_app_client.search_rencontres(name, cached_session)

    def search_multiple_rencontres(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResultRencontres:
        return self.meilisearch_ffbb_app_client.search_multiple_rencontres(
            names, cached_session
        )

    def search_terrains(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResultTerrains:
        return self.meilisearch_ffbb_app_client.search_terrains(name, cached_session)

    def search_multiple_terrains(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResultTerrains:
        return self.meilisearch_ffbb_app_client.search_multiple_terrains(
            names, cached_session
        )

    def search_competitions(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResultCompetitions:
        return self.meilisearch_ffbb_app_client.search_competitions(
            name, cached_session
        )

    def search_multiple_competitions(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResultCompetitions:
        return self.meilisearch_ffbb_app_client.search_multiple_competitions(
            names, cached_session
        )

    def search_salles(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResultSalles:
        return self.meilisearch_ffbb_app_client.search_salles(name, cached_session)

    def search_multiple_salles(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResultSalles:
        return self.meilisearch_ffbb_app_client.search_multiple_salles(
            names, cached_session
        )

    def search_tournois(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResultTournois:
        return self.meilisearch_ffbb_app_client.search_tournois(name, cached_session)

    def search_multiple_tournois(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResultTournois:
        return self.meilisearch_ffbb_app_client.search_multiple_tournois(
            names, cached_session
        )

    def search_pratiques(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResultPratiques:
        return self.meilisearch_ffbb_app_client.search_pratiques(name, cached_session)

    def search_multiple_pratiques(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResultPratiques:
        return self.meilisearch_ffbb_app_client.search_multiple_pratiques(
            names, cached_session
        )
