# FFBB API Client V2 - Examples

This directory contains practical examples demonstrating how to use the FFBB API Client V2.
All examples use **Paris** as the search query to guarantee results.

## Getting Started

### `quick_start.py`
Basic usage example showing the most common operations:
- Searching for basketball clubs
- Getting detailed organization information
- Checking live matches
- Retrieving current seasons

```bash
python examples/quick_start.py
```

### `complete_usage_example.py`
Comprehensive example demonstrating all major features:
- Type-safe model objects
- Field selection (BASIC, DEFAULT, DETAILED)
- Error handling
- Multi-search functionality
- Competition details
- Advanced API usage patterns

```bash
python examples/complete_usage_example.py
```

### `team_ranking_analysis.py`
Advanced example showing team ranking and performance analysis:
- Team search by name with filters
- Competition filtering by gender, zone, division, and category
- Complete ranking table display
- Detailed team statistics and performance metrics
- Match history analysis

```bash
python examples/team_ranking_analysis.py
```

### `basketball_dashboard.py`
Streamlit-based interactive basketball analytics dashboard:
- Advanced metrics and Elo ratings
- Season-end projections
- Requires: `streamlit`, `matplotlib`, `pandas`, `seaborn`

```bash
streamlit run examples/basketball_dashboard.py
```

## Meilisearch Search API

### `search_all_indexes.py`
All 9 Meilisearch search indexes with single and multiple search variants, plus universal `multi_search()`:
- Organismes, Competitions, Rencontres, Salles, Terrains
- Tournois, Pratiques, Engagements, Formations

```bash
python examples/search_all_indexes.py
```

### `index_settings_discovery.py`
Discover filterable and sortable attributes at runtime:
- `get_index_settings()` for a single index
- `get_all_index_settings()` for all 9 indexes
- `get_filterable_attributes()` / `get_sortable_attributes()`
- Practical use case: build dynamic filters from discovered attributes

```bash
python examples/index_settings_discovery.py
```

## Directus REST API

### `directus_collections.py`
All 10 Directus collections with `get`, `list`, and `list_all` methods:
- Rencontres, Salles, Terrains, Tournois, Engagements, Formations, Entraineurs
- Communes, Officiels, Pratiques (list-only collections)

```bash
python examples/directus_collections.py
```

## Advanced Features

### `field_sets_and_filtering.py`
Tutorial on FieldSet, filtering, sorting, and pagination:
- `FieldSet` comparison (BASIC, DEFAULT, DETAILED, WILDCARD)
- Directus `filter_criteria` (JSON) vs Meilisearch `filter` (list)
- Sort syntax differences between APIs
- Manual pagination (offset) and auto-pagination (list_all)

```bash
python examples/field_sets_and_filtering.py
```

### `cross_api_workflows.py`
Four real-world end-to-end workflows combining Meilisearch + Directus:
1. Find a Parisian club and its venue
2. Discover venues and courts near Paris
3. Explore matches and team engagements
4. Tournaments, training, activities, and auxiliary data

```bash
python examples/cross_api_workflows.py
```

## Prerequisites

1. **Install the package:**
   ```bash
   pip install ffbb_api_client_v2
   ```

2. **Token Configuration (Choose one):**

   **Option A - Automatic (Recommended):**
   No configuration needed! Tokens are fetched automatically from the FFBB API.

   **Option B - Environment Variables:**
   Create a `.env` file in the project root:
   ```bash
   API_FFBB_APP_BEARER_TOKEN=your_ffbb_api_token_here
   MEILISEARCH_BEARER_TOKEN=your_meilisearch_token_here
   ```

3. **Install python-dotenv** (only if using Option B):
   ```bash
   pip install python-dotenv
   ```

## Token Management

### Automatic (Recommended)
```python
from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager

tokens = TokenManager.get_tokens()
client = FFBBAPIClientV2.create(
    api_bearer_token=tokens.api_token,
    meilisearch_bearer_token=tokens.meilisearch_token
)
```

### Manual (Environment Variables)
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_token = os.getenv("API_FFBB_APP_BEARER_TOKEN")
meilisearch_token = os.getenv("MEILISEARCH_BEARER_TOKEN")
```

## API Coverage

| API Layer | Endpoints | Example Files |
|---|---|---|
| Meilisearch Search | 18 search methods + multi_search | `search_all_indexes.py`, `quick_start.py`, `complete_usage_example.py` |
| Meilisearch Settings | 4 settings methods | `index_settings_discovery.py` |
| Directus REST (get) | 7 get methods | `directus_collections.py`, `cross_api_workflows.py` |
| Directus REST (list) | 10 list methods | `directus_collections.py`, `field_sets_and_filtering.py` |
| Directus REST (list_all) | 10 list_all methods | `directus_collections.py`, `field_sets_and_filtering.py` |
| Core (lives, saisons) | 2 methods | `quick_start.py` |
| FieldSet | 4 levels | `complete_usage_example.py`, `field_sets_and_filtering.py` |

## Support

If you encounter any issues:
1. Check your API tokens are correctly set in the `.env` file
2. Ensure you have a stable internet connection
3. Review the error messages - the client provides detailed error information
4. Check the test files in `tests/` for additional usage patterns
