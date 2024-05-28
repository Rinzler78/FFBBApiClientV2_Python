import os

from src.ffbb_api_client_v2.api_ffbb_app_client import ApiFFBBAppClient

# Retrieve api user / pass
api_ffbb_app_bearer_token = os.getenv("API_FFBB_APP_BEARER_TOKEN")

# Create an instance of the api client
api_ffbb_app_client: ApiFFBBAppClient = ApiFFBBAppClient(api_ffbb_app_bearer_token)
