import os

from ffbb_api_client_v2.meilisearch_client import MeilisearchClient
from ffbb_api_client_v2.meilisearch_ffbb_client import MeilisearchFFBBClient
from tests.test_03_meilisearch_ffbb_client import Test_03_MeilisearchFFBBClient

meilisearch_ffbb_app_token = os.getenv("MEILISEARCH_BEARER_TOKEN")

meilisearch_prod_ffbb_app_client: MeilisearchClient = MeilisearchClient(
    meilisearch_ffbb_app_token,
    debug=True,
)

# Retrieve api user / pass
meilisearch_ffbb_app_token = os.getenv("MEILISEARCH_BEARER_TOKEN")

meilisearch_prod_ffbb_app_client: MeilisearchFFBBClient = MeilisearchFFBBClient(
    meilisearch_prod_ffbb_app_client
)

test = Test_03_MeilisearchFFBBClient()
test.setUp()

# test.test_recursive_multi_search_with_empty_queries()
# test.test_multi_search_with_all_possible_empty_queries()
test.test_multi_search_with_all_possible_queries()

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

# test.test_search_tournois_with_empty_names()
# test.test_search_tournois_with_most_used_letters()
# test.test_search_tournois_with_known_names()

# test.test_search_pratiques_with_empty_names()
# test.test_search_pratiques_with_most_used_letters()
# test.test_search_pratiques_with_known_names()
