========
Examples
========

This page contains practical examples of how to use the FFBB API Client V2 library.

Basic Usage
===========

Simple Client Creation and Usage
---------------------------------

.. code-block:: python

    import os
    from ffbb_api_client_v2 import FFBBAPIClientV2

    # Load environment variables
    MEILISEARCH_TOKEN = os.getenv("MEILISEARCH_BEARER_TOKEN")
    API_TOKEN = os.getenv("API_FFBB_APP_BEARER_TOKEN")

    # Create the main client
    client = FFBBAPIClientV2.create(MEILISEARCH_TOKEN, API_TOKEN)

    # Get live games
    lives = client.get_lives()
    print(f"Found {len(lives)} live games")

Token Management
================

The FFBB API Client V2 provides advanced token management features introduced in v1.2.0.

Automatic Token Resolution (Recommended)
-----------------------------------------

The ``TokenManager`` class automatically resolves API tokens from multiple sources:

.. code-block:: python

    from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager

    # Automatic token resolution - no configuration needed!
    tokens = TokenManager.get_tokens()

    client = FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token
    )

Token Resolution Priority:

1. **Environment Variables** (if set)
2. **FFBB API Configuration Endpoint** (public, automatic fallback)

Token Caching and Performance
------------------------------

Tokens are automatically cached for performance:

.. code-block:: python

    # First call fetches tokens
    tokens = TokenManager.get_tokens()

    # Subsequent calls use cached tokens (fast!)
    tokens = TokenManager.get_tokens()

    # Force refresh with new parameters (v1.2.0+)
    tokens = TokenManager.get_tokens(use_cache=False)

Cache Management
~~~~~~~~~~~~~~~~

.. code-block:: python

    from ffbb_api_client_v2.utils.cache_manager import CacheManager

    # Clear token cache
    CacheManager().clear()

Configuration Management (v1.2.0+)
====================================

Centralized configuration constants for better maintainability:

.. code-block:: python

    from ffbb_api_client_v2 import config

    # API endpoints
    print(f"API Base URL: {config.API_FFBB_BASE_URL}")
    print(f"Meilisearch URL: {config.MEILISEARCH_BASE_URL}")

    # Default headers
    print(f"User Agent: {config.DEFAULT_USER_AGENT}")

    # Endpoint paths
    print(f"Configuration: {config.ENDPOINT_CONFIGURATION}")
    print(f"Lives: {config.ENDPOINT_LIVES}")

Advanced Features (v1.2.0+)
============================

Parallel Test Execution
-----------------------

Run tests in parallel for faster CI/CD:

.. code-block:: bash

    # Install pytest-xdist
    pip install pytest-xdist

    # Run tests in parallel
    pytest -n auto

Python 3.10+ Features
----------------------

Leverage modern Python features:

.. code-block:: python

    # Union types with | syntax (Python 3.10+)
    from ffbb_api_client_v2.models import GetOrganismeResponse

    def process_organisme(org: GetOrganismeResponse | None) -> str:
        return org.nom if org else "Unknown"

Enhanced Type Safety
--------------------

Comprehensive type hints throughout the codebase:

.. code-block:: python

    from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager
    from typing import Optional

    def safe_get_organisme(client: FFBBAPIClientV2, org_id: int) -> Optional[GetOrganismeResponse]:
        """Safely get organisme with proper error handling."""
        try:
            return client.get_organisme(org_id)
        except Exception:
            return None

Manual Token Configuration
--------------------------

If you prefer to manage tokens manually:

.. code-block:: python

    import os
    from dotenv import load_dotenv
    from ffbb_api_client_v2 import FFBBAPIClientV2

    load_dotenv()
    api_token = os.getenv("API_FFBB_APP_BEARER_TOKEN")
    meilisearch_token = os.getenv("MEILISEARCH_BEARER_TOKEN")

    client = FFBBAPIClientV2.create(
        api_bearer_token=api_token,
        meilisearch_bearer_token=meilisearch_token
    )

Advanced Client Usage
=====================

Using Specific Clients
-----------------------

.. code-block:: python

    from ffbb_api_client_v2 import ApiFFBBAppClient, MeilisearchFFBBClient

    # Use individual clients for specific needs
    api_client = ApiFFBBAppClient(API_TOKEN)
    meilisearch_client = MeilisearchFFBBClient(MEILISEARCH_TOKEN)

    # Get live games from API client
    lives = api_client.get_lives()

    # Search for organizations using Meilisearch
    organismes = meilisearch_client.search_organismes("Paris")

