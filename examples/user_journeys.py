#!/usr/bin/env python3
"""User Journeys - Exercises all 69 facade methods with full FK resolution.

10 journeys covering:
- J1: Club Discovery (organisme deep resolution)
- J2: Competition Hierarchy (longest chain)
- J3: Rencontre Deep-Dive (full FK resolution)
- J4: Venues & Courts (salles, terrains, communes)
- J5: Geo-Proximity (4 geo methods)
- J6: City-Based + Engagement Depth
- J7: Tournois, Formations, Pratiques
- J8: Metadata, Lives, Auxiliary + list_all demos
- J9: Batch Operations (chunked _in filters)
- J10: Multi-Search (9x search_multiple_*)

Usage: python examples/user_journeys.py
"""

from __future__ import annotations

import json
import time

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager
from ffbb_api_client_v2.exceptions import FFBBAuthError

DELAY = 0.3
methods_called: set[str] = set()


def track(name: str) -> None:
    """Track a facade method call."""
    methods_called.add(name)


def safe_print(label: str, value: object) -> None:
    """Print a label-value pair, truncating long values."""
    s = str(value)
    if len(s) > 120:
        s = s[:120] + "..."
    print(f"    {label}: {s}")


def resolve_commune(
    client: FFBBAPIClientV2, commune_id: int | None, label: str = ""
) -> None:
    """Resolve a commune FK via list_communes(filter=eq)."""
    if commune_id is None:
        return
    track("list_communes")
    communes = client.list_communes(
        filter_criteria=json.dumps({"id": {"_eq": commune_id}})
    )
    time.sleep(DELAY)
    if communes:
        c = communes[0]
        prefix = f"  {label} commune" if label else "  Commune"
        print(f"    {prefix}: {c.libelle} ({c.codePostal})")


def create_client() -> FFBBAPIClientV2:
    """Create an authenticated FFBBAPIClientV2 instance."""
    track("create")
    tokens = TokenManager.get_tokens()
    return FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )


# ---------------------------------------------------------------------------
# Journey 1 — Club Discovery
# ---------------------------------------------------------------------------
def journey_1_club_discovery(client: FFBBAPIClientV2) -> None:
    """J1: Search organisme → deep resolve all FK."""
    print("\n" + "=" * 60)
    print("Journey 1: Club Discovery (organisme deep resolution)")
    print("=" * 60)

    # search_organismes
    track("search_organismes")
    result = client.search_organismes("Paris", limit=5)
    time.sleep(DELAY)
    if not result or not result.hits:
        print("  No organismes found.")
        return

    hit = result.hits[0]
    print(f"  Hit: {hit.nom} (id={hit.id})")

    if not hit.id:
        return

    # get_organisme
    track("get_organisme")
    org = client.get_organisme(int(hit.id))
    time.sleep(DELAY)
    if not org:
        print("  Organisme not found via Directus.")
        return

    print(f"  Organisme: {org.nom} (code={org.code})")

    # .commune → list_communes
    resolve_commune(client, org.commune if isinstance(org.commune, int) else None)

    # .salle → get_salle
    if isinstance(org.salle, int) and org.salle:
        track("get_salle")
        salle = client.get_salle(org.salle)
        time.sleep(DELAY)
        if salle:
            print(f"    Salle: {salle.libelle}")
            resolve_commune(
                client,
                salle.commune if isinstance(salle.commune, int) else None,
                "salle",
            )

    # .organisme_id_pere → get_organisme (parent)
    if isinstance(org.organisme_id_pere, int) and org.organisme_id_pere:
        track("get_organisme")
        parent = client.get_organisme(org.organisme_id_pere)
        time.sleep(DELAY)
        if parent:
            print(f"    Parent: {parent.nom}")

    # .logo → get_asset_url
    if org.logo:
        track("get_asset_url")
        url = client.get_asset_url(str(org.logo))
        safe_print("Logo URL", url)

    # .engagements[:2] → list_engagements_by_ids
    eng_ids = org.engagements if isinstance(org.engagements, list) else []
    int_eng_ids = [e for e in eng_ids if isinstance(e, int)][:2]
    if int_eng_ids:
        track("list_engagements_by_ids")
        engs = client.list_engagements_by_ids(int_eng_ids)
        time.sleep(DELAY)
        for eng in engs[:1]:
            print(f"    Engagement: {eng.nom}")
            # .entraineur → get_entraineur
            if eng.entraineur:
                track("get_entraineur")
                ent = client.get_entraineur(eng.entraineur)
                time.sleep(DELAY)
                if ent:
                    print(f"    Entraineur: {ent.nom} {ent.prenom}")
                    resolve_commune(
                        client,
                        ent.commune if isinstance(ent.commune, int) else None,
                        "entraineur",
                    )

    # get_club_contacts
    track("get_club_contacts")
    contacts = client.get_club_contacts(int(hit.id))
    time.sleep(DELAY)
    if contacts:
        print(f"    Club contacts: club_contact={contacts.club_contact is not None}")
        print(f"    Members count: {len(contacts.membres) if contacts.membres else 0}")


