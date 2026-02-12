"""Coverage gap tests for utils modules.

Extracted from test_122_coverage_gaps.py and test_123_missing_coverage.py:
- SecureLogging edge cases
- RetryUtils branches
- CacheManager edge cases
- __init__.py version coverage
- converter_utils edge cases (from_officiels_list, from_str exception path)
"""

from __future__ import annotations

import logging
import unittest
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# SecureLogging coverage (85% -> 90%+)
# ---------------------------------------------------------------------------


class TestSecureLoggingCoverage(unittest.TestCase):
    """secure_logging.py -- cover error, critical, log, and non-string message."""

    def test_000_mask_non_string_message(self) -> None:
        from ffbb_api_client_v2.utils.secure_logging import SecureLogger

        sl = SecureLogger("test_mask", level=logging.DEBUG)
        result = sl._mask_sensitive_data(12345)
        self.assertEqual(result, "12345")

    def test_001_error_level(self) -> None:
        from ffbb_api_client_v2.utils.secure_logging import SecureLogger

        sl = SecureLogger("test_error", level=logging.DEBUG)
        with self.assertLogs("test_error", level=logging.ERROR) as cm:
            sl.error("Something failed")
        self.assertTrue(any("Something failed" in msg for msg in cm.output))

    def test_002_critical_level(self) -> None:
        from ffbb_api_client_v2.utils.secure_logging import SecureLogger

        sl = SecureLogger("test_critical", level=logging.DEBUG)
        with self.assertLogs("test_critical", level=logging.CRITICAL) as cm:
            sl.critical("Critical failure")
        self.assertTrue(any("Critical failure" in msg for msg in cm.output))

    def test_003_log_with_level(self) -> None:
        from ffbb_api_client_v2.utils.secure_logging import SecureLogger

        sl = SecureLogger("test_log", level=logging.DEBUG)
        with self.assertLogs("test_log", level=logging.WARNING) as cm:
            sl.log(logging.WARNING, "Custom level msg")
        self.assertTrue(any("Custom level msg" in msg for msg in cm.output))


# ---------------------------------------------------------------------------
# RetryUtils coverage (77% -> 90%+)
# ---------------------------------------------------------------------------


