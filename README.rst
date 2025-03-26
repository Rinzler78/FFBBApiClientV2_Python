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


    Allow to interact with the new FFBB apis


ffbb_api_client_v2 allow to interact with the new FFBB api.
You can retrieve information about clubs, teams, matches, etc...


Installation
============

.. code-block:: bash

    pip install ffbb_api_client_v2

Quick start
===========

.. code-block:: python

    import os
    from ffbb_api_client_v2 import FFBBAPIClientV2

    # Load env from file if needed
    # from dotenv import load_dotenv
    # load_dotenv()

    # Retrieve apis bearer tokens
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

    # Get pratiques
    pratiques = ffbb_api_client.search_pratiques("Basket")

    # Get tournois
    tournois = ffbb_api_client.search_tournois("Basket")

Examples
========

Take a look at quick_start.py to see how to use the library.

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