# ---------------------------------------------------------------------------
# Journey 2 — Competition Hierarchy
# ---------------------------------------------------------------------------
def journey_2_competition_hierarchy(client: FFBBAPIClientV2) -> None:
    """J2: Search competition → phases → poule → rencontres → engagements."""
    print("\n" + "=" * 60)
    print("Journey 2: Competition Hierarchy (longest chain)")
    print("=" * 60)

    # search_competitions
    track("search_competitions")
    result = client.search_competitions("Departemental", limit=5)
    time.sleep(DELAY)
    if not result or not result.hits:
        print("  No competitions found.")
        return

    hit = result.hits[0]
    print(f"  Hit: {hit.nom} (id={hit.id})")

    if not hit.id:
        return

    # get_competition
    track("get_competition")
    comp = client.get_competition(int(hit.id))
    time.sleep(DELAY)
    if not comp:
        print("  Competition not found via Directus.")
        return

    print(f"  Competition: {comp.nom}")

    # .organisateur → get_organisme
    if isinstance(comp.organisateur, int) and comp.organisateur:
        track("get_organisme")
        org = client.get_organisme(comp.organisateur)
        time.sleep(DELAY)
        if org:
            print(f"    Organisateur: {org.nom}")

    # .logo → get_asset_url
    if comp.logo:
        track("get_asset_url")
        url = client.get_asset_url(str(comp.logo))
        safe_print("Logo URL", url)

    # .phases[0].poules[0].id → get_poule
    poule_id = None
    if comp.phases:
        for phase in comp.phases:
            if phase.poules:
                first_poule = phase.poules[0]
                try:
                    poule_id = int(first_poule.id) if first_poule.id else None
                except (ValueError, TypeError):
                    poule_id = None
                if poule_id:
                    break

    if poule_id:
        track("get_poule")
        poule = client.get_poule(poule_id)
        time.sleep(DELAY)
        if poule:
            print(f"    Poule: {poule.nom} (id={poule.id})")

            # list_rencontres_by_poule
            track("list_rencontres_by_poule")
            rencontres = client.list_rencontres_by_poule(poule_id)
            time.sleep(DELAY)
            if rencontres:
                r = rencontres[0]
                print(f"    First rencontre: {r.nomEquipe1} vs {r.nomEquipe2}")

                # .salle → get_salle
                if isinstance(r.salle, int) and r.salle:
                    track("get_salle")
                    salle = client.get_salle(r.salle)
                    time.sleep(DELAY)
                    if salle:
                        print(f"    Salle rencontre: {salle.libelle}")

                # get_rencontre (full detail)
                if r.id:
                    track("get_rencontre")
                    detail = client.get_rencontre(int(r.id))
                    time.sleep(DELAY)
                    if detail:
                        safe_print("Rencontre detail id", detail.id)

            # list_engagements_by_poule
            track("list_engagements_by_poule")
            engs = client.list_engagements_by_poule(poule_id)
            time.sleep(DELAY)
            if engs:
                eng = engs[0]
                print(f"    First engagement: {eng.nom}")

                # get_engagement_contacts
                if eng.id:
                    track("get_engagement_contacts")
                    contacts = client.get_engagement_contacts(int(eng.id))
                    time.sleep(DELAY)
                    if contacts:
                        print(
                            f"    Engagement contacts: entraineur="
                            f"{contacts.entraineur is not None}"
                        )

    # get_saisons
    track("get_saisons")
    saisons = client.get_saisons()
    time.sleep(DELAY)
    if saisons:
        print(f"    Active saisons: {len(saisons)}")


