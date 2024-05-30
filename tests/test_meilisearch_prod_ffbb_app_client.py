import os
import unittest

from dotenv import load_dotenv

from ffbb_api_client_v2.meilisearch_prod_ffbb_app_client import (
    MeilisearchProdFFBBAPPClient,
)

load_dotenv()

MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN = os.getenv(
    "MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN"
)


class TestMeilisearchProdFFBBAPPClient(unittest.TestCase):

    def setUp(self):
        self.api_client = MeilisearchProdFFBBAPPClient(
            MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN,
            debug=True,
        )

    def setup_method(self, method):
        self.setUp()

    def test_multi_search_with_empty_queries(self):
        result = self.api_client.multi_search()
        self.assertIsNotNone(result)

    def test_search_organismes_with_empty_name(self):
        result = self.api_client.search_organismes()
        self.assertIsNotNone(result)

    def test_search_organismes_with_most_used_letters(self):
        result = self.api_client.search_multiple_organismes(
            ["a", "e", "i", "o", "u", "y", "b", "l", "m", "s"]
        )
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)

    def test_search_organismes_with_known_names(self):
        result = self.api_client.search_multiple_organismes(["Paris", "Senas", "Reims"])
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)

    def test_search_rencontres_with_empty_names(self):
        result = self.api_client.search_rencontres()
        self.assertIsNotNone(result)

    def test_search_rencontres_with_most_used_letters(self):
        result = self.api_client.search_multiple_rencontres(
            ["a", "e", "i", "o", "u", "y", "b", "l", "m", "s"]
        )
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)

    def test_search_rencontres_with_known_names(self):
        result = self.api_client.search_multiple_rencontres(["Paris", "Senas", "Reims"])
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
