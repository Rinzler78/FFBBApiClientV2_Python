#!/usr/bin/env python3
"""Complete Usage Example - Comprehensive demonstration of all major features.

Covers: type-safe models, field selection, error handling, multi-search,
competition details, and advanced API usage patterns.

Usage: python examples/complete_usage_example.py
"""

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager


def create_client() -> FFBBAPIClientV2:
    tokens = TokenManager.get_tokens()
    return FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )


def demo_search_organismes(client: FFBBAPIClientV2) -> int | None:
    """Search for clubs and return the first organisme ID."""
    print("=" * 60)
    print("1. Search Organismes")
    print("=" * 60)

    result = client.search_organismes("Paris", limit=5)
    if not result or not result.hits:
        print("No clubs found.")
        return None

    print(f"Found ~{result.estimated_total_hits} clubs for 'Paris'")
    for hit in result.hits:
        commune_name = hit.commune.libelle if hit.commune else "N/A"
        print(f"  - [{hit.id}] {hit.nom} | {commune_name} | mail={hit.mail}")

    first_id = result.hits[0].id
    return int(first_id) if first_id else None


def demo_multiple_search(client: FFBBAPIClientV2) -> None:
    """Search multiple queries in a single call."""
    print()
    print("=" * 60)
    print("2. Multi-Query Search (search_multiple_organismes)")
    print("=" * 60)

    results = client.search_multiple_organismes(
        ["Paris", "Boulogne", "Nanterre"], limit=3
    )
    if not results:
        print("No results.")
        return

    for res in results:
        print(f"\n  Query: '{res.query}' -> {res.estimated_total_hits} hits")
        if res.hits:
            for hit in res.hits:
                print(f"    - {hit.nom} ({hit.code})")


def demo_field_sets(client: FFBBAPIClientV2, org_id: int) -> None:
    """Show that all queries use comprehensive DEFAULT fields."""
    print()
    print("=" * 60)
    print("3. FieldSet (DEFAULT — single level)")
    print("=" * 60)

    org = client.get_organisme(org_id)
    if org:
        members_count = len(org.membres)
        engagements_count = len(org.engagements)
        has_salle = org.salle is not None
        print(
            f"  DEFAULT: members={members_count}, "
            f"engagements={engagements_count}, has_salle={has_salle}"
        )


def demo_competition_details(client: FFBBAPIClientV2, org_id: int) -> None:
    """Retrieve competition details from an organisme's engagements."""
    print()
    print("=" * 60)
    print("4. Competition Details (from organisme engagements)")
    print("=" * 60)

    organisme = client.get_organisme(org_id)
    if not organisme or not organisme.engagements:
        print("No engagements found.")
        return

    print(f"Organisme '{organisme.nom}' has {len(organisme.engagements)} engagements:")
    for eng in organisme.engagements[:5]:
        comp = eng.id_competition
        if comp:
            print(f"  - {comp.nom} (sexe={comp.sexe}, type={comp.type_competition})")

    # Try to get details for the first competition with an ID
    for eng in organisme.engagements:
        if eng.id_competition and eng.id_competition.id:
            comp_id = int(eng.id_competition.id)
            print(f"\nFetching competition details for ID {comp_id}...")
            competition = client.get_competition(comp_id)
            if competition:
                print(f"  Name: {competition.nom}")
                print(f"  Code: {competition.code}")
            break


def demo_search_other_indexes(client: FFBBAPIClientV2) -> None:
    """Search across competitions, salles, terrains, and rencontres."""
    print()
    print("=" * 60)
    print("5. Searching Other Indexes")
    print("=" * 60)

    # Competitions
    comps = client.search_competitions("Paris", limit=3)
    if comps and comps.hits:
        print(f"\nCompetitions ({comps.estimated_total_hits} total):")
        for hit in comps.hits:
            cat_code = hit.categorie.code if hit.categorie else "N/A"
            print(f"  - {hit.nom} | sexe={hit.sexe} | categorie={cat_code}")

    # Salles
    salles = client.search_salles("Paris", limit=3)
    if salles and salles.hits:
        print(f"\nSalles ({salles.estimated_total_hits} total):")
        for hit in salles.hits:
            commune_name = hit.commune.libelle if hit.commune else "N/A"
            print(f"  - {hit.libelle} | {commune_name} | type={hit.type}")

    # Terrains
    terrains = client.search_terrains("Paris", limit=3)
    if terrains and terrains.hits:
        print(f"\nTerrains ({terrains.estimated_total_hits} total):")
        for hit in terrains.hits:
            commune_name = hit.commune.libelle if hit.commune else "N/A"
            sol = hit.nature_sol.libelle if hit.nature_sol else "N/A"
            print(f"  - {hit.nom} | {commune_name} | sol={sol}")

    # Rencontres via Directus
    rencontres = client.list_rencontres(search="Paris", limit=3)
    if rencontres:
        print("\nRencontres (Directus, top 3):")
        for r in rencontres:
            print(f"  - ID={r.id}")


def demo_multi_search(client: FFBBAPIClientV2) -> None:
    """Universal multi-search across all indexes."""
    print()
    print("=" * 60)
    print("6. Universal Multi-Search")
    print("=" * 60)

    results = client.multi_search("Paris")
    if not results:
        print("No multi-search results.")
        return

    for res in results:
        hits_count = len(res.hits) if res.hits else 0
        print(f"  {res.index_uid}: {hits_count} hit(s) (query='{res.query}')")


def demo_error_handling(client: FFBBAPIClientV2) -> None:
    """Demonstrate error handling patterns."""
    print()
    print("=" * 60)
    print("7. Error Handling Patterns")
    print("=" * 60)

    # Non-existent organisme
    try:
        result = client.get_organisme(999999999)
        if result is None:
            print("  get_organisme(999999999) -> None (not found, as expected)")
    except Exception as e:
        print(f"  get_organisme(999999999) raised: {type(e).__name__}: {e}")

    # Empty search
    result = client.search_organismes("xyznonexistent123")
    if result and result.hits:
        print(f"  Unexpected: found {len(result.hits)} hits for gibberish query")
    else:
        hits_count = len(result.hits) if result and result.hits else 0
        print(
            f"  search_organismes('xyznonexistent123') -> {hits_count} hits (expected)"
        )


def main() -> None:
    client = create_client()

    org_id = demo_search_organismes(client)
    demo_multiple_search(client)

    if org_id:
        demo_field_sets(client, org_id)
        demo_competition_details(client, org_id)

    demo_search_other_indexes(client)
    demo_multi_search(client)
    demo_error_handling(client)

    print()
    print("Complete usage example done!")


if __name__ == "__main__":
    main()
