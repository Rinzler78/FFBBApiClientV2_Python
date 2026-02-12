"""
Tests for centralized configuration.
"""

import unittest

from ffbb_api_client_v2 import config


class Test019Config(unittest.TestCase):
    """Test cases for config module constants."""

    def test_000_api_url_format(self):
        """Test API URL is valid and ends with slash."""
        self.assertTrue(config.API_FFBB_BASE_URL.startswith("https://"))
        self.assertTrue(config.API_FFBB_BASE_URL.endswith("/"))

    def test_001_meilisearch_url_format(self):
        """Test Meilisearch URL is valid and ends with slash."""
        self.assertTrue(config.MEILISEARCH_BASE_URL.startswith("https://"))
        self.assertTrue(config.MEILISEARCH_BASE_URL.endswith("/"))

    def test_002_user_agent_not_empty(self):
        """Test user agent is defined."""
        self.assertIsNotNone(config.DEFAULT_USER_AGENT)
        self.assertGreater(len(config.DEFAULT_USER_AGENT), 0)

    def test_003_env_token_names_defined(self):
        """Test environment variable names are defined."""
        self.assertEqual(config.ENV_API_TOKEN, "API_FFBB_APP_BEARER_TOKEN")
        self.assertEqual(config.ENV_MEILISEARCH_TOKEN, "MEILISEARCH_BEARER_TOKEN")

    def test_004_api_endpoint_constants_defined(self):
        """Test API endpoint constants are defined."""
        self.assertEqual(config.ENDPOINT_CONFIGURATION, "items/configuration")
        self.assertEqual(config.ENDPOINT_LIVES, "json/lives.json")
        self.assertEqual(config.ENDPOINT_COMPETITIONS, "items/ffbbserver_competitions")
        self.assertEqual(config.ENDPOINT_POULES, "items/ffbbserver_poules")
        self.assertEqual(config.ENDPOINT_SAISONS, "items/ffbbserver_saisons")
        self.assertEqual(config.ENDPOINT_ORGANISMES, "items/ffbbserver_organismes")

    def test_005_meilisearch_endpoint_constants_defined(self):
        """Test Meilisearch endpoint constants are defined."""
        self.assertEqual(config.MEILISEARCH_ENDPOINT_MULTI_SEARCH, "multi-search")


if __name__ == "__main__":
    unittest.main()
