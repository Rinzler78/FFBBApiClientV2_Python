import json
from datetime import date, datetime

# Constante pour le nom de l'équipe
TEAM_NAME = "SENAS BASKET BALL"


def calculate_points(wins: int, losses: int, forfeits: int = 0) -> int:
    """Calculate points based on wins and losses.
    - 2 points for a win (including forfeit wins)
    - 1 point for a loss (excluding forfeit losses)
    - 0 points for a forfeit against
    - 2 points for a forfeit in favor

    Args:
        wins: Number of wins (including forfeit wins)
        losses: Number of losses (including forfeit losses)
        forfeits: Number of forfeits against

    Returns:
        Total points
    """
    # Les matchs avec forfait ne doivent pas être comptés comme des défaites normales
    # On retire d'abord les forfaits du total des défaites
    normal_losses = losses - forfeits

    # Calcul des points :
    # - 2 points par victoire (incluant les victoires par forfait)
    # - 1 point par défaite normale (excluant les défaites par forfait)
    # - 0 point par forfait contre
    # - 1 point supplémentaire par forfait contre (compensation)
    points = wins * 2 + normal_losses + forfeits

    return points


def get_official_ranking(data: dict) -> list[dict]:
    """Extract the official ranking from the data."""
    official_ranking = []
    for team in data["data"]["classements"]:
        official_ranking.append(
            {
                "id": team["idEngagement"]["id"],
                "team": team["idEngagement"]["nom"],
                "position": int(team["position"]),
                "points": int(team["points"]),
                "matches": int(team["matchJoues"]),
                "wins": int(team["gagnes"]),
                "losses": int(team["perdus"]),
                "forfeits": int(team["nombreForfaits"]),
                "points_scored": int(team["paniersMarques"]),
                "points_conceded": int(team["paniersEncaisses"]),
                "point_average": int(team["difference"]),
                "quotient": float(team["quotient"]),
            }
        )
    return sorted(official_ranking, key=lambda x: x["position"])


def get_teams(matches: list[dict]) -> dict[str, dict[str, str]]:
    """Extract unique team IDs and names from matches."""
    teams = {}
    for match in matches:
        teams[match["idEngagementEquipe1"]["id"]] = {
            "id": match["idEngagementEquipe1"]["id"],
            "name": match["idEngagementEquipe1"]["nom"],
        }
        teams[match["idEngagementEquipe2"]["id"]] = {
            "id": match["idEngagementEquipe2"]["id"],
            "name": match["idEngagementEquipe2"]["nom"],
        }
    return teams


def find_team_position(ranking: list[dict], team_id: str) -> int:
    """Find team position in the ranking."""
    try:
        return next(i + 1 for i, team in enumerate(ranking) if team_id == team["id"])
    except StopIteration:
        return 0


def get_head_to_head_stats(data: dict, team_id: str, other_teams: list[str]) -> dict:
    """Calculate head-to-head statistics between teams with same points.
    Args:
        data: Full competition data
        team_id: ID of the team to analyze
        other_teams: List of team IDs with same points
    Returns:
        Dict with head-to-head statistics
    """
    points_scored = 0
    points_conceded = 0
    wins = 0
    matches = []

    for match in data["data"]["rencontres"]:
        if not match["joue"]:
            continue

        team1_id = match["idEngagementEquipe1"]["id"]
        team2_id = match["idEngagementEquipe2"]["id"]
        score1 = int(match["resultatEquipe1"])
        score2 = int(match["resultatEquipe2"])

        # Only consider matches between teams with same points
        if team1_id == team_id and team2_id in other_teams:
            matches.append(match)
            points_scored += score1
            points_conceded += score2
            if score1 > score2:
                wins += 1
        elif team2_id == team_id and team1_id in other_teams:
            matches.append(match)
            points_scored += score2
            points_conceded += score1
            if score2 > score1:
                wins += 1

    return {
        "wins": wins,
        "point_diff": points_scored - points_conceded,
        "points_scored": points_scored,
        "matches": matches,
    }


def sort_ranking(ranking: list[dict], data: dict) -> list[dict]:
    """Sort ranking according to official FFBB rules:
    1. Points
    2. Head-to-head record between tied teams
    3. Head-to-head point differential between tied teams
    4. Overall point differential
    5. Total points scored
    6. Random draw (not implemented)
    """
    # First, group teams by points
    points_groups = {}
    for team in ranking:
        points = team["points"]
        if points not in points_groups:
            points_groups[points] = []
        points_groups[points].append(team)

    # Sort each group by head-to-head criteria
    sorted_ranking = []
    for points in sorted(points_groups.keys(), reverse=True):
        group = points_groups[points]
        if len(group) > 1:
            # Get head-to-head stats for teams in this group
            team_ids = [team["id"] for team in group]
            for team in group:
                h2h_stats = get_head_to_head_stats(data, team["id"], team_ids)
                team["h2h_wins"] = h2h_stats["wins"]
                team["h2h_point_diff"] = h2h_stats["point_diff"]
                team["h2h_points_scored"] = h2h_stats["points_scored"]

            # Sort by multiple criteria according to FFBB rules
            group.sort(
                key=lambda x: (
                    -x["h2h_wins"],  # 2a. Head-to-head wins
                    -x["h2h_point_diff"],  # 2b. Head-to-head point differential
                    -x["point_average"],  # 2c. Overall point differential
                    -x["points_scored"],  # 2d. Total points scored
                )
            )

        sorted_ranking.extend(group)

    # Add position to each team
    for i, team in enumerate(sorted_ranking, 1):
        team["position"] = i

    return sorted_ranking


