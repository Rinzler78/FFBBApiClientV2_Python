# FFBB Search Procedures - Complete Guide

This document details all search procedures using exclusively the `FFBBAPIClientV2` client to extract FFBB information via integrated API calls.

## 🔧 Architecture and Fundamental Principle

### Main Client

```python
from ffbb_api_client_v2 import FFBBAPIClientV2

# Initialize main client (single entry point)
client = FFBBAPIClientV2.create(
    meilisearch_bearer_token="...",
    api_bearer_token="...",
    debug=True
)
```

### Automatic Discovery Principle

- ✅ **All IDs are discovered** via client calls
- ❌ **No ID is manually extracted** from URLs
- 🎯 **Single client** encapsulates all APIs (Meilisearch + FFBB)
- 🔄 **Reproducible process** for any search

---

## 📋 USE CASES - CLUB SEARCH

### 1. Club Search by Name

#### 1.1 Exact Search

```python
from typing import Optional, List, Dict, Any, Tuple
from ffbb_api_client_v2 import FFBBAPIClientV2
from ffbb_api_client_v2.models.multi_search_result_organismes import (
    OrganismesMultiSearchResult,
    OrganismesHit
)
from ffbb_api_client_v2.models.organismes_models import GetOrganismeResponse
from ffbb_api_client_v2.models.competitions_models import GetCompetitionResponse
from ffbb_api_client_v2.models.poules_models import GetPouleResponse

def search_club_by_name(client: FFBBAPIClientV2, club_name: str) -> Optional[OrganismesHit]:
    """
    Client function: client.search_organismes()
    Underlying API: POST /multi-search (index: ffbbserver_organismes)

    Args:
        client: FFBBAPIClientV2 instance
        club_name: Name of the club to search

    Returns:
        First matching club or None if not found
    """

    # Search with spelling variants
    variants = [club_name, club_name.upper(), club_name.lower(),
                club_name.replace("é", "e"), club_name.replace("è", "e")]

    for variant in variants:
        result: OrganismesMultiSearchResult = client.search_organismes(variant)
        if result.hits:
            return result.hits[0]  # First result

    return None

# Usage example
club = search_club_by_name(client, "Pelissanne")
# Result: club.id = "123456", club.nom = "PELISSANNE BASKET CLUB"
```

#### 1.2 Fuzzy Search

```python
def search_club_fuzzy(client: FFBBAPIClientV2, search_term: str) -> List[OrganismesHit]:
    """
    Client function: client.search_organismes()
    Strategy: Search with partial keywords

    Args:
        client: FFBBAPIClientV2 instance
        search_term: Search term to find clubs

    Returns:
        List of relevant clubs matching the search term
    """

    # Split search term into keywords
    keywords = search_term.split()

    # Search by individual keywords
    for keyword in keywords:
        if len(keyword) >= 3:  # Avoid too short words
            result = client.search_organismes(keyword)
            if result.hits:
                # Filter relevant results
                relevant_clubs = []
                for hit in result.hits:
                    if any(k.lower() in hit.nom.lower() for k in keywords):
                        relevant_clubs.append(hit)
                return relevant_clubs

    return []
```

### 2. Club Search by City

#### 2.1 Direct City Search

```python
def search_clubs_by_city(client: FFBBAPIClientV2, city_name: str) -> List[OrganismesHit]:
    """
    Client function: client.search_organismes()
    Strategy: Search by city name in results

    Args:
        client: FFBBAPIClientV2 instance
        city_name: Name of the city to search clubs in

    Returns:
        List of clubs with their details in the specified city
    """

    # General search then filter by city
    result: OrganismesMultiSearchResult = client.search_organismes(city_name)

    city_clubs: List[OrganismesHit] = []
    for hit in result.hits:
        # Check if city is in club address or data
        club_details: GetOrganismeResponse = client.api_ffbb_client.get_organisme(int(hit.id))

        # Extract geographic information from club
        if club_details.adresse or club_details.commune:
            if city_name.lower() in str(club_details).lower():
                city_clubs.append(hit)

    return city_clubs
```

#### 2.2 Search by Department/Region

