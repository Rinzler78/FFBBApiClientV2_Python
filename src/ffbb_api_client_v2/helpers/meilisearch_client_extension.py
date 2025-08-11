from requests_cache import CachedSession

from ..clients.meilisearch_client import MeilisearchClient
from ..models.multi_search_query import MultiSearchQuery
from ..models.MultiSearchResults import MultiSearchResults
from .http_requests_helper import default_cached_session


class MeilisearchClientExtension(MeilisearchClient):
    def __init__(
        self,
        bearer_token: str,
        url: str,
        debug: bool = False,
        cached_session: CachedSession = default_cached_session,
    ):
        super().__init__(bearer_token, url, debug, cached_session)

    def smart_multi_search(
        self,
        queries: list[MultiSearchQuery] = None,
        cached_session: CachedSession = None,
    ) -> MultiSearchResults:
        results = self.multi_search(queries, cached_session)

        # Should filter results.hits according to query.q
        if queries:
            for i in range(len(results.results)):
                query = queries[i]

                if query.q:
                    result = results.results[i]
                    results.results[i] = query.filter_result(result)

        return results

    def recursive_smart_multi_search(
        self,
        queries: list[MultiSearchQuery] = None,
        cached_session: CachedSession = None,
    ) -> MultiSearchResults:
        result = self.smart_multi_search(queries, cached_session)
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
            new_result = self.recursive_smart_multi_search(next_queries, cached_session)

            for i in range(len(new_result.results)):
                query_result = new_result.results[i]
                result.results[i].hits.extend(query_result.hits)
        return result