def format_results(results: list[dict], ranking: list[dict]) -> None:
    """Format and display the results of matches and final ranking."""
    print("\nMatches:")
    for match in results:
        home_info = f"{match['home_team']} {match['home_score']}"
        away_info = f"{match['away_score']} {match['away_team']}"
        print(f"{home_info} - {away_info}")

    print("\nFinal Ranking:")
    for team in ranking:
        team_info = f"{team['position']}. {team['name']}: {team['points']} pts"
        diff_info = f"(diff: {team['point_average']:.1f})"
        print(f"{team_info} {diff_info}")

    print("\nOfficial Ranking:")
    for team in ranking:
        print(f"{team['position']}. {team['name']}: {team['points']} pts")


def load_json_data(json_file: str) -> dict:
    """Load and return JSON data from file."""
    with open(json_file, encoding="utf-8") as f:
        return json.load(f)


def extract_teams(data: dict) -> dict[str, dict]:
    """Extract teams and their IDs from the data."""
    teams = {}
    for match in data["data"]["rencontres"]:
        teams[match["idEngagementEquipe1"]["id"]] = {
            "id": match["idEngagementEquipe1"]["id"],
            "name": match["idEngagementEquipe1"]["nom"],
        }
        teams[match["idEngagementEquipe2"]["id"]] = {
            "id": match["idEngagementEquipe2"]["id"],
            "name": match["idEngagementEquipe2"]["nom"],
        }
    return teams


def get_current_ranking(data: dict) -> list[dict]:
    """Extract the current ranking from the data."""
    ranking = []
    for team in data["data"]["classements"]:
        ranking.append(
            {
                "id": team["idEngagement"]["id"],
                "team": team["idEngagement"]["nom"],
                "position": int(team["position"]),
                "points": int(team["points"]),
                "matches": int(team["matchJoues"]),
                "wins": int(team["gagnes"]),
                "losses": int(team["perdus"]),
                "forfeits": int(team["nombreForfaits"]),
                "points_scored": int(team["paniersMarques"]),
                "points_conceded": int(team["paniersEncaisses"]),
                "point_average": int(team["difference"]),
                "quotient": float(team["quotient"]),
            }
        )
    return sorted(ranking, key=lambda x: x["position"])


def get_team_matches(data: dict, team_id: str) -> list[dict]:
    """Get all matches for a specific team."""
    team_matches = []
    for match in data["data"]["rencontres"]:
        if match["joue"] and (
            match["idEngagementEquipe1"]["id"] == team_id
            or match["idEngagementEquipe2"]["id"] == team_id
        ):
            match_info = {
                "date": datetime.strptime(match["date_rencontre"], "%Y-%m-%dT%H:%M:%S"),
                "team1_id": match["idEngagementEquipe1"]["id"],
                "team2_id": match["idEngagementEquipe2"]["id"],
                "team1_name": match["idEngagementEquipe1"]["nom"],
                "team2_name": match["idEngagementEquipe2"]["nom"],
                "score1": int(match["resultatEquipe1"]),
                "score2": int(match["resultatEquipe2"]),
                "forfeit1": match.get("forfaitEquipe1", False),
                "forfeit2": match.get("forfaitEquipe2", False),
            }
            team_matches.append(match_info)
    return sorted(team_matches, key=lambda x: x["date"])


def get_match_days(data: dict) -> list[datetime]:
    """Get all unique match days sorted by date."""
    match_days = set()
    for match in data["data"]["rencontres"]:
        if match["joue"]:
            match_date = datetime.strptime(match["date_rencontre"], "%Y-%m-%dT%H:%M:%S")
            match_days.add(match_date.date())
    return sorted(list(match_days))


def get_teams_playing_on_day(data: dict, day: date) -> set[str]:
    """Get all teams playing on a specific day."""
    teams = set()
    for match in data["data"]["rencontres"]:
        if not match["joue"]:
            continue
        match_date = datetime.strptime(match["date_rencontre"], "%Y-%m-%dT%H:%M:%S")
        if match_date.date() == day:
            teams.add(match["idEngagementEquipe1"]["id"])
            teams.add(match["idEngagementEquipe2"]["id"])
    return teams