```python
def search_clubs_by_geo_zone(client: FFBBAPIClientV2, postal_code_prefix: str) -> List[OrganismesHit]:
    """
    Client function: client.search_organismes() then get_organisme()
    Discovery: Club IDs → geographic details

    Args:
        client: FFBBAPIClientV2 instance
        postal_code_prefix: Postal code prefix to filter by geographic zone

    Returns:
        List of clubs in the specified geographic zone
    """

    # Wide search then geographic filtering
    result: OrganismesMultiSearchResult = client.search_organismes("")  # Wide search

    zone_clubs: List[OrganismesHit] = []
    for hit in result.hits[:50]:  # Limit to avoid too many calls
        club_details: GetOrganismeResponse = client.api_ffbb_client.get_organisme(int(hit.id))

        # Analyze geographic data
        if club_details.cartographie or club_details.adresse:
            # Extract postal code/region from data
            if postal_code_prefix in str(club_details):
                zone_clubs.append(hit)

    return zone_clubs
```

### 3. Club Search by Geographic Radius

```python
def search_clubs_by_radius(client: FFBBAPIClientV2, center_city: str, radius_km: int) -> List[OrganismesHit]:
    """
    Client function: search_organismes() + get_organisme()
    Discovery: Clubs → coordinates → distance calculation

    Args:
        client: FFBBAPIClientV2 instance
        center_city: Reference city for the center of the search radius
        radius_km: Search radius in kilometers

    Returns:
        List of clubs within the specified radius, sorted by distance
    """

    import math

    def calculate_distance(lat1, lon1, lat2, lon2):
        """Calculate distance between two GPS points (haversine formula)"""
        R = 6371  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    # 1. Search reference club to get its coordinates
    center_club = search_club_by_name(client, center_city)
    if not center_club:
        return []

    center_details = client.api_ffbb_client.get_organisme(int(center_club.id))

    # Extract center coordinates (discovered via API)
    lat_center, lon_center = extract_coordinates(center_details)

    # 2. Search all clubs in the region
    region_clubs = search_clubs_by_geo_zone(client, center_city[:2])  # First 2 digits of postal code

    # 3. Filter by distance
    nearby_clubs = []
    for club_info in region_clubs:
        club_details = client.api_ffbb_client.get_organisme(int(club_info['club_id']))
        lat_club, lon_club = extract_coordinates(club_details)

        distance = calculate_distance(lat_center, lon_center, lat_club, lon_club)
        if distance <= radius_km:
            nearby_clubs.append({
                **club_info,
                'distance_km': round(distance, 2)
            })

    return sorted(nearby_clubs, key=lambda x: x['distance_km'])

def extract_coordinates(club_details: GetOrganismeResponse) -> Tuple[float, float]:
    """
    Extract lat/lon from club API data

    Args:
        club_details: Club details from GetOrganismeResponse

    Returns:
        Tuple of (latitude, longitude) coordinates
    """
    # Extract logic based on GetOrganismeResponse structure
    if club_details.cartographie:
        return club_details.cartographie.latitude, club_details.cartographie.longitude
    # Fallback or alternative methods based on exact structure
    return 0.0, 0.0
```

### 4. Club Search by Team Characteristics

#### 4.1 By Age Category

```python
def search_clubs_by_category(client: FFBBAPIClientV2, category: str) -> List[OrganismesHit]:
    """
    Client function: search_organismes() + get_organisme()
    Discovery: Clubs → teams → categories

    Args:
        client: FFBBAPIClientV2 instance
        category: Age category to search for (e.g., "senior", "u18")

    Returns:
        List of clubs that have teams in the specified category
    """

    # Wide club search
    result: OrganismesMultiSearchResult = client.search_organismes("")

    clubs_with_category: List[OrganismesHit] = []
    for hit in result.hits[:100]:  # Reasonable limit
        club_details: GetOrganismeResponse = client.api_ffbb_client.get_organisme(int(hit.id))

        # Analyze club teams
        if club_details.engagements:
            for team in club_details.engagements:
                if category.lower() in str(team).lower():
                    clubs_with_category.append(hit)
                    break  # Once found, move to next club

    return clubs_with_category
```

#### 4.2 By Competition Level

