#!/usr/bin/env python3
"""Index Settings Discovery - Meilisearch settings introspection.

Discover filterable/sortable attributes at runtime for all 9 indexes.

Usage: python examples/index_settings_discovery.py
"""

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager


def create_client() -> FFBBAPIClientV2:
    tokens = TokenManager.get_tokens()
    return FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )


INDEX_UIDS = [
    "ffbbserver_organismes",
    "ffbbserver_rencontres",
    "ffbbserver_terrains",
    "ffbbserver_salles",
    "ffbbserver_tournois",
    "ffbbserver_competitions",
    "ffbbserver_engagements",
    "ffbbserver_formations",
    "ffbbnational_pratiques",
]


def demo_single_index_settings(client: FFBBAPIClientV2) -> None:
    """Get settings for a single index."""
    print("=" * 60)
    print("1. Single Index Settings (ffbbserver_organismes)")
    print("=" * 60)

    settings = client.get_index_settings("ffbbserver_organismes")
    if not settings:
        print("Could not retrieve settings.")
        return

    print(f"Filterable attributes ({len(settings.filterable_attributes)}):")
    for attr in sorted(settings.filterable_attributes):
        print(f"  - {attr}")

    print(f"\nSortable attributes ({len(settings.sortable_attributes)}):")
    for attr in sorted(settings.sortable_attributes):
        print(f"  - {attr}")

    print(f"\nSearchable attributes ({len(settings.searchable_attributes)}):")
    for attr in settings.searchable_attributes[:10]:
        print(f"  - {attr}")
    if len(settings.searchable_attributes) > 10:
        print(f"  ... and {len(settings.searchable_attributes) - 10} more")


def demo_all_index_settings(client: FFBBAPIClientV2) -> None:
    """Get settings for all 9 indexes."""
    print()
    print("=" * 60)
    print("2. All Index Settings Summary")
    print("=" * 60)

    all_settings = client.get_all_index_settings()
    print(
        f"\n{'Index':<35} | {'Filterable':>10} | {'Sortable':>8} | {'Searchable':>10}"
    )
    print("-" * 75)

    for uid in INDEX_UIDS:
        if uid in all_settings:
            s = all_settings[uid]
            print(
                f"{uid:<35} | {len(s.filterable_attributes):>10} | "
                f"{len(s.sortable_attributes):>8} | {len(s.searchable_attributes):>10}"
            )
        else:
            print(f"{uid:<35} | {'N/A':>10} | {'N/A':>8} | {'N/A':>10}")


def demo_filterable_sortable(client: FFBBAPIClientV2) -> None:
    """Get filterable and sortable attributes individually."""
    print()
    print("=" * 60)
    print("3. Filterable & Sortable Attributes Per Index")
    print("=" * 60)

    for uid in INDEX_UIDS:
        filterable = client.get_filterable_attributes(uid)
        sortable = client.get_sortable_attributes(uid)
        f_count = len(filterable) if filterable else 0
        s_count = len(sortable) if sortable else 0
        print(f"\n{uid}:")
        print(f"  Filterable ({f_count}): {', '.join(sorted(filterable or []))[:80]}")
        print(f"  Sortable ({s_count}): {', '.join(sorted(sortable or []))[:80]}")


def demo_practical_use_case(client: FFBBAPIClientV2) -> None:
    """Discover filterable attributes, then use them in a search."""
    print()
    print("=" * 60)
    print("4. Practical Use Case: Dynamic Filter Discovery")
    print("=" * 60)

    filterable = client.get_filterable_attributes("ffbbserver_organismes")
    if not filterable:
        print("No filterable attributes discovered.")
        return

    print(f"Discovered {len(filterable)} filterable attributes for organismes.")

    # Check if 'saison_en_cours' is filterable
    if "saison_en_cours" in filterable:
        print("'saison_en_cours' is filterable -> using it in a search:")
        result = client.search_organismes(
            "Paris",
            filter=["saison_en_cours = true"],
            limit=3,
        )
        if result and result.hits:
            print(f"  Found {result.estimated_total_hits} active clubs in Paris")
            for hit in result.hits:
                print(f"    - {hit.nom}")
    else:
        print("'saison_en_cours' is not filterable for this index.")


def main() -> None:
    client = create_client()

    demo_single_index_settings(client)
    demo_all_index_settings(client)
    demo_filterable_sortable(client)
    demo_practical_use_case(client)

    print()
    print("Index settings discovery complete!")


if __name__ == "__main__":
    main()
