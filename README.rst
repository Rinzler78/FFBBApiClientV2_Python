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

.. code-block:: bash

    pip install ffbb_api_client_v2

Quick Start
===========

.. code-block:: python

    import os
    from ffbb_api_client_v2 import FFBBAPIClientV2
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    # Retrieve API bearer tokens
    MEILISEARCH_TOKEN = os.getenv("MEILISEARCH_BEARER_TOKEN")
    API_TOKEN = os.getenv("API_FFBB_APP_BEARER_TOKEN")

    # Create an instance of the API client
    ffbb_api_client = FFBBAPIClientV2.create(
        meilisearch_bearer_token=MEILISEARCH_TOKEN,
        api_bearer_token=API_TOKEN
    )

    # Search for organizations in Paris
    organismes = ffbb_api_client.search_organismes("Paris")
    print(f"Found {len(organismes.hits)} organizations in Paris")

    # Get detailed information about a specific organization
    if organismes.hits:
        organisme_id = int(organismes.hits[0].id)
        organisme_details = ffbb_api_client.get_organisme(organisme_id)
        print(f"Organization: {organisme_details.nom}")
        print(f"  - Type: {organisme_details.type}")
        print(f"  - Address: {organisme_details.adresse}")
        print(f"  - Teams: {len(organisme_details.engagements)}")

    # Get live matches
    lives = ffbb_api_client.get_lives()
    print(f"Current live matches: {len(lives)}")

    # Get current seasons
    saisons = ffbb_api_client.get_saisons()
    print(f"Available seasons: {len(saisons)}")

    # Search competitions
    competitions = ffbb_api_client.search_competitions("Championnat")
    print(f"Found {len(competitions.hits)} competitions")

Advanced Usage
==============

**Working with Custom Fields**

.. code-block:: python

    from ffbb_api_client_v2.models.query_fields import QueryFieldsManager, FieldSet

    # Get organization with basic fields only
    basic_fields = QueryFieldsManager.get_organisme_fields(FieldSet.BASIC)
    organisme = ffbb_api_client.get_organisme(
        organisme_id=12345,
        fields=basic_fields
    )

    # Get organization with detailed information
    organisme_full = ffbb_api_client.get_organisme(
        organisme_id=12345
    )

**Working with Competitions and Seasons**

.. code-block:: python

    # Get competition details with default fields
    competition = ffbb_api_client.get_competition(competition_id=98765)
    print(f"Competition: {competition.nom}")
    print(f"Season: {competition.saison}")
    print(f"Type: {competition.typeCompetition}")

    # Get active seasons only
    active_saisons = ffbb_api_client.get_saisons(
        filter_criteria='{"actif":{"_eq":true}}'
    )

**Search Across Multiple Resources**

.. code-block:: python

    # Multi-search across all resource types
    results = ffbb_api_client.multi_search("Lyon")
    for result in results:
        print(f"Found: {result.query} in {type(result).__name__}")

    # Search specific resource types
    clubs = ffbb_api_client.search_organismes("Lyon")
    matches = ffbb_api_client.search_rencontres("Lyon")
    venues = ffbb_api_client.search_salles("Lyon")

Package Structure
=================

The library is organized into the following packages:

- **clients/**: API client classes for interacting with FFBB services

  - ``ApiFFBBAppClient``: Direct API client for FFBB App API
  - ``MeilisearchFFBBClient``: Client for search functionality
  - ``FFBBAPIClientV2``: Main client combining both services

- **models/**: Strongly-typed data models and response structures

  - ``competitions_models.py``: Competition and match models
  - ``organismes_models.py``: Organization and team models
  - ``saisons_models.py``: Season models
  - ``poules_models.py``: Pool/group models
  - ``query_fields.py``: Field management for API queries

- **helpers/**: Extensions and utility helpers
- **utils/**: Data conversion and processing utilities

.. code-block:: python

    # Import specific clients
    from ffbb_api_client_v2.clients import ApiFFBBAppClient, MeilisearchFFBBClient

    # Import data models
    from ffbb_api_client_v2.models.organismes_models import GetOrganismeResponse
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

Note
====

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
