"""
Team Ranking Analysis Example

This example demonstrates how to retrieve and analyze a basketball team's ranking
and performance statistics using the FFBB API Client V2.

Features demonstrated:
- Search for a team by name
- Filter competitions by criteria (gender, zone, division, category)
- Retrieve team ranking and match history
- Display detailed statistics and analysis

Usage:
    python team_ranking_analysis.py

Configuration:
    Set the following environment variables in a .env file:
    - API_FFBB_APP_BEARER_TOKEN: Your FFBB API bearer token
    - MEILISEARCH_BEARER_TOKEN: Your Meilisearch bearer token
"""

import os
from dataclasses import dataclass
from typing import Optional, Union

from dotenv import load_dotenv

from ffbb_api_client_v2 import FFBBAPIClientV2
from ffbb_api_client_v2.models.niveau_models import NiveauType
from ffbb_api_client_v2.models.organismes_models import GetOrganismeResponse
from ffbb_api_client_v2.models.poules_models import GetPouleResponse
from ffbb_api_client_v2.models.rankings_models import TeamRanking

# Example configuration - modify these values for your team
TEAM_NAME = "SENAS BASKET BALL"

# Competition filters - customize for your search criteria
RANKING_FILTERS: dict[str, Union[str, int]] = {
    "sexe": "M",  # "M" for Male, "F" for Female
    "zone": "regional",  # "departemental", "regional", "national", or "elite"
    "division": 2,  # Division number (1, 2, 3, etc.)
    "niveau_competition": "DIV",  # Competition type ("DIV", "COUPE", "PLAT", etc.)
    "categorie": "SENIOR",  # Age category ("SENIOR", "U11", "U13", "U15", etc.)
}


@dataclass
class TeamAnalysisResult:
    """Result of team analysis with ranking and match data."""

    classement: Optional[TeamRanking]
    matches: list[GetPouleResponse.RencontresitemModel]
    total_matches: int
    error_message: Optional[str] = None

    @property
    def has_error(self) -> bool:
        """Check if analysis resulted in an error."""
        return self.error_message is not None


def create_custom_filters(
    sexe: str = "M",
    zone: str = "regional",
    division: int = 2,
    niveau: str = "DIV",
    categorie: str = "SENIOR",
) -> dict[str, Union[str, int]]:
    """Create custom competition filters.

    Args:
        sexe: Competition gender ("M" for Male, "F" for Female)
        zone: Geographic zone ("departemental", "regional", "national", "elite")
        division: Division number (1, 2, 3, etc.)
        niveau: Competition type ("DIV", "COUPE", "PLAT", etc.)
        categorie: Age category ("SENIOR", "U11", "U13", "U15", etc.)

    Returns:
        Dictionary with filtering criteria
    """
    return {
        "sexe": sexe.upper(),
        "zone": zone.lower(),
        "division": division,
        "niveau_competition": niveau,
        "categorie": categorie.upper(),
    }


def filter_engagement_by_criteria(
    engagement: GetOrganismeResponse.EngagementsitemModel,
    filters: dict[str, Union[str, int]],
) -> bool:
    """Filter engagement based on competition criteria.

    Args:
        engagement: Engagement object with competition details
        filters: Dictionary with filtering criteria

    Returns:
        True if engagement matches all criteria
    """
    if not engagement.idCompetition:
        return False

    competition = engagement.idCompetition

    # Filter by gender
    if filters.get("sexe") and competition.sexe:
        if competition.sexe.upper() != filters["sexe"].upper():
            return False

    # Filter by competition type
    if filters.get("niveau_competition") and competition.typeCompetition:
        if (
            filters["niveau_competition"].lower()
            not in competition.typeCompetition.lower()
        ):
            return False

    # Filter by zone and division using Niveau class
    zone_filter = filters.get("zone")
    division_filter = filters.get("division")
    categorie_filter = filters.get("categorie")

    if zone_filter:
        niveau = competition.niveau
        if not niveau:
            return False

        # Check zone and division
        if zone_filter.lower() == "elite":
            if niveau.type != NiveauType.ELITE:
                return False
        else:
            if not niveau.matches_filter(zone_filter, division_filter):
                return False

        # Filter by category if specified
        if categorie_filter and niveau.categorie:
            cat_value = niveau.categorie.value.upper()
            if cat_value != categorie_filter.upper():
                # Allow SENIOR/SENIORS variations
                if not (
                    categorie_filter.upper() in ["SENIOR", "SENIORS"]
                    and cat_value in ["SENIOR", "SENIORS"]
                ):
                    return False

    return True


