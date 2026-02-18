from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from requests_cache import CachedSession

from .._http.client import HttpClient
from .._http.helper import HttpHelper
from ..config import (
    DEFAULT_MEILISEARCH_RETRY_CONFIG,
    DEFAULT_MEILISEARCH_TIMEOUT_CONFIG,
    MEILISEARCH_BASE_URL,
    MEILISEARCH_ENDPOINT_MULTI_SEARCH,
)
from ..directus.client import DEFAULT_USER_AGENT
from ..utils.cache_manager import CacheManager
from ..utils.retry_utils import RetryConfig, TimeoutConfig
from ..utils.secure_logging import get_secure_logger, mask_token
from .models.federated_search_result import FederatedSearchResult
from .models.meilisearch_index_settings import MeilisearchIndexSettings
from .models.multi_search_query import MultiSearchQuery
from .models.multi_search_results_class import (
    MultiSearchResults,
    multi_search_results_from_dict,
)


class MeilisearchClient:
    def __init__(
        self,
        bearer_token: str,
        url: str = MEILISEARCH_BASE_URL,
        debug: bool = False,
        cached_session: CachedSession | None = None,
        retry_config: RetryConfig | None = None,
        timeout_config: TimeoutConfig | None = None,
    ):
        """
        Initializes an instance of the MeilisearchClient class.

        Args:
            bearer_token (str): The bearer token used for authentication.
            url (str, optional): The base URL.
                Defaults to "https://meilisearch-prod.ffbb.app/".
            debug (bool, optional): Whether to enable debug mode. Defaults to False.
            cached_session (CachedSession, optional): The cached session to use.
            retry_config (RetryConfig, optional): Retry configuration. Defaults to None.
            timeout_config (TimeoutConfig, optional): Timeout configuration.
                Defaults to None.
        """
        if not bearer_token or not bearer_token.strip():
            raise ValueError("bearer_token cannot be None, empty, or whitespace-only")

        # Store token securely (private attribute)
        self._bearer_token = bearer_token
        self.url = url
        self.debug = debug
        self.cached_session = (
            cached_session if cached_session else CacheManager().session
        )
        self.headers = {
            "Authorization": f"Bearer {self._bearer_token}",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "user-agent": DEFAULT_USER_AGENT,
        }

        # Configure retry and timeout settings
        self.retry_config = retry_config or DEFAULT_MEILISEARCH_RETRY_CONFIG
        self.timeout_config = timeout_config or DEFAULT_MEILISEARCH_TIMEOUT_CONFIG

        # Initialize secure logger
        self.logger = get_secure_logger(f"{self.__class__.__name__}")

        # Log initialization with masked token
        masked_token = mask_token(self._bearer_token)
        if self.debug:
            self.logger.info(
                f"MeilisearchClient initialized with token: {masked_token}"
            )
            self.logger.info(
                f"Retry config: {self.retry_config.max_attempts} attempts, "
                f"timeout: {self.timeout_config.total_timeout}s"
            )
        else:
            self.logger.info("MeilisearchClient initialized successfully")

    @property
    def bearer_token(self) -> str:
        """Get the bearer token."""
        return self._bearer_token

    def multi_search(
        self,
        queries: Sequence[MultiSearchQuery] | None = None,
        cached_session: CachedSession | None = None,
    ) -> MultiSearchResults | None:
        url = f"{self.url}{MEILISEARCH_ENDPOINT_MULTI_SEARCH}"
        params = {"queries": [query.to_dict() for query in queries] if queries else []}
        return HttpHelper.catch_result(
            lambda: multi_search_results_from_dict(
                HttpClient.http_post_json(
                    url,
                    self.headers,
                    params,
                    debug=self.debug,
                    cached_session=cached_session or self.cached_session,
                    retry_config=self.retry_config,
                    timeout_config=self.timeout_config,
                )
            )
        )

    def _get_json(
        self,
        path: str,
        cached_session: CachedSession | None = None,
    ) -> dict[str, Any] | None:
        """Perform an authenticated GET request to a Meilisearch endpoint."""
        url = f"{self.url}{path}"
        return HttpHelper.catch_result(
            lambda: HttpClient.http_get_json(
                url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
                retry_config=self.retry_config,
                timeout_config=self.timeout_config,
            )
        )

    def get_index_settings(
        self,
        index_uid: str,
        cached_session: CachedSession | None = None,
    ) -> MeilisearchIndexSettings | None:
        """Get settings for a Meilisearch index.

        Falls back to facets discovery if the settings API is unavailable
        (requires an admin API key).
        """
        result = self._get_json(f"indexes/{index_uid}/settings", cached_session)
        if result is not None and "code" not in result:
            return HttpHelper.catch_result(
                lambda: MeilisearchIndexSettings.from_dict(result)
            )

        # Fallback: discover filterable attributes via facets: ["*"]
        self.logger.debug(
            f"Settings API unavailable for {index_uid}, using facets fallback"
        )
        filterable = self._discover_filterable_via_facets(index_uid, cached_session)
        if filterable is not None:
            return MeilisearchIndexSettings(filterable_attributes=filterable)
        return None

    def _discover_filterable_via_facets(
        self,
        index_uid: str,
        cached_session: CachedSession | None = None,
    ) -> list[str] | None:
        """Discover filterable attributes by searching with facets: ['*']."""
        query = MultiSearchQuery(index_uid=index_uid, q="", facets=["*"], limit=0)
        results = self.multi_search([query], cached_session)
        if results and results.results:
            first = results.results[0]
            if first.facet_distribution is not None:
                fd = first.facet_distribution
                if isinstance(fd, dict):
                    return sorted(fd.keys())
        return None

    def get_filterable_attributes(
        self,
        index_uid: str,
        cached_session: CachedSession | None = None,
    ) -> list[str] | None:
        """Get filterable attributes for a Meilisearch index."""
        settings = self.get_index_settings(index_uid, cached_session)
        return settings.filterable_attributes if settings else None

    def get_sortable_attributes(
        self,
        index_uid: str,
        cached_session: CachedSession | None = None,
    ) -> list[str] | None:
        """Get sortable attributes for a Meilisearch index."""
        settings = self.get_index_settings(index_uid, cached_session)
        return settings.sortable_attributes if settings else None

    # --- Official Meilisearch API Compliance: Index Operations ---

    def list_indexes(
        self,
        offset: int = 0,
        limit: int = 20,
        cached_session: CachedSession | None = None,
    ) -> dict[str, Any] | None:
        """
        List all available Meilisearch indexes.

        Official Meilisearch API: GET /indexes?offset={offset}&limit={limit}

        Args:
            offset (int): Number of indexes to skip. Defaults to 0.
            limit (int): Number of indexes to return. Defaults to 20.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            dict with:
                - results: List of index objects (uid, createdAt, updatedAt, primaryKey)
                - offset: Number of indexes skipped
                - limit: Number of indexes returned
                - total: Total number of indexes
        """
        url = f"{self.url}indexes?offset={offset}&limit={limit}"
        return self._get_json(url, cached_session)

    def search_index(
        self,
        index_uid: str,
        query: str = "",
        offset: int = 0,
        limit: int = 20,
        filter: str | None = None,
        facets: list[str] | None = None,
        sort: list[str] | None = None,
        attributes_to_retrieve: list[str] | None = None,
        cached_session: CachedSession | None = None,
    ) -> dict[str, Any] | None:
        """
        Search a single Meilisearch index (Official API compliance).

        Official Meilisearch API: POST /indexes/{index_uid}/search

        Args:
            index_uid (str): Unique identifier of the index
            query (str): Search query. Empty string for placeholder search.
            offset (int): Number of documents to skip. Defaults to 0.
            limit (int): Maximum number of documents to return. Defaults to 20.
            filter (str, optional): Filter expression
            facets (list[str], optional): Facets to retrieve
            sort (list[str], optional): Sort attributes (e.g., ["price:asc"])
            attributes_to_retrieve (list[str], optional): Fields to return
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            dict with:
                - hits: List of matching documents
                - offset: Number of documents skipped
                - limit: Documents returned
                - estimatedTotalHits: Estimated total matches
                - totalHits: Exact total (if hitsPerPage/page used)
                - totalPages: Total pages (if hitsPerPage/page used)
                - facetDistribution: Facet counts (if facets requested)
                - facetStats: Min/max per numeric facet
                - processingTimeMs: Query processing time
                - query: Original query
                - requestUid: Unique request identifier
        """
        url = f"{self.url}indexes/{index_uid}/search"
        body: dict[str, Any] = {
            "q": query,
            "offset": offset,
            "limit": limit,
        }

        if filter:
            body["filter"] = filter
        if facets:
            body["facets"] = facets
        if sort:
            body["sort"] = sort
        if attributes_to_retrieve:
            body["attributesToRetrieve"] = attributes_to_retrieve

        return HttpHelper.catch_result(
            lambda: HttpClient.http_post_json(
                url,
                self.headers,
                body,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
                retry_config=self.retry_config,
                timeout_config=self.timeout_config,
            )
        )

    def federated_multi_search(
        self,
        queries: Sequence[MultiSearchQuery] | None = None,
        federation_options: dict[str, Any] | None = None,
        cached_session: CachedSession | None = None,
    ) -> FederatedSearchResult | None:
        """Execute a federated multi-search across multiple indexes.

        Unlike regular multi_search which returns separate results per index,
        federated search merges all results into a single list ranked by
        global relevance.

        Args:
            queries: Search queries targeting different indexes.
            federation_options: Optional federation configuration:
                - weight (float): Per-query weight for ranking (in each query).
                - limit (int): Max total hits in merged results.
                - offset (int): Skip N merged results.
                - facetsByIndex (dict): Per-index facets configuration.
                - mergeFacets (dict): Facet merging configuration.
            cached_session: Optional cached session.

        Returns:
            FederatedSearchResult with merged hits across all indexes,
            or None if the response is empty.
        """
        url = f"{self.url}{MEILISEARCH_ENDPOINT_MULTI_SEARCH}"
        params: dict[str, Any] = {
            "queries": [query.to_dict() for query in queries] if queries else [],
            "federation": federation_options if federation_options else {},
        }
        raw = HttpHelper.catch_result(
            lambda: HttpClient.http_post_json(
                url,
                self.headers,
                params,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
                retry_config=self.retry_config,
                timeout_config=self.timeout_config,
            )
        )
        if raw and isinstance(raw, dict):
            return FederatedSearchResult.from_dict(raw)
        return None
