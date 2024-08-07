import os

from ffbb_api_client_v2.meilisearch_client import MeilisearchClient
from tests.test_01_meilisearch_client import Test_01_MeilisearchClient

# Retrieve api user / pass
meilisearch_ffbb_app_token = os.getenv("MEILISEARCH_BEARER_TOKEN")

meilisearch_prod_ffbb_app_client: MeilisearchClient = MeilisearchClient(
    meilisearch_ffbb_app_token,
    debug=True,
)

test = Test_01_MeilisearchClient()
test.setUp()
test.test_multi_search_with_empty_queries()
