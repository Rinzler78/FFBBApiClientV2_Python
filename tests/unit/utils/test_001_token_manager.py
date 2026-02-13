"""
Tests for TokenManager.
"""

import os
import unittest
from unittest.mock import patch

from ffbb_api_client_v2 import FFBBTokens, TokenManager
from ffbb_api_client_v2.config import ENV_MEILISEARCH_TOKEN
from ffbb_api_client_v2.directus_ffbb.config import ENV_API_TOKEN


class Test020TokenManager(unittest.TestCase):
    """Test cases for TokenManager functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Save original env values
        self.original_api = os.environ.get(ENV_API_TOKEN)
        self.original_ms = os.environ.get(ENV_MEILISEARCH_TOKEN)

    def tearDown(self):
        """Restore environment after each test."""
        # Restore original env values
        if self.original_api:
            os.environ[ENV_API_TOKEN] = self.original_api
        else:
            os.environ.pop(ENV_API_TOKEN, None)
        if self.original_ms:
            os.environ[ENV_MEILISEARCH_TOKEN] = self.original_ms
        else:
            os.environ.pop(ENV_MEILISEARCH_TOKEN, None)

    def test_000_ffbb_tokens_creation(self):
        """Test FFBBTokens can be created with both tokens."""
        tokens = FFBBTokens(api_token="api_123", meilisearch_token="ms_456")
        self.assertEqual(tokens.api_token, "api_123")
        self.assertEqual(tokens.meilisearch_token, "ms_456")

    @patch.dict(
        os.environ,
        {ENV_API_TOKEN: "env_api_token", ENV_MEILISEARCH_TOKEN: "env_ms_token"},
    )
    def test_001_get_tokens_from_env(self):
        """Test tokens are retrieved from environment variables."""
        tokens = TokenManager.get_tokens()

        self.assertEqual(tokens.api_token, "env_api_token")
        self.assertEqual(tokens.meilisearch_token, "env_ms_token")

    @patch.dict(
        os.environ,
        {ENV_API_TOKEN: "env_api_token", ENV_MEILISEARCH_TOKEN: "env_ms_token"},
    )
    def test_002_get_tokens_multiple_calls_from_env(self):
        """Test multiple calls to get_tokens return correct values from env."""
        tokens1 = TokenManager.get_tokens()
        tokens2 = TokenManager.get_tokens()

        # Both calls should return tokens from environment
        self.assertEqual(tokens1.api_token, "env_api_token")
        self.assertEqual(tokens2.api_token, "env_api_token")

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_003_get_tokens_from_api_when_env_missing(self, mock_http):
        """Test tokens are fetched from API when env vars are missing."""
        # Clear env vars
        os.environ.pop(ENV_API_TOKEN, None)
        os.environ.pop(ENV_MEILISEARCH_TOKEN, None)

        mock_http.return_value = {
            "data": {
                "id": 1,
                "key_dh": "api_from_fetch",
                "key_ms": "ms_from_fetch",
            }
        }

        tokens = TokenManager.get_tokens()

        self.assertEqual(tokens.api_token, "api_from_fetch")
        self.assertEqual(tokens.meilisearch_token, "ms_from_fetch")
        mock_http.assert_called_once()

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_004_get_tokens_api_failure(self, mock_http):
        """Test error handling when API fetch fails."""
        # Clear env vars
        os.environ.pop(ENV_API_TOKEN, None)
        os.environ.pop(ENV_MEILISEARCH_TOKEN, None)

        mock_http.return_value = None

        with self.assertRaises(RuntimeError) as context:
            TokenManager.get_tokens()

        self.assertIn("Failed to fetch configuration", str(context.exception))

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_005_get_tokens_partial_env_fetches_from_api(self, mock_http):
        """Test API fetch when only one env var is set."""
        # Set only one env var
        os.environ[ENV_API_TOKEN] = "partial_token"
        os.environ.pop(ENV_MEILISEARCH_TOKEN, None)

        mock_http.return_value = {
            "data": {
                "id": 1,
                "key_dh": "api_from_fetch",
                "key_ms": "ms_from_fetch",
            }
        }

        tokens = TokenManager.get_tokens()

        # Should fetch from API since meilisearch token is missing
        self.assertEqual(tokens.api_token, "api_from_fetch")
        self.assertEqual(tokens.meilisearch_token, "ms_from_fetch")


class Test020TokenManagerIntegration(unittest.TestCase):
    """Integration tests for TokenManager with real API."""

    def test_006_integration_fetch_real_tokens(self):
        """Integration test: fetch real tokens from FFBB API."""
        # Save and clear env vars to force API fetch
        original_api = os.environ.pop(ENV_API_TOKEN, None)
        original_ms = os.environ.pop(ENV_MEILISEARCH_TOKEN, None)

        try:
            tokens = TokenManager.get_tokens()

            # Verify we got valid tokens
            self.assertIsNotNone(tokens.api_token)
            self.assertIsNotNone(tokens.meilisearch_token)
            self.assertGreater(len(tokens.api_token), 10)
            self.assertGreater(len(tokens.meilisearch_token), 10)

        finally:
            # Restore env vars
            if original_api:
                os.environ[ENV_API_TOKEN] = original_api
            if original_ms:
                os.environ[ENV_MEILISEARCH_TOKEN] = original_ms


if __name__ == "__main__":
    unittest.main()