Working with Search Queries
============================

Creating Custom Search Queries
-------------------------------

.. code-block:: python

    from ffbb_api_client_v2 import MultiSearchQuery, generate_queries

    # Generate default queries for all entity types
    queries = generate_queries("basketball", limit=10)

    # Create custom queries
    from ffbb_api_client_v2 import OrganismesMultiSearchQuery

    custom_query = OrganismesMultiSearchQuery(
        q="Paris",
        limit=20,
        offset=0
    )

    # Execute the search
    results = client.meilisearch_ffbb_client.multi_search([custom_query])

Data Models and Processing
==========================

Working with Live Games
------------------------

.. code-block:: python

    from ffbb_api_client_v2 import Live

    # Get live games
    lives = client.get_lives()

    for live in lives:
        if live.match_status == "EN_COURS":
            print(f"Live: {live.team_name_home} vs {live.team_name_out}")
            print(f"Score: {live.score_home} - {live.score_out}")
            print(f"Time: {live.clock.minutes}:{live.clock.seconds}")

Processing Search Results
-------------------------

.. code-block:: python

    # Search for organizations
    organismes_result = client.search_organismes("Basketball Club")

    print(f"Total results: {organismes_result.estimated_total_hits}")
    print(f"Results returned: {len(organismes_result.hits)}")

    for hit in organismes_result.hits:
        org = hit.source  # The actual organization data
        print(f"Organization: {org.nom_officiel}")
        print(f"Type: {org.type_association_libelle}")
        print(f"City: {org.commune}")

Multiple Search Operations
==========================

Batch Searches
---------------

.. code-block:: python

    # Search multiple entities in one operation
    search_terms = ["Paris", "Lyon", "Marseille"]

    # Search organisations in multiple cities
    all_organismes = client.search_multiple_organismes(search_terms)

    # Search competitions
    competitions = client.search_multiple_competitions(search_terms)

    # Search venues (salles)
    salles = client.search_multiple_salles(search_terms)

Advanced Features
=================

Using Client Extensions
-----------------------

.. code-block:: python

    from ffbb_api_client_v2 import MeilisearchClientExtension

    # Create extended client with additional features
    extended_client = MeilisearchClientExtension(
        bearer_token=MEILISEARCH_TOKEN,
        url="https://meilisearch-prod.ffbb.app/"
    )

    # Use smart search with automatic filtering
    results = extended_client.smart_multi_search(queries)

    # Use recursive search to get all results
    all_results = extended_client.recursive_smart_multi_search(queries)

Error Handling
==============

Robust Error Handling
----------------------

.. code-block:: python

    from ffbb_api_client_v2 import FFBBAPIClientV2
    import requests

    try:
        client = FFBBAPIClientV2.create(MEILISEARCH_TOKEN, API_TOKEN)

        # Perform searches with error handling
        lives = client.get_lives()

    except ValueError as e:
        print(f"Configuration error: {e}")
    except requests.RequestException as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

Caching and Performance
=======================

Using Cached Sessions
---------------------

.. code-block:: python

    from requests_cache import CachedSession
    from ffbb_api_client_v2 import FFBBAPIClientV2

    # Create custom cached session
    cached_session = CachedSession(
        'ffbb_cache',
        backend='sqlite',
        expire_after=3600  # 1 hour cache
    )

    # Create client with custom session
    api_client = ApiFFBBAppClient(
        bearer_token=API_TOKEN,
        cached_session=cached_session
    )

    meilisearch_client = MeilisearchFFBBClient(
        bearer_token=MEILISEARCH_TOKEN,
        cached_session=cached_session
    )

    # Create main client
    client = FFBBAPIClientV2(api_client, meilisearch_client)

Data Export and Processing
==========================

Exporting Search Results
-------------------------

.. code-block:: python

    import json
    import csv

    # Get organization data
    organismes = client.search_organismes("Club", limit=100)

    # Export to JSON
    with open('organismes.json', 'w', encoding='utf-8') as f:
        json.dump([hit.source.to_dict() for hit in organismes.hits], f,
                  indent=2, ensure_ascii=False)

    # Export to CSV
    with open('organismes.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Type', 'City', 'Department'])

        for hit in organismes.hits:
            org = hit.source
            writer.writerow([
                org.nom_officiel,
                org.type_association_libelle,
                org.commune,
                org.code_postal[:2] if org.code_postal else ''
            ])