```python
def search_clubs_by_level(client: FFBBAPIClientV2, level: str) -> List[OrganismesHit]:
    """
    Client function: get_organisme() + get_competition()
    Discovery: Clubs → competitions → levels

    Args:
        client: FFBBAPIClientV2 instance
        level: Competition level to search for (e.g., "regional", "national")

    Returns:
        List of clubs participating in competitions at the specified level
    """

    # Search clubs then analyze their competitions
    result: OrganismesMultiSearchResult = client.search_organismes("")

    level_clubs: List[OrganismesHit] = []
    for hit in result.hits[:50]:
        club_details: GetOrganismeResponse = client.api_ffbb_client.get_organisme(int(hit.id))

        # Analyze club competitions
        if club_details.competitions:
            for comp in club_details.competitions:
                if isinstance(comp, dict):
                    comp_id = comp.get('id')
                else:
                    comp_id = str(comp) if comp else None

                if comp_id:
                    competition: GetCompetitionResponse = client.api_ffbb_client.get_competition(int(comp_id))

                    # Check competition level
                    if level.lower() in str(competition).lower():
                        level_clubs.append(hit)
                        break

    return level_clubs
```

---

## 🏀 USE CASES - TEAM SEARCH

### 1. Team Search by Name

```python
def search_team_by_name(client: FFBBAPIClientV2, team_name: str) -> Optional[GetOrganismeResponse.EngagementsitemModel]:
    """
    Client function: search_organismes() + get_organisme()
    Discovery: Club → teams → name match

    Args:
        client: FFBBAPIClientV2 instance
        team_name: Full name of the team to search for

    Returns:
        Team information dict or None if not found
    """

    # Extract club name from team name
    team_words = team_name.split()
    probable_club_name = " ".join(team_words[:-2])  # Remove category/level

    # 1. Find the club
    club = search_club_by_name(client, probable_club_name)
    if not club:
        return None

    # 2. Analyze club teams
    club_details: GetOrganismeResponse = client.api_ffbb_client.get_organisme(int(club.id))

    if club_details.engagements:
        for engagement in club_details.engagements:
            engagement_name = str(engagement)
            if team_name.lower() in engagement_name.lower():
                return engagement

    return None

# Example
team = search_team_by_name(client, "PELISSANNE BASKET AVENIR")
```

### 2. Team Search by Category and Gender

```python
def search_teams_by_category_gender(client: FFBBAPIClientV2, category: str, gender: str, city: Optional[str] = None) -> List[GetOrganismeResponse.EngagementsitemModel]:
    """
    Client function: get_organisme() for each club
    Discovery: Clubs → teams → filter category/gender

    Args:
        client: FFBBAPIClientV2 instance
        category: Team category (e.g., "senior", "u18")
        gender: Team gender (e.g., "male", "female")
        city: Optional city to limit search to specific location

    Returns:
        List of teams matching the category and gender criteria
    """

    # 1. Get club list (by city if specified)
    if city:
        clubs = search_clubs_by_city(client, city)
    else:
        result: OrganismesMultiSearchResult = client.search_organismes("")
        clubs = result.hits[:100]

    # 2. Analyze teams for each club
    matching_teams: List[GetOrganismeResponse.EngagementsitemModel] = []

    for club_hit in clubs:
        club_details: GetOrganismeResponse = client.api_ffbb_client.get_organisme(int(club_hit.id))

        if club_details.engagements:
            for engagement in club_details.engagements:
                engagement_name = str(engagement)

                # Check category and gender criteria
                if (category.lower() in engagement_name.lower() and
                    gender.lower() in engagement_name.lower()):

                    matching_teams.append(engagement)

    return matching_teams
```

### 3. Team Search by Geographic Zone

