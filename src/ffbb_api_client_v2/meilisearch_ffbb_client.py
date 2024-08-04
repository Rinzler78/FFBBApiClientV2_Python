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
from ffbb_api_client_v2.http_requests_helper import default_cached_session
from ffbb_api_client_v2.meilisearch_client_extension import MeilisearchClientExtension

from .multi_search_query import (
    CompetitionsMultiSearchQuery,
    OrganismesMultiSearchQuery,
    PratiquesMultiSearchQuery,
    RencontresMultiSearchQuery,
    SallesMultiSearchQuery,
    TerrainsMultiSearchQuery,
    TournoisMultiSearchQuery,
)


class MeilisearchFFBBClient(MeilisearchClientExtension):
    def __init__(
        self,
        bearer_token: str,
        url: str = "https://meilisearch-prod.ffbb.app/",
        debug: bool = False,
        cached_session: CachedSession = default_cached_session,
    ):
        super().__init__(bearer_token, url, debug, cached_session)

    def search_multiple_organismes(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResultOrganismes:
        if not names:
            return None

        queries = [OrganismesMultiSearchQuery(name) for name in names]
        results = self.recursive_multi_search(queries, cached_session)

        return results

    def search_organismes(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResultOrganismes:
        return self.search_multiple_organismes([name], cached_session)

    def search_multiple_rencontres(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResultRencontres:
        if not names:
            return None

        queries = [RencontresMultiSearchQuery(name) for name in names]
        return self.recursive_multi_search(queries, cached_session)

    def search_rencontres(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResultRencontres:
        return self.search_multiple_rencontres([name], cached_session)

    def search_multiple_terrains(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResultTerrains:
        if not names:
            return None

        queries = [TerrainsMultiSearchQuery(name) for name in names]
        return self.recursive_multi_search(queries, cached_session)

    def search_terrains(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResultTerrains:
        return self.search_multiple_terrains([name], cached_session)

    def search_multiple_competitions(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResultCompetitions:
        if not names:
            return None

        queries = [CompetitionsMultiSearchQuery(name) for name in names]
        return self.recursive_multi_search(queries, cached_session)

    def search_competitions(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResultCompetitions:
        return self.search_multiple_competitions([name], cached_session)

    def search_multiple_salles(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResultSalles:
        if not names:
            return None

        queries = [SallesMultiSearchQuery(name) for name in names]
        return self.recursive_multi_search(queries, cached_session)

    def search_salles(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResultSalles:
        return self.search_multiple_salles([name], cached_session)

    def search_multiple_tournois(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResultTournois:
        if not names:
            return None

        queries = [TournoisMultiSearchQuery(name) for name in names]
        return self.recursive_multi_search(queries, cached_session)

    def search_tournois(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResultTournois:
        return self.search_multiple_tournois([name], cached_session)

    def search_multiple_pratiques(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResultPratiques:
        if not names:
            return None

        queries = [PratiquesMultiSearchQuery(name) for name in names]
        return self.recursive_multi_search(queries, cached_session)

    def search_pratiques(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResultPratiques:
        return self.search_multiple_pratiques([name], cached_session)
