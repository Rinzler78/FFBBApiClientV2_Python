#!/usr/bin/env python3
"""Team Ranking Analysis - Advanced team search, ranking tables, and match history.

Demonstrates: team search with filters, competition filtering by gender/category,
ranking table display, team stats, and match history analysis.

Usage: python examples/team_ranking_analysis.py
"""

from datetime import datetime

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager

_EPOCH = datetime(1970, 1, 1)


def create_client() -> FFBBAPIClientV2:
    tokens = TokenManager.get_tokens()
    return FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )


def find_team_and_poule(
    client: FFBBAPIClientV2,
) -> tuple[str, int] | None:
    """Search for a Parisian team, find a Seniors competition, return (team_name, poule_id)."""
    print("=" * 60)
    print("1. Searching for Parisian basketball clubs")
    print("=" * 60)

    result = client.search_organismes("PARIS", limit=10)
    if not result or not result.hits:
        print("No clubs found for 'PARIS'.")
        return None

    print(f"Found ~{result.estimated_total_hits} clubs. Checking engagements...")

    for hit in result.hits:
        if not hit.id:
            continue

        organisme = client.get_organisme(int(hit.id))
        if not organisme or not organisme.engagements:
            continue

        # Resolve engagement FK IDs to full objects
        eng_ids = [e for e in organisme.engagements if isinstance(e, int)]
        if not eng_ids:
            continue
        engagements = client.list_engagements_by_ids(eng_ids)

        for eng in engagements:
            if not eng.idCompetition or not eng.idPoule:
                continue

            # Resolve competition FK to get details
            comp = client.get_competition(eng.idCompetition)
            if not comp:
                continue

            # Look for a Seniors Masculins competition
            categorie_code = comp.categorie.code if comp.categorie else ""
            is_seniors = categorie_code in ("S", "SEN", "SENIOR")
            is_masc = comp.sexe == "M"

            if is_seniors and is_masc:
                poule_id = eng.idPoule
                print(f"\nFound: {organisme.nom}")
                print(f"  Competition: {comp.nom} (sexe={comp.sexe})")
                print(f"  Poule ID: {poule_id}")
                return organisme.nom or "Unknown", poule_id

    # Fallback: try any competition with a poule
    print("\nNo Seniors Masculins found, trying any competition with a poule...")
    for hit in result.hits[:5]:
        if not hit.id:
            continue
        organisme = client.get_organisme(int(hit.id))
        if not organisme or not organisme.engagements:
            continue

        eng_ids = [e for e in organisme.engagements if isinstance(e, int)]
        if not eng_ids:
            continue
        engagements = client.list_engagements_by_ids(eng_ids)

        for eng in engagements:
            if eng.idPoule and eng.idCompetition:
                comp = client.get_competition(eng.idCompetition)
                comp_name = comp.nom if comp else f"Competition #{eng.idCompetition}"
                poule_id = eng.idPoule
                print(f"\nFound: {organisme.nom}")
                print(f"  Competition: {comp_name}")
                print(f"  Poule ID: {poule_id}")
                return organisme.nom or "Unknown", poule_id

    print("No team with a poule found.")
    return None


