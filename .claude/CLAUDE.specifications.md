# CLAUDE.specifications.md - FFBBApiClientV2_Python

Spécifications techniques du client Python pour l'API FFBB (Fédération Française de Basketball).

## Vue d'Ensemble

**FFBBApiClientV2_Python** est une bibliothèque cliente Python permettant l'accès programmatique aux données officielles de la Fédération Française de Basketball (FFBB).

### Objectifs
- Abstraction haut niveau de l'API FFBB
- Gestion transparente de l'authentification
- Types Python stricts et validation données
- Support async/sync pour flexibilité
- Caching intelligent avec TTL
- Gestion erreurs robuste avec retries

## Architecture Client

### Structure Modulaire
```
ffbb_api_client_v2/
├── client/           # Core client HTTP
├── models/           # Modèles données FFBB
├── endpoints/        # Wrappers endpoints API
├── auth/            # Gestion authentification
├── cache/           # Système cache optionnel
├── exceptions/      # Exceptions custom client
└── utils/           # Utilitaires helper
```

### Configuration
```python
from ffbb_api_client_v2 import FFBBApiClientV2

client = FFBBApiClientV2(
    meilisearch_token="your_meilisearch_token",
    api_token="your_api_token",
    base_url="https://api.ffbb.com/v2",  # optionnel
    timeout=30.0,                        # optionnel
    max_retries=3,                       # optionnel
    cache_ttl=300                        # optionnel (5min)
)
```

## Endpoints Disponibles

### 🌍 Geography
```python
# Recherche villes
cities = await client.search_cities("Paris", limit=10)
city_details = await client.get_city_details(city_ffbb_id="123")

# Régions et départements
regions = await client.get_regions()
departments = await client.get_departments(region_id="11")
```

### 🏢 Organismes & Clubs
```python
# Recherche organismes
organismes = await client.search_organismes("Comité Seine")
organisme = await client.get_organisme_details("org_123")

# Recherche clubs
clubs = await client.search_clubs("Basketball Club", city_ffbb_id="456")
club = await client.get_club_details("club_789")
```

### 🏟️ Facilities & Salles
```python
# Recherche salles
salles = await client.search_salles("Gymnase", city_ffbb_id="456")
salle = await client.get_salle_details("salle_101")
```

### 🏆 Competitions & Seasons
```python
# Saisons disponibles
seasons = await client.get_seasons()
current_season = await client.get_current_season()

# Compétitions
competitions = await client.search_competitions("Championnat U15")
competition = await client.get_competition_details("comp_123")

# Poules (groupes)
poules = await client.get_competition_poules("comp_123")
```

### 👥 Teams & Players
```python
# Équipes
teams = await client.search_teams("Lakers", competition_id="comp_123")
team = await client.get_team_details("team_456")
team_players = await client.get_team_players("team_456")

# Joueurs
players = await client.search_players("Martin", club_id="club_789")
player = await client.get_player_details("player_101")
player_stats = await client.get_player_statistics("player_101", season="2024-2025")
```

### ⚡ Live Data
```python
# Matchs en direct
live_matches = await client.get_live_matches()
live_match = await client.get_live_match_details("match_123")

# Résultats temps réel
match_result = await client.get_match_result("match_123")
```

## Types de Données

### Core Types
```python
from ffbb_api_client_v2.models import (
    FFBBCity,
    FFBBOrganisme,
    FFBBClub,
    FFBBSalle,
    FFBBSeason,
    FFBBCompetition,
    FFBBPoule,
    FFBBTeam,
    FFBBPlayer,
    FFBBMatch,
    FFBBLiveMatch,
    FFBBStatistics
)
```

### Search Result Types
```python
from ffbb_api_client_v2.models import (
    FFBBCitySearchResult,
    FFBBClubSearchResult,
    FFBBTeamSearchResult,
    FFBBPlayerSearchResult,
    FFBBSearchStatus  # SUCCESS, ERROR, PARTIAL, NO_RESULTS
)
```

### Response Wrappers
```python
from ffbb_api_client_v2.models import (
    FFBBSearchResponse,
    FFBBPaginatedResponse,
    FFBBErrorResponse
)
```

## Gestion Authentification