def find_organisme_by_name(client: FFBBAPIClientV2, team_name: str) -> Optional[int]:
    """Find organisme ID by searching for team name.

    Args:
        client: FFBB API client instance
        team_name: Name of the team to search for

    Returns:
        Organisme ID if found, None otherwise
    """
    print(f"🔍 Searching for organisme: {team_name}...")

    try:
        search_results = client.search_organismes(name=team_name)

        if search_results and search_results.hits:
            for hit in search_results.hits:
                # Look for exact or close match
                if (
                    team_name.upper() in hit.nom.upper()
                    or hit.nom.upper() in team_name.upper()
                ):
                    print(f"✅ Organisme found: {hit.nom} (ID: {hit.id})")
                    return int(hit.id)

            # If no exact match, return the first result
            first_hit = search_results.hits[0]
            print(
                f"⚠️ No exact match, using first result: "
                f"{first_hit.nom} (ID: {first_hit.id})"
            )
            return int(first_hit.id)

        print(f"❌ No organisme found for {team_name}")
        return None

    except Exception as e:
        print(f"❌ Error searching for organisme: {e}")
        return None


def find_team_poule_id(
    client: FFBBAPIClientV2,
    team_name: str,
    filters: Optional[dict[str, Union[str, int]]] = None,
) -> int:
    """Find the poule (pool) ID for a team using filtering criteria.

    Args:
        client: FFBB API client instance
        team_name: Name of the team to search for
        filters: Dictionary with filtering criteria

    Returns:
        Poule ID for the filtered engagement

    Raises:
        ValueError: If no matching poule is found
    """
    if filters is None:
        filters = RANKING_FILTERS

    print(f"🔍 Searching for {team_name} with filters: {filters}")

    # Step 1: Find organisme ID
    organisme_id = find_organisme_by_name(client, team_name)
    if not organisme_id:
        raise ValueError(f"Could not find organisme for {team_name}")

    # Step 2: Get organisme details with engagements
    organisme_response = client.get_organisme(organisme_id)
    print(f"✅ Organisme found: {organisme_response.nom}")

    if not organisme_response.engagements:
        raise ValueError(f"No engagements found for {team_name}")

    print(f"🔍 Found {len(organisme_response.engagements)} engagement(s)")

    # Step 3: Filter engagements based on criteria
    matching_engagements = []
    for engagement in organisme_response.engagements:
        if filter_engagement_by_criteria(engagement, filters):
            matching_engagements.append(engagement)
            if engagement.idCompetition:
                comp = engagement.idCompetition
                print("🎯 Matching engagement found:")
                print(f"   Competition: {comp.nom}")
                print(f"   Gender: {comp.sexe}")
                print(f"   Type: {comp.typeCompetition}")

    if not matching_engagements:
        print(f"❌ No matching engagement found for criteria: {filters}")
        # Show available engagements for debugging
        print("📋 Available engagements:")
        for i, engagement in enumerate(organisme_response.engagements[:5]):
            if engagement.idCompetition:
                comp = engagement.idCompetition
                niveau = comp.niveau
                niveau_info = (
                    f"{niveau.type.value} D{niveau.division} {niveau.categorie.value}"
                    if niveau
                    else "Level not detected"
                )
                print(
                    f"   {i+1}. {comp.nom} ({comp.sexe}, "
                    f"{comp.typeCompetition}) -> {niveau_info}"
                )
        raise ValueError(
            f"No matching engagement found for {team_name} with filters {filters}"
        )

    # Step 4: Get current season
    saisons = client.get_saisons()
    current_season_id = None
    if saisons:
        for saison in saisons:
            try:
                if saison.actif:
                    current_season_id = saison.id
                    break
            except AttributeError:
                continue
        if not current_season_id and saisons:
            current_season_id = saisons[0].id

    print(f"🎯 Current season: {current_season_id}")

    # Step 5: Find engagement for current season
    current_season_engagement = None
    for engagement in matching_engagements:
        if (
            engagement.idCompetition
            and engagement.idCompetition.saison
            and engagement.idCompetition.saison.id == current_season_id
        ):
            current_season_engagement = engagement
            break

    if not current_season_engagement and matching_engagements:
        current_season_engagement = matching_engagements[0]

    if current_season_engagement and current_season_engagement.idPoule:
        poule_id = int(current_season_engagement.idPoule.id)
        print(f"✅ Poule found: ID={poule_id}")
        if current_season_engagement.idCompetition:
            print(f"✅ Competition: {current_season_engagement.idCompetition.nom}")
        return poule_id
    else:
        raise ValueError(f"No poule found for {team_name} with filters {filters}")


