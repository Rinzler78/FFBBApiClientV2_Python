import os

from ffbb_api_client_v2.meilisearch_ffbb_app_client_helper import (
    MeilisearchFFBBAPPClientHelper,
)
from tests.test_meilisearch_ffbb_app_client_helper import (
    TestMeilisearchFFBBAPPClientHelper,
)

# Retrieve api user / pass
MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN = os.getenv(
    "MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN"
)

meilisearch_prod_ffbb_app_client: MeilisearchFFBBAPPClientHelper = (
    MeilisearchFFBBAPPClientHelper(
        MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN,
        debug=True,
    )
)

test = TestMeilisearchFFBBAPPClientHelper()
test.setUp()

test.test_multi_search_with_all_possible_empty_queries()

# test.test_search_organismes_with_empty_name()
# test.test_search_organismes_with_most_used_letters()
# test.test_search_organismes_with_known_names()

# test.test_search_rencontres_with_empty_names()
# test.test_search_rencontres_with_most_used_letters()
# test.test_search_rencontres_with_known_names()

# test.test_search_terrains_with_empty_names()
# test.test_search_terrains_with_most_used_letters()
# test.test_search_terrains_with_known_names()

# test.test_search_competitions_with_empty_names()
# test.test_search_competitions_with_most_used_letters()
# test.test_search_competitions_with_known_names()

# test.test_search_salles_with_empty_names()
# test.test_search_salles_with_most_used_letters()
# test.test_search_salles_with_known_names()

test.test_search_tournois_with_empty_names()
test.test_search_tournois_with_most_used_letters()
test.test_search_tournois_with_known_names()