# ---------------------------------------------------------------------------
# Journey 3 — Rencontre Deep-Dive
# ---------------------------------------------------------------------------
def journey_3_rencontre_deep_dive(client: FFBBAPIClientV2) -> None:
    """J3: Search rencontre → resolve all FK."""
    print("\n" + "=" * 60)
    print("Journey 3: Rencontre Deep-Dive (full FK resolution)")
    print("=" * 60)

    # search_engagements (to get an initial engagement ID)
    track("search_engagements")
    eng_search = client.search_engagements("Paris", limit=1)
    time.sleep(DELAY)
    if eng_search and eng_search.hits:
        print(f"  Engagement search: {eng_search.hits[0].nom}")

    # search_rencontres (Meilisearch — all seasons, for demo)
    track("search_rencontres")
    result = client.search_rencontres("Paris", limit=5)
    time.sleep(DELAY)
    if result and result.hits:
        hit = result.hits[0]
        print(f"  Search hit: {hit.nom_equipe1} vs {hit.nom_equipe2} (id={hit.id})")

    # get_rencontre — use Directus list to get a valid current-season ID
    # (Meilisearch IDs may belong to previous seasons → Directus 403)
    track("list_rencontres")
    recent = client.list_rencontres(
        limit=1,
        filter_criteria='{"joue":{"_eq":true}}',
        sort=["-date_rencontre"],
    )
    time.sleep(DELAY)
    if not recent:
        print("  No current-season rencontres found via Directus.")
        return

    track("get_rencontre")
    r = client.get_rencontre(int(recent[0].id))
    time.sleep(DELAY)
    if not r:
        print("  Rencontre not found via Directus.")
        return

    print(f"  Rencontre: {r.nomEquipe1} vs {r.nomEquipe2}")

    # .salle → get_salle
    if isinstance(r.salle, int) and r.salle:
        track("get_salle")
        salle = client.get_salle(r.salle)
        time.sleep(DELAY)
        if salle:
            print(f"    Salle: {salle.libelle}")

    # .idEngagementEquipe1 → get_engagement
    if r.idEngagementEquipe1:
        track("get_engagement")
        eng = client.get_engagement(r.idEngagementEquipe1)
        time.sleep(DELAY)
        if eng:
            print(f"    Engagement Eq1: {eng.nom}")
            # .entraineur → get_entraineur
            if eng.entraineur:
                track("get_entraineur")
                ent = client.get_entraineur(eng.entraineur)
                time.sleep(DELAY)
                if ent:
                    print(f"    Entraineur Eq1: {ent.nom} {ent.prenom}")
            # .idOrganisme → get_organisme
            if eng.idOrganisme:
                track("get_organisme")
                org = client.get_organisme(eng.idOrganisme)
                time.sleep(DELAY)
                if org:
                    print(f"    Organisme Eq1: {org.nom}")

    # .idOrganismeEquipe1 → get_organisme
    if r.idOrganismeEquipe1:
        track("get_organisme")
        org1 = client.get_organisme(r.idOrganismeEquipe1)
        time.sleep(DELAY)
        if org1:
            print(f"    idOrganismeEquipe1: {org1.nom}")

    # .idOrganismeEquipe2 → get_organisme
    if r.idOrganismeEquipe2:
        track("get_organisme")
        org2 = client.get_organisme(r.idOrganismeEquipe2)
        time.sleep(DELAY)
        if org2:
            print(f"    idOrganismeEquipe2: {org2.nom}")

    # .competitionId → get_competition
    if r.competitionId:
        track("get_competition")
        comp = client.get_competition(r.competitionId)
        time.sleep(DELAY)
        if comp:
            print(f"    Competition: {comp.nom}")