def load_team_data(
    team_name: str, filters: Optional[dict[str, Union[str, int]]] = None
) -> GetPouleResponse:
    """Load team ranking and match data from FFBB API.

    Args:
        team_name: Name of the team to search for
        filters: Dictionary with filtering criteria

    Returns:
        GetPouleResponse with competition data

    Raises:
        ValueError: If environment variables are not set or team not found
    """
    load_dotenv()
    api_token = os.getenv("API_FFBB_APP_BEARER_TOKEN")
    meilisearch_token = os.getenv("MEILISEARCH_BEARER_TOKEN")

    if not api_token:
        raise ValueError("API_FFBB_APP_BEARER_TOKEN environment variable not set")
    if not meilisearch_token:
        raise ValueError("MEILISEARCH_BEARER_TOKEN environment variable not set")

    client = FFBBAPIClientV2.create(
        meilisearch_bearer_token=meilisearch_token,
        api_bearer_token=api_token,
        debug=False,
    )

    # Find the poule ID using the search procedure with filters
    poule_id = find_team_poule_id(client, team_name, filters)

    # Get poule data with rankings and matches
    poule_response = client.get_poule(poule_id)
    return poule_response


def display_official_ranking(poule_response: GetPouleResponse) -> None:
    """Display the official ranking table."""
    if not poule_response.classements:
        print("No ranking data available")
        return

    # Sort by position
    sorted_classements = sorted(poule_response.classements, key=lambda x: x.position)

    print(
        f"{'Pos':>3}  {'Team':<35}  {'Pts':>3}  {'W':>3}  {'L':>3}  "
        f"{'PF':>5}  {'PA':>5}  {'Diff':>5}"
    )
    print("-" * 85)

    for classement in sorted_classements:
        print(
            f"{classement.position:3}  "
            f"{classement.id_engagement.nom:<35}  "
            f"{classement.points:3}  "
            f"{classement.gagnes:3}  "
            f"{classement.perdus:3}  "
            f"{classement.paniers_marques:5}  "
            f"{classement.paniers_encaisses:5}  "
            f"{classement.difference:5}"
        )


def find_team_by_name(
    poule_response: GetPouleResponse, team_name: str
) -> Optional[TeamRanking]:
    """Find a team by name in the rankings."""
    if not poule_response.classements:
        return None

    for classement in poule_response.classements:
        if classement.id_engagement.nom == team_name:
            return classement
    return None


def get_team_matches(
    poule_response: GetPouleResponse, team_name: str
) -> list[GetPouleResponse.RencontresitemModel]:
    """Get all matches for a specific team."""
    team_matches = []
    if not poule_response.rencontres:
        return team_matches

    for rencontre in poule_response.rencontres:
        if rencontre.joue and (
            rencontre.nomEquipe1 == team_name or rencontre.nomEquipe2 == team_name
        ):
            team_matches.append(rencontre)

    # Sort by date
    return sorted(team_matches, key=lambda x: x.date_rencontre)


def analyze_team(
    poule_response: GetPouleResponse, team_name: str
) -> TeamAnalysisResult:
    """Analyze a team's performance."""
    team_classement = find_team_by_name(poule_response, team_name)
    if not team_classement:
        return TeamAnalysisResult(
            classement=None,
            matches=[],
            total_matches=0,
            error_message=f"Team {team_name} not found",
        )

    team_matches = get_team_matches(poule_response, team_name)

    return TeamAnalysisResult(
        classement=team_classement,
        matches=team_matches,
        total_matches=len(team_matches),
    )


