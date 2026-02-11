#!/usr/bin/env python3
"""Directus Collections - All 10 Directus collections: get, list, list_all.

Demonstrates every Directus REST API endpoint (30 methods for 10 collections).

Usage: python examples/directus_collections.py
"""

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager


def create_client() -> FFBBAPIClientV2:
    tokens = TokenManager.get_tokens()
    return FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )


def demo_rencontres(client: FFBBAPIClientV2) -> None:
    print("=" * 60)
    print("1. Rencontres (matches)")
    print("=" * 60)

    # list
    items = client.list_rencontres(limit=3, search="Paris")
    print(f"list_rencontres(search='Paris'): {len(items)} item(s)")
    for item in items:
        print(f"  - ID={item.id} | {item.nomEquipe1} vs {item.nomEquipe2}")

    # get (use ID from list)
    if items:
        detail = client.get_rencontre(int(items[0].id))
        if detail:
            print(
                f"get_rencontre({items[0].id}): {detail.nomEquipe1} vs {detail.nomEquipe2}"
            )

    # list_all
    all_items = client.list_all_rencontres(search="Paris", max_items=20)
    print(
        f"list_all_rencontres(search='Paris', max_items=20): {len(all_items)} item(s)"
    )


def demo_salles(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("2. Salles (venues)")
    print("=" * 60)

    items = client.list_salles(limit=3, search="Paris")
    print(f"list_salles(search='Paris'): {len(items)} item(s)")
    for item in items:
        print(f"  - ID={item.id} | {item.libelle}")

    if items:
        detail = client.get_salle(int(items[0].id))
        if detail:
            print(f"get_salle({items[0].id}): {detail.libelle}")

    all_items = client.list_all_salles(search="Paris", max_items=20)
    print(f"list_all_salles(max_items=20): {len(all_items)} item(s)")


def demo_terrains(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("3. Terrains (courts)")
    print("=" * 60)

    items = client.list_terrains(limit=3, search="Paris")
    print(f"list_terrains(search='Paris'): {len(items)} item(s)")
    for item in items:
        print(f"  - ID={item.id} | {item.nom}")

    if items:
        detail = client.get_terrain(int(items[0].id))
        if detail:
            print(f"get_terrain({items[0].id}): {detail.nom}")

    all_items = client.list_all_terrains(search="Paris", max_items=20)
    print(f"list_all_terrains(max_items=20): {len(all_items)} item(s)")


def demo_tournois(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("4. Tournois (tournaments)")
    print("=" * 60)

    items = client.list_tournois(limit=3)
    print(f"list_tournois(limit=3): {len(items)} item(s)")
    for item in items:
        print(f"  - ID={item.id} | {item.nom}")

    if items:
        detail = client.get_tournoi(int(items[0].id))
        if detail:
            print(f"get_tournoi({items[0].id}): {detail.nom}")

    all_items = client.list_all_tournois(max_items=20)
    print(f"list_all_tournois(max_items=20): {len(all_items)} item(s)")


def demo_engagements(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("5. Engagements (team entries)")
    print("=" * 60)

    items = client.list_engagements(limit=3, search="Paris")
    print(f"list_engagements(search='Paris'): {len(items)} item(s)")
    for item in items:
        print(f"  - ID={item.id} | {item.nom} | equipe={item.nomEquipe}")

    if items:
        detail = client.get_engagement(int(items[0].id))
        if detail:
            print(f"get_engagement({items[0].id}): {detail.nom}")

    all_items = client.list_all_engagements(search="Paris", max_items=20)
    print(f"list_all_engagements(max_items=20): {len(all_items)} item(s)")


def demo_formations(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("6. Formations (training courses)")
    print("=" * 60)

    items = client.list_formations(limit=3)
    print(f"list_formations(limit=3): {len(items)} item(s)")
    for item in items:
        print(f"  - ID={item.id} | {item.title}")

    # Note: formation_id is str, not int
    if items:
        detail = client.get_formation(items[0].id)
        if detail:
            print(f"get_formation('{items[0].id}'): {detail.title}")

    all_items = client.list_all_formations(max_items=20)
    print(f"list_all_formations(max_items=20): {len(all_items)} item(s)")


def demo_entraineurs(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("7. Entraineurs (coaches)")
    print("=" * 60)

    items = client.list_entraineurs(limit=3)
    print(f"list_entraineurs(limit=3): {len(items)} item(s)")
    for item in items:
        print(f"  - Licence={item.idLicence} | {item.nom} {item.prenom}")

    # get_entraineur requires an int ID (different from idLicence)
    # We'll skip get for entraineurs since list doesn't expose the DB int ID

    all_items = client.list_all_entraineurs(max_items=20)
    print(f"list_all_entraineurs(max_items=20): {len(all_items)} item(s)")


def demo_communes(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("8. Communes (cities) - list only, no get")
    print("=" * 60)

    items = client.list_communes(limit=3, search="Paris")
    print(f"list_communes(search='Paris'): {len(items)} item(s)")
    for item in items:
        print(
            f"  - ID={item.id} | {item.libelle} ({item.codePostal}) | dept={item.departement}"
        )

    all_items = client.list_all_communes(search="Paris", max_items=20)
    print(f"list_all_communes(max_items=20): {len(all_items)} item(s)")


def demo_officiels(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("9. Officiels (referees) - list only, no get")
    print("=" * 60)

    items = client.list_officiels(limit=3)
    print(f"list_officiels(limit=3): {len(items)} item(s)")
    for item in items:
        print(f"  - {item.nom} {item.prenom} | numero={item.numeroNational}")

    all_items = client.list_all_officiels(max_items=20)
    print(f"list_all_officiels(max_items=20): {len(all_items)} item(s)")


def demo_pratiques(client: FFBBAPIClientV2) -> None:
    print()
    print("=" * 60)
    print("10. Pratiques (activities) - list only, no get")
    print("=" * 60)

    items = client.list_pratiques(limit=3)
    print(f"list_pratiques(limit=3): {len(items)} item(s)")
    for item in items:
        print(f"  - ID={item.id} | {item.titre} | type={item.type}")

    all_items = client.list_all_pratiques(max_items=20)
    print(f"list_all_pratiques(max_items=20): {len(all_items)} item(s)")


def main() -> None:
    client = create_client()

    demo_rencontres(client)
    demo_salles(client)
    demo_terrains(client)
    demo_tournois(client)
    demo_engagements(client)
    demo_formations(client)
    demo_entraineurs(client)
    demo_communes(client)
    demo_officiels(client)
    demo_pratiques(client)

    print()
    print("All 10 Directus collections demonstrated!")


if __name__ == "__main__":
    main()
