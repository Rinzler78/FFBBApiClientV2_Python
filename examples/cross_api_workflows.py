#!/usr/bin/env python3
"""Cross-API Workflows - Real-world scenarios combining Meilisearch + Directus.

Four end-to-end workflows demonstrating how to combine search (Meilisearch)
with detailed data retrieval (Directus REST API).

Usage: python examples/cross_api_workflows.py
"""

import json

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager


def create_client() -> FFBBAPIClientV2:
    tokens = TokenManager.get_tokens()
    return FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )


def workflow_club_and_venue(client: FFBBAPIClientV2) -> None:
    """Workflow 1: Find a Parisian club and its venue."""
    print("=" * 60)
    print("Workflow 1: Find a Parisian club and its venue")
    print("=" * 60)

    # Step 1: Search for a club
    result = client.search_organismes("Paris", limit=5)
    if not result or not result.hits:
        print("No clubs found.")
        return

    print(f"Found ~{result.estimated_total_hits} clubs. Picking first with ID...")

    for hit in result.hits:
        if not hit.id:
            continue

        # Step 2: Get full details via Directus
        organisme = client.get_organisme(int(hit.id))
        if not organisme:
            continue

        print(f"\nClub: {organisme.nom}")
        print(f"  CodeEnum: {organisme.code}")
        print(f"  Address: {organisme.adresse}")
        if isinstance(organisme.commune, int):
            communes = client.list_communes(
                filter_criteria=json.dumps({"id": {"_eq": organisme.commune}})
            )
            if communes:
                c = communes[0]
                print(f"  City: {c.libelle} ({c.codePostal})")
        print(f"  Phone: {organisme.telephone}")
        print(f"  Email: {organisme.mail}")

        if isinstance(organisme.salle, int):
            salle = client.get_salle(organisme.salle)
            if salle:
                print("\n  Associated venue:")
                print(f"    Name: {salle.libelle}")
                print(f"    Address: {salle.adresse}")
                if isinstance(salle.commune, int):
                    salle_communes = client.list_communes(
                        filter_criteria=json.dumps({"id": {"_eq": salle.commune}})
                    )
                    if salle_communes:
                        sc = salle_communes[0]
                        print(f"    City: {sc.libelle} ({sc.codePostal})")
        else:
            print("\n  No venue associated with this club.")

        break


def workflow_salles_and_terrains(client: FFBBAPIClientV2) -> None:
    """Workflow 2: Discover venues and courts near Paris."""
    print()
    print("=" * 60)
    print("Workflow 2: Discover venues and courts near Paris")
    print("=" * 60)

    # Step 1: Search salles
    salles_result = client.search_salles("Paris", limit=5)
    if salles_result and salles_result.hits:
        print(f"\nSalles found: ~{salles_result.estimated_total_hits}")

        # Step 2: Get detailed info for top 3
        for hit in salles_result.hits[:3]:
            if not hit.id:
                continue
            salle = client.get_salle(int(hit.id))
            if salle:
                print(f"\n  Salle '{salle.libelle}':")
                print(f"    Address: {salle.adresse}")
                if isinstance(salle.commune, int):
                    salle_communes = client.list_communes(
                        filter_criteria=json.dumps({"id": {"_eq": salle.commune}})
                    )
                    if salle_communes:
                        print(f"    City: {salle_communes[0].libelle}")

    # Step 3: Search terrains
    terrains_result = client.search_terrains("Paris", limit=5)
    if terrains_result and terrains_result.hits:
        print(f"\nTerrains found: ~{terrains_result.estimated_total_hits}")

        # Get details for first terrain
        for hit in terrains_result.hits[:1]:
            if hit.id is None:
                continue
            terrain = client.get_terrain(int(hit.id))
            if terrain:
                print(f"\n  Terrain '{terrain.nom}':")
                print(f"    Dimensions: {terrain.longueur}m x {terrain.largeur}m")
                sol_data = terrain.natureSol
                if isinstance(sol_data, dict):
                    print(f"    Surface: {sol_data.get('libelle', 'N/A')}")