def display_ranking_table(client: FFBBAPIClientV2, poule_id: int) -> None:
    """Display the full ranking table for a poule."""
    print()
    print("=" * 60)
    print("2. Ranking Table")
    print("=" * 60)

    poule = client.get_poule(poule_id)
    if not poule:
        print(f"Could not retrieve poule {poule_id}")
        return

    print(f"Poule: {poule.nom or poule.id}")
    print()

    if not poule.classements:
        print("No rankings available for this poule.")
        return

    # Header
    print(
        f"{'Pos':>3} | {'Team':<35} | {'Pts':>3} | {'W':>2} | {'L':>2} "
        f"| {'GP':>3} | {'PF':>5} | {'PA':>5} | {'Diff':>5} | {'Quot':>5}"
    )
    print("-" * 110)

    for r in poule.classements:
        team_name = r.id_engagement.nom if r.id_engagement else f"Team {r.id}"
        if len(team_name) > 35:
            team_name = team_name[:32] + "..."
        print(
            f"{r.position:>3} | {team_name:<35} | {r.points:>3} | {r.gagnes:>2} | "
            f"{r.perdus:>2} | {r.match_joues:>3} | {r.paniers_marques:>5} | "
            f"{r.paniers_encaisses:>5} | {r.difference:>+5} | {r.quotient:>5.2f}"
        )

    # Match history analysis
    print()
    print("=" * 60)
    print("3. Match History")
    print("=" * 60)

    # poule.rencontres is list[int] (FK IDs) — resolve via batch helper
    rencontres = client.list_rencontres_by_poule(poule_id)

    played = [r for r in rencontres if r.joue]
    upcoming = [r for r in rencontres if not r.joue]

    print(f"\nPlayed matches: {len(played)}")
    print(f"Upcoming matches: {len(upcoming)}")

    if played:
        # Sort by date (handle None dates)
        played_sorted = sorted(
            played,
            key=lambda m: m.date_rencontre or _EPOCH,
            reverse=True,
        )

        print("\nLast 10 results:")
        print(f"  {'Date':<12} | {'Home':<25} | {'Score':^9} | {'Away':<25}")
        print("  " + "-" * 80)

        for match in played_sorted[:10]:
            date_str = (
                match.date_rencontre.strftime("%Y-%m-%d")
                if match.date_rencontre
                else "N/A"
            )
            home = match.nomEquipe1[:25] if match.nomEquipe1 else "?"
            away = match.nomEquipe2[:25] if match.nomEquipe2 else "?"
            score = f"{match.resultatEquipe1}-{match.resultatEquipe2}"
            print(f"  {date_str:<12} | {home:<25} | {score:^9} | {away:<25}")

    if upcoming:
        upcoming_sorted = sorted(upcoming, key=lambda m: m.date_rencontre or _EPOCH)
        print("\nNext 5 upcoming matches:")
        for match in upcoming_sorted[:5]:
            date_str = (
                match.date_rencontre.strftime("%Y-%m-%d")
                if match.date_rencontre
                else "TBD"
            )
            print(f"  {date_str} : {match.nomEquipe1} vs {match.nomEquipe2}")

    # Team stats summary
    if poule.classements:
        print()
        print("=" * 60)
        print("4. Team Stats Summary")
        print("=" * 60)

        total_points_scored = sum(r.paniers_marques for r in poule.classements)
        total_games = sum(r.match_joues for r in poule.classements) // 2
        avg_points = total_points_scored / max(1, total_games * 2)

        best_offense = max(poule.classements, key=lambda r: r.paniers_marques)
        best_defense = min(poule.classements, key=lambda r: r.paniers_encaisses)
        best_diff = max(poule.classements, key=lambda r: r.difference)

        best_off_name = (
            best_offense.id_engagement.nom if best_offense.id_engagement else "?"
        )
        best_def_name = (
            best_defense.id_engagement.nom if best_defense.id_engagement else "?"
        )
        best_diff_name = best_diff.id_engagement.nom if best_diff.id_engagement else "?"

        print(f"  Total games played: {total_games}")
        print(f"  Average points per game: {avg_points:.1f}")
        print(f"  Best offense: {best_off_name} ({best_offense.paniers_marques} pts)")
        print(f"  Best defense: {best_def_name} ({best_defense.paniers_encaisses} pts)")
        print(f"  Best diff: {best_diff_name} ({best_diff.difference:+d})")


def main() -> None:
    client = create_client()

    result = find_team_and_poule(client)
    if not result:
        print("\nCould not find a suitable team/poule. Exiting.")
        return

    _, poule_id = result
    display_ranking_table(client, poule_id)

    print()
    print("Team ranking analysis complete!")


if __name__ == "__main__":
    main()