```python
def search_teams_geo_zone(client: FFBBAPIClientV2, zone: str, category: Optional[str] = None) -> List[GetOrganismeResponse.EngagementsitemModel]:
    """
    Client function: search_organismes() + get_organisme()
    Discovery: Zone → clubs → teams

    Args:
        client: FFBBAPIClientV2 instance
        zone: Geographic zone to search in
        category: Optional category filter for teams

    Returns:
        List of teams in the specified geographic zone
    """

    # 1. Find clubs in zone
    zone_clubs = search_clubs_by_city(client, zone)

    # 2. Extract all teams
    zone_teams: List[GetOrganismeResponse.EngagementsitemModel] = []

    for club_hit in zone_clubs:
        club_details: GetOrganismeResponse = client.api_ffbb_client.get_organisme(int(club_hit.id))

        if club_details.engagements:
            for engagement in club_details.engagements:
                engagement_name = str(engagement)

                # Filter by category if specified
                if not category or category.lower() in engagement_name.lower():
                    zone_teams.append(engagement)

    return zone_teams
```

---

## 🏆 USE CASES - RANKING SEARCH

### 1. Team Ranking - Current Season

```python
def get_team_current_ranking(client: FFBBAPIClientV2, team_name: str) -> Optional[Dict[str, Any]]:
    """
    Complete flow: Team → Club → Competitions → Poules → Ranking
    Client functions: search_organismes() + get_organisme() + get_competition() + get_poule()

    Args:
        client: FFBBAPIClientV2 instance
        team_name: Full name of the team to get ranking for

    Returns:
        Dict containing team ranking information or None if not found
    """

    # 1. Find team and its club
    team_info = search_team_by_name(client, team_name)
    if not team_info:
        return None

    # 2. Get club details and competitions - need to reconstruct from engagement
    team_engagement: GetOrganismeResponse.EngagementsitemModel = team_info
    club_details: GetOrganismeResponse = client.api_ffbb_client.get_organisme(int(team_engagement.idCompetition.id))

    # 3. Explore each competition to find the team
    for comp in club_details.competitions:
        if isinstance(comp, dict):
            comp_id = comp.get('id')
        else:
            comp_id = str(comp) if comp else None

        if not comp_id:
            continue

        # 4. Analyze the competition
        competition: GetCompetitionResponse = client.api_ffbb_client.get_competition(int(comp_id))

        # 5. Explore each phase and poule
        if competition.phases:
            for phase in competition.phases:
                if phase.poules:
                    for poule in phase.poules:
                        if not poule.id:
                            continue

                        # 6. Check if team is in this poule
                        poule_details: GetPouleResponse = client.api_ffbb_client.get_poule(int(poule.id))

                        # 7. Search for team in matches
                        team_found = False
                        if poule_details.rencontres:
                            for match in poule_details.rencontres:
                                if (team_name.lower() in match.nomEquipe1.lower() or
                                    team_name.lower() in match.nomEquipe2.lower()):
                                    team_found = True
                                    break

                        if team_found:
                            # 8. Calculate ranking from this poule
                            ranking = calculate_poule_ranking(poule_details.rencontres)

                            # 9. Find team position
                            position = find_team_position(ranking, team_name)

                            return {
                                'team': team_name,
                                'poule_id': poule.id,
                                'competition_id': comp_id,
                                'full_ranking': ranking,
                                'position': position,
                                'statistics': extract_team_stats(ranking, team_name)
                            }

    return None

# ⚠️ IMPORTANT NOTE ABOUT RANKINGS
#
# Rankings are normally returned directly by the FFBB API and should NOT be calculated manually.
# The API response contains a "classements" field with complete ranking information including:
# - position: Team position in ranking
# - points: Points earned
# - matchJoues: Matches played
# - gagnes: Wins
# - perdus: Losses
# - nombreForfaits: Forfeits
# - paniersMarques: Points scored
# - paniersEncaisses: Points conceded
# - difference: Goal average
# - quotient: Quotient
#
# The function below is provided as a fallback for cases where direct ranking data is not available,
# but the preferred approach is to use the official rankings from the API when possible.

def calculate_poule_ranking(matches: List[GetPouleResponse.RencontresitemModel]) -> List[Dict[str, Any]]:
    """
    Calculate ranking from poule matches

    Args:
        matches: List of match objects from poule

    Returns:
        List of team rankings sorted by points and goal difference
    """
    teams_stats = {}

    for match in matches:
        if not match.joue:
            continue

        team1 = match.nomEquipe1
        team2 = match.nomEquipe2
        score1 = int(match.resultatEquipe1) if match.resultatEquipe1 else 0
        score2 = int(match.resultatEquipe2) if match.resultatEquipe2 else 0

        # Initialize stats if necessary
        for team in [team1, team2]:
            if team not in teams_stats:
                teams_stats[team] = {
                    'points': 0, 'played': 0, 'won': 0, 'lost': 0,
                    'for': 0, 'against': 0, 'diff': 0
                }

        # Update statistics
        teams_stats[team1]['played'] += 1
        teams_stats[team2]['played'] += 1
        teams_stats[team1]['for'] += score1
        teams_stats[team1]['against'] += score2
        teams_stats[team2]['for'] += score2
        teams_stats[team2]['against'] += score1

        # Award points (2 pts win, 1 pt loss)
        if score1 > score2:
            teams_stats[team1]['points'] += 2
            teams_stats[team1]['won'] += 1
            teams_stats[team2]['points'] += 1
            teams_stats[team2]['lost'] += 1
        elif score2 > score1:
            teams_stats[team2]['points'] += 2
            teams_stats[team2]['won'] += 1
            teams_stats[team1]['points'] += 1
            teams_stats[team1]['lost'] += 1

    # Calculate difference
    for stats in teams_stats.values():
        stats['diff'] = stats['for'] - stats['against']

    # Sort by points then difference
    ranking = []
    for team, stats in teams_stats.items():
        ranking.append({'team': team, **stats})

    ranking.sort(key=lambda x: (x['points'], x['diff']), reverse=True)

    return ranking

def find_team_position(ranking: List[Dict[str, Any]], team_name: str) -> Optional[int]:
    """
    Find team position in ranking

    Args:
        ranking: List of team rankings
        team_name: Name of team to find position for

    Returns:
        Position number (1-indexed) or None if not found
    """
    for i, team_data in enumerate(ranking, 1):
        if team_name.lower() in team_data['team'].lower():
            return i
    return None

def extract_team_stats(ranking: List[Dict[str, Any]], team_name: str) -> Optional[Dict[str, Any]]:
    """
    Extract statistics for specific team

    Args:
        ranking: List of team rankings
        team_name: Name of team to extract stats for

    Returns:
        Team statistics dict or None if not found
    """
    for team_data in ranking:
        if team_name.lower() in team_data['team'].lower():
            return team_data
    return None
```

