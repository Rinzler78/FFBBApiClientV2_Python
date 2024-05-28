import os

from src.ffbb_api_client_v2.api_ffbb_app_client import ApiFFBBAppClient
from tests.test_api_ffbb_app_client import TestApiFFBBAppClient

# Retrieve api user / pass
API_FFBB_APP_BEARER_TOKEN = os.getenv("API_FFBB_APP_BEARER_TOKEN")

# Create an instance of the api client
api_ffbb_app_client: ApiFFBBAppClient = ApiFFBBAppClient(
    API_FFBB_APP_BEARER_TOKEN,
    debug=True,
)

test = TestApiFFBBAppClient()
test.setUp()
test.test_lives()