# ---------------------------------------------------------------------------
# Journey 4 — Venues & Courts
# ---------------------------------------------------------------------------
def journey_4_venues_courts(client: FFBBAPIClientV2) -> None:
    """J4: search_salles, get_salle, search_terrains, get_terrain, list_communes."""
    print("\n" + "=" * 60)
    print("Journey 4: Venues & Courts (salles, terrains, communes)")
    print("=" * 60)

    # search_salles
    track("search_salles")
    salles_result = client.search_salles("Paris", limit=3)
    time.sleep(DELAY)
    if salles_result and salles_result.hits:
        hit = salles_result.hits[0]
        print(f"  Salle hit: {hit.libelle} (id={hit.id})")
        if hit.id is not None:
            track("get_salle")
            salle = client.get_salle(int(hit.id))
            time.sleep(DELAY)
            if salle:
                print(f"    Salle detail: {salle.libelle}")
                resolve_commune(
                    client,
                    salle.commune if isinstance(salle.commune, int) else None,
                )

    # search_terrains
    track("search_terrains")
    terrains_result = client.search_terrains("Paris", limit=3)
    time.sleep(DELAY)
    if terrains_result and terrains_result.hits:
        hit = terrains_result.hits[0]
        print(f"  Terrain hit: {hit.nom} (id={hit.id})")
        if hit.id is not None:
            track("get_terrain")
            terrain = client.get_terrain(int(hit.id))
            time.sleep(DELAY)
            if terrain:
                print(f"    Terrain detail: {terrain.nom}")
                resolve_commune(
                    client,
                    terrain.commune if isinstance(terrain.commune, int) else None,
                )


# ---------------------------------------------------------------------------
# Journey 5 — Geo-Proximity
# ---------------------------------------------------------------------------
def journey_5_geo_proximity(client: FFBBAPIClientV2) -> None:
    """J5: 4 geo-search methods (Paris center coordinates)."""
    print("\n" + "=" * 60)
    print("Journey 5: Geo-Proximity (4 geo methods)")
    print("=" * 60)

    lat, lng = 48.856, 2.352  # Paris center

    # search_organismes_by_geo
    track("search_organismes_by_geo")
    result = client.search_organismes_by_geo(lat, lng, radius_km=10, limit=3)
    time.sleep(DELAY)
    if result and result.hits:
        print(f"  Organismes near Paris: {len(result.hits)} hits")
        for h in result.hits[:2]:
            print(f"    - {h.nom}")

    # search_salles_by_geo
    track("search_salles_by_geo")
    result2 = client.search_salles_by_geo(lat, lng, radius_km=10, limit=3)
    time.sleep(DELAY)
    if result2 and result2.hits:
        print(f"  Salles near Paris: {len(result2.hits)} hits")

    # search_engagements_by_geo
    track("search_engagements_by_geo")
    result3 = client.search_engagements_by_geo(lat, lng, radius_km=10, limit=3)
    time.sleep(DELAY)
    if result3 and result3.hits:
        print(f"  Engagements near Paris: {len(result3.hits)} hits")

    # search_engagements_filtered
    track("search_engagements_filtered")
    result4 = client.search_engagements_filtered(
        lat, lng, radius_km=10, sexes=["Masculin"], niveau_codes=["SEN"], limit=5
    )
    time.sleep(DELAY)
    if result4 and result4.hits:
        print(f"  Engagements filtered (M/SEN): {len(result4.hits)} hits")
    else:
        print("  Engagements filtered (M/SEN): no results")