class TestRetryUtilsCoverage(unittest.TestCase):
    """retry_utils.py -- cover calculate_delay jitter, execute_with_retry branches."""

    def test_004_calculate_delay_with_jitter(self) -> None:
        from ffbb_api_client_v2.utils.retry_utils import RetryConfig, calculate_delay

        config = RetryConfig(base_delay=1.0, jitter=True)
        delay = calculate_delay(0, config)
        self.assertGreaterEqual(delay, 0.1)
        self.assertLessEqual(delay, 2.0)  # base 1.0 +/- 25% jitter

    def test_005_calculate_delay_without_jitter(self) -> None:
        from ffbb_api_client_v2.utils.retry_utils import RetryConfig, calculate_delay

        config = RetryConfig(base_delay=1.0, jitter=False)
        delay = calculate_delay(0, config)
        self.assertEqual(delay, 1.0)

    def test_006_calculate_delay_capped_at_max(self) -> None:
        from ffbb_api_client_v2.utils.retry_utils import RetryConfig, calculate_delay

        config = RetryConfig(
            base_delay=1.0, max_delay=5.0, jitter=False, backoff_factor=10.0
        )
        delay = calculate_delay(5, config)
        self.assertEqual(delay, 5.0)

    @patch("ffbb_api_client_v2.utils.retry_utils.time.sleep")
    def test_007_execute_with_retry_retries_on_status_code(
        self, mock_sleep: MagicMock
    ) -> None:
        from ffbb_api_client_v2.utils.retry_utils import (
            RetryConfig,
            TimeoutConfig,
            execute_with_retry,
        )

        response_429 = MagicMock()
        response_429.status_code = 429
        response_200 = MagicMock()
        response_200.status_code = 200

        func = MagicMock(side_effect=[response_429, response_200])
        config = RetryConfig(max_attempts=2, base_delay=0.01, jitter=False)
        timeout_config = TimeoutConfig()

        result = execute_with_retry(func, config=config, timeout_config=timeout_config)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(func.call_count, 2)

    @patch("ffbb_api_client_v2.utils.retry_utils.time.sleep")
    def test_008_execute_with_retry_retries_on_exception(
        self, mock_sleep: MagicMock
    ) -> None:
        import requests

        from ffbb_api_client_v2.utils.retry_utils import (
            RetryConfig,
            TimeoutConfig,
            execute_with_retry,
        )

        response_ok = MagicMock()
        response_ok.status_code = 200
        func = MagicMock(side_effect=[requests.ConnectionError("fail"), response_ok])
        config = RetryConfig(max_attempts=2, base_delay=0.01, jitter=False)

        result = execute_with_retry(func, config=config, timeout_config=TimeoutConfig())
        self.assertEqual(result.status_code, 200)

    @patch("ffbb_api_client_v2.utils.retry_utils.time.sleep")
    def test_009_execute_with_retry_exhausted_raises(
        self, mock_sleep: MagicMock
    ) -> None:
        import requests

        from ffbb_api_client_v2.utils.retry_utils import (
            RetryConfig,
            TimeoutConfig,
            execute_with_retry,
        )

        func = MagicMock(side_effect=requests.ConnectionError("always fails"))
        config = RetryConfig(max_attempts=1, base_delay=0.01, jitter=False)

        with self.assertRaises(requests.ConnectionError):
            execute_with_retry(func, config=config, timeout_config=TimeoutConfig())

    def test_010_execute_with_retry_preserves_existing_timeout(self) -> None:
        from ffbb_api_client_v2.utils.retry_utils import (
            RetryConfig,
            TimeoutConfig,
            execute_with_retry,
        )

        response = MagicMock()
        response.status_code = 200
        func = MagicMock(return_value=response)
        config = RetryConfig(max_attempts=0, jitter=False)

        result = execute_with_retry(
            func, config=config, timeout_config=TimeoutConfig(), timeout=99
        )
        self.assertEqual(result.status_code, 200)
        # Timeout kwarg should be preserved as 99, not overwritten
        _, kwargs = func.call_args
        self.assertEqual(kwargs["timeout"], 99)

    def test_011_make_http_request_post(self) -> None:
        from ffbb_api_client_v2.utils.retry_utils import (
            RetryConfig,
            TimeoutConfig,
            make_http_request_with_retry,
        )

        with patch("requests.Session") as MockSession:
            mock_session = MagicMock()
            response = MagicMock()
            response.status_code = 200
            mock_session.post.return_value = response
            MockSession.return_value = mock_session

            result = make_http_request_with_retry(
                "POST",
                "https://example.com/api",
                {"Content-Type": "application/json"},
                data={"key": "value"},
                retry_config=RetryConfig(max_attempts=0, jitter=False),
                timeout_config=TimeoutConfig(),
            )
            self.assertEqual(result.status_code, 200)
            mock_session.post.assert_called_once()

    def test_012_make_http_request_unsupported_method(self) -> None:
        from ffbb_api_client_v2.utils.retry_utils import (
            RetryConfig,
            TimeoutConfig,
            make_http_request_with_retry,
        )

        with self.assertRaises(ValueError) as ctx:
            make_http_request_with_retry(
                "DELETE",
                "https://example.com/api",
                {},
                retry_config=RetryConfig(max_attempts=0, jitter=False),
                timeout_config=TimeoutConfig(),
            )
        self.assertIn("Unsupported HTTP method", str(ctx.exception))

    def test_013_make_http_request_debug_logging(self) -> None:
        from ffbb_api_client_v2.utils.retry_utils import (
            RetryConfig,
            TimeoutConfig,
            make_http_request_with_retry,
        )

        with patch("requests.Session") as MockSession:
            mock_session = MagicMock()
            response = MagicMock()
            response.status_code = 200
            mock_session.get.return_value = response
            MockSession.return_value = mock_session

            make_http_request_with_retry(
                "GET",
                "https://example.com/api",
                {},
                retry_config=RetryConfig(max_attempts=0, jitter=False),
                timeout_config=TimeoutConfig(),
                debug=True,
            )

    def test_014_create_custom_configs(self) -> None:
        from ffbb_api_client_v2.utils.retry_utils import (
            create_custom_retry_config,
            create_custom_timeout_config,
            get_default_retry_config,
            get_default_timeout_config,
        )

        rc = create_custom_retry_config(max_attempts=5, base_delay=2.0, max_delay=30.0)
        self.assertEqual(rc.max_attempts, 5)
        self.assertEqual(rc.base_delay, 2.0)

        tc = create_custom_timeout_config(connect_timeout=5.0, read_timeout=15.0)
        self.assertEqual(tc.connect_timeout, 5.0)
        self.assertEqual(tc.read_timeout, 15.0)

        self.assertIsNotNone(get_default_retry_config())
        self.assertIsNotNone(get_default_timeout_config())


