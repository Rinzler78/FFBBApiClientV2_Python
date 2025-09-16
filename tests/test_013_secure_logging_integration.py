"""
Integration tests for secure logging in API clients.
"""

import unittest
from unittest.mock import MagicMock, patch

from ffbb_api_client_v2.clients.api_ffbb_app_client import ApiFFBBAppClient
from ffbb_api_client_v2.clients.meilisearch_client import MeilisearchClient


class Test013SecureLoggingIntegration(unittest.TestCase):
    """Integration tests for secure logging in API clients."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_token = "test_token_123456789"
        self.masked_token = "test***MASKED***"

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.get_secure_logger")
    def test_api_ffbb_client_secure_logging(self, mock_get_logger):
        """Test that ApiFFBBAppClient uses secure logging."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Create client with debug=True to trigger logging
        client = ApiFFBBAppClient(bearer_token=self.test_token, debug=True)

        # Verify that secure logger was initialized
        mock_get_logger.assert_called_once_with("ApiFFBBAppClient")
        self.assertIsNotNone(client.logger)

        # Verify that token is stored securely (private attribute)
        self.assertEqual(client._bearer_token, self.test_token)
        # Verify that public property exposes the token
        self.assertEqual(client.bearer_token, self.test_token)

        # Verify that logger was called during initialization
        # (debug=True results in 2 calls)
        self.assertEqual(mock_logger.info.call_count, 2)

        # Check the first call (token initialization) contains masked token
        first_call_args = mock_logger.info.call_args_list[0][0][0]
        self.assertIn("***MASKED***", first_call_args)
        self.assertNotIn(self.test_token, first_call_args)

    @patch("ffbb_api_client_v2.clients.meilisearch_client.get_secure_logger")
    def test_meilisearch_client_secure_logging(self, mock_get_logger):
        """Test that MeilisearchClient uses secure logging."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Create client with debug=True to trigger logging
        client = MeilisearchClient(bearer_token=self.test_token, debug=True)

        # Verify that secure logger was initialized
        mock_get_logger.assert_called_once_with("MeilisearchClient")
        self.assertIsNotNone(client.logger)

        # Verify that token is stored securely (private attribute)
        self.assertEqual(client._bearer_token, self.test_token)
        # Verify that public property exposes the token
        self.assertEqual(client.bearer_token, self.test_token)

        # Verify that logger was called during initialization
        # (debug=True results in 2 calls)
        self.assertEqual(mock_logger.info.call_count, 2)

        # Check the first call (token initialization) contains masked token
        first_call_args = mock_logger.info.call_args_list[0][0][0]
        self.assertIn("***MASKED***", first_call_args)
        self.assertNotIn(self.test_token, first_call_args)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.get_secure_logger")
    def test_api_client_no_debug_logging(self, mock_get_logger):
        """Test that ApiFFBBAppClient doesn't log token details when debug=False."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Create client with debug=False
        client = ApiFFBBAppClient(bearer_token=self.test_token, debug=False)

        # Verify that client was created successfully
        self.assertIsNotNone(client)

        # Verify that logger was called but without token details
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]

        # Should log success message without token
        self.assertEqual(call_args, "ApiFFBBAppClient initialized successfully")
        self.assertNotIn("***MASKED***", call_args)
        self.assertNotIn(self.test_token, call_args)

    def test_token_validation(self):
        """Test that clients validate tokens properly."""
        # Test empty token
        with self.assertRaises(ValueError) as context:
            ApiFFBBAppClient(bearer_token="")
        self.assertIn(
            "bearer_token cannot be None, empty, or whitespace-only",
            str(context.exception),
        )

        # Test None token
        with self.assertRaises(ValueError) as context:
            ApiFFBBAppClient(bearer_token=None)
        self.assertIn(
            "bearer_token cannot be None, empty, or whitespace-only",
            str(context.exception),
        )

        # Test whitespace-only token
        with self.assertRaises(ValueError) as context:
            ApiFFBBAppClient(bearer_token="   ")
        self.assertIn(
            "bearer_token cannot be None, empty, or whitespace-only",
            str(context.exception),
        )

    def test_headers_use_secure_token(self):
        """Test that headers use the securely stored token."""
        test_token = "secure_test_token_123"
        client = ApiFFBBAppClient(bearer_token=test_token)

        # Verify that headers contain the correct authorization
        expected_auth = f"Bearer {test_token}"
        self.assertEqual(client.headers["Authorization"], expected_auth)

        # Verify that the token is stored securely
        self.assertEqual(client._bearer_token, test_token)


if __name__ == "__main__":
    unittest.main()
