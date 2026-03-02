.. image:: https://img.shields.io/pypi/v/ffbb_api_client_v2.svg
    :alt: PyPI version
    :target: https://pypi.org/project/ffbb_api_client_v2/

.. image:: https://img.shields.io/pypi/pyversions/ffbb_api_client_v2.svg
    :alt: Python versions
    :target: https://pypi.org/project/ffbb_api_client_v2/

.. image:: https://img.shields.io/pypi/l/ffbb_api_client_v2.svg
    :alt: License
    :target: https://github.com/Rinzler78/FFBBApiClientV2_Python/blob/master/LICENSE.txt

.. image:: https://github.com/Rinzler78/FFBBApiClientV2_Python/actions/workflows/ci.yml/badge.svg
    :alt: CI status
    :target: https://github.com/Rinzler78/FFBBApiClientV2_Python/actions/workflows/ci.yml

.. image:: https://coveralls.io/repos/github/Rinzler78/FFBBApiClientV2_Python/badge.svg?branch=master
    :alt: Coverage
    :target: https://coveralls.io/github/Rinzler78/FFBBApiClientV2_Python?branch=master

.. image:: https://pepy.tech/badge/ffbb_api_client_v2/month
    :alt: Monthly downloads
    :target: https://pepy.tech/project/ffbb_api_client_v2

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

======================
FFBBApiClientV2_Python
======================


    Modern Python client library for FFBB (French Basketball Federation) APIs


**1700+ tests** | **96%+ branch coverage** | **MyPy strict** | **Python 3.10+** | **9 Meilisearch indexes**

ffbb_api_client_v2 is a modern Python client library for interacting with the French Basketball Federation (FFBB) APIs.
It provides a comprehensive interface to retrieve information about clubs, teams, competitions, matches, seasons, and more.

**Key Features:**

- **Complete API Coverage**: Access all FFBB services including competitions, organismes, seasons, lives, and search
- **Type-Safe Models**: Strongly-typed data models with automatic validation and error handling
- **Flexible Field Selection**: Comprehensive field queries with per-endpoint field definitions
- **Modern Architecture**: Clean, modular design with organized package structure
- **Request Caching**: Built-in caching support for improved performance
- **Thoroughly Tested**: Comprehensive unit and integration tests ensuring reliability

What's New
==========

- **v1.4.0**: Simplified field management (single ``FieldSet.DEFAULT``), ``QueryFieldsManager`` is now an ABC, all ``*Fields`` classes expose ``get_fields()``
- **v1.3.0**: Simplified Directus API (``fields`` removed, typed deep params), 2 new Meilisearch indexes (engagements, formations), ``filter``/``sort``/``limit`` on all 18 search methods, corrected TerrainsHit/TournoisHit models
- **v1.2.0**: TokenManager with automatic token resolution from FFBB public endpoint
- **Basketball analytics notebooks** for Elo rating and season projection


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

**Working with Field Sets (v1.4.0+)**

.. code-block:: python

    # All queries use comprehensive DEFAULT field lists
    organisme = client.get_organisme(organisme_id=12345)

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
    from ffbb_api_client_v2 import FieldSet

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
    from ffbb_api_client_v2.utils.cache_manager import CacheConfig
    tokens = TokenManager.get_tokens(cache_config=CacheConfig(enabled=False))

    # Clear cache (use CacheManager directly in v1.2.0+)
    from ffbb_api_client_v2.utils.cache_manager import CacheManager
    CacheManager().clear()

API Reference
=============

**Main Client Methods:**

- ``get_lives()`` - Get current live matches
- ``get_saisons()`` - Get seasons with optional filtering
- ``get_organisme(organisme_id)`` - Get detailed organization info
- ``get_competition(competition_id)`` - Get competition details
- ``get_poule(poule_id)`` - Get pool/group information
- ``search_organismes(name)`` - Search organizations by name
- ``search_competitions(name)`` - Search competitions by name
- ``search_rencontres(name)`` - Search matches by name
- ``search_salles(name)`` - Search venues by name
- ``multi_search(name)`` - Search across all resource types

**Field Selection:**

- ``FieldSet.DEFAULT`` - Comprehensive field set (the only level)

Testing
=======

The library includes comprehensive test coverage: **1700+ unit tests, 96%+ branch coverage**.

.. code-block:: bash

    # Unit tests (parallel)
    python -m pytest tests/unit/ -x -q -n auto

    # Integration tests (requires API tokens)
    python -m pytest tests/integration/ -q

    # Coverage report
    python -m pytest tests/ --cov=ffbb_api_client_v2 --cov-branch -q

Examples
========

Interactive notebooks and scripts are available in the ``examples/`` directory:

- ``examples/simple_rating_notebook.ipynb`` - Elo rating analysis for a championship
- ``examples/projection_notebook.ipynb`` - End-of-season projection
- ``examples/basketball_dashboard.py`` - Interactive Streamlit dashboard
- ``examples/user_journeys.py`` - End-to-end user journey examples
- ``docs/api_architecture.md`` - API architecture and data model documentation

Contributing
============

Contributions are welcome! See `CONTRIBUTING.rst <https://github.com/Rinzler78/FFBBApiClientV2_Python/blob/master/CONTRIBUTING.rst>`_ for development setup, branching conventions, and the pull request workflow.

Licence
=======

ffbb_api_client_v2 is distributed under the Apache 2.0 license.

.. note::

    This project has been set up using `PyScaffold <https://pyscaffold.org/>`_ 4.5.