def calculate_ranking_evolution(data: dict) -> dict[str, list[dict]]:
    """Calculate ranking evolution for all teams.
    Returns a dictionary with team_id as key and list of rankings as value.
    """
    teams = extract_teams(data)
    match_days = get_match_days(data)

    # Initialize statistics for all teams
    team_stats = {
        id: {
            "matches": 0,
            "wins": 0,
            "losses": 0,
            "forfeits": 0,
            "points_scored": 0,
            "points_conceded": 0,
            "results": [],
            "exempt_days": [],  # New: track exempt days
        }
        for id in teams
    }

    # Dictionary to store evolution for each team
    evolution = {id: [] for id in teams}

    for match_day in match_days:
        # Get teams playing on this day
        playing_teams = get_teams_playing_on_day(data, match_day)

        # Record exempt teams
        for team_id in teams:
            if team_id not in playing_teams:
                team_stats[team_id]["exempt_days"].append(match_day)

        # Update stats for all matches on this date
        day_matches = [
            m
            for m in data["data"]["rencontres"]
            if m["joue"]
            and datetime.strptime(m["date_rencontre"], "%Y-%m-%dT%H:%M:%S").date()
            == match_day
        ]

        for match in day_matches:
            team1_id = match["idEngagementEquipe1"]["id"]
            team2_id = match["idEngagementEquipe2"]["id"]
            score1 = int(match["resultatEquipe1"])
            score2 = int(match["resultatEquipe2"])
            forfeit1, forfeit2 = is_forfeit_match(match)

            # Update match statistics
            team_stats[team1_id]["matches"] += 1
            team_stats[team2_id]["matches"] += 1

            # Handle forfeit matches
            if forfeit1 or forfeit2:
                if forfeit1:
                    team_stats[team1_id]["forfeits"] += 1
                    team_stats[team2_id]["wins"] += 1
                    team_stats[team1_id]["results"].append("❌")
                    team_stats[team2_id]["results"].append("✅")
                    # For forfeit matches, use 20-0 score for point differential
                    team_stats[team1_id]["points_scored"] += 0
                    team_stats[team1_id]["points_conceded"] += 20
                    team_stats[team2_id]["points_scored"] += 20
                    team_stats[team2_id]["points_conceded"] += 0
                elif forfeit2:
                    team_stats[team2_id]["forfeits"] += 1
                    team_stats[team1_id]["wins"] += 1
                    team_stats[team2_id]["results"].append("❌")
                    team_stats[team1_id]["results"].append("✅")
                    # For forfeit matches, use 20-0 score for point differential
                    team_stats[team2_id]["points_scored"] += 0
                    team_stats[team2_id]["points_conceded"] += 20
                    team_stats[team1_id]["points_scored"] += 20
                    team_stats[team1_id]["points_conceded"] += 0
            else:
                # Normal match
                if score1 > score2:
                    team_stats[team1_id]["wins"] += 1
                    team_stats[team2_id]["losses"] += 1
                    team_stats[team1_id]["results"].append("✅")
                    team_stats[team2_id]["results"].append("❌")
                else:
                    team_stats[team2_id]["wins"] += 1
                    team_stats[team1_id]["losses"] += 1
                    team_stats[team2_id]["results"].append("✅")
                    team_stats[team1_id]["results"].append("❌")

                # Update points scored/conceded for normal matches
                team_stats[team1_id]["points_scored"] += score1
                team_stats[team2_id]["points_scored"] += score2
                team_stats[team1_id]["points_conceded"] += score2
                team_stats[team2_id]["points_conceded"] += score1

        # Calculate current ranking for all teams
        current_ranking = []
        for tid, team_info in teams.items():
            stats = team_stats[tid]
            points = calculate_points(stats["wins"], stats["losses"], stats["forfeits"])

            quotient = (
                stats["points_scored"] / stats["points_conceded"]
                if stats["points_conceded"] > 0
                else 0
            )

            current_ranking.append(
                {
                    "id": tid,
                    "name": team_info["name"],
                    "points": points,
                    "matches": stats["matches"],
                    "wins": stats["wins"],
                    "losses": stats["losses"],
                    "points_scored": stats["points_scored"],
                    "points_conceded": stats["points_conceded"],
                    "point_average": stats["points_scored"] - stats["points_conceded"],
                    "quotient": quotient,
                    "results": stats["results"].copy(),
                    "exempt_days": stats["exempt_days"].copy(),
                }
            )

        # Sort ranking according to FFBB rules
        current_ranking = sort_ranking(current_ranking, data)

        # Store evolution for each team
        for team in current_ranking:
            evolution[team["id"]].append(
                {
                    "date": match_day.strftime("%Y-%m-%d"),
                    "position": team["position"],
                    "points": team["points"],
                    "wins": team["wins"],
                    "losses": team["losses"],
                    "points_scored": team["points_scored"],
                    "points_conceded": team["points_conceded"],
                    "point_average": team["point_average"],
                    "quotient": team["quotient"],
                    "results": team["results"].copy(),
                }
            )

    return evolution


def is_forfeit_score(score1: int, score2: int) -> bool:
    """Check if the score indicates a forfeit (20-0 or 0-20 or 0-0)."""
    return (
        (score1 == 20 and score2 == 0)
        or (score1 == 0 and score2 == 20)
        or (score1 == 0 and score2 == 0)
    )


def is_forfeit_match(match: dict) -> tuple[bool, bool]:
    """Check if a match has a forfeit and which team forfeited.

    Args:
        match: Match data dictionary

    Returns:
        tuple[bool, bool]: (team1_forfeit, team2_forfeit)
    """
    # Si le match n'est pas joué, ce n'est pas un forfait
    if not match["joue"]:
        return False, False

    # Vérifier d'abord les champs forfaitEquipe1 et forfaitEquipe2
    if match.get("forfaitEquipe1", False):
        return True, False
    if match.get("forfaitEquipe2", False):
        return False, True

    # Sinon, vérifier les scores
    score1 = int(match["resultatEquipe1"])
    score2 = int(match["resultatEquipe2"])

    # Si c'est un match avec forfait (score 20-0, 0-20 ou 0-0)
    if score1 == 20 and score2 == 0:
        # L'équipe 2 a forfait
        return False, True
    elif score1 == 0 and score2 == 20:
        # L'équipe 1 a forfait
        return True, False
    elif score1 == 0 and score2 == 0:
        # Double forfait
        return True, True

    return False, False


