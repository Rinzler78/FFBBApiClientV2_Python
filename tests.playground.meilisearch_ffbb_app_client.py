import os

from ffbb_api_client_v2.meilisearch_ffbb_app_client import MeilisearchFFBBAPPClient
from tests.test_meilisearch_ffbb_app_client import TestMeilisearchFFBBAPPClient

# Retrieve api user / pass
MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN = os.getenv(
    "MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN"
)

meilisearch_prod_ffbb_app_client: MeilisearchFFBBAPPClient = MeilisearchFFBBAPPClient(
    MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN,
    debug=True,
)

test = TestMeilisearchFFBBAPPClient()
test.setUp()
test.test_multi_search_with_empty_queries()
