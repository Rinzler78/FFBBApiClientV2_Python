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

from .meilisearch_ffbb_app_client import MeilisearchFFBBAPPClient
from .multi_search_query import (
    CompetitionsMultiSearchQuery,
    MultiSearchQuery,
    OrganismesMultiSearchQuery,
    PratiquesMultiSearchQuery,
    RencontresMultiSearchQuery,
    SallesMultiSearchQuery,
    TerrainsMultiSearchQuery,
    TournoisMultiSearchQuery,
)
from .MultiSearchResults import MultiSearchResults


class MeilisearchFFBBAPPClientHelper:
    def __init__(self, meilisearch_ffbb_app_client: MeilisearchFFBBAPPClient):
        self._meilisearch_ffbb_app_client = meilisearch_ffbb_app_client

    def recursive_multi_search(
        self,
        queries: List[MultiSearchQuery] = None,
        cached_session: CachedSession = None,
    ) -> MultiSearchResults:
        result = self._meilisearch_ffbb_app_client.multi_search(queries, cached_session)
        next_queries = []

        for i in range(len(result.results)):
            query_result = result.results[i]
            querie = queries[i]
            nb_hits = len(query_result.hits)

            if nb_hits < (query_result.estimated_total_hits - querie.offset):
                querie.offset += querie.limit
                querie.limit = query_result.estimated_total_hits - nb_hits
                next_queries.append(querie)

        if next_queries:
            new_result = self.recursive_multi_search(next_queries, cached_session)

            for i in range(len(new_result.results)):
                query_result = new_result.results[i]
                result.results[i].hits.extend(query_result.hits)
        return result

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
