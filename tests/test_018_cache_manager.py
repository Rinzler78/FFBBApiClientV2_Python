"""
Tests for advanced cache management functionality.
"""

import unittest
from unittest.mock import MagicMock, patch

from ffbb_api_client_v2.utils.cache_manager import (
    AdvancedCacheManager,
    CacheConfig,
    CacheMetrics,
    create_cache_key,
)


class Test018CacheManager(unittest.TestCase):
    """Test cases for advanced cache management."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = CacheConfig(
            enabled=True,
            backend="memory",
            expire_after=1800,
            max_size=100,
        )

    def test_cache_config_defaults(self):
        """Test CacheConfig default values."""
        config = CacheConfig()

        self.assertTrue(config.enabled)
        self.assertEqual(config.backend, "sqlite")
        self.assertEqual(config.expire_after, 1800)
        self.assertEqual(config.max_size, 1000)
        self.assertIsNone(config.redis_url)
        self.assertEqual(config.key_prefix, "ffbb_api")
        self.assertFalse(config.compression)

    def test_cache_metrics(self):
        """Test CacheMetrics functionality."""
        metrics = CacheMetrics()

        # Initial state
        self.assertEqual(metrics.hits, 0)
        self.assertEqual(metrics.misses, 0)
        self.assertEqual(metrics.hit_rate, 0.0)

        # Add some data
        metrics.hits = 7
        metrics.misses = 3

        self.assertEqual(metrics.hit_rate, 0.7)

        # Reset
        metrics.reset()
        self.assertEqual(metrics.hits, 0)
        self.assertEqual(metrics.misses, 0)

    def test_cache_manager_initialization_memory(self):
        """Test cache manager initialization with memory backend."""
        config = CacheConfig(backend="memory")
        manager = AdvancedCacheManager(config)

        self.assertTrue(manager.is_enabled())
        self.assertIsNotNone(manager.get_session())
        self.assertEqual(manager.config.backend, "memory")

    def test_cache_manager_initialization_sqlite(self):
        """Test cache manager initialization with SQLite backend."""
        config = CacheConfig(backend="sqlite")
        manager = AdvancedCacheManager(config)

        self.assertTrue(manager.is_enabled())
        self.assertIsNotNone(manager.get_session())
        self.assertEqual(manager.config.backend, "sqlite")

    def test_cache_manager_initialization_disabled(self):
        """Test cache manager with caching disabled."""
        config = CacheConfig(enabled=False)
        manager = AdvancedCacheManager(config)

        self.assertFalse(manager.is_enabled())
        self.assertIsNone(manager.get_session())

    @patch("ffbb_api_client_v2.utils.cache_manager.CachedSession")
    def test_cache_manager_initialization_redis(self, mock_cached_session):
        """Test cache manager initialization with Redis backend."""
        config = CacheConfig(backend="redis", redis_url="redis://localhost:6379")
        manager = AdvancedCacheManager(config)

        self.assertTrue(manager.is_enabled())
        mock_cached_session.assert_called_once()

    def test_cache_manager_initialization_redis_no_url(self):
        """Test cache manager initialization with Redis backend but no URL."""
        config = CacheConfig(backend="redis")

        with self.assertRaises(ValueError) as context:
            AdvancedCacheManager(config)

        self.assertIn("Redis URL is required", str(context.exception))

    def test_cache_manager_initialization_invalid_backend(self):
        """Test cache manager initialization with invalid backend."""
        config = CacheConfig(backend="invalid")

        with self.assertRaises(ValueError) as context:
            AdvancedCacheManager(config)

        self.assertIn("Unsupported cache backend", str(context.exception))

    def test_create_cache_key(self):
        """Test cache key creation."""
        AdvancedCacheManager(self.config)

        # Mock request
        mock_request = MagicMock()
        mock_request.method = "GET"
        mock_request.url = "https://api.example.com/test"
        mock_request.headers = {"Authorization": "Bearer token123"}
        mock_request.body = None

        key = create_cache_key(mock_request)
        self.assertIsInstance(key, str)
        self.assertTrue(key.startswith("ffbb_api:"))

    def test_create_cache_key_with_body(self):
        """Test cache key creation with request body."""
        AdvancedCacheManager(self.config)

        mock_request = MagicMock()
        mock_request.method = "POST"
        mock_request.url = "https://api.example.com/test"
        mock_request.headers = {}
        mock_request.body = "test data"

        key = create_cache_key(mock_request)
        self.assertIsInstance(key, str)
        self.assertTrue(key.startswith("ffbb_api:"))

    def test_cache_operations(self):
        """Test basic cache operations."""
        manager = AdvancedCacheManager(self.config)

        # Test cache size (may not be available for all backends)
        size = manager.get_cache_size()
        self.assertIsInstance(size, int)

        # Test metrics
        metrics = manager.get_metrics()
        self.assertIsInstance(metrics, CacheMetrics)

        # Test clear cache
        manager.clear_cache()  # Should not raise an exception

    def test_warm_cache(self):
        """Test cache warming functionality."""
        manager = AdvancedCacheManager(self.config)

        urls = ["https://api.example.com/test1", "https://api.example.com/test2"]
        headers = {"Authorization": "Bearer token"}

        # This should not raise an exception even if URLs are not reachable
        manager.warm_cache(urls, headers)

    def test_invalidate_pattern(self):
        """Test cache invalidation by pattern."""
        manager = AdvancedCacheManager(self.config)

        # This should not raise an exception
        manager.invalidate_pattern("test_pattern")

    def test_get_cache_manager_singleton(self):
        """Test that get_cache_manager returns a singleton."""
        from ffbb_api_client_v2.utils.cache_manager import get_cache_manager

        manager1 = get_cache_manager()
        manager2 = get_cache_manager()

        self.assertIs(manager1, manager2)

    def test_backward_compatibility(self):
        """Test backward compatibility functions."""
        from ffbb_api_client_v2.utils.cache_manager import default_cached_session

        self.assertIsNotNone(default_cached_session)

    def test_cache_key_masking(self):
        """Test that authorization headers are masked in cache keys."""
        AdvancedCacheManager(self.config)

        mock_request = MagicMock()
        mock_request.method = "GET"
        mock_request.url = "https://api.example.com/test"
        mock_request.headers = {"Authorization": "Bearer sensitive_token_123"}
        mock_request.body = None

        key1 = create_cache_key(mock_request)
        key2 = create_cache_key(mock_request)

        # Same request should generate same key
        self.assertEqual(key1, key2)

        # Test that different auth tokens produce the same key (masked)
        mock_request_different_auth = MagicMock()
        mock_request_different_auth.method = "GET"
        mock_request_different_auth.url = "https://api.example.com/test"
        mock_request_different_auth.headers = {
            "Authorization": "Bearer different_token_456"
        }
        mock_request_different_auth.body = None

        key3 = create_cache_key(mock_request_different_auth)

        # Different auth tokens should produce the same key (because auth is masked)
        self.assertEqual(key1, key3)


if __name__ == "__main__":
    unittest.main()
