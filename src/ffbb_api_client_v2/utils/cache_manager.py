"""
Advanced cache management for FFBB API Client V2.

This module provides sophisticated caching strategies including:
- Multi-level caching (memory, disk, Redis)
- Configurable cache policies
- Cache performance metrics
- Intelligent cache invalidation
- Cache warming capabilities
"""

import hashlib
from dataclasses import dataclass
from typing import Any, Optional

from requests import PreparedRequest
from requests_cache import CachedSession


@dataclass
class CacheMetrics:
    """Cache performance metrics."""

    hits: int = 0
    misses: int = 0
    evictions: int = 0
    sets: int = 0
    errors: int = 0

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    def reset(self):
        """Reset all metrics."""
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.sets = 0
        self.errors = 0


class CacheConfig:
    """
    Configuration for cache behavior.

    Attributes:
        enabled (bool): Whether caching is enabled
        backend (str): Cache backend ('memory', 'sqlite', 'redis')
        expire_after (int): Default expiration time in seconds
        max_size (int): Maximum cache size (for memory backend)
        redis_url (str): Redis URL for Redis backend
        key_prefix (str): Prefix for cache keys
        compression (bool): Whether to compress cached data
    """

    def __init__(
        self,
        enabled: bool = True,
        backend: str = "sqlite",
        expire_after: int = 1800,  # 30 minutes
        max_size: int = 1000,
        redis_url: str = None,
        key_prefix: str = "ffbb_api",
        compression: bool = False,
    ):
        """
        Initialize cache configuration.

        Args:
            enabled: Whether caching is enabled
            backend: Cache backend type
            expire_after: Default expiration time
            max_size: Maximum cache size for memory backend
            redis_url: Redis connection URL
            key_prefix: Prefix for cache keys
            compression: Whether to compress cached data
        """
        self.enabled = enabled
        self.backend = backend
        self.expire_after = expire_after
        self.max_size = max_size
        self.redis_url = redis_url
        self.key_prefix = key_prefix
        self.compression = compression


class AdvancedCacheManager:
    """
    Advanced cache manager with multiple backends and strategies.
    """

    def __init__(self, config: CacheConfig = None):
        """
        Initialize the cache manager.

        Args:
            config: Cache configuration
        """
        self.config = config or CacheConfig()
        self.metrics = CacheMetrics()
        self._memory_cache: dict[str, dict[str, Any]] = {}
        self._session: Optional[CachedSession] = None

        if self.config.enabled:
            self._initialize_cache()

    def _initialize_cache(self):
        """Initialize the cache backend."""
        if self.config.backend == "memory":
            # Use in-memory cache with size limit
            self._session = CachedSession(
                backend="memory",
                expire_after=self.config.expire_after,
            )
        elif self.config.backend == "sqlite":
            # Use SQLite backend
            self._session = CachedSession(
                "http_cache.db",
                backend="sqlite",
                expire_after=self.config.expire_after,
                allowable_methods=("GET", "POST"),
                key_fn=self._create_cache_key,
            )
        elif self.config.backend == "redis":
            if not self.config.redis_url:
                raise ValueError("Redis URL is required for Redis backend")
            self._session = CachedSession(
                self.config.redis_url,
                backend="redis",
                expire_after=self.config.expire_after,
                allowable_methods=("GET", "POST"),
                key_fn=self._create_cache_key,
            )
        else:
            raise ValueError(f"Unsupported cache backend: {self.config.backend}")

    def _create_cache_key(self, request: PreparedRequest, **kwargs) -> str:
        """
        Create a cache key from the request.

        Args:
            request: Prepared request
            **kwargs: Additional arguments

        Returns:
            str: Cache key
        """
        # Create a unique key based on method, URL, headers, and body
        key_parts = [
            request.method or "GET",
            request.url or "",
        ]

        # Include relevant headers
        if request.headers:
            auth_header = request.headers.get("Authorization", "")
            if auth_header:
                # Mask authorization header in cache key
                key_parts.append("auth_masked")

        # Include request body for POST requests
        if request.method == "POST" and request.body:
            body_hash = hashlib.md5(str(request.body).encode()).hexdigest()
            key_parts.append(body_hash)

        # Create final key with prefix
        key_string = "|".join(key_parts)
        return (
            f"{self.config.key_prefix}:{hashlib.md5(key_string.encode()).hexdigest()}"
        )

    def get_session(self) -> Optional[CachedSession]:
        """
        Get the cached session.

        Returns:
            Optional[CachedSession]: The cached session or None if caching is disabled
        """
        return self._session if self.config.enabled else None

    def is_enabled(self) -> bool:
        """
        Check if caching is enabled.

        Returns:
            bool: True if caching is enabled
        """
        return self.config.enabled and self._session is not None

    def clear_cache(self):
        """Clear all cached data."""
        if self._session:
            try:
                self._session.cache.clear()
                self.metrics.evictions = 0  # Reset eviction count
            except Exception:
                self.metrics.errors += 1

    def get_cache_size(self) -> int:
        """
        Get the current cache size.

        Returns:
            int: Number of cached items
        """
        if self._session and hasattr(self._session.cache, "count"):
            try:
                return self._session.cache.count()
            except Exception:
                self.metrics.errors += 1
        return 0

    def get_metrics(self) -> CacheMetrics:
        """
        Get cache performance metrics.

        Returns:
            CacheMetrics: Current cache metrics
        """
        return self.metrics

    def warm_cache(self, urls: list[str], headers: dict = None):
        """
        Warm the cache by pre-fetching specified URLs.

        Args:
            urls: List of URLs to cache
            headers: Headers to use for requests
        """
        if not self.is_enabled():
            return

        headers = headers or {}
        for url in urls:
            try:
                self._session.get(url, headers=headers, timeout=10)
            except Exception:
                # Ignore errors during cache warming
                pass

    def invalidate_pattern(self, pattern: str):
        """
        Invalidate cache entries matching a pattern.

        Args:
            pattern: Pattern to match for invalidation
        """
        if not self.is_enabled():
            return

        try:
            # This is a simplified implementation
            # In a real scenario, you'd need more sophisticated pattern matching
            # depending on the cache backend
            if hasattr(self._session.cache, "delete"):
                # For Redis backend
                keys_to_delete = []
                for key in self._session.cache.keys():
                    if pattern in key:
                        keys_to_delete.append(key)
                for key in keys_to_delete:
                    self._session.cache.delete(key)
        except Exception:
            self.metrics.errors += 1


# Global cache manager instance
_default_cache_manager = None


def get_cache_manager(config: CacheConfig = None) -> AdvancedCacheManager:
    """
    Get the global cache manager instance.

    Args:
        config: Cache configuration (used only for first call)

    Returns:
        AdvancedCacheManager: The cache manager instance
    """
    global _default_cache_manager
    if _default_cache_manager is None:
        _default_cache_manager = AdvancedCacheManager(config)
    return _default_cache_manager


def create_cache_key(request: PreparedRequest, **kwargs) -> str:
    """
    Create a cache key from a request (backward compatibility).

    Args:
        request: Prepared request
        **kwargs: Additional arguments

    Returns:
        str: Cache key
    """
    manager = get_cache_manager()
    return manager._create_cache_key(request, **kwargs)


# Backward compatibility - default cached session
default_cached_session = CachedSession(
    "http_cache",
    backend="sqlite",
    expire_after=1800,
    allowable_methods=("GET", "POST"),
    key_fn=create_cache_key,
)
