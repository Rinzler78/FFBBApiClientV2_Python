import os
import unittest

from dotenv import load_dotenv

from ffbb_api_client_v2.api_ffbb_app_client import ApiFFBBAppClient
from ffbb_api_client_v2.ffbb_api_client_v2 import FFBBAPIClientV2
from ffbb_api_client_v2.meilisearch_client import MeilisearchClient
from ffbb_api_client_v2.meilisearch_ffbb_client import MeilisearchFFBBClient

load_dotenv()

meilisearch_ffbb_app_token = os.getenv("MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN")
API_FFBB_APP_BEARER_TOKEN = os.getenv("API_FFBB_APP_BEARER_TOKEN")


class TestFFBBAPIClientV2(unittest.TestCase):
    def setUp(self):
        self.meilisearch_client: MeilisearchClient = MeilisearchClient(
            meilisearch_ffbb_app_token,
            debug=True,
        )
        self.meilisearch_client_helper: MeilisearchFFBBClient = MeilisearchFFBBClient(
            self.meilisearch_client
        )

        self.api_ffbb_client = ApiFFBBAppClient(API_FFBB_APP_BEARER_TOKEN, debug=True)

        self.ffbb_api_client: FFBBAPIClientV2 = FFBBAPIClientV2(
            self.api_ffbb_client, self.meilisearch_client_helper
        )

    def setup_method(self, method):
        self.setUp()

    def test_get_lives(self):
        lives = self.ffbb_api_client.get_lives()
        self.assertIsNotNone(lives)


if __name__ == "__main__":
    unittest.main()