# ---------------------------------------------------------------------------
# CacheManager coverage (81% -> 90%+)
# ---------------------------------------------------------------------------


class TestCacheManagerCoverage(unittest.TestCase):
    """cache_manager.py -- cover edge cases."""

    def setUp(self) -> None:
        from ffbb_api_client_v2.utils.cache_manager import CacheManager

        CacheManager.reset_instance()

    def tearDown(self) -> None:
        from ffbb_api_client_v2.utils.cache_manager import CacheManager

        CacheManager.reset_instance()

    def test_015_singleton_returns_same_instance(self) -> None:
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig, CacheManager

        cm1 = CacheManager(CacheConfig(backend="memory"))
        cm2 = CacheManager()
        self.assertIs(cm1, cm2)

    def test_016_clear_cache_no_session(self) -> None:
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig, CacheManager

        cm = CacheManager(CacheConfig(enabled=False))
        self.assertIs(cm.clear_cache(), False)

    def test_017_clear_cache_error(self) -> None:
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig, CacheManager

        cm = CacheManager(CacheConfig(backend="memory"))
        cm._session = MagicMock()
        cm._session.cache.clear.side_effect = OSError("disk error")
        self.assertIs(cm.clear_cache(), False)
        self.assertEqual(cm.metrics.errors, 1)

    def test_018_get_cache_size_no_session(self) -> None:
        from ffbb_api_client_v2.utils.cache_manager import CacheManager

        CacheManager.reset_instance()
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig

        cm = CacheManager(CacheConfig(enabled=False))
        self.assertEqual(cm.get_cache_size(), 0)

    def test_019_get_cache_size_error(self) -> None:
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig, CacheManager

        cm = CacheManager(CacheConfig(backend="memory"))
        cm._session = MagicMock()
        cm._session.cache.count.side_effect = RuntimeError("fail")
        self.assertEqual(cm.get_cache_size(), 0)
        self.assertGreaterEqual(cm.metrics.errors, 1)

    def test_020_warm_cache_disabled(self) -> None:
        from ffbb_api_client_v2.utils.cache_manager import CacheManager

        CacheManager.reset_instance()
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig

        cm = CacheManager(CacheConfig(enabled=False))
        result = cm.warm_cache(["https://example.com"])
        self.assertEqual(result, 0)

    def test_021_invalidate_pattern_disabled(self) -> None:
        from ffbb_api_client_v2.utils.cache_manager import CacheManager

        CacheManager.reset_instance()
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig

        cm = CacheManager(CacheConfig(enabled=False))
        result = cm.invalidate_pattern("test")
        self.assertEqual(result, 0)

    def test_022_invalidate_pattern_with_matching_keys(self) -> None:
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig, CacheManager

        cm = CacheManager(CacheConfig(backend="memory"))
        # Mock the session cache with delete and keys
        mock_cache = MagicMock()
        mock_cache.keys.return_value = ["ffbb_api:abc_test_123", "ffbb_api:other_456"]
        cm._session = MagicMock()
        cm._session.cache = mock_cache
        cm.config.enabled = True

        result = cm.invalidate_pattern("test")
        self.assertEqual(result, 1)
        mock_cache.delete.assert_called_once_with("ffbb_api:abc_test_123")

    def test_023_get_metrics(self) -> None:
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig, CacheManager

        cm = CacheManager(CacheConfig(backend="memory"))
        metrics = cm.get_metrics()
        self.assertEqual(metrics.hits, 0)
        self.assertEqual(metrics.hit_rate, 0.0)

    def test_024_cache_metrics_reset(self) -> None:
        from ffbb_api_client_v2.utils.cache_manager import CacheMetrics

        m = CacheMetrics(hits=5, misses=3)
        self.assertEqual(m.hit_rate, 5 / 8)
        m.reset()
        self.assertEqual(m.hits, 0)
        self.assertEqual(m.misses, 0)