def analyze_team_matches(data: dict, team_id: str) -> dict:
    """Analyze all matches for a team to get detailed statistics."""
    team_stats = {
        "wins": 0,
        "losses": 0,
        "forfeits_for": 0,
        "forfeits_against": 0,
        "points_scored": 0,
        "points_conceded": 0,
        "results": [],
        "forfeit_matches": [],
    }

    for match in data["data"]["rencontres"]:
        if not match["joue"]:
            continue

        is_team1 = match["idEngagementEquipe1"]["id"] == team_id
        is_team2 = match["idEngagementEquipe2"]["id"] == team_id

        if not (is_team1 or is_team2):
            continue

        score1 = int(match["resultatEquipe1"])
        score2 = int(match["resultatEquipe2"])
        forfeit1, forfeit2 = is_forfeit_match(match)

        # Conversion de la date du match
        match_date = datetime.strptime(
            match["date_rencontre"], "%Y-%m-%dT%H:%M:%S"
        ).strftime("%Y-%m-%d")

        if is_team1:
            opponent_name = match["idEngagementEquipe2"]["nom"]
            opponent_score = score2
            team_score = score1
        else:  # is_team2
            opponent_name = match["idEngagementEquipe1"]["nom"]
            opponent_score = score1
            team_score = score2

        # Gestion des forfaits et scores
        forfeit_against = (is_team1 and forfeit1) or (is_team2 and forfeit2)
        forfeit_for = (is_team1 and forfeit2) or (is_team2 and forfeit1)

        if forfeit_against:
            # Forfait contre
            team_stats["forfeits_against"] += 1
            team_stats["losses"] += 1
            team_stats["results"].append("❌")
            forfeit_info = {
                "date": match_date,
                "opponent": opponent_name,
                "score": f"{team_score}-{opponent_score}",
                "type": "contre",
            }
            team_stats["forfeit_matches"].append(forfeit_info)
            # Score officiel pour un forfait : 0-20
            team_stats["points_scored"] += 0
            team_stats["points_conceded"] += 20
        elif forfeit_for:
            # Forfait en faveur
            team_stats["forfeits_for"] += 1
            team_stats["wins"] += 1
            team_stats["results"].append("✅")
            forfeit_info = {
                "date": match_date,
                "opponent": opponent_name,
                "score": f"{team_score}-{opponent_score}",
                "type": "pour",
            }
            team_stats["forfeit_matches"].append(forfeit_info)
            # Score officiel pour un forfait : 20-0
            team_stats["points_scored"] += 20
            team_stats["points_conceded"] += 0
        else:
            # Match normal
            team_stats["points_scored"] += team_score
            team_stats["points_conceded"] += opponent_score
            if team_score > opponent_score:
                team_stats["wins"] += 1
                team_stats["results"].append("✅")
            else:
                team_stats["losses"] += 1
                team_stats["results"].append("❌")

    return team_stats


def determine_winner(match: dict) -> str:
    """Determine the winning team name for a match.

    Args:
        match: Match data with scores and team information

    Returns:
        Name of the winning team, or empty string if match not played
    """
    if not match["joue"]:
        return ""

    score1 = int(match["resultatEquipe1"])
    score2 = int(match["resultatEquipe2"])

    if score1 > score2:
        return match["idEngagementEquipe1"]["nom"]
    elif score2 > score1:
        return match["idEngagementEquipe2"]["nom"]

    # Pour les matchs forfaits avec score 0-0, on considère l'équipe 2 comme gagnante
    # car c'est le seul scénario qui correspond au classement officiel
    if is_forfeit_score(score1, score2) and score1 == 0 and score2 == 0:
        return match["idEngagementEquipe2"]["nom"]

    return ""


def find_match_index(matches: list[dict], match_id: str) -> int:
    """Find the index of a match by its ID."""
    for i, match in enumerate(matches):
        if match["id"] == match_id:
            return i
    return -1


