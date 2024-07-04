import os
import unittest

from dotenv import load_dotenv

from ffbb_api_client_v2.api_ffbb_app_client import ApiFFBBAppClient

load_dotenv()

API_FFBB_APP_BEARER_TOKEN = os.getenv("API_FFBB_APP_BEARER_TOKEN")


class TestApiFFBBAppClient(unittest.TestCase):

    def setUp(self):
        self.api_client = ApiFFBBAppClient(
            API_FFBB_APP_BEARER_TOKEN,
            debug=True,
        )

    def setup_method(self, method):
        self.setUp()

    def test_lives(self):
        result = self.api_client.get_lives()
        self.assertIsNotNone(result)
