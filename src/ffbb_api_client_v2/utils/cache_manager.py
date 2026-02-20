"""
Advanced cache management for FFBB API Client V2.

This module provides sophisticated caching strategies including:
- Multi-level caching (memory, disk, Redis)
- Configurable cache policies
- Cache performance metrics
- Intelligent cache invalidation
- Cache warming capabilities
"""

from __future__ import annotations

import hashlib
import threading
from dataclasses import dataclass
from typing import Any, cast

from requests import PreparedRequest, Response
from requests_cache import CachedSession


class ThreadSafeCachedSession(CachedSession):
    """Thread-safe wrapper around ``CachedSession``.

    ``requests.Session`` (and its subclass ``CachedSession``) is **not**
    thread-safe: concurrent calls from multiple threads can corrupt
    internal state and — with the SQLite backend — trigger
    ``sqlite3.DatabaseError`` or even segfaults.

    This subclass serialises every request through a single
    ``threading.Lock`` on the ``request()`` method, which is the common
    dispatch point for all HTTP verbs (``get()``, ``post()``, etc. all
    delegate to ``request()``).
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._ts_lock = threading.Lock()

    def __getstate__(self) -> dict[str, Any]:
        """Preserve parent cache/session pickling contract."""
        return cast(dict[str, Any], super().__getstate__())

    def request(self, *args: Any, **kwargs: Any) -> Response:  # type: ignore[override]
        with self._ts_lock:
            return cast(Response, super().request(*args, **kwargs))


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

    def reset(self) -> None:
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
        enabled: Whether caching is enabled.
        backend: Cache backend ('memory', 'sqlite', 'redis').
        expire_after: Default expiration time in seconds.
        max_size: Maximum cache size (for memory backend).
        redis_url: Redis URL for Redis backend.
        key_prefix: Prefix for cache keys.
        compression: Whether to compress cached data.
    """

    def __init__(
        self,
        enabled: bool = True,
        backend: str = "sqlite",
        expire_after: int = 1800,  # 30 minutes
        max_size: int = 1000,
        redis_url: str | None = None,
        key_prefix: str = "ffbb_api",
        compression: bool = False,
    ) -> None:
        """
        Initialize cache configuration.

        Args:
            enabled: Whether caching is enabled.
            backend: Cache backend type.
            expire_after: Default expiration time.
            max_size: Maximum cache size for memory backend.
            redis_url: Redis connection URL.
            key_prefix: Prefix for cache keys.
            compression: Whether to compress cached data.
        """
        self.enabled = enabled
        self.backend = backend
        self.expire_after = expire_after
        self.max_size = max_size
        self.redis_url = redis_url
        self.key_prefix = key_prefix
        self.compression = compression


