"""Helper modules and class extensions."""

from .http_requests_helper import catch_result, create_cache_key, default_cached_session
from .http_requests_utils import (
    encode_params,
    http_get,
    http_get_json,
    http_post,
    http_post_json,
    to_json_from_response,
    url_with_params,
)
from .meilisearch_client_extension import MeilisearchClientExtension
from .multi_search_query_helper import generate_queries

__all__ = [
    "MeilisearchClientExtension",
    "catch_result",
    "create_cache_key",
    "default_cached_session",
    "encode_params",
    "generate_queries",
    "http_get",
    "http_get_json",
    "http_post",
    "http_post_json",
    "to_json_from_response",
    "url_with_params",
]
