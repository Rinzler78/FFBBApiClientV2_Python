"""Centralized configuration for FFBB Directus API client."""

from ..utils.retry_utils import RetryConfig, TimeoutConfig

# Directus needs longer read timeout for deep wildcard field queries (*.*.*.*.*)
DEFAULT_DIRECTUS_TIMEOUT_CONFIG = TimeoutConfig(
    connect_timeout=10.0, read_timeout=120.0
)
# Fewer retries since each attempt is expensive with deep queries
DEFAULT_DIRECTUS_RETRY_CONFIG = RetryConfig(max_attempts=1)

# API URL
API_FFBB_BASE_URL = "https://api.ffbb.app/"

# Environment variable name for the API token
ENV_API_TOKEN = "API_FFBB_APP_BEARER_TOKEN"

# API Endpoint Paths (relative to base URL)
ENDPOINT_CONFIGURATION = "items/configuration"
ENDPOINT_LIVES = "json/lives.json"
ENDPOINT_COMPETITIONS = "items/ffbbserver_competitions"
ENDPOINT_POULES = "items/ffbbserver_poules"
ENDPOINT_SAISONS = "items/ffbbserver_saisons"
ENDPOINT_ORGANISMES = "items/ffbbserver_organismes"
ENDPOINT_COMMUNES = "items/ffbbserver_communes"
ENDPOINT_OFFICIELS = "items/ffbbserver_officiels"
ENDPOINT_ENTRAINEURS = "items/ffbbserver_entraineurs"
ENDPOINT_RENCONTRES = "items/ffbbserver_rencontres"
ENDPOINT_SALLES = "items/ffbbserver_salles"
ENDPOINT_TERRAINS = "items/ffbbserver_terrains"
ENDPOINT_TOURNOIS = "items/ffbbserver_tournois"
ENDPOINT_ENGAGEMENTS = "items/ffbbserver_engagements"
ENDPOINT_FORMATIONS = "items/ffbbserver_formations"
ENDPOINT_PRATIQUES = "items/ffbbnational_pratiques"
ENDPOINT_ASSETS = "assets/"