# ---------------------------------------------------------------------------
# Journey 6 — City-Based + Engagement Depth
# ---------------------------------------------------------------------------
def journey_6_city_engagement_depth(client: FFBBAPIClientV2) -> None:
    """J6: search_organismes_by_city → organisme → engagement → poule → competition."""
    print("\n" + "=" * 60)
    print("Journey 6: City-Based + Engagement Depth")
    print("=" * 60)

    # search_organismes_by_city
    track("search_organismes_by_city")
    result = client.search_organismes_by_city("Lyon", limit=5)
    time.sleep(DELAY)
    if not result or not result.hits:
        print("  No organismes found in Lyon.")
        return

    hit = result.hits[0]
    print(f"  Organisme in Lyon: {hit.nom} (id={hit.id})")

    if not hit.id:
        return

    # get_organisme
    track("get_organisme")
    org = client.get_organisme(int(hit.id))
    time.sleep(DELAY)
    if not org:
        return

    # .engagements[:1] → get_engagement
    eng_ids = org.engagements if isinstance(org.engagements, list) else []
    int_eng_ids = [e for e in eng_ids if isinstance(e, int)][:1]
    if int_eng_ids:
        track("get_engagement")
        eng = client.get_engagement(int_eng_ids[0])
        time.sleep(DELAY)
        if eng:
            print(f"    Engagement: {eng.nom}")

            # .idPoule → get_poule
            if eng.idPoule:
                track("get_poule")
                poule = client.get_poule(eng.idPoule)
                time.sleep(DELAY)
                if poule:
                    print(f"    Poule: {poule.nom}")

            # .idCompetition → get_competition
            if eng.idCompetition:
                track("get_competition")
                comp = client.get_competition(eng.idCompetition)
                time.sleep(DELAY)
                if comp:
                    print(f"    Competition: {comp.nom}")

            # .logo → get_asset_url
            if eng.logo:
                track("get_asset_url")
                url = client.get_asset_url(str(eng.logo))
                safe_print("Logo URL", url)


# ---------------------------------------------------------------------------
# Journey 7 — Tournois, Formations, Pratiques
# ---------------------------------------------------------------------------
def journey_7_tournois_formations_pratiques(client: FFBBAPIClientV2) -> None:
    """J7: search + get for tournois, formations, pratiques."""
    print("\n" + "=" * 60)
    print("Journey 7: Tournois, Formations, Pratiques")
    print("=" * 60)

    # search_tournois → get_tournoi
    track("search_tournois")
    tournois = client.search_tournois("Paris", limit=3)
    time.sleep(DELAY)
    if tournois and tournois.hits:
        hit = tournois.hits[0]
        print(f"  Tournoi hit: {hit.nom} (id={hit.id})")
        if hit.id is not None:
            track("get_tournoi")
            detail = client.get_tournoi(int(hit.id))
            time.sleep(DELAY)
            if detail:
                print(f"    Tournoi detail: {detail.nom}")
                resolve_commune(
                    client,
                    detail.commune if isinstance(detail.commune, int) else None,
                )

    # search_formations → get_formation
    track("search_formations")
    formations = client.search_formations(None, limit=3)
    time.sleep(DELAY)
    if formations and formations.hits:
        hit = formations.hits[0]
        print(f"  Formation hit: {hit.title} (id={hit.id})")
        if hit.id:
            track("get_formation")
            detail = client.get_formation(hit.id)
            time.sleep(DELAY)
            if detail:
                print(f"    Formation detail: {detail.title}")
                # .image → get_asset_url
                if detail.image:
                    track("get_asset_url")
                    url = client.get_asset_url(str(detail.image))
                    safe_print("Image URL", url)

    # search_pratiques + list_pratiques
    track("search_pratiques")
    pratiques = client.search_pratiques("Paris", limit=3)
    time.sleep(DELAY)
    if pratiques and pratiques.hits:
        print(f"  Pratiques: {len(pratiques.hits)} hits")

    track("list_pratiques")
    prat_list = client.list_pratiques(search="Paris", limit=3)
    time.sleep(DELAY)
    print(f"  list_pratiques: {len(prat_list)} items")


