#!/usr/bin/env python3
"""Field Sets & Filtering - FieldSet, filters, sort, and pagination tutorial.

Demonstrates: FieldSet enum, Directus filter_criteria (JSON), Meilisearch
filter/sort syntax, and manual/automatic pagination.

Usage: python examples/field_sets_and_filtering.py
"""

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager


def create_client() -> FFBBAPIClientV2:
    tokens = TokenManager.get_tokens()
    return FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )


def demo_directus_filtering(client: FFBBAPIClientV2) -> None:
    """Directus filter_criteria (JSON) and sort."""
    print()
    print("=" * 60)
    print("2. Directus Filtering (filter_criteria JSON)")
    print("=" * 60)

    # Filter rencontres where team 1 name contains "PARIS"
    filter_json = '{"nomEquipe1":{"_contains":"PARIS"}}'
    items = client.list_rencontres(
        filter_criteria=filter_json,
        sort=["-date_rencontre"],
        limit=5,
    )
    print("list_rencontres(filter_criteria='...PARIS...', sort=[\"-date_rencontre\"]):")
    print(f"  {len(items)} result(s)")
    for item in items:
        print(
            f"  - {item.nomEquipe1} vs {item.nomEquipe2} (date={item.date_rencontre})"
        )

    # Salles sorted by libelle
    print()
    salles = client.list_salles(search="Paris", sort=["libelle"], limit=5)
    print('list_salles(search="Paris", sort=["libelle"]):')
    print(f"  {len(salles)} result(s)")
    for s in salles:
        print(f"  - {s.libelle}")


def demo_meilisearch_filtering(client: FFBBAPIClientV2) -> None:
    """Meilisearch filter and sort parameters."""
    print()
    print("=" * 60)
    print("3. Meilisearch Filtering (filter list, sort)")
    print("=" * 60)

    # Organismes with saison_en_cours = true
    result = client.search_organismes(
        "Paris",
        filter=["saison_en_cours = true"],
        sort=["nom:asc"],
        limit=5,
    )
    if result and result.hits:
        print(
            'search_organismes("Paris", filter=["saison_en_cours = true"], sort=["nom:asc"]):'
        )
        print(f"  {result.estimated_total_hits} total, showing {len(result.hits)}")
        for hit in result.hits:
            print(f"  - {hit.nom} (saison_en_cours={hit.saison_en_cours})")

    # Competitions sorted by saison code descending
    print()
    comps = client.search_competitions(
        "Paris",
        sort=["saison.code:desc"],
        limit=5,
    )
    if comps and comps.hits:
        print('search_competitions("Paris", sort=["saison.code:desc"]):')
        print(f"  {comps.estimated_total_hits} total, showing {len(comps.hits)}")
        for hit in comps.hits:
            saison = hit.saison.code if hit.saison else "N/A"
            print(f"  - {hit.nom} | saison={saison}")


def demo_pagination(client: FFBBAPIClientV2) -> None:
    """Manual offset-based pagination (Directus) and auto-pagination (list_all)."""
    print()
    print("=" * 60)
    print("4. Pagination")
    print("=" * 60)

    # Manual pagination with offset
    print("Manual pagination (list_rencontres with offset):")
    for page, offset in enumerate([0, 5, 10]):
        items = client.list_rencontres(limit=5, offset=offset)
        print(f"  Page {page + 1} (offset={offset}): {len(items)} item(s)")

    # Auto-pagination with list_all
    print()
    filter_json = '{"nomEquipe1":{"_contains":"PARIS"}}'
    all_items = client.list_all_rencontres(
        filter_criteria=filter_json,
        max_items=50,
    )
    print(
        f"Auto-pagination (list_all_rencontres, max_items=50): {len(all_items)} item(s)"
    )


def main() -> None:
    client = create_client()

    demo_directus_filtering(client)
    demo_meilisearch_filtering(client)
    demo_pagination(client)

    print()
    print("Field sets and filtering tutorial complete!")


if __name__ == "__main__":
    main()
