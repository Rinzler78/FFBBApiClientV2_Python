.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/FFBBApiClientV2_Python.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/FFBBApiClientV2_Python
    .. image:: https://readthedocs.org/projects/FFBBApiClientV2_Python/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://FFBBApiClientV2_Python.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/FFBBApiClientV2_Python/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/FFBBApiClientV2_Python
    .. image:: https://img.shields.io/pypi/v/FFBBApiClientV2_Python.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/FFBBApiClientV2_Python/
    .. image:: https://img.shields.io/conda/vn/conda-forge/FFBBApiClientV2_Python.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/FFBBApiClientV2_Python
    .. image:: https://pepy.tech/badge/FFBBApiClientV2_Python/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/FFBBApiClientV2_Python
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/FFBBApiClientV2_Python
.. image:: https://img.shields.io/pypi/v/ffbb_api_client_v2.svg
    :alt: PyPI-Server
    :target: https://pypi.org/project/ffbb_api_client_v2/

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

======================
FFBBApiClientV2_Python
======================


    Modern Python client library for FFBB (French Basketball Federation) APIs


ffbb_api_client_v2 is a modern Python client library for interacting with the French Basketball Federation (FFBB) APIs.
It provides a comprehensive interface to retrieve information about clubs, teams, competitions, matches, seasons, and more.

**Key Features:**

- 🏀 **Complete API Coverage**: Access all FFBB services including competitions, organismes, seasons, lives, and search
- 🔧 **Type-Safe Models**: Strongly-typed data models with automatic validation and error handling
- 🎯 **Flexible Field Selection**: Customizable field queries (BASIC, DEFAULT, DETAILED) for optimized API calls
- 📦 **Modern Architecture**: Clean, modular design with organized package structure
- ⚡ **Request Caching**: Built-in caching support for improved performance
- 🧪 **Thoroughly Tested**: Comprehensive unit and integration tests ensuring reliability


Installation
============

**For Users (Production):**

.. code-block:: bash

    pip install ffbb_api_client_v2

**For Developers (with examples and analysis tools):**

.. code-block:: bash

    # Clone the repository
    git clone https://github.com/Rinzler78/FFBBApiClientV2_Python.git
    cd FFBBApiClientV2_Python

    # Run the automated setup script (recommended)
    ./setup_dev.sh

    # Or set up manually:
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e .
    pip install -r requirements.txt

The development setup includes:

- Core FFBB API Client library
- Data analysis libraries (pandas, numpy, matplotlib, seaborn)
- Jupyter notebook environment for interactive analysis
- Testing framework (pytest, coverage)
- Pre-commit hooks for code quality
- Type checking tools

**Requirements File:**

The ``requirements.txt`` file contains all development dependencies including:

- Core dependencies (requests, python-dotenv, etc.)
- Data analysis libraries for examples
- Testing and development tools
- Jupyter notebook environment

Quick Start
===========

.. code-block:: python

    from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager

    # Simplified method: automatic token retrieval
    tokens = TokenManager.get_tokens()
    client = FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token
    )

    # Search for organizations in Paris
    organismes = client.search_organismes("Paris")
    print(f"Found {len(organismes.hits)} organizations in Paris")

    # Get detailed information about a specific organization
    if organismes.hits:
        organisme_id = int(organismes.hits[0].id)
        organisme_details = client.get_organisme(organisme_id)
        print(f"Organization: {organisme_details.nom}")
        print(f"  - Type: {organisme_details.type}")
        print(f"  - Address: {organisme_details.adresse}")
        print(f"  - Teams: {len(organisme_details.engagements)}")

    # Get live matches
    lives = client.get_lives()
    print(f"Current live matches: {len(lives)}")

    # Get current seasons
    saisons = client.get_saisons()
    print(f"Available seasons: {len(saisons)}")

    # Search competitions
    competitions = client.search_competitions("Championnat")
    print(f"Found {len(competitions.hits)} competitions")

Advanced Usage
==============

**Working with Custom Fields**

.. code-block:: python

    from ffbb_api_client_v2.models.query_fields import QueryFieldsManager, FieldSet

    # Get organization with basic fields only
    basic_fields = QueryFieldsManager.get_organisme_fields(FieldSet.BASIC)
    organisme = client.get_organisme(
        organisme_id=12345,
        fields=basic_fields
    )

    # Get organization with detailed information
    organisme_full = client.get_organisme(
        organisme_id=12345
    )

**Working with Competitions and Seasons**

.. code-block:: python

    # Get competition details with default fields
    competition = client.get_competition(competition_id=98765)
    print(f"Competition: {competition.nom}")
    print(f"Season: {competition.saison}")
    print(f"Type: {competition.typeCompetition}")

    # Get active seasons only
    active_saisons = client.get_saisons(
        filter_criteria='{"actif":{"_eq":true}}'
    )

**Search Across Multiple Resources**

