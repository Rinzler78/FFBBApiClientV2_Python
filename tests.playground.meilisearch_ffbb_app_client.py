import os

from ffbb_api_client_v2.meilisearch_client import MeilisearchClient
from tests.test_01_meilisearch_client import TestMeilisearchClient

# Retrieve api user / pass
meilisearch_ffbb_app_token = os.getenv("MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN")

meilisearch_prod_ffbb_app_client: MeilisearchClient = MeilisearchClient(
    meilisearch_ffbb_app_token,
    debug=True,
)

test = TestMeilisearchClient()
test.setUp()
test.test_multi_search_with_empty_queries()