# ---------------------------------------------------------------------------
# Journey 8 — Metadata, Lives, Auxiliary + list_all
# ---------------------------------------------------------------------------
def journey_8_metadata_auxiliary(client: FFBBAPIClientV2) -> None:
    """J8: get_lives, get_saisons, multi_search, list_*, list_all_*, settings."""
    print("\n" + "=" * 60)
    print("Journey 8: Metadata, Lives, Auxiliary + list_all demos")
    print("=" * 60)

    # get_lives
    track("get_lives")
    lives = client.get_lives()
    time.sleep(DELAY)
    if lives:
        print(f"  Lives: {len(lives)} match(es) en cours")
        first = lives[0]
        # NOTE: Live.match_id is the live-scores API identifier, NOT the
        # Directus rencontre item ID (which looks like 200000012286822).
        # Passing match_id directly to get_rencontre() would return a 403.
        # To fetch a live rencontre via Directus, use list_rencontres() and
        # match on team names or use the `external_id` field of the Live object.
        print(
            f"    Live match: {first.team_name_home} vs {first.team_name_out}"
            f" (status={first.match_status})"
        )
    else:
        print("  Lives: aucun match en cours")

    # get_saisons
    track("get_saisons")
    saisons = client.get_saisons()
    time.sleep(DELAY)
    print(f"  Saisons: {len(saisons) if saisons else 0} active")

    # multi_search
    track("multi_search")
    multi = client.multi_search("basketball")
    time.sleep(DELAY)
    if multi:
        print(f"  Multi-search: {len(multi)} result sets")

    # list_entraineurs
    track("list_entraineurs")
    ents = client.list_entraineurs(limit=3)
    time.sleep(DELAY)
    print(f"  list_entraineurs: {len(ents)} items")

    # list_officiels
    track("list_officiels")
    offs = client.list_officiels(limit=3)
    time.sleep(DELAY)
    print(f"  list_officiels: {len(offs)} items")

    # list_communes
    track("list_communes")
    comms = client.list_communes(search="Paris", limit=3)
    time.sleep(DELAY)
    print(f"  list_communes: {len(comms)} items")

    # Index settings — require admin Meilisearch key; skip gracefully otherwise
    track("get_all_index_settings")
    try:
        all_settings = client.get_all_index_settings()
        print(f"  get_all_index_settings: {len(all_settings)} indexes")
    except FFBBAuthError:
        print("  get_all_index_settings: [SKIP] admin key required")
    time.sleep(DELAY)

    track("get_index_settings")
    try:
        settings = client.get_index_settings("ffbbserver_organismes")
        print(f"  get_index_settings: {'ok' if settings else 'none'}")
    except FFBBAuthError:
        print("  get_index_settings: [SKIP] admin key required")
    time.sleep(DELAY)

    track("get_filterable_attributes")
    try:
        fa = client.get_filterable_attributes("ffbbserver_organismes")
        print(f"  get_filterable_attributes: {len(fa) if fa else 0} attrs")
    except FFBBAuthError:
        print("  get_filterable_attributes: [SKIP] admin key required")
    time.sleep(DELAY)

    track("get_sortable_attributes")
    try:
        sa = client.get_sortable_attributes("ffbbserver_organismes")
        print(f"  get_sortable_attributes: {len(sa) if sa else 0} attrs")
    except FFBBAuthError:
        print("  get_sortable_attributes: [SKIP] admin key required")
    time.sleep(DELAY)

    # list_all_* demos (max_items=5 to avoid overload)
    print("\n  --- list_all_* demos (max_items=5) ---")

    for name, method in [
        ("list_all_communes", client.list_all_communes),
        ("list_all_salles", client.list_all_salles),
        ("list_all_terrains", client.list_all_terrains),
        ("list_all_rencontres", client.list_all_rencontres),
        ("list_all_tournois", client.list_all_tournois),
        ("list_all_engagements", client.list_all_engagements),
        ("list_all_formations", client.list_all_formations),
        ("list_all_entraineurs", client.list_all_entraineurs),
        ("list_all_officiels", client.list_all_officiels),
        ("list_all_pratiques", client.list_all_pratiques),
    ]:
        track(name)
        items = method(max_items=5)
        time.sleep(DELAY)
        print(f"  {name}: {len(items)} items")


