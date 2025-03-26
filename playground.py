import os

from src.ffbb_api_client_v2 import FFBBAPIClientV2

# ffbb api client
MEILISEARCH_TOKEN = os.getenv("MEILISEARCH_BEARER_TOKEN")
API_TOKEN = os.getenv("API_FFBB_APP_BEARER_TOKEN")

# Meilisearch api client
# meilisearch_client = MeilisearchFFBBClient(MEILISEARCH_TOKEN, debug=True)
# queries = generate_queries("Senas Basket Ball", limit=1000)
# senas_organisation = meilisearch_client.sea(
#     queries,
#     cached_session=default_cached_session
# )

# Create an instance of the api client
ffbb_api_client = FFBBAPIClientV2.create(MEILISEARCH_TOKEN, API_TOKEN, debug=True)

organismes = ffbb_api_client.search_organismes()

senas_organisme = ffbb_api_client.search_organismes("Senas")
senas_rencontres = ffbb_api_client.search_rencontres(
    "_geoBoundingBox("
    "[43.92744016015007, 5.372531832467132], "
    "[43.55851862669806, 4.782588819381317])"
)


print()
