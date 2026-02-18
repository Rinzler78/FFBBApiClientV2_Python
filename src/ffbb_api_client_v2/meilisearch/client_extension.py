from __future__ import annotations

import logging
from collections.abc import Sequence

from requests_cache import CachedSession

from ..utils.cache_manager import CacheManager
from ..utils.retry_utils import RetryConfig, TimeoutConfig
from .client import MeilisearchClient
from .models.multi_search_query import MultiSearchQuery
from .models.multi_search_results_class import MultiSearchResults

logger = logging.getLogger(__name__)

# Meilisearch default pagination.maxTotalHits is 1000
DEFAULT_MAX_TOTAL_HITS = 1000
DEFAULT_MAX_ITERATIONS = 20


class MeilisearchClientExtension(MeilisearchClient):
    def __init__(
        self,
        bearer_token: str,
        url: str,
        debug: bool = False,
        cached_session: CachedSession | None = None,
        retry_config: RetryConfig | None = None,
        timeout_config: TimeoutConfig | None = None,
    ):
        if cached_session is None:
            cached_session = CacheManager().session
        super().__init__(
            bearer_token, url, debug, cached_session, retry_config, timeout_config
        )

    def smart_multi_search(
        self,
        queries: Sequence[MultiSearchQuery] | None = None,
        cached_session: CachedSession | None = None,
    ) -> MultiSearchResults | None:
        results = self.multi_search(queries, cached_session)

        # Should filter results.hits according to query.q
        if queries and results and results.results:
            for i in range(len(results.results)):
                query = queries[i]

                if query.q:
                    result = results.results[i]
                    results.results[i] = query.filter_result(result)

        return results

    def recursive_smart_multi_search(
        self,
        queries: Sequence[MultiSearchQuery] | None = None,
        cached_session: CachedSession | None = None,
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
        max_total_hits: int = DEFAULT_MAX_TOTAL_HITS,
    ) -> MultiSearchResults | None:
        """Recursively paginate through Meilisearch results.

        Args:
            queries: Search queries to execute.
            cached_session: Optional cached session.
            max_iterations: Maximum number of recursive iterations to prevent
                infinite loops. Defaults to 20.
            max_total_hits: Maximum offset+limit cap per query, matching
                Meilisearch's pagination.maxTotalHits (default 1000).

        Returns:
            Aggregated search results, or None if no results.
        """
        return self._recursive_smart_multi_search_impl(
            queries=queries,
            cached_session=cached_session,
            max_iterations=max_iterations,
            max_total_hits=max_total_hits,
            iteration=0,
        )

    def _recursive_smart_multi_search_impl(
        self,
        queries: Sequence[MultiSearchQuery] | None,
        cached_session: CachedSession | None,
        max_iterations: int,
        max_total_hits: int,
        iteration: int,
    ) -> MultiSearchResults | None:
        result = self.smart_multi_search(queries, cached_session)
        if not result or not queries or not result.results:
            return result

        # Guard-rail: stop if we've hit the max iterations
        if iteration >= max_iterations:
            logger.warning(
                "Recursive pagination stopped: max_iterations (%d) reached.",
                max_iterations,
            )
            return result

        next_queries: list[MultiSearchQuery] = []

        for i in range(len(result.results)):
            query_result = result.results[i]
            querie = queries[i]
            nb_hits = len(query_result.hits) if query_result.hits else 0
            querie_offset = querie.offset or 0
            querie_limit = querie.limit or 20

            if query_result.estimated_total_hits is not None and nb_hits < (
                query_result.estimated_total_hits - querie_offset
            ):
                new_offset = querie_offset + querie_limit

                # Guard-rail: stop if offset exceeds Meilisearch maxTotalHits
                if new_offset >= max_total_hits:
                    logger.warning(
                        "Recursive pagination stopped for index '%s': "
                        "offset (%d) reached max_total_hits (%d).",
                        querie.index_uid,
                        new_offset,
                        max_total_hits,
                    )
                    continue

                querie.offset = new_offset
                querie.limit = min(
                    query_result.estimated_total_hits - nb_hits,
                    max_total_hits - new_offset,
                )
                next_queries.append(querie)

        if next_queries:
            new_result = self._recursive_smart_multi_search_impl(
                queries=next_queries,
                cached_session=cached_session,
                max_iterations=max_iterations,
                max_total_hits=max_total_hits,
                iteration=iteration + 1,
            )

            if new_result and new_result.results:
                for i in range(len(new_result.results)):
                    query_result = new_result.results[i]
                    hits_list = result.results[i].hits
                    if query_result.hits and hits_list is not None:
                        hits_list.extend(query_result.hits)
        return result

    def recursive_multi_search(
        self,
        queries: Sequence[MultiSearchQuery] | None = None,
        cached_session: CachedSession | None = None,
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
        max_total_hits: int = DEFAULT_MAX_TOTAL_HITS,
    ) -> MultiSearchResults | None:
        """Alias for recursive_smart_multi_search for backward compatibility."""
        return self.recursive_smart_multi_search(
            queries, cached_session, max_iterations, max_total_hits
        )