# ---------------------------------------------------------------------------
# Journey 9 — Batch Operations
# ---------------------------------------------------------------------------
def journey_9_batch_operations(client: FFBBAPIClientV2) -> None:
    """J9: Batch helpers + list methods with filters."""
    print("\n" + "=" * 60)
    print("Journey 9: Batch Operations (chunked _in filters)")
    print("=" * 60)

    # Get an organisme to harvest engagement IDs.
    # ID 1 often does not exist or is access-restricted; resolve a real ID
    # from a Meilisearch hit instead.
    track("get_organisme")
    _org_result = client.search_organismes("Paris", limit=1)
    _org_id = (
        int(_org_result.hits[0].id)
        if (_org_result and _org_result.hits and _org_result.hits[0].id)
        else None
    )
    org = client.get_organisme(_org_id) if _org_id else None
    time.sleep(DELAY)

    # list_engagements_by_ids (from organisme.engagements)
    if org:
        eng_ids = org.engagements if isinstance(org.engagements, list) else []
        int_eng_ids = [e for e in eng_ids if isinstance(e, int)][:10]
        if int_eng_ids:
            track("list_engagements_by_ids")
            engs = client.list_engagements_by_ids(int_eng_ids)
            time.sleep(DELAY)
            print(f"  list_engagements_by_ids: {len(engs)} items")

            # Harvest entraineur IDs
            ent_ids = [
                e.entraineur
                for e in engs
                if e.entraineur and isinstance(e.entraineur, int)
            ]
            if ent_ids:
                track("list_entraineurs_by_ids")
                ents = client.list_entraineurs_by_ids(ent_ids)
                time.sleep(DELAY)
                print(f"  list_entraineurs_by_ids: {len(ents)} items")

    # Get a competition to harvest poule IDs
    track("search_competitions")
    comp_result = client.search_competitions("Departemental", limit=1)
    time.sleep(DELAY)
    if comp_result and comp_result.hits and comp_result.hits[0].id:
        track("get_competition")
        comp = client.get_competition(int(comp_result.hits[0].id))
        time.sleep(DELAY)
        if comp and comp.phases:
            poule_ids: list[int] = []
            for phase in comp.phases:
                if phase.poules:
                    for p in phase.poules:
                        try:
                            pid = int(p.id) if p.id else None
                        except (ValueError, TypeError):
                            pid = None
                        if pid:
                            poule_ids.append(pid)
            if poule_ids:
                # list_engagements_by_poules
                track("list_engagements_by_poules")
                engs = client.list_engagements_by_poules(poule_ids[:5])
                time.sleep(DELAY)
                print(f"  list_engagements_by_poules: {len(engs)} items")

                # list_rencontres_by_poules
                track("list_rencontres_by_poules")
                rens = client.list_rencontres_by_poules(poule_ids[:5])
                time.sleep(DELAY)
                print(f"  list_rencontres_by_poules: {len(rens)} items")

    # Simple list with filters
    print("\n  --- list methods with filters ---")

    track("list_rencontres")
    r = client.list_rencontres(limit=5, filter_criteria='{"joue":{"_eq":true}}')
    time.sleep(DELAY)
    print(f"  list_rencontres (joue=true): {len(r)} items")

    track("list_engagements")
    e = client.list_engagements(limit=5)
    time.sleep(DELAY)
    print(f"  list_engagements: {len(e)} items")

    track("list_salles")
    s = client.list_salles(limit=5)
    time.sleep(DELAY)
    print(f"  list_salles: {len(s)} items")

    track("list_terrains")
    t = client.list_terrains(limit=5)
    time.sleep(DELAY)
    print(f"  list_terrains: {len(t)} items")

    track("list_tournois")
    to = client.list_tournois(limit=5)
    time.sleep(DELAY)
    print(f"  list_tournois: {len(to)} items")

    track("list_formations")
    f = client.list_formations(limit=5)
    time.sleep(DELAY)
    print(f"  list_formations: {len(f)} items")


# ---------------------------------------------------------------------------
# Journey 10 — Multi-Search (9x search_multiple_*)
# ---------------------------------------------------------------------------
def journey_10_multi_search(client: FFBBAPIClientV2) -> None:
    """J10: 9 search_multiple_* methods."""
    print("\n" + "=" * 60)
    print("Journey 10: Multi-Search (9x search_multiple_*)")
    print("=" * 60)

    for name, method, queries in [
        (
            "search_multiple_organismes",
            client.search_multiple_organismes,
            ["Paris", "Lyon", "Marseille"],
        ),
        (
            "search_multiple_competitions",
            client.search_multiple_competitions,
            ["Senior", "U18"],
        ),
        (
            "search_multiple_engagements",
            client.search_multiple_engagements,
            ["basket"],
        ),
        (
            "search_multiple_rencontres",
            client.search_multiple_rencontres,
            ["Paris"],
        ),
        (
            "search_multiple_salles",
            client.search_multiple_salles,
            ["Gymnase"],
        ),
        (
            "search_multiple_terrains",
            client.search_multiple_terrains,
            ["Paris"],
        ),
        (
            "search_multiple_tournois",
            client.search_multiple_tournois,
            ["3x3"],
        ),
        (
            "search_multiple_pratiques",
            client.search_multiple_pratiques,
            ["basket"],
        ),
        (
            "search_multiple_formations",
            client.search_multiple_formations,
            [None],
        ),
    ]:
        track(name)
        results = method(queries)  # type: ignore[arg-type]
        time.sleep(DELAY)
        count = len(results) if results else 0
        total_hits = sum(r.estimated_total_hits or 0 for r in results) if results else 0
        print(f"  {name}: {count} result set(s), ~{total_hits} total hits")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