### 2. Team Ranking - Specific Season

```python
def get_team_season_ranking(client: FFBBAPIClientV2, team_name: str, season: str) -> Optional[Dict[str, Any]]:
    """
    Client functions: Same flow + filter by season
    Discovery: Team → season competitions → poules → ranking

    Args:
        client: FFBBAPIClientV2 instance
        team_name: Full name of the team
        season: Season identifier to search in

    Returns:
        Dict containing team ranking for specified season or None if not found
    """

    # 1. Get all available seasons
    seasons_response = client.api_ffbb_client.get_saisons()
    season_id = None

    # 2. Find requested season ID
    if seasons_response.saisons:
        for s in seasons_response.saisons:
            if season in str(s):
                season_id = s.id if s.id else None
                break

    if not season_id:
        return None

    # 3. Adapt search with season filter
    # (Use same functions as current season but with season_id filter)
    return get_team_ranking_with_season_filter(client, team_name, season_id)

def get_team_ranking_with_season_filter(client: FFBBAPIClientV2, team_name: str, season_id: str) -> Optional[Dict[str, Any]]:
    """
    Same logic as current season with season filter

    Args:
        client: FFBBAPIClientV2 instance
        team_name: Full name of the team
        season_id: Season ID to filter by

    Returns:
        Dict containing team ranking for the filtered season or None if not found
    """
    # Implementation similar to get_team_current_ranking
    # but with season_id verification in competitions
    pass
```

### 3. Rankings History - All Seasons