def save_json_data(data: dict, json_file: str) -> None:
    """Save data to a JSON file."""
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def calculate_ranking_possibilities(
    data: dict, max_scenarios: int = 1000
) -> tuple[list[dict], dict]:
    """Calculate possible ranking evolutions considering forfeit uncertainties.

    Args:
        data: Competition data
        max_scenarios: Maximum number of scenarios to test

    Returns:
        Tuple of (list of possible evolutions, updated data)
    """
    # Add winner information to all matches
    data_copy = data.copy()
    data_copy["data"] = data["data"].copy()
    data_copy["data"]["rencontres"] = []

    for match in data["data"]["rencontres"]:
        match_copy = match.copy()
        match_copy["customEquipeGagnante"] = determine_winner(match)
        data_copy["data"]["rencontres"].append(match_copy)

    # First, calculate current ranking evolution
    current_evolution = calculate_ranking_evolution(data_copy)
    official_ranking = get_current_ranking(data)

    # Compare with official ranking
    matches_official = True
    calculated_ranking = []

    for team_id, snapshots in current_evolution.items():
        if snapshots:
            last_snapshot = snapshots[-1]
            official = next(t for t in official_ranking if t["id"] == team_id)

            calculated_ranking.append(
                {
                    "id": team_id,
                    "position": last_snapshot["position"],
                    "points": last_snapshot["points"],
                    "wins": last_snapshot["wins"],
                    "losses": last_snapshot["losses"],
                    "points_scored": last_snapshot["points_scored"],
                    "points_conceded": last_snapshot["points_conceded"],
                }
            )

            # Check if this team's stats match official ranking
            if (
                last_snapshot["position"] != official["position"]
                or last_snapshot["points"] != official["points"]
                or last_snapshot["wins"] != official["wins"]
                or last_snapshot["losses"] != official["losses"]
            ):
                matches_official = False
                print(f"\nDifférence trouvée pour {official['team']}:")
                print(
                    f"Calculé: P{last_snapshot['position']}, "
                    f"{last_snapshot['points']}pts, "
                    f"{last_snapshot['wins']}V {last_snapshot['losses']}D"
                )
                print(
                    f"Officiel: P{official['position']}, "
                    f"{official['points']}pts, "
                    f"{official['wins']}V {official['losses']}D"
                )

    # If current ranking matches official, no need to explore possibilities
    if matches_official:
        print("\nLe classement calculé correspond au classement officiel.")
        return [
            {
                "evolution": current_evolution,
                "forfeit_config": [],
                "matches_official": True,
                "ranking": calculated_ranking,
                "score": 1000,
            }
        ], data_copy

    print("\nRecherche des différentes possibilités...")

    # Reset data copy without winners
    data_copy = data.copy()
    data_copy["data"] = data["data"].copy()
    data_copy["data"]["rencontres"] = []

    for match in data["data"]["rencontres"]:
        match_copy = match.copy()
        if match["joue"]:
            score1 = int(match["resultatEquipe1"])
            score2 = int(match["resultatEquipe2"])
            if not is_forfeit_score(score1, score2):
                # Keep winner for normal matches
                match_copy["customEquipeGagnante"] = determine_winner(match)
        data_copy["data"]["rencontres"].append(match_copy)

    # Identify potential forfeit matches
    potential_forfeits = []
    for match in data_copy["data"]["rencontres"]:
        if match["joue"]:
            score1 = int(match["resultatEquipe1"])
            score2 = int(match["resultatEquipe2"])
            if is_forfeit_score(score1, score2):
                potential_forfeits.append(match)
        elif (
            datetime.strptime(match["date_rencontre"], "%Y-%m-%dT%H:%M:%S").date()
            < datetime.now().date()
        ):
            potential_forfeits.append(match)

    print(f"Matchs potentiellement forfaits : {len(potential_forfeits)}")

    # If no potential forfeits, we can't improve the ranking
    if not potential_forfeits:
        print(
            "\nAucun match potentiellement forfait trouvé pour améliorer le classement."
        )
        return [
            {
                "evolution": current_evolution,
                "forfeit_config": [],
                "matches_official": False,
                "ranking": calculated_ranking,
                "score": 0,
            }
        ], data_copy

    # Limit the number of matches to consider to avoid explosion
    potential_forfeits = potential_forfeits[:3]
    n_matches = len(potential_forfeits)
    n_possibilities = min(2**n_matches, max_scenarios)

    all_evolutions = []

    # For each possibility
    for i in range(n_possibilities):
        # Create a copy of the data
        scenario_data = data_copy.copy()
        scenario_data["data"] = data_copy["data"].copy()
        scenario_data["data"]["rencontres"] = data_copy["data"]["rencontres"].copy()

        # For each match
        forfeit_config = []
        for j in range(n_matches):
            match = potential_forfeits[j]
            match_idx = find_match_index(
                scenario_data["data"]["rencontres"], match["id"]
            )

            # If the j-th bit of i is 1, team1 wins, else team2 wins
            if (i >> j) & 1:
                # Team 1 wins by forfeit
                scenario_data["data"]["rencontres"][match_idx] = {
                    **match,
                    "joue": True,
                    "resultatEquipe1": "20",
                    "resultatEquipe2": "0",
                    "customEquipeGagnante": match["idEngagementEquipe1"]["nom"],
                }
                winner = "team1"
            else:
                # Team 2 wins by forfeit
                scenario_data["data"]["rencontres"][match_idx] = {
                    **match,
                    "joue": True,
                    "resultatEquipe1": "0",
                    "resultatEquipe2": "20",
                    "customEquipeGagnante": match["idEngagementEquipe2"]["nom"],
                }
                winner = "team2"

            forfeit_config.append(
                {
                    "date": match["date_rencontre"],
                    "team1": match["idEngagementEquipe1"]["nom"],
                    "team2": match["idEngagementEquipe2"]["nom"],
                    "winner": winner,
                    "played": match["joue"],
                }
            )

        # Calculate evolution with this combination
        evolution = calculate_ranking_evolution(scenario_data)

        # Compare with official ranking
        calculated_ranking = []
        score = 0  # Score to evaluate how close this scenario is
        matches_official = True

        for team_id, snapshots in evolution.items():
            if snapshots:
                last_snapshot = snapshots[-1]
                official = next(t for t in official_ranking if t["id"] == team_id)

                # Calculate score based on differences
                if last_snapshot["position"] == official["position"]:
                    score += 10
                if last_snapshot["points"] == official["points"]:
                    score += 5
                if last_snapshot["wins"] == official["wins"]:
                    score += 3
                if last_snapshot["losses"] == official["losses"]:
                    score += 3

                calculated_ranking.append(
                    {
                        "id": team_id,
                        "position": last_snapshot["position"],
                        "points": last_snapshot["points"],
                        "wins": last_snapshot["wins"],
                        "losses": last_snapshot["losses"],
                        "points_scored": last_snapshot["points_scored"],
                        "points_conceded": last_snapshot["points_conceded"],
                    }
                )

                if (
                    last_snapshot["position"] != official["position"]
                    or last_snapshot["points"] != official["points"]
                    or last_snapshot["wins"] != official["wins"]
                    or last_snapshot["losses"] != official["losses"]
                ):
                    matches_official = False

        # Sort by position
        calculated_ranking.sort(key=lambda x: x["position"])

        # If this scenario matches official ranking, update match winners
        if matches_official:
            for match_config, match in zip(forfeit_config, potential_forfeits):
                match_idx = find_match_index(
                    data_copy["data"]["rencontres"], match["id"]
                )
                if match_config["winner"] == "team1":
                    data_copy["data"]["rencontres"][match_idx][
                        "customEquipeGagnante"
                    ] = match["idEngagementEquipe1"]["nom"]
                else:
                    data_copy["data"]["rencontres"][match_idx][
                        "customEquipeGagnante"
                    ] = match["idEngagementEquipe2"]["nom"]

        all_evolutions.append(
            {
                "evolution": evolution,
                "forfeit_config": forfeit_config,
                "matches_official": matches_official,
                "ranking": calculated_ranking,
                "score": score,
            }
        )

    # Sort by score, highest first
    all_evolutions.sort(key=lambda x: x["score"], reverse=True)
    return all_evolutions, data_copy


def display_current_ranking(data: dict) -> None:
    """Affiche le classement actuel avec les statistiques détaillées."""
    print("\nClassement actuel :")
    print(
        f"{'Pos':>3}  {'Équipe':<35}  {'Pts':>3}  {'V':>3}  {'D':>3}  "
        f"{'Pts M':>5}  {'Pts E':>5}  {'Diff':>5}"
    )
    print("-" * 85)

    ranking = get_current_ranking(data)
    for team in ranking:
        print(
            f"{team['position']:3}  "
            f"{team['team']:<35}  "
            f"{team['points']:3}  "
            f"{team['wins']:3}  "
            f"{team['losses']:3}  "
            f"{team['points_scored']:5}  "
            f"{team['points_conceded']:5}  "
            f"{team['point_average']:5}"
        )


