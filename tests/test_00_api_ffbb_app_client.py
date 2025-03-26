import os
import unittest

from dotenv import load_dotenv

from ffbb_api_client_v2.api_ffbb_app_client import ApiFFBBAppClient


class Test_00_ApiFFBBAppClient(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        self.api_client = ApiFFBBAppClient(
            bearer_token=os.getenv("API_FFBB_APP_BEARER_TOKEN"),
            debug=True,
        )

    def setup_method(self, method):
        self.setUp()

    def test_lives(self):
        result = self.api_client.get_lives()
        self.assertIsNotNone(result)