```python
def get_team_rankings_history(client: FFBBAPIClientV2, team_name: str) -> List[Dict[str, Any]]:
    """
    Client functions: get_saisons() + search for each season
    Discovery: All seasons → rankings per season

    Args:
        client: FFBBAPIClientV2 instance
        team_name: Full name of the team

    Returns:
        List of rankings across all seasons, sorted by season (newest first)
    """

    # 1. Get all seasons
    seasons_response = client.api_ffbb_client.get_saisons()

    history = []

    # 2. For each season, search for ranking
    if seasons_response.saisons:
        for season in seasons_response.saisons:
            season_name = season.nom if season.nom else str(season)
            season_id = season.id if season.id else None

            if season_id:
                season_ranking = get_team_ranking_with_season_filter(
                    client, team_name, season_id
                )

                if season_ranking:
                    history.append({
                        'season': season_name,
                        'season_id': season_id,
                        'position': season_ranking['position'],
                        'statistics': season_ranking['statistics']
                    })

    return sorted(history, key=lambda x: x['season'], reverse=True)
```

### 4. Complete Poule Ranking

```python
def get_complete_poule_ranking(client: FFBBAPIClientV2, competition_name: str, poule_name: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
    """
    Client functions: search_competitions() + get_competition() + get_poule()
    Discovery: Competition → phases → poules → ranking

    Args:
        client: FFBBAPIClientV2 instance
        competition_name: Name of the competition
        poule_name: Optional specific poule name to filter

    Returns:
        List of poule rankings or None if competition not found
    """

    # 1. Search for competition
    competitions_result = client.search_competitions(competition_name)
    if not competitions_result.hits:
        return None

    competition_id = competitions_result.hits[0].id

    # 2. Get competition details
    competition = client.api_ffbb_client.get_competition(int(competition_id))

    # 3. Explore phases and poules
    found_poules = []

    if competition.phases:
        for phase in competition.phases:
            if phase.poules:
                for poule in phase.poules:
                    poule_nom = poule.nom if poule.nom else ''

                    # Filter by poule name if specified
                    if not poule_name or poule_name.lower() in poule_nom.lower():
                        if poule.id:
                            # 4. Get ranking for this poule
                            poule_details = client.api_ffbb_client.get_poule(int(poule.id))
                            ranking = calculate_poule_ranking(poule_details.rencontres)

                            found_poules.append({
                                'poule_id': poule.id,
                                'poule_name': poule_nom,
                                'phase_name': phase.nom if phase.nom else 'Phase',
                                'competition_name': competition_name,
                                'ranking': ranking
                            })

    return found_poules
```

---

## 📊 UTILITY FUNCTIONS

### Ranking Display

```python
def display_ranking(ranking_data: Dict[str, Any]) -> None:
    """
    Formatted ranking display

    Args:
        ranking_data: Dict containing ranking information to display

    Returns:
        None (prints to console)
    """

    print(f"🏆 RANKING - {ranking_data.get('poule_name', 'Poule')}")
    print(f"Competition: {ranking_data.get('competition_name', 'N/A')}")
    print(f"Poule ID: {ranking_data.get('poule_id', 'N/A')} (discovered via API)")
    print("=" * 80)
    print(f"{'Pos':<4} {'Team':<35} {'Pts':<4} {'P':<3} {'W':<3} {'L':<3} {'For':<6} {'Ag':<7} {'Diff'}")
    print("-" * 80)

    for i, team_data in enumerate(ranking_data['ranking'], 1):
        marker = "👉" if i == ranking_data.get('position') else "  "
        print(f"{marker}{i:<4} {team_data['team']:<35} {team_data['points']:<4} "
              f"{team_data['played']:<3} {team_data['won']:<3} {team_data['lost']:<3} "
              f"{team_data['for']:<6} {team_data['against']:<7} {team_data['diff']:+d}")

    if 'position' in ranking_data:
        print(f"\n🎯 Position: {ranking_data['position']} of {len(ranking_data['ranking'])} teams")
```

### Error Handling and Validation

```python
def robust_search(func: callable, *args, **kwargs) -> Any:
    """
    Wrapper for robust error handling

    Args:
        func: Function to execute with error handling
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function

    Returns:
        Function result or None if error occurred
    """

    try:
        result = func(*args, **kwargs)
        if result:
            return result
        else:
            print(f"❌ No results found for {func.__name__}")
            return None

    except Exception as e:
        print(f"❌ Error in {func.__name__}: {str(e)}")
        return None
```

---

## 🎯 COMPLETE USAGE EXAMPLES

