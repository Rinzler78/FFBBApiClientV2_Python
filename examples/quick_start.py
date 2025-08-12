#!/usr/bin/env python3
"""
Quick Start Example for FFBB API Client V2

This example shows the most basic usage of the FFBB API Client V2.

Prerequisites:
1. Install the package: pip install ffbb_api_client_v2
2. Set up your .env file with:
   API_FFBB_APP_BEARER_TOKEN=your_api_token_here
   MEILISEARCH_BEARER_TOKEN=your_meilisearch_token_here
"""

import os

from dotenv import load_dotenv

from ffbb_api_client_v2 import FFBBAPIClientV2


def main():
    """Quick start example."""

    # Load environment variables from .env file
    load_dotenv()

    # Get your API tokens
    api_token = os.getenv("API_FFBB_APP_BEARER_TOKEN")
    meilisearch_token = os.getenv("MEILISEARCH_BEARER_TOKEN")

    if not api_token or not meilisearch_token:
        print("Please set up your API tokens in a .env file")
        return

    # Create the API client
    client = FFBBAPIClientV2.create(
        api_bearer_token=api_token, meilisearch_bearer_token=meilisearch_token
    )

    print("🏀 FFBB API Client V2 - Quick Start")
    print("=" * 40)

    # Example 1: Search for basketball clubs in Paris
    print("\n1. Searching for clubs in Paris...")
    paris_clubs = client.search_organismes("Paris")
    print(f"   Found {len(paris_clubs.hits)} clubs")

    # Example 2: Get detailed information about the first club
    if paris_clubs.hits:
        club = paris_clubs.hits[0]
        print(f"\n2. Getting details for: {club.nom}")

        club_details = client.get_organisme(int(club.id))
        if club_details:
            print(f"   Name: {club_details.nom}")
            print(f"   Type: {club_details.type}")
            print(f"   Address: {club_details.adresse}")
            print(
                f"   Teams: "
                f"{len(club_details.engagements) if club_details.engagements else 0}"
            )

    # Example 3: Get current live matches
    print("\n3. Getting live matches...")
    lives = client.get_lives()
    print(f"   Currently {len(lives)} live matches")

    # Example 4: Get current seasons
    print("\n4. Getting current seasons...")
    seasons = client.get_saisons()
    active_seasons = [s for s in seasons if s.actif]
    print(f"   Found {len(active_seasons)} active seasons")

    print("\n✅ Quick start completed!")
    print("📚 Check out complete_usage_example.py for advanced features")


if __name__ == "__main__":
    main()
