from typing import List

from requests_cache import CachedSession

from ffbb_api_client_v2.Result import QueryResult

from .ffbb_api_client_helper import catch_result, default_cached_session
from .http_requests_utils import http_post_json
from .multi_search_query import (
    MultiSearchQuery,
    OrganismesMultiSearchQuery,
    RencontresMultiSearchQuery,
)
from .multi_search_results import MultiSearchResults, multi_search_results_from_dict


class MeilisearchProdFFBBAPPClient:
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

    def __multi_search(
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

    def multi_search(
        self,
        queries: List[MultiSearchQuery] = None,
        cached_session: CachedSession = None,
    ) -> MultiSearchResults:
        result = self.__multi_search(queries, cached_session)
        next_queries = []

        for i in range(len(result.results)):
            query_result = result.results[i]
            querie = queries[i]
            query_result.hits.sort(key=lambda x: x.nom)
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
                result.results[i].hits.sort(key=lambda x: x.nom)
        return result

    def search_multiple_organismes(self, names: List[str] = None) -> List[QueryResult]:
        if not names:
            return None

        queries = [OrganismesMultiSearchQuery(name) for name in names]
        return self.multi_search(queries).results

    def search_organismes(self, name: str = None) -> QueryResult:
        return self.search_multiple_organismes([name])

    def search_multiple_rencontres(self, names: List[str] = None) -> List[QueryResult]:
        if not names:
            return None

        queries = [RencontresMultiSearchQuery(name) for name in names]
        return self.multi_search(queries).results

    def search_rencontres(self, name: str = None) -> QueryResult:
        return self.search_multiple_rencontres([name])
