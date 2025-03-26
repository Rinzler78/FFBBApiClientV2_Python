import os

from dotenv import load_dotenv

from ffbb_api_client_v2 import FFBBAPIClientV2

load_dotenv()

MEILISEARCH_TOKEN = os.getenv("MEILISEARCH_BEARER_TOKEN")
API_TOKEN = os.getenv("API_FFBB_APP_BEARER_TOKEN")

# Create an instance of the api client
ffbb_api_client = FFBBAPIClientV2.create(MEILISEARCH_TOKEN, API_TOKEN, debug=True)

# Get the lives
lives = ffbb_api_client.get_lives()

# Get the organismes
organismes = ffbb_api_client.search_organismes()
organismes = ffbb_api_client.search_organismes("Paris")
organismes = ffbb_api_client.search_multiple_organismes(["Paris", "Chartres"])

# Get the rencontres
rencontres = ffbb_api_client.search_rencontres()
rencontres = ffbb_api_client.search_rencontres("Basket")
rencontres = ffbb_api_client.search_multiple_rencontres(["Basket", "ASPTT"])

# Get the terrains
terrains = ffbb_api_client.search_terrains()
terrains = ffbb_api_client.search_terrains("Basket")
terrains = ffbb_api_client.search_multiple_terrains(["Basket", "ASPTT"])

# Get the competitions
competitions = ffbb_api_client.search_competitions()
competitions = ffbb_api_client.search_competitions("Basket")
competitions = ffbb_api_client.search_multiple_competitions(["Basket", "ASPTT"])

# Get the salles
salles = ffbb_api_client.search_salles()
salles = ffbb_api_client.search_salles("Basket")
salles = ffbb_api_client.search_multiple_salles(["Basket", "ASPTT"])

# Get pratiques
pratiques = ffbb_api_client.search_pratiques()
pratiques = ffbb_api_client.search_pratiques("Basket")
pratiques = ffbb_api_client.search_multiple_pratiques(["Basket", "ASPTT"])

# Get tournois
tournois = ffbb_api_client.search_tournois()
tournois = ffbb_api_client.search_tournois("Basket")
tournois = ffbb_api_client.search_multiple_tournois(["Basket", "ASPTT"])
