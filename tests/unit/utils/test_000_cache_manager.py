"""
Tests for advanced cache management functionality.
"""

import unittest
from unittest.mock import MagicMock, patch

from ffbb_api_client_v2.utils.cache_manager import (
    CacheConfig,
    CacheManager,
    CacheMetrics,
)


class Test018CacheManager(unittest.TestCase):
    """Test cases for advanced cache management."""

    def setUp(self):
        """Set up test fixtures."""
        # Reset singleton before each test to ensure clean state
        CacheManager.reset_instance()
        self.config = CacheConfig(
            enabled=True,
            backend="memory",
            expire_after=1800,
            max_size=100,
        )

    def tearDown(self):
        """Clean up after each test."""
        # Reset singleton after each test
        CacheManager.reset_instance()

    def test_000_cache_config_defaults(self):
        """Test CacheConfig default values."""
        config = CacheConfig()

        self.assertTrue(config.enabled)
        self.assertEqual(config.backend, "sqlite")
        self.assertEqual(config.expire_after, 1800)
        self.assertEqual(config.max_size, 1000)
        self.assertIsNone(config.redis_url)
        self.assertEqual(config.key_prefix, "ffbb_api")
        self.assertFalse(config.compression)

    def test_001_cache_metrics(self):
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

    def test_002_cache_manager_initialization_memory(self):
        """Test cache manager initialization with memory backend."""
        config = CacheConfig(backend="memory")
        manager = CacheManager(config)

        self.assertTrue(manager.is_enabled())
        self.assertIsNotNone(manager.get_session())
        self.assertEqual(manager.config.backend, "memory")

    def test_003_cache_manager_initialization_sqlite(self):
        """Test cache manager initialization with SQLite backend."""
        CacheManager.reset_instance()  # Reset first
        config = CacheConfig(backend="sqlite")
        manager = CacheManager(config)

        self.assertTrue(manager.is_enabled())
        self.assertIsNotNone(manager.get_session())
        self.assertEqual(manager.config.backend, "sqlite")

    def test_004_cache_manager_initialization_disabled(self):
        """Test cache manager with caching disabled."""
        config = CacheConfig(enabled=False)
        manager = CacheManager(config)

        self.assertFalse(manager.is_enabled())
        self.assertIsNone(manager.get_session())

    @patch("ffbb_api_client_v2.utils.cache_manager.ThreadSafeCachedSession")
    def test_005_cache_manager_initialization_redis(self, mock_cached_session):
        """Test cache manager initialization with Redis backend."""
        config = CacheConfig(backend="redis", redis_url="redis://localhost:6379")
        manager = CacheManager(config)

        self.assertTrue(manager.is_enabled())
        mock_cached_session.assert_called_once()

    def test_006_cache_manager_initialization_redis_no_url(self):
        """Test cache manager initialization with Redis backend but no URL."""
        config = CacheConfig(backend="redis")

        with self.assertRaises(ValueError) as context:
            CacheManager(config)

        self.assertIn("Redis URL is required", str(context.exception))

    def test_007_cache_manager_initialization_invalid_backend(self):
        """Test cache manager initialization with invalid backend."""
        config = CacheConfig(backend="invalid")

        with self.assertRaises(ValueError) as context:
            CacheManager(config)

        self.assertIn("Unsupported cache backend", str(context.exception))

    def test_008_create_cache_key(self):
        """Test cache key creation."""
        manager = CacheManager(self.config)

        # Mock request
        mock_request = MagicMock()
        mock_request.method = "GET"
        mock_request.url = "https://api.example.com/test"
        mock_request.headers = {"Authorization": "Bearer token123"}
        mock_request.body = None

        key = manager.create_cache_key(mock_request)
        self.assertIsInstance(key, str)
        self.assertTrue(key.startswith("ffbb_api:"))

    def test_009_create_cache_key_with_body(self):
        """Test cache key creation with request body."""
        manager = CacheManager(self.config)

        mock_request = MagicMock()
        mock_request.method = "POST"
        mock_request.url = "https://api.example.com/test"
        mock_request.headers = {}
        mock_request.body = "test data"

        key = manager.create_cache_key(mock_request)
        self.assertIsInstance(key, str)
        self.assertTrue(key.startswith("ffbb_api:"))

    def test_010_cache_operations(self):
        """Test basic cache operations."""
        manager = CacheManager(self.config)

        # Test cache size (may not be available for all backends)
        size = manager.get_cache_size()
        self.assertIsInstance(size, int)

        # Test metrics
        metrics = manager.get_metrics()
        self.assertIsInstance(metrics, CacheMetrics)

        # Test clear cache
        manager.clear_cache()  # Should not raise an exception

    def test_011_warm_cache(self):
        """Test cache warming functionality."""
        manager = CacheManager(self.config)

        urls = ["https://api.example.com/test1", "https://api.example.com/test2"]
        headers = {"Authorization": "Bearer token"}

        # This should not raise an exception even if URLs are not reachable
        manager.warm_cache(urls, headers)

    def test_012_invalidate_pattern(self):
        """Test cache invalidation by pattern."""
        manager = CacheManager(self.config)

        # This should not raise an exception
        manager.invalidate_pattern("test_pattern")

    def test_013_singleton_pattern(self):
        """Test that CacheManager follows singleton pattern."""
        manager1 = CacheManager(self.config)
        manager2 = CacheManager()

        self.assertIs(manager1, manager2)

    def test_014_cache_key_masking(self):
        """Test that authorization headers are masked in cache keys."""
        manager = CacheManager(self.config)

        mock_request = MagicMock()
        mock_request.method = "GET"
        mock_request.url = "https://api.example.com/test"
        mock_request.headers = {"Authorization": "Bearer sensitive_token_123"}
        mock_request.body = None

        key1 = manager.create_cache_key(mock_request)
        key2 = manager.create_cache_key(mock_request)

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

        key3 = manager.create_cache_key(mock_request_different_auth)

        # Different auth tokens should produce the same key (because auth is masked)
        self.assertEqual(key1, key3)

    def test_015_reset_instance(self):
        """Test that reset_instance properly clears the singleton."""
        CacheManager(self.config)
        CacheManager.reset_instance()

        # Now create a new instance with different config
        new_config = CacheConfig(backend="sqlite")
        manager2 = CacheManager(new_config)

        # Should be a different backend since we reset
        self.assertEqual(manager2.config.backend, "sqlite")


if __name__ == "__main__":
    unittest.main()