def workflow_matches_and_engagements(client: FFBBAPIClientV2) -> None:
    """Workflow 3: Explore matches and team engagements for Paris."""
    print()
    print("=" * 60)
    print("Workflow 3: Matches and team engagements for Paris")
    print("=" * 60)

    # Step 1: Search recent matches via Meilisearch (all seasons)
    rencontres = client.search_rencontres("Paris", limit=5)
    if rencontres and rencontres.hits:
        print(f"\nMatches found: ~{rencontres.estimated_total_hits}")

        for hit in rencontres.hits[:3]:
            date_str = (
                hit.date_rencontre.strftime("%Y-%m-%d") if hit.date_rencontre else "N/A"
            )
            print(f"  - {hit.nom_equipe1} vs {hit.nom_equipe2} ({date_str})")

    # Step 2: Get detailed match via Directus (current-season rencontre)
    # Meilisearch IDs may belong to previous seasons (→ Directus 403),
    # so we fetch a recent played match directly from Directus.
    recent = client.list_rencontres(
        limit=1,
        filter_criteria='{"joue":{"_eq":true}}',
        sort=["-date_rencontre"],
    )
    if recent:
        match_detail = client.get_rencontre(int(recent[0].id))
        if match_detail:
            print(f"\n  Match detail (ID={match_detail.id}):")
            print(f"    {match_detail.nomEquipe1} vs {match_detail.nomEquipe2}")
            print(
                f"    Score: {match_detail.resultatEquipe1}-"
                f"{match_detail.resultatEquipe2}"
            )

    # Step 3: Search engagements
    engagements = client.search_engagements("Paris", limit=5)
    if engagements and engagements.hits:
        print(f"\nEngagements found: ~{engagements.estimated_total_hits}")

        for hit in engagements.hits[:3]:
            print(f"  - {hit.nom} | club={hit.nom_club} | sexe={hit.sexe}")

        # Step 4: Get detailed engagement
        first_eng = engagements.hits[0]
        if first_eng.id:
            eng_detail = client.get_engagement(int(first_eng.id))
            if eng_detail:
                print(f"\n  Engagement detail (ID={eng_detail.id}):")
                print(f"    Name: {eng_detail.nom}")
                print(f"    Team: {eng_detail.nomEquipe}")


def workflow_tournois_formations_pratiques(client: FFBBAPIClientV2) -> None:
    """Workflow 4: Tournaments, training, activities, and auxiliary data."""
    print()
    print("=" * 60)
    print("Workflow 4: Tournaments, training, activities, and more")
    print("=" * 60)

    # Step 1: Tournaments
    tournois = client.search_tournois("Paris", limit=3)
    if tournois and tournois.hits:
        print(f"\nTournois found: ~{tournois.estimated_total_hits}")
        for hit in tournois.hits:
            print(f"  - {hit.nom} | sexe={hit.sexe} | org={hit.nom_organisateur}")

        # Get detail
        first_t = tournois.hits[0]
        if first_t.id is not None:
            detail = client.get_tournoi(int(first_t.id))
            if detail:
                print(f"  Detail: {detail.nom} | {detail.debut} - {detail.fin}")

    # Step 2: Formations (small dataset, ~90 records)
    formations = client.search_formations(None, limit=3)
    if formations and formations.hits:
        print(f"\nFormations found: ~{formations.estimated_total_hits}")
        for hit in formations.hits:
            print(f"  - {hit.title} | domain={hit.domain} | {hit.duration_hours}h")

        # Get detail (ID is str!)
        first_f = formations.hits[0]
        if first_f.id:
            detail = client.get_formation(first_f.id)
            if detail:
                print(f"  Detail: {detail.title} | mode={detail.mode}")

    # Step 3: Pratiques
    pratiques = client.search_pratiques("Paris", limit=3)
    if pratiques and pratiques.hits:
        print(f"\nPratiques found: ~{pratiques.estimated_total_hits}")
        for hit in pratiques.hits:
            print(f"  - {hit.titre} | type={hit.type}")

    # Step 4: Auxiliary Directus collections (list only)
    print("\n--- Auxiliary collections ---")

    communes = client.list_communes(search="Paris", limit=3)
    print(f"Communes (search='Paris'): {len(communes)} item(s)")
    for c in communes:
        print(f"  - {c.libelle} ({c.codePostal}) dept={c.departement}")

    entraineurs = client.list_entraineurs(limit=3)
    print(f"\nEntraineurs: {len(entraineurs)} item(s)")
    for e in entraineurs:
        print(f"  - {e.nom} {e.prenom}")

    officiels = client.list_officiels(limit=3)
    print(f"\nOfficiels: {len(officiels)} item(s)")
    for o in officiels:
        print(f"  - {o.nom} {o.prenom}")


def main() -> None:
    client = create_client()

    workflow_club_and_venue(client)
    workflow_salles_and_terrains(client)
    workflow_matches_and_engagements(client)
    workflow_tournois_formations_pratiques(client)

    print()
    print("All cross-API workflows complete!")


if __name__ == "__main__":
    main()
