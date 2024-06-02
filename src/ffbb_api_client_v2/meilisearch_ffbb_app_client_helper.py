from typing import List

from requests_cache import CachedSession

from ffbb_api_client_v2.api_ffbb_app_client_helper import default_cached_session
from ffbb_api_client_v2.meilisearch_ffbb_app_client import MeilisearchFFBBAPPClient
from ffbb_api_client_v2.multi_search_query import (
    CompetitionsMultiSearchQuery,
    MultiSearchQuery,
    OrganismesMultiSearchQuery,
    PratiquesMultiSearchQuery,
    RencontresMultiSearchQuery,
    SallesMultiSearchQuery,
    TerrainsMultiSearchQuery,
    TournoisMultiSearchQuery,
)
from ffbb_api_client_v2.MultiSearchResults import MultiSearchResults


class MeilisearchFFBBAPPClientHelper:
    def __init__(
        self,
        bearer_token: str,
        url: str = "https://meilisearch-prod.ffbb.app/",
        debug: bool = False,
        cached_session: CachedSession = default_cached_session,
    ):

        self._meilisearch_ffbb_app_client = MeilisearchFFBBAPPClient(
            bearer_token, url, debug, cached_session
        )

    def multi_search(
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
            new_result = self.multi_search(next_queries, cached_session)

            for i in range(len(new_result.results)):
                query_result = new_result.results[i]
                result.results[i].hits.extend(query_result.hits)
        return result

    def search_multiple_organismes(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResults:
        if not names:
            return None

        queries = [OrganismesMultiSearchQuery(name) for name in names]
        return self.multi_search(queries, cached_session)

    def search_organismes(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResults:
        return self.search_multiple_organismes([name], cached_session)

    def search_multiple_rencontres(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResults:
        if not names:
            return None

        queries = [RencontresMultiSearchQuery(name) for name in names]
        return self.multi_search(queries, cached_session)

    def search_rencontres(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResults:
        return self.search_multiple_rencontres([name], cached_session)

    def search_multiple_terrains(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResults:
        if not names:
            return None

        queries = [TerrainsMultiSearchQuery(name) for name in names]
        return self.multi_search(queries, cached_session)

    def search_terrains(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResults:
        return self.search_multiple_terrains([name], cached_session)

    def search_multiple_competitions(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResults:
        if not names:
            return None

        queries = [CompetitionsMultiSearchQuery(name) for name in names]
        return self.multi_search(queries, cached_session)

    def search_competitions(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResults:
        return self.search_multiple_competitions([name], cached_session)

    def search_multiple_salles(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResults:
        if not names:
            return None

        queries = [SallesMultiSearchQuery(name) for name in names]
        return self.multi_search(queries, cached_session)

    def search_salles(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResults:
        return self.search_multiple_salles([name], cached_session)

    def search_multiple_tournois(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResults:
        if not names:
            return None

        queries = [TournoisMultiSearchQuery(name) for name in names]
        return self.multi_search(queries, cached_session)

    def search_tournois(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResults:
        return self.search_multiple_tournois([name], cached_session)

    def search_multiple_pratiques(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> MultiSearchResults:
        if not names:
            return None

        queries = [PratiquesMultiSearchQuery(name) for name in names]
        return self.multi_search(queries, cached_session)

    def search_pratiques(
        self, name: str = None, cached_session: CachedSession = None
    ) -> MultiSearchResults:
        return self.search_multiple_pratiques([name], cached_session)
