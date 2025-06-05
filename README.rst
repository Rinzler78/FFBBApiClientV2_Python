FFBBApiClientV2_Python
======================

.. image:: https://github.com/Rinzler78/FFBBApiClientV2_Python/actions/workflows/ci.yml/badge.svg?branch=main
   :alt: Build Status
   :target: https://github.com/Rinzler78/FFBBApiClientV2_Python/actions/workflows/ci.yml

.. image:: https://readthedocs.org/projects/ffbbapiclientv2-python/badge/?version=latest
   :alt: Documentation Status
   :target: https://ffbbapiclientv2-python.readthedocs.io/en/latest/

.. image:: https://coveralls.io/repos/github/Rinzler78/FFBBApiClientV2_Python/badge.svg?branch=main
   :alt: Coverage
   :target: https://coveralls.io/github/Rinzler78/FFBBApiClientV2_Python

.. image:: https://img.shields.io/pypi/v/ffbb_api_client_v2.svg
   :alt: PyPI Version
   :target: https://pypi.org/project/ffbb_api_client_v2/

.. image:: https://pepy.tech/badge/ffbb_api_client_v2/month
   :alt: Monthly Downloads
   :target: https://pepy.tech/project/ffbb_api_client_v2

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
   :alt: Project generated with PyScaffold
   :target: https://pyscaffold.org/

ffbb_api_client_v2 allows you to interact with the new FFBB APIs. You can retrieve information about clubs, teams, matches and much more.

Features
--------

* Retrieve live events
* Search organismes
* Search rencontres
* Search terrains
* Search competitions
* Search salles
* Search pratiques
* Search tournois

Installation
============

.. code-block:: bash

    pip install ffbb_api_client_v2

Prerequisites
-------------

Set the following environment variables with your API credentials:

* ``MEILISEARCH_BEARER_TOKEN`` – token to access the search API
* ``API_FFBB_APP_BEARER_TOKEN`` – token to access the main FFBB API

Quick start
===========

.. code-block:: python

    import os
    from ffbb_api_client_v2 import FFBBAPIClientV2

    # Load env from file if needed
    # from dotenv import load_dotenv
    # load_dotenv()

    MEILISEARCH_TOKEN = os.getenv("MEILISEARCH_BEARER_TOKEN")
    API_TOKEN = os.getenv("API_FFBB_APP_BEARER_TOKEN")

    # Create an instance of the api client
    ffbb_api_client = FFBBAPIClientV2.create(MEILISEARCH_TOKEN, API_TOKEN)

    # Get the lives
    lives = ffbb_api_client.get_lives()

    # Get the organismes
    organismes = ffbb_api_client.search_organismes("Paris")

    # Get the rencontres
    rencontres = ffbb_api_client.search_rencontres("Basket")

    # Get the terrains
    terrains = ffbb_api_client.search_terrains("Basket")

    # Get the competitions
    competitions = ffbb_api_client.search_competitions("Basket")

    # Get the salles
    salles = ffbb_api_client.search_salles("Basket")

    # Get practices
    pratiques = ffbb_api_client.search_pratiques("Basket")

    # Get tournois
    tournois = ffbb_api_client.search_tournois("Basket")

Examples
========

Take a look at ``quick_start.py`` to see how to use the library.

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

Running tests
=============

Install the project in editable mode with the ``testing`` extras and execute
``pytest``:

.. code-block:: bash

    pip install -e .[testing]
    pytest -q