def display_team_statistics(poule_response: GetPouleResponse, team_name: str) -> None:
    """Display detailed team statistics."""
    team_ranking = find_team_by_name(poule_response, team_name)
    if not team_ranking:
        print(f"Team {team_name} not found in ranking")
        return

    team_matches = get_team_matches(poule_response, team_name)

    print(f"\nDetailed statistics for {team_name}:")
    print(f"Ranking position: {team_ranking.position}")
    print(f"Points: {team_ranking.points}")
    print(f"Games played: {team_ranking.match_joues}")
    print(f"Wins: {team_ranking.gagnes}")
    print(f"Losses: {team_ranking.perdus}")
    print(f"Forfeits: {team_ranking.nombre_forfaits}")
    print(f"Points scored: {team_ranking.paniers_marques}")
    print(f"Points allowed: {team_ranking.paniers_encaisses}")
    print(f"Point difference: {team_ranking.difference}")
    print(f"Quotient: {team_ranking.quotient:.3f}")

    # Calculate home/away statistics
    if team_matches:
        wins_at_home = 0
        wins_away = 0
        total_scored_home = 0
        total_scored_away = 0

        for match in team_matches:
            if match.nomEquipe1 == team_name:  # Playing at home
                our_score = int(match.resultatEquipe1)
                opponent_score = int(match.resultatEquipe2)
                total_scored_home += our_score
                if our_score > opponent_score:
                    wins_at_home += 1
            else:  # Playing away
                our_score = int(match.resultatEquipe2)
                opponent_score = int(match.resultatEquipe1)
                total_scored_away += our_score
                if our_score > opponent_score:
                    wins_away += 1

        matches_home = sum(1 for m in team_matches if m.nomEquipe1 == team_name)
        matches_away = len(team_matches) - matches_home

        print("\nHome/Away breakdown:")
        if matches_home > 0:
            avg_home = total_scored_home / matches_home
            print(
                f"  Home: {wins_at_home}/{matches_home} wins, "
                f"{avg_home:.1f} pts/game"
            )
        if matches_away > 0:
            avg_away = total_scored_away / matches_away
            print(f"  Away: {wins_away}/{matches_away} wins, {avg_away:.1f} pts/game")


def display_team_matches(poule_response: GetPouleResponse, team_name: str) -> None:
    """Display all matches for a team."""
    team_matches = get_team_matches(poule_response, team_name)

    if not team_matches:
        print(f"No matches found for {team_name}")
        return

    print(f"\nMatches for {team_name}:")
    print(f"{'Date':<12} {'Team 1':<30} {'Score':<7} {'Team 2':<30}")
    print("-" * 85)

    for rencontre in team_matches:
        # Format date
        try:
            date_str = rencontre.date_rencontre.strftime("%Y-%m-%d")
        except AttributeError:
            date_str = str(rencontre.date_rencontre)

        # Format score
        score = f"{rencontre.resultatEquipe1}-{rencontre.resultatEquipe2}"

        # Highlight our team
        equipe1 = (
            f"* {rencontre.nomEquipe1} *"
            if rencontre.nomEquipe1 == team_name
            else rencontre.nomEquipe1
        )
        equipe2 = (
            f"* {rencontre.nomEquipe2} *"
            if rencontre.nomEquipe2 == team_name
            else rencontre.nomEquipe2
        )

        print(f"{date_str:<12} {equipe1:<30} {score:<7} {equipe2:<30}")


def main() -> None:
    """Main function to demonstrate team ranking analysis."""
    print("🏀 Team Ranking Analysis Example")
    print("=" * 50)
    print("🔄 Loading data from FFBB API...")
    print(f"🎯 Search parameters: {RANKING_FILTERS}")
    print(f"   - Gender: {RANKING_FILTERS['sexe']}")
    print(f"   - Zone: {RANKING_FILTERS['zone']}")
    print(f"   - Division: {RANKING_FILTERS['division']}")
    print(f"   - Type: {RANKING_FILTERS['niveau_competition']}")
    print(f"   - Category: {RANKING_FILTERS['categorie']}")

    try:
        # Load data using filtered search procedure
        poule_data = load_team_data(TEAM_NAME, RANKING_FILTERS)
        print("✅ Data loaded successfully!")

        # Display official ranking
        print("\n" + "=" * 50)
        print("OFFICIAL RANKING")
        print("=" * 50)
        display_official_ranking(poule_data)

        # Display detailed team statistics
        print("\n" + "=" * 50)
        print("DETAILED STATISTICS")
        print("=" * 50)
        display_team_statistics(poule_data, TEAM_NAME)

        # Display team matches
        print("\n" + "=" * 50)
        print("TEAM MATCHES")
        print("=" * 50)
        display_team_matches(poule_data, TEAM_NAME)

        print("\n✅ Analysis completed successfully!")

    except Exception as e:
        print(f"❌ Error loading API data: {e}")
        print("💡 Please check your environment configuration:")
        print("   - API_FFBB_APP_BEARER_TOKEN is set")
        print("   - MEILISEARCH_BEARER_TOKEN is set")
        print("   - Network connection is working")
        return


if __name__ == "__main__":
    main()