def get_match_for_date(
    data: dict, team_name: str, date_str: str
) -> tuple[str, str, int, int]:
    """Trouve le match d'une équipe à une date donnée.

    Returns:
        tuple[str, str, int, int]: (équipe adverse, score équipe, score adversaire)
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

    for match in data["data"]["rencontres"]:
        match_date = datetime.strptime(
            match["date_rencontre"], "%Y-%m-%dT%H:%M:%S"
        ).date()

        if match_date == date_obj and match["joue"]:
            team1 = match["idEngagementEquipe1"]["nom"]
            team2 = match["idEngagementEquipe2"]["nom"]
            score1 = int(match["resultatEquipe1"])
            score2 = int(match["resultatEquipe2"])

            if team1 == team_name:
                return team2, score1, score2
            elif team2 == team_name:
                return team1, score2, score1

    return "", 0, 0


def display_team_evolution(data: dict, team_name: str) -> None:
    """Affiche l'évolution du classement d'une équipe."""
    evolution = calculate_ranking_evolution(data)

    # Trouver l'ID de l'équipe
    team_id = None
    for match in data["data"]["rencontres"]:
        if match["idEngagementEquipe1"]["nom"] == team_name:
            team_id = match["idEngagementEquipe1"]["id"]
            break
        elif match["idEngagementEquipe2"]["nom"] == team_name:
            team_id = match["idEngagementEquipe2"]["id"]
            break

    if team_id is None or team_id not in evolution:
        print(f"\nÉquipe {team_name} non trouvée.")
        return

    print(f"\nÉvolution du classement de {team_name} :")
    header1 = f"{'':2}  {'Date':<10}  {'Pos':>3}  {'Pts':>3}  {'V':>3}  {'D':>3}"
    header2 = f"{'Pts M':>5}  {'Pts E':>5}  {'Diff':>5}  {'Score':>7}  {'Adversaire'}"
    print(f"{header1}  {header2}")
    print("-" * 120)

    for snapshot in evolution[team_id]:
        # Déterminer l'emoji basé sur le dernier résultat
        last_result = snapshot["results"][-1] if snapshot["results"] else " "

        # Trouver le match du jour
        opponent, score_team, score_opp = get_match_for_date(
            data, team_name, snapshot["date"]
        )

        # N'afficher que si l'équipe joue ce jour-là
        if opponent:
            if is_forfeit_score(score_team, score_opp):
                score_str = "Forfait"
                match_str = opponent
            else:
                score_str = f"{score_team}-{score_opp}"
                match_str = opponent

            stats = (
                f"{last_result:2}  {snapshot['date']}  {snapshot['position']:3}  "
                f"{snapshot['points']:3}  {snapshot['wins']:3}  "
                f"{snapshot['losses']:3}  {snapshot['points_scored']:5}  "
                f"{snapshot['points_conceded']:5}  {snapshot['point_average']:5}  "
                f"{score_str:>7}  {match_str}"
            )
            print(stats)


def get_matches_for_date(data: dict, date_str: str) -> list[dict]:
    """Récupère tous les matchs d'une journée donnée."""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    matches = []

    for match in data["data"]["rencontres"]:
        match_date = datetime.strptime(
            match["date_rencontre"], "%Y-%m-%dT%H:%M:%S"
        ).date()

        if match_date == date_obj and match["joue"]:
            team1 = match["idEngagementEquipe1"]["nom"]
            team2 = match["idEngagementEquipe2"]["nom"]
            score1 = int(match["resultatEquipe1"])
            score2 = int(match["resultatEquipe2"])
            matches.append(
                {"team1": team1, "team2": team2, "score1": score1, "score2": score2}
            )

    return matches


