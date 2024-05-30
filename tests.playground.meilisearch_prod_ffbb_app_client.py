import os

from src.ffbb_api_client_v2.meilisearch_prod_ffbb_app_client import (
    MeilisearchProdFFBBAPPClient,
)
from tests.test_meilisearch_prod_ffbb_app_client import TestMeilisearchProdFFBBAPPClient

# Retrieve api user / pass
MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN = os.getenv(
    "MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN"
)

meilisearch_prod_ffbb_app_client: MeilisearchProdFFBBAPPClient = (
    MeilisearchProdFFBBAPPClient(
        MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN,
        debug=True,
    )
)

test = TestMeilisearchProdFFBBAPPClient()
test.setUp()
# test.test_multi_search_with_empty_queries()

# test.test_search_organismes_with_empty_name()
# test.test_search_organismes_with_most_used_letters()
# test.test_search_organismes_with_known_names()

test.test_search_rencontres_with_empty_names()
test.test_search_rencontres_with_most_used_letters()
test.test_search_rencontres_with_known_names()
