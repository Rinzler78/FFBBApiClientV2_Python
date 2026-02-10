from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from requests_cache import CachedSession

from ..config import (
    DEFAULT_USER_AGENT,
    MEILISEARCH_BASE_URL,
    MEILISEARCH_ENDPOINT_MULTI_SEARCH,
)
from ..helpers.http_requests_helper import catch_result
from ..helpers.http_requests_utils import http_get_json, http_post_json
from ..models.meilisearch_index_settings import MeilisearchIndexSettings
from ..models.multi_search_query import MultiSearchQuery
from ..models.multi_search_results_class import (
    MultiSearchResults,
    multi_search_results_from_dict,
)
from ..utils.cache_manager import CacheManager
from ..utils.retry_utils import (
    RetryConfig,
    TimeoutConfig,
    get_default_retry_config,
    get_default_timeout_config,
)
from ..utils.secure_logging import get_secure_logger, mask_token


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
            "user-agent": DEFAULT_USER_AGENT,
        }

        # Configure retry and timeout settings
        self.retry_config = retry_config or get_default_retry_config()
        self.timeout_config = timeout_config or get_default_timeout_config()

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
        return catch_result(
            lambda: multi_search_results_from_dict(
                http_post_json(
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
        return catch_result(
            lambda: http_get_json(
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
            return catch_result(lambda: MeilisearchIndexSettings.from_dict(result))

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