### Tokens Requis
```bash
# Variables environnement
export FFBB_MEILISEARCH_TOKEN="your_meilisearch_token"
export FFBB_API_TOKEN="your_api_token"
```

### Auto-refresh
```python
# Client gère automatiquement refresh tokens
client = FFBBApiClientV2(
    meilisearch_token=os.getenv("FFBB_MEILISEARCH_TOKEN"),
    api_token=os.getenv("FFBB_API_TOKEN"),
    auto_refresh=True  # défaut: True
)
```

## Gestion Erreurs

### Exceptions Custom
```python
from ffbb_api_client_v2.exceptions import (
    FFBBApiError,           # Erreur générale API
    FFBBAuthenticationError, # Problème authentification
    FFBBRateLimitError,     # Limite taux dépassée
    FFBBTimeoutError,       # Timeout requête
    FFBBNotFoundError,      # Ressource non trouvée
    FFBBValidationError     # Validation données
)
```

### Retry Strategy
```python
client = FFBBApiClientV2(
    max_retries=3,              # Nombre tentatives
    retry_backoff_factor=2.0,   # Facteur backoff exponentiel
    retry_on_status=[500, 502, 503, 504]  # Codes statut retry
)
```

## Système Cache

### Configuration Cache
```python
client = FFBBApiClientV2(
    cache_enabled=True,         # Activer cache (défaut: True)
    cache_ttl=300,             # TTL 5 minutes (défaut)
    cache_max_size=1000        # Taille max cache (défaut: 1000)
)
```

### Cache Keys Strategy
- **Search queries**: `search:{endpoint}:{query_hash}`
- **Details**: `details:{resource_type}:{id}`
- **Live data**: `live:{endpoint}` (TTL court)

### Manual Cache Control
```python
# Vider cache spécifique
await client.cache.clear_pattern("search:cities:*")

# Vider tout le cache
await client.cache.clear_all()

# Désactiver cache pour requête
result = await client.search_cities("Paris", use_cache=False)
```

## Async/Sync Support

### Async (Recommandé)
```python
import asyncio
from ffbb_api_client_v2 import FFBBApiClientV2

async def main():
    client = FFBBApiClientV2(...)
    cities = await client.search_cities("Lyon")
    await client.close()  # Important: fermer sessions

asyncio.run(main())
```

### Sync (Wrapper)
```python
from ffbb_api_client_v2 import FFBBApiClientV2Sync

client = FFBBApiClientV2Sync(...)
cities = client.search_cities("Lyon")  # Bloquant
client.close()
```

## Logging & Debug

### Configuration Logs
```python
import logging

# Activer logs debug client
logging.getLogger("ffbb_api_client_v2").setLevel(logging.DEBUG)

# Logs requêtes HTTP détaillées
logging.getLogger("httpx").setLevel(logging.DEBUG)
```

### Debug Mode
```python
client = FFBBApiClientV2(
    debug=True,                # Logs détaillés
    log_requests=True,         # Log toutes requêtes
    log_responses=True         # Log toutes réponses
)
```

## Rate Limiting

### Limites FFBB
- **Search endpoints**: 100 req/min
- **Details endpoints**: 500 req/min
- **Live data**: 10 req/min

### Client Rate Limiting
```python
client = FFBBApiClientV2(
    rate_limit_enabled=True,    # Respect limites (défaut: True)
    rate_limit_margin=0.8       # Marge sécurité 80% (défaut)
)
```

## Testing & Validation

### Mock Client (Testing)
```python
from ffbb_api_client_v2.testing import MockFFBBClient

# Client mock pour tests
mock_client = MockFFBBClient()
mock_client.set_response("search_cities", mock_cities_data)

# Utilisation identique au client réel
cities = await mock_client.search_cities("Test")
```

### Validation Schema
```python
from ffbb_api_client_v2.validation import validate_ffbb_response

# Validation automatique réponses API
is_valid = validate_ffbb_response(response_data, "city")
```

## Installation & Setup

### Installation
```bash
pip install ffbb-api-client-v2
```

### Requirements
- Python 3.8+
- httpx (async HTTP client)
- pydantic (validation données)
- typing-extensions (types avancés)

---

*Client optimisé pour intégration robuste et performante avec l'API FFBB officielle*