EXPECTED_METHODS = {
    "create",
    "get_asset_url",
    "get_competition",
    "get_lives",
    "get_organisme",
    "get_poule",
    "get_saisons",
    "get_rencontre",
    "get_salle",
    "get_terrain",
    "get_tournoi",
    "get_engagement",
    "get_formation",
    "get_entraineur",
    "list_rencontres",
    "list_salles",
    "list_terrains",
    "list_tournois",
    "list_engagements",
    "list_formations",
    "list_entraineurs",
    "list_communes",
    "list_officiels",
    "list_pratiques",
    "list_all_communes",
    "list_all_salles",
    "list_all_terrains",
    "list_all_rencontres",
    "list_all_tournois",
    "list_all_engagements",
    "list_all_formations",
    "list_all_entraineurs",
    "list_all_officiels",
    "list_all_pratiques",
    "multi_search",
    "search_competitions",
    "search_multiple_competitions",
    "search_organismes",
    "search_multiple_organismes",
    "search_pratiques",
    "search_multiple_pratiques",
    "search_rencontres",
    "search_multiple_rencontres",
    "search_salles",
    "search_multiple_salles",
    "search_terrains",
    "search_multiple_terrains",
    "search_engagements",
    "search_multiple_engagements",
    "search_formations",
    "search_multiple_formations",
    "search_tournois",
    "search_multiple_tournois",
    "get_index_settings",
    "get_all_index_settings",
    "get_filterable_attributes",
    "get_sortable_attributes",
    "search_organismes_by_geo",
    "search_organismes_by_city",
    "search_salles_by_geo",
    "search_engagements_by_geo",
    "search_engagements_filtered",
    "get_engagement_contacts",
    "get_club_contacts",
    "list_engagements_by_ids",
    "list_engagements_by_poule",
    "list_engagements_by_poules",
    "list_rencontres_by_poule",
    "list_rencontres_by_poules",
    "list_entraineurs_by_ids",
}


def print_summary() -> None:
    """Print summary of methods covered."""
    print("\n" + "=" * 60)
    print("SUMMARY: Method Coverage")
    print("=" * 60)

    covered = methods_called & EXPECTED_METHODS
    missing = EXPECTED_METHODS - methods_called
    extra = methods_called - EXPECTED_METHODS

    print(f"\n  Expected: {len(EXPECTED_METHODS)} methods")
    print(f"  Covered:  {len(covered)}/{len(EXPECTED_METHODS)}")

    if missing:
        print(f"\n  MISSING ({len(missing)}):")
        for m in sorted(missing):
            print(f"    - {m}")

    if extra:
        print(f"\n  Extra (not in expected set): {sorted(extra)}")

    if not missing:
        print("\n  ALL 69 METHODS COVERED!")


def main() -> None:
    """Run all 10 user journeys."""
    print("FFBB API Client v2 — User Journeys")
    print("Exercising all 69 facade methods with full FK resolution.\n")

    client = create_client()

    journey_1_club_discovery(client)
    journey_2_competition_hierarchy(client)
    journey_3_rencontre_deep_dive(client)
    journey_4_venues_courts(client)
    journey_5_geo_proximity(client)
    journey_6_city_engagement_depth(client)
    journey_7_tournois_formations_pratiques(client)
    journey_8_metadata_auxiliary(client)
    journey_9_batch_operations(client)
    journey_10_multi_search(client)

    print_summary()


if __name__ == "__main__":
    main()
