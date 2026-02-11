#!/usr/bin/env python3
"""Search All Indexes - Demonstrates all 9 Meilisearch indexes + multi_search.

Covers all 18 single/multiple search methods and the universal multi_search.

Usage: python examples/search_all_indexes.py
"""

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager


def create_client() -> FFBBAPIClientV2:
    tokens = TokenManager.get_tokens()
    return FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )


def demo_organismes(client: FFBBAPIClientV2) -> None:
    print("=" * 60)
    print("1. Organismes (clubs/associations)")
    print("=" * 60)

    # Single search
    result = client.search_organismes("Paris", limit=3)
    if result and result.hits:
        print(f"search_organismes('Paris'): {result.estimated_total_hits} total")
        for hit in result.hits:
            commune = hit.commune.libelle if hit.commune else "N/A"
            print(f"  - {hit.nom} ({hit.code}) | {commune} | type={hit.type}")

    # Multiple search
    results = client.search_multiple_organismes(["Paris", "Boulogne"], limit=2)
    if results:
        print("\nsearch_multiple_organismes(['Paris', 'Boulogne']):")
        for res in results:
            hits_count = len(res.hits) if res.hits else 0
            print(f"  '{res.query}': {hits_count} hit(s)")


def demo_competitions(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("2. Competitions")
    print("=" * 60)

    result = client.search_competitions("Paris", limit=3)
    if result and result.hits:
        print(f"search_competitions('Paris'): {result.estimated_total_hits} total")
        for hit in result.hits:
            cat = hit.categorie.code if hit.categorie else "N/A"
            org = hit.organisateur.nom if hit.organisateur else "N/A"
            print(
                f"  - {hit.nom} ({hit.code}) | sexe={hit.sexe} | cat={cat} | org={org}"
            )

    results = client.search_multiple_competitions(["Paris", "Ile de France"], limit=2)
    if results:
        print("\nsearch_multiple_competitions:")
        for res in results:
            hits_count = len(res.hits) if res.hits else 0
            print(f"  '{res.query}': {hits_count} hit(s)")


def demo_rencontres(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("3. Rencontres (matches)")
    print("=" * 60)

    result = client.search_rencontres("Paris", limit=3)
    if result and result.hits:
        print(f"search_rencontres('Paris'): {result.estimated_total_hits} total")
        for hit in result.hits:
            poule = hit.id_poule.nom if hit.id_poule else "N/A"
            date_str = (
                hit.date_rencontre.strftime("%Y-%m-%d") if hit.date_rencontre else "N/A"
            )
            print(f"  - {hit.nom_equipe1} vs {hit.nom_equipe2} | {date_str} | {poule}")

    results = client.search_multiple_rencontres(["Paris"], limit=2)
    if results:
        print("\nsearch_multiple_rencontres(['Paris']):")
        for res in results:
            hits_count = len(res.hits) if res.hits else 0
            print(f"  '{res.query}': {hits_count} hit(s)")


def demo_salles(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("4. Salles (venues)")
    print("=" * 60)

    result = client.search_salles("Paris", limit=3)
    if result and result.hits:
        print(f"search_salles('Paris'): {result.estimated_total_hits} total")
        for hit in result.hits:
            commune = hit.commune.libelle if hit.commune else "N/A"
            print(f"  - {hit.libelle} | {hit.adresse} | {commune} | type={hit.type}")

    results = client.search_multiple_salles(["Paris"], limit=2)
    if results:
        print("\nsearch_multiple_salles(['Paris']):")
        for res in results:
            hits_count = len(res.hits) if res.hits else 0
            print(f"  '{res.query}': {hits_count} hit(s)")


def demo_terrains(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("5. Terrains (courts)")
    print("=" * 60)

    result = client.search_terrains("Paris", limit=3)
    if result and result.hits:
        print(f"search_terrains('Paris'): {result.estimated_total_hits} total")
        for hit in result.hits:
            commune = hit.commune.libelle if hit.commune else "N/A"
            sol = hit.nature_sol.libelle if hit.nature_sol else "N/A"
            print(f"  - {hit.nom} | {commune} | sol={sol}")

    results = client.search_multiple_terrains(["Paris"], limit=2)
    if results:
        print("\nsearch_multiple_terrains(['Paris']):")
        for res in results:
            hits_count = len(res.hits) if res.hits else 0
            print(f"  '{res.query}': {hits_count} hit(s)")


def demo_tournois(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("6. Tournois (tournaments)")
    print("=" * 60)

    result = client.search_tournois("Paris", limit=3)
    if result and result.hits:
        print(f"search_tournois('Paris'): {result.estimated_total_hits} total")
        for hit in result.hits:
            commune = hit.commune.libelle if hit.commune else "N/A"
            print(
                f"  - {hit.nom} | sexe={hit.sexe} | {hit.nom_organisateur} | {commune}"
            )

    results = client.search_multiple_tournois(["Paris"], limit=2)
    if results:
        print("\nsearch_multiple_tournois(['Paris']):")
        for res in results:
            hits_count = len(res.hits) if res.hits else 0
            print(f"  '{res.query}': {hits_count} hit(s)")


def demo_pratiques(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("7. Pratiques (activities)")
    print("=" * 60)

    result = client.search_pratiques("Paris", limit=3)
    if result and result.hits:
        print(f"search_pratiques('Paris'): {result.estimated_total_hits} total")
        for hit in result.hits:
            print(
                f"  - {hit.titre} | type={hit.type} | "
                f"{hit.nom_structure} | {hit.adresse_salle}"
            )

    results = client.search_multiple_pratiques(["Paris"], limit=2)
    if results:
        print("\nsearch_multiple_pratiques(['Paris']):")
        for res in results:
            hits_count = len(res.hits) if res.hits else 0
            print(f"  '{res.query}': {hits_count} hit(s)")


def demo_engagements(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("8. Engagements (team entries)")
    print("=" * 60)

    result = client.search_engagements("Paris", limit=3)
    if result and result.hits:
        print(f"search_engagements('Paris'): {result.estimated_total_hits} total")
        for hit in result.hits:
            print(
                f"  - {hit.nom} | equipe={hit.nom_equipe} | "
                f"club={hit.nom_club} | sexe={hit.sexe}"
            )

    results = client.search_multiple_engagements(["Paris"], limit=2)
    if results:
        print("\nsearch_multiple_engagements(['Paris']):")
        for res in results:
            hits_count = len(res.hits) if res.hits else 0
            print(f"  '{res.query}': {hits_count} hit(s)")


def demo_formations(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("9. Formations (training courses, ~90 records)")
    print("=" * 60)

    # Formations has a small dataset, search with None to get all
    result = client.search_formations(None, limit=3)
    if result and result.hits:
        print(f"search_formations(None): {result.estimated_total_hits} total")
        for hit in result.hits:
            print(
                f"  - {hit.title} | domain={hit.domain} | "
                f"theme={hit.theme} | type={hit.type} | {hit.duration_hours}h"
            )

    results = client.search_multiple_formations([None], limit=2)
    if results:
        print("\nsearch_multiple_formations([None]):")
        for res in results:
            hits_count = len(res.hits) if res.hits else 0
            print(f"  '{res.query}': {hits_count} hit(s)")


def demo_multi_search(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("10. Universal Multi-Search (all 9 indexes at once)")
    print("=" * 60)

    results = client.multi_search("Paris")
    if not results:
        print("No results.")
        return

    for res in results:
        hits_count = len(res.hits) if res.hits else 0
        total = res.estimated_total_hits or 0
        print(f"  {res.index_uid}: {hits_count} hit(s), ~{total} total")


def main() -> None:
    client = create_client()

    demo_organismes(client)
    demo_competitions(client)
    demo_rencontres(client)
    demo_salles(client)
    demo_terrains(client)
    demo_tournois(client)
    demo_pratiques(client)
    demo_engagements(client)
    demo_formations(client)
    demo_multi_search(client)

    print()
    print("All 9 Meilisearch indexes + multi_search demonstrated!")


if __name__ == "__main__":
    main()