.. code-block:: python

    # Multi-search across all resource types
    results = client.multi_search("Lyon")
    for result in results:
        print(f"Found: {result.query} in {type(result).__name__}")

    # Search specific resource types
    clubs = client.search_organismes("Lyon")
    matches = client.search_rencontres("Lyon")
    venues = client.search_salles("Lyon")

Package Structure
=================

The library is organized into the following packages:

- **clients/**: API client classes for interacting with FFBB services

  - ``FFBBAPIClientV2``: Main client combining all services
  - ``ApiFFBBAppClient``: Direct API client for FFBB App API
  - ``MeilisearchFFBBClient``: Client for search functionality

- **models/**: Strongly-typed data models and response structures

  - ``get_*_response.py``: Response models for API endpoints
  - ``*_models.py``: Specialized models for competitions, organizations, etc.
  - ``query_fields.py``: Field management for API queries

- **helpers/**: Extensions and utility helpers
- **utils/**: Data conversion and processing utilities

.. code-block:: python

    # Import specific clients
    from ffbb_api_client_v2.clients import ApiFFBBAppClient, MeilisearchFFBBClient

    # Import data models
    from ffbb_api_client_v2.models.get_organisme_response import GetOrganismeResponse
    from ffbb_api_client_v2.models.competitions_models import GetCompetitionResponse
    from ffbb_api_client_v2.models.saisons_models import GetSaisonsResponse

    # Import field management
    from ffbb_api_client_v2.models.query_fields import QueryFieldsManager, FieldSet

Environment Configuration
=========================

Create a ``.env`` file in your project root:

.. code-block:: bash

    # .env file
    API_FFBB_APP_BEARER_TOKEN=your_ffbb_api_token_here
    MEILISEARCH_BEARER_TOKEN=your_meilisearch_token_here

Token Management
================

The library provides a ``TokenManager`` class for simplified token handling:

**Automatic Token Resolution:**

.. code-block:: python

    from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager

    # Tokens are resolved automatically:
    # 1. From environment variables (if set)
    # 2. From FFBB API configuration endpoint (public)
    tokens = TokenManager.get_tokens()

    client = FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token
    )

**Environment Variables (Optional):**

If you prefer to use environment variables, set these in your ``.env`` file:

.. code-block:: bash

    API_FFBB_APP_BEARER_TOKEN=your_token_here
    MEILISEARCH_BEARER_TOKEN=your_token_here

**Token Caching:**

.. code-block:: python

    # Tokens are cached by default
    tokens = TokenManager.get_tokens()  # Fetched
    tokens = TokenManager.get_tokens()  # From cache

    # Force refresh (v1.2.0+)
    tokens = TokenManager.get_tokens(use_cache=False)

    # Clear cache (use CacheManager directly in v1.2.0+)
    from ffbb_api_client_v2.utils.cache_manager import CacheManager
    CacheManager().clear()

API Reference
=============

**Main Client Methods:**

- ``get_lives()`` - Get current live matches
- ``get_saisons()`` - Get seasons with optional filtering
- ``get_organisme(organisme_id, fields=None)`` - Get detailed organization info
- ``get_competition(competition_id, fields=None)`` - Get competition details
- ``get_poule(poule_id, fields=None)`` - Get pool/group information
- ``search_organismes(name)`` - Search organizations by name
- ``search_competitions(name)`` - Search competitions by name
- ``search_rencontres(name)`` - Search matches by name
- ``search_salles(name)`` - Search venues by name
- ``multi_search(name)`` - Search across all resource types

**Field Selection Options:**

- ``FieldSet.BASIC`` - Essential fields only
- ``FieldSet.DEFAULT`` - Standard field set (used when fields=None)
- ``FieldSet.DETAILED`` - Comprehensive field set with nested data

Testing
=======

The library includes comprehensive test coverage:

.. code-block:: bash

    # Run specific unit tests
    python -m unittest tests.test_001_unit_tests_core -v

    # Run integration tests (requires API tokens)
    python -m unittest tests.test_011_enhanced_integration -v

    # Run all tests with discovery
    python -m unittest discover tests/ -v

    # Alternative: use tox for comprehensive testing
    tox

Examples
========

For more examples, check out the test files in the ``tests/`` directory, particularly:

- ``test_011_enhanced_integration.py`` - Real-world usage scenarios
- ``test_001_unit_tests_core.py`` - Unit test examples showing all client methods
- ``test_005_integration_user_journey.py`` - Complete user journey scenarios
- ``test_010_integration_user_journey.py`` - Multi-city comparison examples

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.

Licence
=======

ffbb_api_client_v2 is distributed under the Apache 2.0 license.

Dev notes
=========

Command used to create this project:

.. code-block:: bash

    putup FFBBApiClientV2_Python -p ffbb_api_client_v2 -l Apache-2.0 -d "Allow to interact with the new FFBB apis" -u "https://github.com/Rinzler78/FFBBApiClientV2_Python" -v --github-actions --venv .venv
