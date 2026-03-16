"""
Tests for retry and timeout functionality.
"""

import unittest
from unittest.mock import patch

from ffbb_api_client_v2.utils.retry_utils import (
    RetryConfig,
    TimeoutConfig,
    calculate_delay,
    create_custom_retry_config,
    create_custom_timeout_config,
    execute_with_retry,
    get_default_retry_config,
    get_default_timeout_config,
    should_retry,
)


class Test016RetryTimeout(unittest.TestCase):
    """Test cases for retry and timeout functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.retry_config = RetryConfig(
            max_attempts=3,
            base_delay=1.0,
            max_delay=10.0,
            backoff_factor=2.0,
            jitter=False,  # Disable jitter for predictable tests
        )
        self.timeout_config = TimeoutConfig(
            connect_timeout=5.0,
            read_timeout=10.0,
        )

    def test_000_default_configs(self):
        """Test default retry and timeout configurations."""
        retry_config = get_default_retry_config()
        timeout_config = get_default_timeout_config()

        self.assertIsInstance(retry_config, RetryConfig)
        self.assertIsInstance(timeout_config, TimeoutConfig)
        self.assertEqual(retry_config.max_attempts, 3)
        self.assertEqual(timeout_config.connect_timeout, 10.0)
        self.assertEqual(timeout_config.read_timeout, 30.0)

    def test_001_custom_configs(self):
        """Test custom retry and timeout configurations."""
        retry_config = create_custom_retry_config(max_attempts=5, base_delay=2.0)
        timeout_config = create_custom_timeout_config(
            connect_timeout=3.0, read_timeout=15.0
        )

        self.assertEqual(retry_config.max_attempts, 5)
        self.assertEqual(retry_config.base_delay, 2.0)
        self.assertEqual(timeout_config.connect_timeout, 3.0)
        self.assertEqual(timeout_config.read_timeout, 15.0)
        self.assertEqual(timeout_config.total_timeout, 18.0)  # 3 + 15

    def test_002_calculate_delay(self):
        """Test delay calculation for retries."""
        # First retry (attempt 0)
        delay = calculate_delay(0, self.retry_config)
        self.assertEqual(delay, 1.0)

        # Second retry (attempt 1)
        delay = calculate_delay(1, self.retry_config)
        self.assertEqual(delay, 2.0)

        # Third retry (attempt 2)
        delay = calculate_delay(2, self.retry_config)
        self.assertEqual(delay, 4.0)

    def test_003_calculate_delay_with_max(self):
        """Test delay calculation respects max_delay."""
        config = RetryConfig(
            max_attempts=3,
            base_delay=1.0,
            max_delay=3.0,
            backoff_factor=10.0,
            jitter=False,
        )
        delay = calculate_delay(2, config)  # 1 * (10^2) = 100, but max is 3
        self.assertEqual(delay, 3.0)

    def test_004_should_retry_success_response(self):
        """Test should_retry with successful response."""
        from requests import Response

        response = Response()
        response.status_code = 200

        should = should_retry(0, response, None, self.retry_config)
        self.assertFalse(should)

    def test_005_should_retry_retryable_status(self):
        """Test should_retry with retryable status codes."""
        from unittest.mock import MagicMock

        # Create a mock response with status_code
        response = MagicMock()
        response.status_code = 429  # Too Many Requests

        should = should_retry(0, response, None, self.retry_config)
        self.assertTrue(should)

    def test_006_should_retry_max_attempts(self):
        """Test should_retry with retryable status codes."""
        from unittest.mock import MagicMock

        response = MagicMock()
        response.status_code = 500

        # Should retry on retryable status codes regardless of attempt number
        should = should_retry(0, response, None, self.retry_config)
        self.assertTrue(should)

        should = should_retry(3, response, None, self.retry_config)
        self.assertTrue(should)

    def test_007_should_retry_exception(self):
        """Test should_retry with exceptions."""
        exception = ConnectionError("Connection failed")

        should = should_retry(0, None, exception, self.retry_config)
        self.assertTrue(should)

    def test_008_execute_with_retry_success(self):
        """Test execute_with_retry with successful function."""

        def success_func(**kwargs):
            return "success"

        result = execute_with_retry(success_func, config=self.retry_config)
        self.assertEqual(result, "success")

    def test_009_execute_with_retry_failure_then_success(self):
        """Test execute_with_retry with failure then success."""
        call_count = 0

        def failing_func(**kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Temporary failure")
            return "success"

        result = execute_with_retry(failing_func, config=self.retry_config)
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)

    def test_010_execute_with_retry_max_retries_exceeded(self):
        """Test execute_with_retry when max retries are exceeded."""

        def always_failing_func(**kwargs):
            raise ConnectionError("Always fails")

        with self.assertRaises(ConnectionError):
            execute_with_retry(always_failing_func, config=self.retry_config)

    @patch("time.sleep")
    def test_011_execute_with_retry_delays(self, mock_sleep):
        """Test that execute_with_retry applies delays between retries."""
        call_count = 0

        def failing_func(**kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Temporary failure")
            return "success"

        result = execute_with_retry(failing_func, config=self.retry_config)
        self.assertEqual(result, "success")

        # Should have slept twice (after attempt 1 and 2)
        self.assertEqual(mock_sleep.call_count, 2)
        mock_sleep.assert_any_call(1.0)  # First delay
        mock_sleep.assert_any_call(2.0)  # Second delay

    def test_012_timeout_config_total_timeout(self):
        """Test that TimeoutConfig calculates total_timeout correctly."""
        config = TimeoutConfig(connect_timeout=5.0, read_timeout=15.0)
        self.assertEqual(config.total_timeout, 20.0)

        # Test with explicit total_timeout
        config_explicit = TimeoutConfig(
            connect_timeout=5.0, read_timeout=15.0, total_timeout=25.0
        )
        self.assertEqual(config_explicit.total_timeout, 25.0)

    def test_013_retry_config_defaults(self):
        """Test RetryConfig default values."""
        config = RetryConfig()

        self.assertEqual(config.max_attempts, 3)
        self.assertEqual(config.base_delay, 1.0)
        self.assertEqual(config.max_delay, 60.0)
        self.assertEqual(config.backoff_factor, 2.0)
        self.assertTrue(config.jitter)
        self.assertEqual(config.retry_on_status_codes, [429, 500, 502, 503, 504])
        import requests

        self.assertEqual(
            config.retry_on_exceptions,
            (requests.RequestException, ConnectionError, TimeoutError),
        )


class Test016RetryTimeoutCoverage(unittest.TestCase):
    """Additional tests to reach > 95% coverage on retry_utils."""

    def setUp(self):
        self.retry_config_no_jitter = RetryConfig(
            max_attempts=2,
            base_delay=0.001,
            max_delay=1.0,
            backoff_factor=2.0,
            jitter=False,
        )
        self.timeout_config = TimeoutConfig(connect_timeout=1.0, read_timeout=2.0)

    # ---- calculate_delay with jitter ----

    def test_014_calculate_delay_with_jitter(self):
        """Test calculate_delay when jitter=True adds randomness."""
        config = RetryConfig(
            max_attempts=3,
            base_delay=1.0,
            max_delay=60.0,
            backoff_factor=2.0,
            jitter=True,
        )
        delay = calculate_delay(0, config)
        # Jitter is ±25% so delay must be between 0.75 and 1.25 (or at least > 0.1)
        self.assertGreater(delay, 0.1)
        self.assertLess(delay, 2.0)

    def test_015_calculate_delay_jitter_clamps_to_minimum(self):
        """Test that jitter delay is always >= 0.1."""
        config = RetryConfig(
            max_attempts=1,
            base_delay=0.001,
            max_delay=0.002,
            backoff_factor=1.0,
            jitter=True,
        )
        for _ in range(20):
            delay = calculate_delay(0, config)
            self.assertGreaterEqual(delay, 0.1)

    # ---- execute_with_retry: retry on bad status code ----

    @patch("time.sleep")
    def test_016_execute_with_retry_retries_on_bad_status(self, mock_sleep):
        """Test retry on HTTP 429 status code."""
        from unittest.mock import MagicMock

        call_count = 0

        def flaky_func(**kwargs):
            nonlocal call_count
            call_count += 1
            resp = MagicMock()
            resp.status_code = 429 if call_count < 3 else 200
            return resp

        config = RetryConfig(max_attempts=3, base_delay=0.001, jitter=False)
        result = execute_with_retry(flaky_func, config=config)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)

    @patch("time.sleep")
    def test_017_execute_with_retry_exhausts_on_bad_status(self, mock_sleep):
        """Test that last response returned after all retries on bad status."""
        from unittest.mock import MagicMock

        def always_429(**kwargs):
            resp = MagicMock()
            resp.status_code = 429
            return resp

        config = RetryConfig(max_attempts=2, base_delay=0.001, jitter=False)
        result = execute_with_retry(always_429, config=config)
        # Returns last response even if still retryable
        self.assertEqual(result.status_code, 429)

    # ---- execute_with_retry: non-retryable exception ----

    def test_018_execute_with_retry_non_retryable_raises(self):
        """Test that non-retryable exceptions are raised immediately."""

        def raises_value_error(**kwargs):
            raise ValueError("Not retryable")

        config = RetryConfig(max_attempts=3, base_delay=0.001, jitter=False)
        with self.assertRaises(ValueError):
            execute_with_retry(raises_value_error, config=config)

    # ---- execute_with_retry: timeout already in kwargs ----

    @patch("time.sleep")
    def test_019_execute_with_retry_timeout_already_set(self, mock_sleep):
        """Test that existing timeout kwarg is not overridden."""
        received_timeout = []

        def capture_timeout(**kwargs):
            received_timeout.append(kwargs.get("timeout"))
            return "ok"

        execute_with_retry(
            capture_timeout, config=self.retry_config_no_jitter, timeout=99
        )
        self.assertEqual(received_timeout[0], 99)

    # ---- make_http_request_with_retry ----

    def test_020_make_http_request_get(self):
        """Test make_http_request_with_retry with GET method (mocked session)."""
        from unittest.mock import MagicMock, patch

        from ffbb_api_client_v2.utils.retry_utils import make_http_request_with_retry

        mock_response = MagicMock()
        mock_response.status_code = 200

        with patch("requests.Session") as mock_session_cls:
            mock_session = MagicMock()
            mock_session.get.return_value = mock_response
            mock_session_cls.return_value = mock_session

            config = RetryConfig(max_attempts=1, base_delay=0.001, jitter=False)
            result = make_http_request_with_retry(
                "GET",
                "https://example.com",
                {"Authorization": "Bearer token"},
                retry_config=config,
                timeout_config=self.timeout_config,
            )
        self.assertEqual(result.status_code, 200)

    def test_021_make_http_request_post(self):
        """Test make_http_request_with_retry with POST method."""
        from unittest.mock import MagicMock, patch

        from ffbb_api_client_v2.utils.retry_utils import make_http_request_with_retry

        mock_response = MagicMock()
        mock_response.status_code = 201

        with patch("requests.Session") as mock_session_cls:
            mock_session = MagicMock()
            mock_session.post.return_value = mock_response
            mock_session_cls.return_value = mock_session

            config = RetryConfig(max_attempts=1, base_delay=0.001, jitter=False)
            result = make_http_request_with_retry(
                "POST",
                "https://example.com",
                {"Content-Type": "application/json"},
                data={"key": "value"},
                retry_config=config,
                timeout_config=self.timeout_config,
            )
        self.assertEqual(result.status_code, 201)

    def test_022_make_http_request_unsupported_method(self):
        """Test make_http_request_with_retry raises on unsupported HTTP method."""
        from ffbb_api_client_v2.utils.retry_utils import make_http_request_with_retry

        config = RetryConfig(max_attempts=1, base_delay=0.001, jitter=False)
        with self.assertRaises(ValueError):
            make_http_request_with_retry(
                "DELETE", "https://example.com", {}, retry_config=config
            )

    def test_023_make_http_request_with_debug(self):
        """Test make_http_request_with_retry with debug=True."""
        from unittest.mock import MagicMock, patch

        from ffbb_api_client_v2.utils.retry_utils import make_http_request_with_retry

        mock_response = MagicMock()
        mock_response.status_code = 200

        with patch("requests.Session") as mock_session_cls:
            mock_session = MagicMock()
            mock_session.get.return_value = mock_response
            mock_session_cls.return_value = mock_session

            config = RetryConfig(max_attempts=1, base_delay=0.001, jitter=False)
            result = make_http_request_with_retry(
                "GET", "https://example.com", {}, retry_config=config, debug=True
            )
        self.assertEqual(result.status_code, 200)

    def test_024_make_http_request_with_cached_session(self):
        """Test make_http_request_with_retry uses cached session when provided."""
        from unittest.mock import MagicMock

        from ffbb_api_client_v2.utils.retry_utils import make_http_request_with_retry

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_cached_session = MagicMock()
        mock_cached_session.get.return_value = mock_response

        config = RetryConfig(max_attempts=1, base_delay=0.001, jitter=False)
        result = make_http_request_with_retry(
            "GET",
            "https://example.com",
            {},
            cached_session=mock_cached_session,
            retry_config=config,
        )
        mock_cached_session.get.assert_called_once()
        self.assertEqual(result.status_code, 200)

    # ---- should_retry edge cases ----

    def test_025_should_retry_no_exception_no_response(self):
        """Test should_retry returns False with no exception and no response."""
        config = RetryConfig(max_attempts=3, jitter=False)
        self.assertFalse(should_retry(0, None, None, config))

    def test_026_should_retry_non_retryable_exception(self):
        """Test should_retry returns False for non-retryable exception."""
        config = RetryConfig(
            max_attempts=3, retry_on_exceptions=(ValueError,), jitter=False
        )
        exc = RuntimeError("not retryable")
        self.assertFalse(should_retry(0, None, exc, config))

    def test_027_should_retry_retryable_exception_type(self):
        """Test should_retry returns True for configured exception type."""
        config = RetryConfig(
            max_attempts=3, retry_on_exceptions=(ValueError,), jitter=False
        )
        exc = ValueError("retryable")
        self.assertTrue(should_retry(0, None, exc, config))

    def test_028_execute_with_retry_oserror_not_retried(self):
        """Test that OSError (caught but not in retry_on_exceptions) raises immediately."""
        # Default retry_on_exceptions does not include OSError explicitly
        # OSError is caught in the except block but should_retry returns False
        config = RetryConfig(
            max_attempts=3,
            base_delay=0.001,
            jitter=False,
            retry_on_exceptions=(ValueError,),  # OSError not in list
        )

        def raises_oserror(**kwargs):
            raise OSError("disk error")

        with self.assertRaises(OSError):
            execute_with_retry(raises_oserror, config=config)


if __name__ == "__main__":
    unittest.main()