Searching Engagements & Formations (v1.3.0+)
=============================================

Two new Meilisearch indexes are available: engagements (~105k hits) and formations (~90 hits).

.. code-block:: python

    from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager

    tokens = TokenManager.get_tokens()
    client = FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token
    )

    # Search engagements
    engagements = client.search_engagements("Paris", limit=10)
    print(f"Found {engagements.estimated_total_hits} engagements")
    for hit in engagements.hits:
        print(f"  - {hit.source}")

    # Search formations
    formations = client.search_formations("arbitre", limit=5)
    print(f"Found {formations.estimated_total_hits} formations")
    for hit in formations.hits:
        print(f"  - {hit.source}")

Filtered & Sorted Search (v1.3.0+)
====================================

All 18 search methods now support ``filter``, ``sort``, and ``limit`` parameters.

.. code-block:: python

    # Search with filter and sort
    organismes = client.search_organismes(
        "Paris",
        filter="type_association_libelle = 'Association'",
        sort=["nom_officiel:asc"],
        limit=20
    )

    # Search competitions with sorting
    competitions = client.search_competitions(
        "Championnat",
        sort=["saison:desc"],
        limit=10
    )

    # Search rencontres with filter
    rencontres = client.search_rencontres(
        "Lyon",
        filter="saison_sportive = '2025-2026'",
        limit=50
    )

Index Settings Discovery (v1.3.0+)
====================================

Retrieve the settings of any Meilisearch index at runtime.

.. code-block:: python

    from ffbb_api_client_v2 import MeilisearchFFBBClient

    meilisearch_client = MeilisearchFFBBClient(meilisearch_token)

    # Get settings for the organismes index
    settings = meilisearch_client.get_index_settings("ffbbserver_organismes")
    print(f"Filterable attributes: {settings.filterable_attributes}")
    print(f"Sortable attributes: {settings.sortable_attributes}")
    print(f"Searchable attributes: {settings.searchable_attributes}")

Using FieldSet.WILDCARD (v1.3.0+)
===================================

Use ``FieldSet.WILDCARD`` to retrieve all available fields from a Directus endpoint.

.. code-block:: python

    from ffbb_api_client_v2.models.query_fields import FieldSet

    # Get all available fields for an organisme
    organisme = client.get_organisme(123, field_set=FieldSet.WILDCARD)

    # Get all fields for a competition
    competition = client.get_competition(456, field_set=FieldSet.WILDCARD)

Complete Example Script
=======================

Here's a complete example that demonstrates various features:

.. code-block:: python

    #!/usr/bin/env python3
    """
    Complete example of FFBB API Client V2 usage
    """
    import os
    import json
    from dotenv import load_dotenv
    from ffbb_api_client_v2 import FFBBAPIClientV2

    def main():
        # Load environment
        load_dotenv()

        MEILISEARCH_TOKEN = os.getenv("MEILISEARCH_BEARER_TOKEN")
        API_TOKEN = os.getenv("API_FFBB_APP_BEARER_TOKEN")

        if not MEILISEARCH_TOKEN or not API_TOKEN:
            print("Error: Missing API tokens in environment")
            return

        # Create client
        client = FFBBAPIClientV2.create(MEILISEARCH_TOKEN, API_TOKEN, debug=True)

        try:
            # Get live games
            print("=== Live Games ===")
            lives = client.get_lives()
            print(f"Found {len(lives)} live games")

            # Search organizations
            print("\n=== Organizations in Paris ===")
            organismes = client.search_organismes("Paris", limit=5)
            print(f"Total found: {organismes.estimated_total_hits}")

            for hit in organismes.hits[:3]:  # Show first 3
                org = hit.source
                print(f"- {org.nom_officiel} ({org.commune})")

            # Search competitions
            print("\n=== Basketball Competitions ===")
            competitions = client.search_competitions("basketball", limit=3)

            for hit in competitions.hits:
                comp = hit.source
                print(f"- {comp.nom} ({comp.saison})")

            print("\nExample completed successfully!")

        except Exception as e:
            print(f"Error: {e}")

    if __name__ == "__main__":
        main()

This example can be saved as a script and run directly to test the library functionality.