def display_detailed_evolution(data: dict, team_name: str) -> None:
    """Affiche l'évolution détaillée du classement avec tous les matchs."""
    evolution = calculate_ranking_evolution(data)
    official_ranking = get_official_ranking(data)

    # Trouver l'ID de l'équipe suivie
    team_id = None
    for match in data["data"]["rencontres"]:
        if match["idEngagementEquipe1"]["nom"] == team_name:
            team_id = match["idEngagementEquipe1"]["id"]
            break
        elif match["idEngagementEquipe2"]["nom"] == team_name:
            team_id = match["idEngagementEquipe2"]["id"]
            break

    if team_id is None or team_id not in evolution:
        print(f"\nÉquipe {team_name} non trouvée.")
        return

    print("\nÉvolution détaillée du championnat :")

    # Trouver la dernière date
    last_date = max(snap["date"] for snap in evolution[team_id])

    # Pour chaque journée où l'équipe suivie a joué
    for snapshot in evolution[team_id]:
        matches = get_matches_for_date(data, snapshot["date"])
        if not matches:
            continue

        print(f"\nJournée du {snapshot['date']} :")
        print("Matchs :")
        for match in matches:
            # Vérifier si c'est un forfait
            forfeit1, forfeit2 = False, False
            if is_forfeit_score(match["score1"], match["score2"]):
                if match["score1"] == 20:
                    forfeit2 = True
                elif match["score2"] == 20:
                    forfeit1 = True
                else:  # 0-0
                    forfeit1, forfeit2 = True, True

            # Déterminer le score à afficher
            if forfeit1 or forfeit2:
                if forfeit1 and forfeit2:
                    score_str = "Double forfait"
                else:
                    score_str = "Forfait"
            else:
                score_str = f"{match['score1']}-{match['score2']}"

            # Déterminer les gagnants/perdants
            team1_win = match["score1"] > match["score2"] or (forfeit2 and not forfeit1)
            team2_win = match["score2"] > match["score1"] or (forfeit1 and not forfeit2)

            # Ajouter les emojis selon le résultat
            team1_emoji = "✅ " if team1_win else "❌ "
            team2_emoji = "✅ " if team2_win else "❌ "

            # Mettre en évidence l'équipe suivie
            team1 = (
                f"* {match['team1']} *"
                if match["team1"] == team_name
                else match["team1"]
            )
            team2 = (
                f"* {match['team2']} *"
                if match["team2"] == team_name
                else match["team2"]
            )

            # Ajouter l'indicateur de forfait au nom de l'équipe
            if forfeit1:
                team1 += " (F)"
            if forfeit2:
                team2 += " (F)"

            print(f"  {team1_emoji}{team1:<40} {score_str:>12}  {team2_emoji}{team2}")

        # Afficher le classement après cette journée
        print("\nClassement :")
        header = (
            f"{'Pos':>3}  {'Équipe':<35}  {'Pts':>3}  {'Off':>3}  "
            f"{'V':>3}  {'D':>3}  {'Pts M':>5}  {'Pts E':>5}  {'Diff':>5}  {'Off':>5}"
        )
        print(header)
        print("-" * len(header))

        # Récupérer le classement de tous les équipes à cette date
        ranking = []
        for tid in evolution:
            for snap in evolution[tid]:
                if snap["date"] == snapshot["date"]:
                    team_name = next(
                        t["name"]
                        for t in extract_teams(data).values()
                        if t["id"] == tid
                    )
                    # Trouver le classement officiel pour cette équipe
                    off = next(
                        (t for t in official_ranking if t["team"] == team_name), None
                    )
                    ranking.append(
                        {
                            "name": team_name,
                            "position": snap["position"],
                            "points": snap["points"],
                            "wins": snap["wins"],
                            "losses": snap["losses"],
                            "points_scored": snap["points_scored"],
                            "points_conceded": snap["points_conceded"],
                            "point_average": snap["point_average"],
                            "official_pos": off["position"] if off else 0,
                            "official_pts": off["points"] if off else 0,
                            "official_wins": off["wins"] if off else 0,
                            "official_losses": off["losses"] if off else 0,
                            "official_diff": off["point_average"] if off else 0,
                        }
                    )
                    break

        # Trier par position
        ranking.sort(key=lambda x: x["position"])

        # Vérifier si c'est la dernière journée
        is_last_day = snapshot["date"] == last_date

        # Afficher chaque équipe
        for team in ranking:
            name = f"* {team['name']} *" if team["name"] == team_name else team["name"]
            # Ajouter des indicateurs de différence uniquement pour la dernière journée
            if is_last_day:
                pts_diff = "≠" if team["points"] != team["official_pts"] else " "
                # Ne plus afficher de différence pour le point average
                diff_diff = " "
            else:
                pts_diff = " "
                diff_diff = " "

            print(
                f"{team['position']:3}  "
                f"{name:<35}  "
                f"{team['points']:3} {pts_diff} {team['official_pts']:3}  "
                f"{team['wins']:3}  {team['losses']:3}  "
                f"{team['points_scored']:5}  {team['points_conceded']:5}  "
                f"{team['point_average']:5} {diff_diff} {team['official_diff']:5}"
            )
        print()


def calculate_estimations(data: dict, team_name: str) -> tuple[dict, dict]:
    """Calcule les estimations de classement dans le meilleur et le pire des cas.

    Args:
        data: Les données de la compétition
        team_name: Le nom de l'équipe à analyser

    Returns:
        tuple[Dict, Dict]: (meilleur cas, pire cas)
    """
    current_date = datetime.now().date()

    # Récupérer le classement actuel
    current_ranking = get_current_ranking(data)

    # Trouver notre position actuelle
    our_position = next(
        i for i, team in enumerate(current_ranking) if team["team"] == team_name
    )

    # Récupérer les équipes au-dessus de nous
    teams_above = [team["team"] for team in current_ranking[:our_position]]
    teams_to_watch = teams_above + [team_name]

    # Récupérer tous les matchs restants dans l'ordre chronologique
    remaining_matches = []
    for match in data["data"]["rencontres"]:
        match_date = datetime.strptime(
            match["date_rencontre"], "%Y-%m-%dT%H:%M:%S"
        ).date()

        if not match["joue"] and match_date > current_date:
            team1 = match["idEngagementEquipe1"]["nom"]
            team2 = match["idEngagementEquipe2"]["nom"]

            # On ne garde que les matchs qui concernent les équipes qui nous intéressent
            if team1 in teams_to_watch or team2 in teams_to_watch:
                remaining_matches.append(
                    {"date": match_date, "team1": team1, "team2": team2}
                )

    # Trier les matchs par date
    remaining_matches.sort(key=lambda x: x["date"])

    # Initialiser les cas avec le classement actuel
    best_case = {
        team["team"]: {
            "points": team["points"],
            "wins": team["wins"],
            "losses": team["losses"],
            "matches_left": 0,
        }
        for team in current_ranking
    }

    worst_case = {
        team["team"]: {
            "points": team["points"],
            "wins": team["wins"],
            "losses": team["losses"],
            "matches_left": 0,
        }
        for team in current_ranking
    }

    # Simuler chaque match dans l'ordre chronologique
    for match in remaining_matches:
        team1 = match["team1"]
        team2 = match["team2"]

        # Compter les matchs restants
        best_case[team1]["matches_left"] += 1
        best_case[team2]["matches_left"] += 1
        worst_case[team1]["matches_left"] += 1
        worst_case[team2]["matches_left"] += 1

        # Meilleur cas : notre équipe gagne, les équipes au-dessus perdent
        if team1 == team_name:
            # On gagne
            best_case[team1]["points"] += 2
            best_case[team1]["wins"] += 1
            best_case[team2]["points"] += 1
            best_case[team2]["losses"] += 1
        elif team2 == team_name:
            # On gagne
            best_case[team2]["points"] += 2
            best_case[team2]["wins"] += 1
            best_case[team1]["points"] += 1
            best_case[team1]["losses"] += 1
        elif team1 in teams_above:
            # L'équipe au-dessus perd
            best_case[team1]["points"] += 1
            best_case[team1]["losses"] += 1
            best_case[team2]["points"] += 2
            best_case[team2]["wins"] += 1
        elif team2 in teams_above:
            # L'équipe au-dessus perd
            best_case[team2]["points"] += 1
            best_case[team2]["losses"] += 1
            best_case[team1]["points"] += 2
            best_case[team1]["wins"] += 1

        # Pire cas : notre équipe perd, les équipes au-dessus gagnent
        if team1 == team_name:
            # On perd
            worst_case[team1]["points"] += 1
            worst_case[team1]["losses"] += 1
            worst_case[team2]["points"] += 2
            worst_case[team2]["wins"] += 1
        elif team2 == team_name:
            # On perd
            worst_case[team2]["points"] += 1
            worst_case[team2]["losses"] += 1
            worst_case[team1]["points"] += 2
            worst_case[team1]["wins"] += 1
        elif team1 in teams_above:
            # L'équipe au-dessus gagne
            worst_case[team1]["points"] += 2
            worst_case[team1]["wins"] += 1
            worst_case[team2]["points"] += 1
            worst_case[team2]["losses"] += 1
        elif team2 in teams_above:
            # L'équipe au-dessus gagne
            worst_case[team2]["points"] += 2
            worst_case[team2]["wins"] += 1
            worst_case[team1]["points"] += 1
            worst_case[team1]["losses"] += 1

    return best_case, worst_case


