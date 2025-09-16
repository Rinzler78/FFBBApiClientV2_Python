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

    def test_default_configs(self):
        """Test default retry and timeout configurations."""
        retry_config = get_default_retry_config()
        timeout_config = get_default_timeout_config()

        self.assertIsInstance(retry_config, RetryConfig)
        self.assertIsInstance(timeout_config, TimeoutConfig)
        self.assertEqual(retry_config.max_attempts, 3)
        self.assertEqual(timeout_config.connect_timeout, 10.0)
        self.assertEqual(timeout_config.read_timeout, 30.0)

    def test_custom_configs(self):
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

    def test_calculate_delay(self):
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

    def test_calculate_delay_with_max(self):
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

    def test_should_retry_success_response(self):
        """Test should_retry with successful response."""
        from requests import Response

        response = Response()
        response.status_code = 200

        should = should_retry(0, response, None, self.retry_config)
        self.assertFalse(should)

    def test_should_retry_retryable_status(self):
        """Test should_retry with retryable status codes."""
        from unittest.mock import MagicMock

        # Create a mock response with status_code
        response = MagicMock()
        response.status_code = 429  # Too Many Requests

        should = should_retry(0, response, None, self.retry_config)
        self.assertTrue(should)

    def test_should_retry_max_attempts(self):
        """Test should_retry with retryable status codes."""
        from unittest.mock import MagicMock

        response = MagicMock()
        response.status_code = 500

        # Should retry on retryable status codes regardless of attempt number
        should = should_retry(0, response, None, self.retry_config)
        self.assertTrue(should)

        should = should_retry(3, response, None, self.retry_config)
        self.assertTrue(should)

    def test_should_retry_exception(self):
        """Test should_retry with exceptions."""
        exception = ConnectionError("Connection failed")

        should = should_retry(0, None, exception, self.retry_config)
        self.assertTrue(should)

    def test_execute_with_retry_success(self):
        """Test execute_with_retry with successful function."""

        def success_func(**kwargs):
            return "success"

        result = execute_with_retry(success_func, self.retry_config)
        self.assertEqual(result, "success")

    def test_execute_with_retry_failure_then_success(self):
        """Test execute_with_retry with failure then success."""
        call_count = 0

        def failing_func(**kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Temporary failure")
            return "success"

        result = execute_with_retry(failing_func, self.retry_config)
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)

    def test_execute_with_retry_max_retries_exceeded(self):
        """Test execute_with_retry when max retries are exceeded."""

        def always_failing_func(**kwargs):
            raise ConnectionError("Always fails")

        with self.assertRaises(ConnectionError):
            execute_with_retry(always_failing_func, self.retry_config)

    @patch("time.sleep")
    def test_execute_with_retry_delays(self, mock_sleep):
        """Test that execute_with_retry applies delays between retries."""
        call_count = 0

        def failing_func(**kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Temporary failure")
            return "success"

        result = execute_with_retry(failing_func, self.retry_config)
        self.assertEqual(result, "success")

        # Should have slept twice (after attempt 1 and 2)
        self.assertEqual(mock_sleep.call_count, 2)
        mock_sleep.assert_any_call(1.0)  # First delay
        mock_sleep.assert_any_call(2.0)  # Second delay

    def test_timeout_config_total_timeout(self):
        """Test that TimeoutConfig calculates total_timeout correctly."""
        config = TimeoutConfig(connect_timeout=5.0, read_timeout=15.0)
        self.assertEqual(config.total_timeout, 20.0)

        # Test with explicit total_timeout
        config_explicit = TimeoutConfig(
            connect_timeout=5.0, read_timeout=15.0, total_timeout=25.0
        )
        self.assertEqual(config_explicit.total_timeout, 25.0)

    def test_retry_config_defaults(self):
        """Test RetryConfig default values."""
        config = RetryConfig()

        self.assertEqual(config.max_attempts, 3)
        self.assertEqual(config.base_delay, 1.0)
        self.assertEqual(config.max_delay, 60.0)
        self.assertEqual(config.backoff_factor, 2.0)
        self.assertTrue(config.jitter)
        self.assertEqual(config.retry_on_status_codes, [429, 500, 502, 503, 504])
        self.assertEqual(
            config.retry_on_exceptions, (Exception, ConnectionError, TimeoutError)
        )


if __name__ == "__main__":
    unittest.main()