### Example 1: Pelissanne Ranking (Reference Case)

```python
# Initialize
client = FFBBAPIClientV2.create(
    meilisearch_bearer_token=os.getenv("MEILISEARCH_BEARER_TOKEN"),
    api_bearer_token=os.getenv("API_FFBB_APP_BEARER_TOKEN"),
    debug=True
)

# Search for Pelissanne ranking
pelissanne_ranking = get_team_current_ranking(client, "PELISSANNE BASKET AVENIR")

if pelissanne_ranking:
    display_ranking(pelissanne_ranking)
    # Result: Pelissanne 11th of 12 teams
```

### Example 2: City Clubs

```python
# Search all clubs in Marseille
marseille_clubs = search_clubs_by_city(client, "Marseille")

for club in marseille_clubs:
    print(f"Club: {club['nom']} (ID: {club['club_id']})")
```

### Example 3: Senior Male Teams in PACA

```python
# Search SM teams in PACA region
sm_paca_teams = search_teams_by_category_gender(
    client,
    category="senior",
    gender="male"
)

for team in sm_paca_teams[:10]:  # Top 10
    print(f"Team: {team['team_name']} - Club: {team['club_name']}")
```

---

## ✅ PROCESS VALIDATION

### Approach Advantages

1. **✅ Automatic discovery**: All IDs obtained via API
2. **✅ Reproducibility**: Works for any team/club
3. **✅ Complete encapsulation**: Only FFBBAPIClientV2 is used
4. **✅ Robustness**: Error handling and fuzzy search
5. **✅ Scalability**: Easy to add new search criteria

### Client Functions Used

| Use Case | Main Function | Secondary Functions |
|----------|---------------|---------------------|
| Club search | `client.search_organismes()` | `client.api_ffbb_client.get_organisme()` |
| Team search | `client.search_organismes()` | `client.api_ffbb_client.get_organisme()` |
| Team ranking | All previous | `get_competition()`, `get_poule()`, **⚠️ Missing: `get_ranking()`** |
| Rankings history | `client.api_ffbb_client.get_saisons()` | All previous |

---

## 🚀 EXTENSIBILITY

This framework can be extended for:

- **New search criteria**: Level, age, performance
- **Advanced analytics**: Ranking evolution, team comparisons
- **Data export**: CSV, JSON, reports
- **Real-time alerts**: New results notifications
- **User interface**: Web app, CLI, REST API

All additions will respect the fundamental principle: **exclusive use of FFBBAPIClientV2 client with automatic ID discovery**.

### 🔧 API Client Improvements Needed

The current implementation reveals that some functionality could be enhanced in the FFBBAPIClientV2:

1. **Direct Ranking API**: Add a `get_ranking(poule_id)` or `get_competition_ranking(competition_id, phase_id)` method that returns official rankings directly from the FFBB API, including:
   ```python
   def get_ranking(self, poule_id: int) -> List[RankingEntry]:
       """Get official ranking for a poule with complete statistics."""
   ```

2. **Ranking Data Model**: Create a `RankingEntry` model to handle the structured ranking data:
   ```python
   @dataclass
   class RankingEntry:
       position: int
       team_name: str
       points: int
       matches_played: int
       wins: int
       losses: int
       forfeits: int
       points_scored: int
       points_conceded: int
       goal_average: int
       quotient: float
   ```

3. **Enhanced Search**: Add more specific search filters for teams by level, age category, or geographical area.

These improvements would eliminate the need for manual ranking calculations and provide more robust access to official FFBB data.

## 📝 Complete Type Imports

For full type safety, include these imports at the top of your implementation files:

```python
from typing import Optional, List, Dict, Any, Tuple, Callable
from ffbb_api_client_v2 import FFBBAPIClientV2
from ffbb_api_client_v2.models.multi_search_result_organismes import (
    OrganismesMultiSearchResult,
    OrganismesHit
)
from ffbb_api_client_v2.models.organismes_models import GetOrganismeResponse
from ffbb_api_client_v2.models.competitions_models import GetCompetitionResponse
from ffbb_api_client_v2.models.poules_models import GetPouleResponse
from ffbb_api_client_v2.models.saisons_models import GetSaisonsResponse
```
