"""
Integration tests for retry and timeout in API clients.
"""

import unittest
from unittest.mock import MagicMock, patch

from ffbb_api_client_v2.clients.api_ffbb_app_client import ApiFFBBAppClient
from ffbb_api_client_v2.clients.meilisearch_client import MeilisearchClient
from ffbb_api_client_v2.utils.retry_utils import (
    RetryConfig,
    TimeoutConfig,
    create_custom_retry_config,
    create_custom_timeout_config,
)


class Test017RetryTimeoutIntegration(unittest.TestCase):
    """Integration tests for retry and timeout in API clients."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_token = "valid_test_token_123456789"
        self.custom_retry_config = create_custom_retry_config(
            max_attempts=2, base_delay=0.5
        )
        self.custom_timeout_config = create_custom_timeout_config(
            connect_timeout=2.0, read_timeout=5.0
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.get_secure_logger")
    def test_api_client_with_custom_retry_config(self, mock_logger):
        """Test ApiFFBBAppClient with custom retry configuration."""
        mock_logger.return_value = MagicMock()

        client = ApiFFBBAppClient(
            bearer_token=self.valid_token,
            retry_config=self.custom_retry_config,
            timeout_config=self.custom_timeout_config,
            debug=True,
        )

        # Verify configurations are set
        self.assertEqual(client.retry_config.max_attempts, 2)
        self.assertEqual(client.retry_config.base_delay, 0.5)
        self.assertEqual(client.timeout_config.connect_timeout, 2.0)
        self.assertEqual(client.timeout_config.read_timeout, 5.0)
        self.assertEqual(client.timeout_config.total_timeout, 7.0)

        # Verify logger was called with retry info
        mock_logger.return_value.info.assert_any_call(
            "Retry config: 2 attempts, timeout: 7.0s"
        )

    @patch("ffbb_api_client_v2.clients.meilisearch_client.get_secure_logger")
    def test_meilisearch_client_with_custom_timeout_config(self, mock_logger):
        """Test MeilisearchClient with custom timeout configuration."""
        mock_logger.return_value = MagicMock()

        client = MeilisearchClient(
            bearer_token=self.valid_token,
            timeout_config=self.custom_timeout_config,
            debug=True,
        )

        # Verify timeout configuration is set
        self.assertEqual(client.timeout_config.connect_timeout, 2.0)
        self.assertEqual(client.timeout_config.read_timeout, 5.0)
        self.assertEqual(client.timeout_config.total_timeout, 7.0)

        # Verify logger was called with timeout info
        mock_logger.return_value.info.assert_any_call(
            "Retry config: 3 attempts, timeout: 7.0s"
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.get_secure_logger")
    def test_api_client_default_configs(self, mock_logger):
        """Test ApiFFBBAppClient uses default configurations."""
        mock_logger.return_value = MagicMock()

        client = ApiFFBBAppClient(bearer_token=self.valid_token)

        # Verify default configurations are used
        self.assertEqual(client.retry_config.max_attempts, 3)
        self.assertEqual(client.timeout_config.connect_timeout, 10.0)
        self.assertEqual(client.timeout_config.read_timeout, 30.0)
        self.assertEqual(client.timeout_config.total_timeout, 40.0)

    @patch("ffbb_api_client_v2.clients.meilisearch_client.get_secure_logger")
    def test_meilisearch_client_default_configs(self, mock_logger):
        """Test MeilisearchClient uses default configurations."""
        mock_logger.return_value = MagicMock()

        client = MeilisearchClient(bearer_token=self.valid_token)

        # Verify default configurations are used
        self.assertEqual(client.retry_config.max_attempts, 3)
        self.assertEqual(client.timeout_config.connect_timeout, 10.0)
        self.assertEqual(client.timeout_config.read_timeout, 30.0)
        self.assertEqual(client.timeout_config.total_timeout, 40.0)

    def test_retry_config_validation(self):
        """Test that retry configurations are properly validated."""
        # Valid configurations
        config1 = RetryConfig(max_attempts=1)
        self.assertEqual(config1.max_attempts, 1)

        config2 = RetryConfig(max_attempts=10)
        self.assertEqual(config2.max_attempts, 10)

        # Edge cases
        config3 = RetryConfig(base_delay=0.1)
        self.assertEqual(config3.base_delay, 0.1)

        config4 = RetryConfig(max_delay=120.0)
        self.assertEqual(config4.max_delay, 120.0)

    def test_timeout_config_validation(self):
        """Test that timeout configurations are properly validated."""
        # Valid configurations
        config1 = TimeoutConfig(connect_timeout=1.0, read_timeout=2.0)
        self.assertEqual(config1.total_timeout, 3.0)

        config2 = TimeoutConfig(
            connect_timeout=5.0, read_timeout=10.0, total_timeout=20.0
        )
        self.assertEqual(config2.total_timeout, 20.0)

        # Edge cases
        config3 = TimeoutConfig(connect_timeout=0.1, read_timeout=0.1)
        self.assertEqual(config3.total_timeout, 0.2)

    def test_client_initialization_with_configs(self):
        """Test that clients can be initialized with various configurations."""
        configs = [
            (RetryConfig(max_attempts=1), TimeoutConfig(connect_timeout=1.0)),
            (RetryConfig(max_attempts=5), TimeoutConfig(read_timeout=60.0)),
            (
                create_custom_retry_config(2, 0.5),
                create_custom_timeout_config(3.0, 7.0),
            ),
        ]

        for retry_config, timeout_config in configs:
            with self.subTest():
                with patch(
                    "ffbb_api_client_v2.clients.api_ffbb_app_client.get_secure_logger"
                ):
                    client = ApiFFBBAppClient(
                        bearer_token=self.valid_token,
                        retry_config=retry_config,
                        timeout_config=timeout_config,
                    )

                    self.assertEqual(
                        client.retry_config.max_attempts, retry_config.max_attempts
                    )
                    self.assertEqual(
                        client.timeout_config.connect_timeout,
                        timeout_config.connect_timeout,
                    )

    def test_config_immutability(self):
        """Test that configuration objects are not modified after client creation."""
        original_max_attempts = self.custom_retry_config.max_attempts
        original_connect_timeout = self.custom_timeout_config.connect_timeout

        with patch("ffbb_api_client_v2.clients.api_ffbb_app_client.get_secure_logger"):
            client = ApiFFBBAppClient(
                bearer_token=self.valid_token,
                retry_config=self.custom_retry_config,
                timeout_config=self.custom_timeout_config,
            )

        # Original configs should remain unchanged
        self.assertEqual(self.custom_retry_config.max_attempts, original_max_attempts)
        self.assertEqual(
            self.custom_timeout_config.connect_timeout, original_connect_timeout
        )

        # Client should have its own copies
        self.assertEqual(client.retry_config.max_attempts, original_max_attempts)
        self.assertEqual(
            client.timeout_config.connect_timeout, original_connect_timeout
        )


if __name__ == "__main__":
    unittest.main()
