"""Generic Meilisearch configuration shared across all instances."""

from .utils.retry_utils import RetryConfig, TimeoutConfig

# Meilisearch is fast, keep shorter timeouts with more retries
DEFAULT_MEILISEARCH_TIMEOUT_CONFIG = TimeoutConfig(
    connect_timeout=10.0, read_timeout=30.0
)
DEFAULT_MEILISEARCH_RETRY_CONFIG = RetryConfig(max_attempts=3)

# Meilisearch URLs
MEILISEARCH_BASE_URL = "https://meilisearch-prod.ffbb.app/"

# Environment variable names
ENV_MEILISEARCH_TOKEN = "MEILISEARCH_BEARER_TOKEN"

# Meilisearch Endpoint Paths
MEILISEARCH_ENDPOINT_MULTI_SEARCH = "multi-search"
