import os
import unittest

from dotenv import load_dotenv

from ffbb_api_client_v2.meilisearch_ffbb_app_client import MeilisearchFFBBAPPClient

load_dotenv()

MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN = os.getenv(
    "MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN"
)


class TestMeilisearchFFBBAPPClient(unittest.TestCase):

    def setUp(self):
        self.api_client: MeilisearchFFBBAPPClient = MeilisearchFFBBAPPClient(
            MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN,
            debug=True,
        )

    def setup_method(self, method):
        self.setUp()

    def test_multi_search_with_empty_queries(self):
        result = self.api_client.multi_search()
        self.assertIsNotNone(result)
