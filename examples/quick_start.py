#!/usr/bin/env python3
"""Quick Start - Basic usage of the FFBB API Client V2.

Demonstrates: searching clubs, getting org info, checking live matches,
and retrieving active seasons.

Usage: python examples/quick_start.py
"""

import json

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager


def create_client() -> FFBBAPIClientV2:
    tokens = TokenManager.get_tokens()
    return FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )


def main() -> None:
    client = create_client()

    # --- 1. Search for clubs in Paris ---
    print("=" * 60)
    print("1. Searching for clubs in Paris")
    print("=" * 60)
    result = client.search_organismes("Paris", limit=5)
    if not result or not result.hits:
        print("No clubs found.")
        return

    print(f"Found {result.estimated_total_hits} total clubs matching 'Paris'")
    for hit in result.hits:
        commune_name = hit.commune.libelle if hit.commune else "N/A"
        print(f"  - {hit.nom} ({hit.code}) | {commune_name} | type={hit.type}")

    # --- 2. Get detailed info for the first club ---
    print()
    print("=" * 60)
    print("2. Getting detailed info for the first club")
    print("=" * 60)
    first_hit = result.hits[0]
    if not first_hit.id:
        print("First hit has no ID.")
        return
    org_id = int(first_hit.id)
    organisme = client.get_organisme(org_id)
    if not organisme:
        print(f"Could not retrieve organisme {org_id}")
        return

    print(f"Name:      {organisme.nom}")
    print(f"CodeEnum:      {organisme.code}")
    print(f"Address:   {organisme.adresse}")
    print(f"Phone:     {organisme.telephone}")
    print(f"Email:     {organisme.mail}")
    print(f"Website:   {organisme.url_site_web}")

    # organisme.commune is an int FK ID from Directus — resolve it
    if isinstance(organisme.commune, int):
        communes = client.list_communes(
            filter_criteria=json.dumps({"id": {"_eq": organisme.commune}})
        )
        if communes:
            c = communes[0]
            print(f"City:      {c.libelle} ({c.codePostal})")
    # organisme.salle is also an int FK ID
    if isinstance(organisme.salle, int):
        salle = client.get_salle(organisme.salle)
        if salle:
            print(f"Venue:     {salle.libelle}")
    print(f"Members:   {len(organisme.membres)}")
    print(f"Engagements: {len(organisme.engagements)}")

    # --- 3. Check live matches ---
    print()
    print("=" * 60)
    print("3. Checking live matches")
    print("=" * 60)
    lives = client.get_lives()
    if not lives:
        print("No live matches at the moment (normal outside of game hours).")
    else:
        print(f"{len(lives)} live match(es) in progress:")
        for live in lives[:5]:
            print(f"  - {live}")

    # --- 4. Retrieve active seasons ---
    print()
    print("=" * 60)
    print("4. Retrieving active seasons")
    print("=" * 60)
    saisons = client.get_saisons()
    if not saisons:
        print("No active seasons found.")
    else:
        for saison in saisons:
            print(f"  - {saison.libelle} (code={saison.code}, active={saison.actif})")

    print()
    print("Quick start complete!")


if __name__ == "__main__":
    main()
