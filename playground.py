import os

from .api_ffbb_app_client import ApiFFBBAppClient

# Retrieve api user / pass
api_ffbb_app_bearer_token = os.getenv("API_TOKEN")

# Create an instance of the api client
api_client: ApiFFBBAppClient = ApiFFBBAppClient(
    api_ffbb_app_bearer_token,
    debug=True,
)
