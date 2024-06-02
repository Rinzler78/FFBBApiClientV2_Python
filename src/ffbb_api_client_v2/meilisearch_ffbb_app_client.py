from typing import List

from requests_cache import CachedSession

from .ffbb_api_client_helper import catch_result, default_cached_session
from .http_requests_utils import http_post_json
from .multi_search_query import (
    CompetitionsMultiSearchQuery,
    MultiSearchQuery,
    OrganismesMultiSearchQuery,
    RencontresMultiSearchQuery,
    TerrainsMultiSearchQuery,
)
from .MultiSearchResults import MultiSearchResults, multi_search_results_from_dict


class MeilisearchFFBBAPPClient:
    def __init__(
        self,
        bearer_token: str,
        url: str = "https://meilisearch-prod.ffbb.app/",
        debug: bool = False,
        cached_session: CachedSession = default_cached_session,
    ):
        """
        Initializes an instance of the ApiFFBBAppClient class.

        Args:
            bearer_token (str): The bearer token used for authentication.
            url (str, optional): The base URL. Defaults to "https://api.ffbb.app/".
            debug (bool, optional): Whether to enable debug mode. Defaults to False.
            cached_session (CachedSession, optional): The cached session to use.
        """
        self.bearer_token = bearer_token
        self.url = url
        self.debug = debug
        self.cached_session = cached_session
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
        }

    def multi_search(
        self,
        queries: List[MultiSearchQuery] = None,
        cached_session: CachedSession = None,
    ) -> MultiSearchResults:
        url = f"{self.url}multi-search"
        params = {"queries": [query.to_dict() for query in queries] if queries else []}
        result = catch_result(
            lambda: multi_search_results_from_dict(
                http_post_json(
                    url,
                    self.headers,
                    params,
                    debug=self.debug,
                    cached_session=cached_session or self.cached_session,
                )
            )
        )

        return result


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