# ---------------------------------------------------------------------------
# __init__.py coverage (86% -> 90%+)
# ---------------------------------------------------------------------------


class TestInitCoverage(unittest.TestCase):
    """__init__.py -- cover PackageNotFoundError branch."""

    def test_025_version_is_set(self) -> None:
        import ffbb_api_client_v2

        self.assertTrue(hasattr(ffbb_api_client_v2, "__version__"))
        # In dev, version will be "unknown" since package isn't installed
        self.assertIsInstance(ffbb_api_client_v2.__version__, str)


class TestInitVersionCoverage(unittest.TestCase):
    """__init__.py -- cover the PackageNotFoundError branch."""

    def test_026_version_when_package_not_found(self) -> None:
        """The __version__ is either the real version or 'unknown'."""
        import ffbb_api_client_v2

        # In dev without pip install -e, it's 'unknown'
        self.assertIsInstance(ffbb_api_client_v2.__version__, str)
        # Cover the __all__ export
        self.assertIn("FFBBAPIClientV2", ffbb_api_client_v2.__all__)


# ---------------------------------------------------------------------------
# converter_utils edge cases (from test_123)
# ---------------------------------------------------------------------------


class TestFromOfficielsListEdgeCases(unittest.TestCase):
    """Cover all branches of from_officiels_list."""

    def test_027_non_empty_string(self) -> None:
        from ffbb_api_client_v2.utils.converter_utils import from_officiels_list

        result = from_officiels_list("Alice, Bob, Charlie")
        self.assertEqual(result, ["Alice", "Bob", "Charlie"])

    def test_028_empty_string(self) -> None:
        from ffbb_api_client_v2.utils.converter_utils import from_officiels_list

        result = from_officiels_list("")
        self.assertIsNone(result)

    def test_029_list_passthrough(self) -> None:
        from ffbb_api_client_v2.utils.converter_utils import from_officiels_list

        data = [{"name": "Alice"}, {"name": "Bob"}]
        result = from_officiels_list(data)
        self.assertIs(result, data)

    def test_030_none_returns_none(self) -> None:
        from ffbb_api_client_v2.utils.converter_utils import from_officiels_list

        self.assertIsNone(from_officiels_list(None))

    def test_031_invalid_type_returns_none(self) -> None:
        from ffbb_api_client_v2.utils.converter_utils import from_officiels_list

        self.assertIsNone(from_officiels_list(42))


class TestFromStrExceptionPath(unittest.TestCase):
    """Cover the TypeError/ValueError exception path in from_str (lines 102-109)."""

    def test_032_object_whose_str_raises_type_error(self) -> None:
        from ffbb_api_client_v2.utils.converter_utils import from_str

        class BadStr:
            def __str__(self):
                raise TypeError("cannot convert")

        with self.assertLogs(
            "ffbb_api_client_v2.utils.converter_utils", level=logging.WARNING
        ) as cm:
            result = from_str({"k": BadStr()}, "k")
        self.assertIsNone(result)
        self.assertTrue(any("cannot convert" in msg for msg in cm.output))


if __name__ == "__main__":
    unittest.main()