class CacheManager:
    """
    Thread-safe singleton cache manager for API requests.

    This class implements the singleton pattern with double-check locking
    to ensure thread safety during instance creation.

    Attributes:
        config: Cache configuration settings.
        metrics: Cache performance metrics.
    """

    _instance: CacheManager | None = None
    _lock: threading.Lock = threading.Lock()
    _initialized: bool = False

    def __new__(cls, config: CacheConfig | None = None) -> CacheManager:
        """
        Create or return the singleton instance.

        Uses double-check locking for thread safety.

        Args:
            config: Optional configuration for first instantiation.

        Returns:
            The singleton CacheManager instance.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    instance = super().__new__(cls)
                    cls._instance = instance
        return cls._instance

    def __init__(self, config: CacheConfig | None = None) -> None:
        """
        Initialize the cache manager instance.

        Only initializes on first call to avoid re-initialization.

        Args:
            config: Cache configuration settings.
        """
        if CacheManager._initialized:
            return

        with CacheManager._lock:
            if CacheManager._initialized:
                return

            self.config = config or CacheConfig()
            self.metrics = CacheMetrics()
            self._memory_cache: dict[str, dict[str, Any]] = {}
            self._session: CachedSession | None = None

            if self.config.enabled:
                self._initialize_cache()

            CacheManager._initialized = True

    def _initialize_cache(self) -> None:
        """Initialize the cache backend.

        Uses ``ThreadSafeCachedSession`` so that the singleton session
        can be shared safely across multiple threads.
        """
        if self.config.backend == "memory":
            self._session = ThreadSafeCachedSession(
                backend="memory",
                expire_after=self.config.expire_after,
            )
        elif self.config.backend == "sqlite":
            self._session = ThreadSafeCachedSession(
                "http_cache.db",
                backend="sqlite",
                expire_after=self.config.expire_after,
                allowable_methods=("GET", "POST"),
                key_fn=self.create_cache_key,
            )
        elif self.config.backend == "redis":
            if not self.config.redis_url:
                raise ValueError("Redis URL is required for Redis backend")
            self._session = ThreadSafeCachedSession(
                self.config.redis_url,
                backend="redis",
                expire_after=self.config.expire_after,
                allowable_methods=("GET", "POST"),
                key_fn=self.create_cache_key,
            )
        else:
            raise ValueError(f"Unsupported cache backend: {self.config.backend}")

    def create_cache_key(self, request: PreparedRequest, **_kwargs: Any) -> str:
        """
        Create a cache key from the request.

        Args:
            request: Prepared request.
            **_kwargs: Additional arguments (ignored).

        Returns:
            Cache key string.
        """
        key_parts = [
            request.method or "GET",
            request.url or "",
        ]

        if request.headers:
            auth_header = request.headers.get("Authorization", "")
            if auth_header:
                key_parts.append("auth_masked")

        if request.method == "POST" and request.body:
            body_hash = hashlib.md5(str(request.body).encode()).hexdigest()
            key_parts.append(body_hash)

        key_string = "|".join(key_parts)
        return (
            f"{self.config.key_prefix}:{hashlib.md5(key_string.encode()).hexdigest()}"
        )

    @property
    def session(self) -> CachedSession | None:
        """Get the cached session."""
        return self._session if self.config.enabled else None

    def get_session(self) -> CachedSession | None:
        """
        Get the cached session.

        Returns:
            The cached session or None if caching is disabled.
        """
        return self.session

    def is_enabled(self) -> bool:
        """
        Check if caching is enabled.

        Returns:
            True if caching is enabled.
        """
        return self.config.enabled and self._session is not None

    def clear_cache(self) -> bool:
        """
        Clear all cached data.

        Returns:
            True if cache was cleared successfully, False otherwise.
        """
        if self._session is None:
            return False
        try:
            self._session.cache.clear()
            self.metrics.evictions = 0
            return True
        except (OSError, RuntimeError, AttributeError):
            self.metrics.errors += 1
            return False

    def get_cache_size(self) -> int:
        """
        Get the current cache size.

        Returns:
            Number of cached items.
        """
        if self._session is None:
            return 0
        try:
            count_method = getattr(self._session.cache, "count", None)
            if count_method is not None:
                return cast(int, count_method())
        except (OSError, RuntimeError, AttributeError):
            self.metrics.errors += 1
        return 0

    def get_metrics(self) -> CacheMetrics:
        """
        Get cache performance metrics.

        Returns:
            Current cache metrics.
        """
        return self.metrics

    def warm_cache(self, urls: list[str], headers: dict[str, str] | None = None) -> int:
        """
        Warm the cache by pre-fetching specified URLs.

        Args:
            urls: List of URLs to cache.
            headers: Headers to use for requests.

        Returns:
            Number of URLs successfully cached.
        """
        if not self.is_enabled() or self._session is None:
            return 0

        headers = headers or {}
        count = 0
        for url in urls:
            try:
                self._session.get(url, headers=headers, timeout=10)
                count += 1
            except (OSError, ConnectionError, TimeoutError, ValueError):
                pass
        return count

    def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalidate cache entries matching a pattern.

        Args:
            pattern: Pattern to match for invalidation.

        Returns:
            Number of entries invalidated.
        """
        if not self.is_enabled() or self._session is None:
            return 0

        try:
            if hasattr(self._session.cache, "delete") and hasattr(
                self._session.cache, "keys"
            ):
                keys_to_delete = []
                for key in cast(Any, self._session.cache).keys():
                    if pattern in key:
                        keys_to_delete.append(key)
                for key in keys_to_delete:
                    cast(Any, self._session.cache).delete(key)
                return len(keys_to_delete)
        except (OSError, RuntimeError, AttributeError, KeyError):
            self.metrics.errors += 1
        return 0

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (for testing purposes)."""
        with cls._lock:
            cls._instance = None
            cls._initialized = False