def display_estimation(data: dict, team_name: str) -> None:
    """Affiche les estimations de classement."""
    best_case, worst_case = calculate_estimations(data, team_name)

    print("\nEstimations de fin de saison :")
    print("\nMeilleur des cas (on gagne tout, les autres perdent) :")
    print("Position  Équipe                               Pts    V    D  Matchs")
    print("---------------------------------------------------------------")

    # Trier par points puis par victoires
    teams_sorted = sorted(
        best_case.items(), key=lambda x: (-x[1]["points"], -x[1]["wins"])
    )

    # Afficher avec les positions
    for i, (team, stats) in enumerate(teams_sorted, 1):
        name = f"* {team} *" if team == team_name else team
        print(
            f"{i:^8}  {name:<35}  {stats['points']:3}  "
            f"{stats['wins']:3}  {stats['losses']:3}  {stats['matches_left']:6}"
        )

    print("\nPire des cas (on perd tout, les autres gagnent) :")
    print("Position  Équipe                               Pts    V    D  Matchs")
    print("---------------------------------------------------------------")

    # Trier par points puis par victoires
    teams_sorted = sorted(
        worst_case.items(), key=lambda x: (-x[1]["points"], -x[1]["wins"])
    )

    # Afficher avec les positions
    for i, (team, stats) in enumerate(teams_sorted, 1):
        name = f"* {team} *" if team == team_name else team
        print(
            f"{i:^8}  {name:<35}  {stats['points']:3}  "
            f"{stats['wins']:3}  {stats['losses']:3}  {stats['matches_left']:6}"
        )

    # Trouver les positions possibles
    best_pos = next(
        i
        for i, (team, _) in enumerate(
            sorted(best_case.items(), key=lambda x: (-x[1]["points"], -x[1]["wins"])), 1
        )
        if team == team_name
    )

    worst_pos = next(
        i
        for i, (team, _) in enumerate(
            sorted(worst_case.items(), key=lambda x: (-x[1]["points"], -x[1]["wins"])),
            1,
        )
        if team == team_name
    )

    print(f"\nRésumé pour {team_name} :")
    print(f"Position possible : entre {best_pos}e et {worst_pos}e")
    print(
        f"Points possibles : entre {worst_case[team_name]['points']} "
        f"et {best_case[team_name]['points']}"
    )


def display_remaining_matches(data: dict, team_name: str) -> None:
    """Affiche les matchs restants des équipes qui nous intéressent."""
    current_date = datetime.now().date()
    current_ranking = get_current_ranking(data)

    # Trouver notre position actuelle
    our_position = next(
        i for i, team in enumerate(current_ranking) if team["team"] == team_name
    )

    # Récupérer les équipes au-dessus de nous
    teams_above = [team["team"] for team in current_ranking[:our_position]]
    teams_to_watch = teams_above + [team_name]

    print("\nMatchs restants :")
    for team in teams_to_watch:
        matches = []
        for match in data["data"]["rencontres"]:
            match_date = datetime.strptime(
                match["date_rencontre"], "%Y-%m-%dT%H:%M:%S"
            ).date()

            if not match["joue"] and match_date > current_date:
                team1 = match["idEngagementEquipe1"]["nom"]
                team2 = match["idEngagementEquipe2"]["nom"]

                if team in [team1, team2]:
                    opponent = team2 if team == team1 else team1
                    matches.append({"date": match_date, "opponent": opponent})

        if matches:
            print(f"\n{team} ({len(matches)} matchs) :")
            for match in sorted(matches, key=lambda x: x["date"]):
                print(f"  {match['date']} vs {match['opponent']}")
        else:
            print(f"\n{team} : Plus de match à jouer")


def main():
    json_file = "data/ffbb senas.json"
    data = load_json_data(json_file)

    # Calculate possible ranking evolutions
    possible_evolutions, updated_data = calculate_ranking_possibilities(data)

    # Afficher le classement actuel
    display_current_ranking(updated_data)

    # Afficher l'évolution de SENAS BASKET BALL
    display_team_evolution(updated_data, TEAM_NAME)

    # Afficher l'évolution détaillée
    display_detailed_evolution(updated_data, TEAM_NAME)

    # Afficher les matchs restants
    display_remaining_matches(updated_data, TEAM_NAME)

    # # Afficher les estimations
    # display_estimation(updated_data, TEAM_NAME)

    print(f"\nDonnées sauvegardées dans {json_file}")


if __name__ == "__main__":
    main()
