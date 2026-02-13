"""Generic Directus API client base class."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

from requests_cache import CachedSession

from .._http.client import HttpClient
from ..exceptions import FFBBApiError
from ..utils.cache_manager import CacheConfig, CacheManager
from ..utils.retry_utils import (
    RetryConfig,
    TimeoutConfig,
    get_default_retry_config,
    get_default_timeout_config,
)
from ..utils.secure_logging import get_secure_logger, mask_token
from .exceptions import DirectusError

# HTTP Headers
DEFAULT_USER_AGENT = "okhttp/4.12.0"

T = TypeVar("T")


class DirectusClient:
    """Generic Directus API client.

    Provides base HTTP operations for any Directus instance:
    - GET single item
    - GET list of items
    - Automatic pagination
    - Schema introspection (collections, fields)

    Catches generic FFBBApiError and enriches into DirectusError when
    the response body matches the Directus error format.
    """

    def __init__(
        self,
        bearer_token: str,
        url: str,
        debug: bool = False,
        cached_session: CachedSession | None = None,
        retry_config: RetryConfig | None = None,
        timeout_config: TimeoutConfig | None = None,
        cache_config: CacheConfig | None = None,
    ):
        if not bearer_token or not bearer_token.strip():
            raise ValueError("bearer_token cannot be None, empty, or whitespace-only")

        self._bearer_token = bearer_token
        self.url = url
        self.debug = debug
        self.headers = {
            "Authorization": f"Bearer {self._bearer_token}",
            "user-agent": DEFAULT_USER_AGENT,
        }

        self.retry_config = retry_config or get_default_retry_config()
        self.timeout_config = timeout_config or get_default_timeout_config()

        self.cache_manager = CacheManager(cache_config)
        self.cached_session = cached_session or self.cache_manager.session

        self.logger = get_secure_logger(f"{self.__class__.__name__}")

        masked_token = mask_token(self._bearer_token)
        if self.debug:
            self.logger.info(
                f"{self.__class__.__name__} initialized with token: {masked_token}"
            )
            self.logger.info(
                f"Retry config: {self.retry_config.max_attempts} attempts, "
                f"timeout: {self.timeout_config.total_timeout}s"
            )
        else:
            self.logger.info(f"{self.__class__.__name__} initialized successfully")

    @property
    def bearer_token(self) -> str:
        """Get the bearer token."""
        return self._bearer_token

    def _get_json(
        self,
        url: str,
        cached_session: CachedSession | None = None,
    ) -> dict[str, Any]:
        """Perform an authenticated GET and return JSON, enriching errors.

        Catches generic FFBB exceptions and re-raises as DirectusError
        when the response body matches the Directus error format.
        """
        try:
            return HttpClient.http_get_json(
                url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
                retry_config=self.retry_config,
                timeout_config=self.timeout_config,
            )
        except FFBBApiError as e:
            self._maybe_raise_directus_error(e)
            raise

    def _maybe_raise_directus_error(self, exc: FFBBApiError) -> None:
        """If the response body is a Directus error format, re-raise."""
        body = exc.response_body
        if body and isinstance(body, dict) and "errors" in body:
            raise DirectusError.from_response(body, exc.status_code or 0) from exc

    def _get_item(
        self,
        endpoint: str,
        fields: list[str] | None = None,
        params: dict[str, Any] | None = None,
        cached_session: CachedSession | None = None,
    ) -> dict[str, Any] | None:
        """GET a single item from a Directus endpoint.

        Returns the unwrapped data (from response.data), or None.
        """
        url = f"{self.url}{endpoint}"
        if params is None:
            params = {}
        if fields:
            params["fields[]"] = fields
        if params:
            url = HttpClient.url_with_params(url, params)

        from .._http.helper import HttpHelper

        data = HttpHelper.catch_result(lambda: self._get_json(url, cached_session))
        if data and isinstance(data, dict):
            return data.get("data")
        return None

    def _list_items(
        self,
        endpoint: str,
        fields: list[str] | None = None,
        params: dict[str, Any] | None = None,
        limit: int = 10,
        offset: int | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[dict[str, Any]]:
        """GET a list of items from a Directus endpoint."""
        url = f"{self.url}{endpoint}"
        if params is None:
            params = {}
        params["limit"] = str(limit)
        if offset is not None:
            params["offset"] = str(offset)
        if fields:
            params["fields[]"] = fields
        if params:
            url = HttpClient.url_with_params(url, params)

        from .._http.helper import HttpHelper

        data = HttpHelper.catch_result(lambda: self._get_json(url, cached_session))
        if data and isinstance(data, dict):
            actual = data.get("data")
            if isinstance(actual, list):
                return actual
        return []

    def _fetch_all_pages(
        self,
        endpoint: str,
        fields: list[str],
        from_list_fn: Callable[[list[dict[str, Any]]], list[T]],
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[T]:
        """Paginate automatically via meta=total_count until all items are fetched."""
        from .._http.helper import HttpHelper

        all_items: list[T] = []
        offset = 0

        while True:
            params: dict[str, Any] = {
                "limit": str(page_size),
                "offset": str(offset),
                "meta": "total_count,filter_count",
            }
            params["fields[]"] = fields
            if filter_criteria:
                params["filter"] = filter_criteria
            if sort:
                params["sort[]"] = sort
            if search:
                params["search"] = search

            url = f"{self.url}{endpoint}"
            final_url = HttpClient.url_with_params(url, params)
            data = HttpHelper.catch_result(
                lambda: self._get_json(final_url, cached_session)
            )

            if not data or not isinstance(data, dict):
                break

            actual_data = data.get("data")
            if not actual_data or not isinstance(actual_data, list):
                break

            items = from_list_fn(actual_data)
            all_items.extend(items)

            meta = data.get("meta", {})
            total = meta.get("filter_count") or meta.get("total_count") or 0

            if len(all_items) >= total:
                break

            if len(all_items) >= max_items:
                self.logger.warning(
                    "Pagination stopped: max_items limit (%d) reached for %s. "
                    "Total available: %d. Results may be truncated.",
                    max_items,
                    endpoint,
                    total,
                )
                break

            if len(actual_data) < page_size:
                break

            offset += page_size

        return all_items

    # --- Directus Schema Discovery ---

    def get_collections(
        self,
        cached_session: CachedSession | None = None,
    ) -> list[dict[str, Any]]:
        """Retrieves all available collections from the Directus schema.

        Official Directus API: GET /collections
        """
        from .._http.helper import HttpHelper

        url = f"{self.url}collections"
        data = HttpHelper.catch_result(lambda: self._get_json(url, cached_session))
        if data and isinstance(data, dict):
            collections = data.get("data", [])
            if isinstance(collections, list):
                return collections
        return []

    def get_fields(
        self,
        collection: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[dict[str, Any]]:
        """Retrieves field schema information from Directus.

        Official Directus API: GET /fields or GET /fields/{collection}
        """
        from .._http.helper import HttpHelper

        if collection:
            url = f"{self.url}fields/{collection}"
        else:
            url = f"{self.url}fields"

        data = HttpHelper.catch_result(lambda: self._get_json(url, cached_session))
        if data and isinstance(data, dict):
            fields = data.get("data", [])
            if isinstance(fields, list):
                return fields
        return []

    def get_collection_fields(
        self,
        collection: str,
        cached_session: CachedSession | None = None,
    ) -> list[dict[str, Any]]:
        """Convenience method to get fields for a specific collection."""
        return self.get_fields(collection=collection, cached_session=cached_session)
