"""Unit tests for FFBB API Client V2 integration user journey."""

import os
import time
import unittest

from ffbb_api_client_v2 import (
    FFBBAPIClientV2,
    OrganismesHit,
    OrganismesMultiSearchResult,
)
from ffbb_api_client_v2.models.competitions_models import GetCompetitionResponse
from ffbb_api_client_v2.models.organismes_models import GetOrganismeResponse


class Test010UserJourneyIntegration(unittest.TestCase):
    """
    Integration tests that follow real user journeys:
    1. Search for a city
    2. Find clubs in the city
    3. Get teams for a club
    4. Get season calendar for a team
    """

    @classmethod
    def setUpClass(cls):
        """Set up the API client for all tests."""
        api_token = os.getenv("API_FFBB_APP_BEARER_TOKEN")
        if not api_token:
            raise Exception("API_FFBB_APP_BEARER_TOKEN environment variable not set")

        mls_token = os.getenv("MEILISEARCH_BEARER_TOKEN")
        if not mls_token:
            raise Exception("MEILISEARCH_BEARER_TOKEN environment variable not set")

        # NOTE: Set debug=True for detailed logging if needed during debugging
        cls.api_client = FFBBAPIClientV2.create(
            meilisearch_bearer_token=mls_token,
            api_bearer_token=api_token,
            debug=False,
        )

    def setUp(self):
        """Set up each test with a delay to respect API rate limits."""
        time.sleep(0.5)

    def test_001_search_for_city(self):
        """Test Step 1: Search for a city (Paris)."""
        city_name = "Paris"

        search_results = self.api_client.multi_search(city_name)

        self.assertIsNotNone(
            search_results, f"No search results found for city: {city_name}"
        )
        self.assertGreater(
            len(search_results), 0, f"Empty search results for city: {city_name}"
        )

        print(
            f"✓ Successfully found {len(search_results)} search results for city: {city_name}"
        )

    def test_002_find_clubs_in_city(self):
        """Test Step 2: Find clubs in a specific city."""
        city_name = "Paris"

        organismes_result = self.api_client.search_organismes(city_name)

        self.assertIsNotNone(
            organismes_result, f"No organismes found for city: {city_name}"
        )
        self.assertIsInstance(organismes_result, OrganismesMultiSearchResult)

        if organismes_result.hits:
            self.assertGreater(
                len(organismes_result.hits),
                0,
                f"No club hits found for city: {city_name}",
            )

            first_club = organismes_result.hits[0]
            self.assertIsInstance(first_club, OrganismesHit)
            self.assertIsNotNone(first_club.id, "Club should have an ID")
            self.assertIsNotNone(first_club.nom, "Club should have a name")

            print(
                f"✓ Successfully found {len(organismes_result.hits)} clubs in {city_name}"
            )
            print(f"  First club: {first_club.nom} (ID: {first_club.id})")
        else:
            print(f"⚠ No club hits found for city: {city_name}")

    def test_003_get_teams_for_club(self):
        """Test Step 3: Get teams (engagements) for a specific club."""
        city_name = "Paris"

        organismes_result = self.api_client.search_organismes(city_name)
        self.assertIsNotNone(
            organismes_result, f"No organismes found for city: {city_name}"
        )

        if not organismes_result.hits:
            self.skipTest(f"No clubs found in {city_name} to test team retrieval")

        first_club = organismes_result.hits[0]
        club_id = int(first_club.id)

        club_details = self.api_client.api_ffbb_client.get_organisme(
            organisme_id=club_id
        )

        self.assertIsNotNone(club_details, f"No details found for club ID: {club_id}")
        self.assertIsInstance(club_details, GetOrganismeResponse)
        self.assertEqual(club_details.id, str(club_id), "Club ID should match")

        engagements = club_details.engagements if club_details.engagements else []
        if engagements:
            self.assertIsInstance(engagements, list, "Engagements should be a list")
            self.assertGreater(
                len(engagements), 0, f"Club {first_club.nom} should have teams"
            )

            first_team = engagements[0]
            self.assertIsNotNone(first_team.id, "Team should have an ID")

            print(
                f"✓ Successfully found {len(engagements)} teams for club: {first_club.nom}"
            )
            print(f"  First team ID: {first_team.id}")
        else:
            print(f"⚠ No teams found for club: {first_club.nom}")

    def test_004_get_season_calendar_for_team(self):
        """Test Step 4: Get season calendar for a specific team."""
        city_name = "Paris"

        organismes_result = self.api_client.search_organismes(city_name)
        self.assertIsNotNone(organismes_result)

        if not organismes_result.hits:
            self.skipTest(f"No clubs found in {city_name} to test calendar retrieval")

        first_club = organismes_result.hits[0]
        club_id = int(first_club.id)
        club_details = self.api_client.api_ffbb_client.get_organisme(
            organisme_id=club_id
        )

        engagements = club_details.engagements if club_details.engagements else []
        if not engagements:
            self.skipTest(
                f"No teams found for club {first_club.nom} to test calendar retrieval"
            )

        competitions = club_details.competitions if club_details.competitions else []
        if not competitions:
            self.skipTest(f"No competitions found for club {first_club.nom}")

        first_competition = competitions[0]
        competition_id = int(
            first_competition.get("id")
            if isinstance(first_competition, dict)
            else first_competition
        )

        competition_details = self.api_client.api_ffbb_client.get_competition(
            competition_id=competition_id
        )

        self.assertIsNotNone(
            competition_details,
            f"No details found for competition ID: {competition_id}",
        )
        self.assertIsInstance(competition_details, GetCompetitionResponse)

        phases = competition_details.phases if competition_details.phases else []
        if phases:
            self.assertIsInstance(phases, list)

            print(
                f"✓ Successfully retrieved competition details for: {competition_details.nom}"
            )
            print(f"  Competition ID: {competition_details.id}")
            print(f"  Competition type: {competition_details.typeCompetition}")
        else:
            print(f"⚠ No phases found for competition: {competition_details.nom}")

    def test_005_complete_user_journey(self):
        """Test the complete user journey from city search to calendar retrieval."""
        print("\n" + "=" * 60)
        print("COMPLETE USER JOURNEY TEST")
        print("=" * 60)

        journey_data = {}

        print("\n1. Searching for city: 'Paris'")
        city_name = "Paris"
        search_results = self.api_client.multi_search(city_name)
        self.assertIsNotNone(search_results)
        journey_data["city_search_results"] = len(search_results)
        print(f"   ✓ Found {len(search_results)} search results")

        print("\n2. Finding clubs in the city")
        organismes_result = self.api_client.search_organismes(city_name)
        self.assertIsNotNone(organismes_result)

        if not organismes_result.hits:
            self.skipTest("No clubs found to continue the journey")

        journey_data["clubs_found"] = len(organismes_result.hits)
        selected_club = organismes_result.hits[0]
        print(f"   ✓ Found {len(organismes_result.hits)} clubs")
        print(f"   Selected club: {selected_club.nom} (ID: {selected_club.id})")

        print("\n3. Getting teams for the selected club")
        club_id = int(selected_club.id)
        club_details = self.api_client.api_ffbb_client.get_organisme(
            organisme_id=club_id
        )
        self.assertIsNotNone(club_details)

        engagements = club_details.engagements if club_details.engagements else []
        competitions = club_details.competitions if club_details.competitions else []
        journey_data["teams_found"] = len(engagements)
        journey_data["competitions_found"] = len(competitions)

        print(f"   ✓ Found {len(engagements)} teams")
        print(f"   ✓ Found {len(competitions)} competitions")

        if not competitions:
            print("   ⚠ No competitions found, cannot retrieve calendar")
            return

        print("\n4. Getting season calendar")
        first_competition = competitions[0]
        competition_id = int(
            first_competition.get("id")
            if isinstance(first_competition, dict)
            else first_competition
        )
        print(
            f"   Selected competition: {first_competition.get('nom') if isinstance(first_competition, dict) else 'Unknown'} (ID: {competition_id})"
        )

        competition_details = self.api_client.api_ffbb_client.get_competition(
            competition_id=competition_id
        )
        self.assertIsNotNone(competition_details)

        journey_data["calendar_matches"] = 0  # Simplified
        print(f"   ✓ Retrieved competition details: {competition_details.nom}")

        print("\n" + "=" * 60)
        print("JOURNEY SUMMARY")
        print("=" * 60)
        print(f"City searched: {city_name}")
        print(f"Search results: {journey_data['city_search_results']}")
        print(f"Clubs found: {journey_data['clubs_found']}")
        print(f"Selected club: {selected_club.nom}")
        print(f"Teams in club: {journey_data['teams_found']}")
        print(f"Competitions in club: {journey_data['competitions_found']}")
        print("✓ Complete user journey successful!")

        self.assertGreater(
            journey_data["city_search_results"], 0, "Should find city search results"
        )
        self.assertGreater(journey_data["clubs_found"], 0, "Should find clubs")
        self.assertGreater(
            journey_data["competitions_found"], 0, "Should find competitions"
        )

    def test_006_error_handling_journey(self):
        """Test user journey with error conditions."""
        print("\n" + "=" * 60)
        print("ERROR HANDLING JOURNEY TEST")
        print("=" * 60)

        print("\n1. Testing with non-existent city")
        fake_city = "NonExistentCityName12345"
        search_results = self.api_client.multi_search(fake_city)

        if search_results:
            print(
                f"   Found {len(search_results)} results for fake city (expected few/none)"
            )
        else:
            print("   ✓ No results for non-existent city (expected)")

        print("\n2. Testing with empty search")
        empty_results = self.api_client.search_organismes("")
        self.assertIsNotNone(
            empty_results, "Should return a result object even for empty search"
        )
        print("   ✓ Empty search handled gracefully")

        print("\n3. Testing with None search")
        none_results = self.api_client.search_organismes(None)
        self.assertIsNotNone(
            none_results, "Should return a result object even for None search"
        )
        print("   ✓ None search handled gracefully")

    def test_007_multiple_cities_comparison(self):
        """Test searching and comparing multiple cities."""
        cities = ["Paris", "Lyon", "Marseille"]
        city_data = {}

        print("\n" + "=" * 60)
        print("MULTIPLE CITIES COMPARISON TEST")
        print("=" * 60)

        for city in cities:
            print(f"\nAnalyzing city: {city}")

            organismes_result = self.api_client.search_organismes(city)
            self.assertIsNotNone(organismes_result)

            clubs_count = len(organismes_result.hits) if organismes_result.hits else 0
            city_data[city] = {"clubs_count": clubs_count, "clubs": []}

            if organismes_result.hits:
                for i, club in enumerate(organismes_result.hits[:3]):
                    try:
                        club_details = self.api_client.api_ffbb_client.get_organisme(
                            organisme_id=int(club.id)
                        )
                        teams_count = (
                            len(club_details.engagements)
                            if club_details.engagements
                            else 0
                        )
                        competitions_count = (
                            len(club_details.competitions)
                            if club_details.competitions
                            else 0
                        )

                        city_data[city]["clubs"].append(
                            {
                                "name": club.nom,
                                "id": club.id,
                                "teams": teams_count,
                                "competitions": competitions_count,
                            }
                        )

                    except Exception as e:
                        print(
                            f"   Warning: Could not get details for club {club.nom}: {e}"
                        )
                        continue

            print(f"   ✓ Found {clubs_count} clubs")
            if city_data[city]["clubs"]:
                print(f"   Analyzed {len(city_data[city]['clubs'])} club details")

        print("\n" + "=" * 60)
        print("CITIES COMPARISON SUMMARY")
        print("=" * 60)

        for city, data in city_data.items():
            print(f"\n{city}:")
            print(f"  Total clubs: {data['clubs_count']}")

            if data["clubs"]:
                total_teams = sum(club["teams"] for club in data["clubs"])
                total_competitions = sum(club["competitions"] for club in data["clubs"])
                print(f"  Sample teams: {total_teams}")
                print(f"  Sample competitions: {total_competitions}")

                for club in data["clubs"][:2]:
                    print(
                        f"    - {club['name']}: {club['teams']} teams, {club['competitions']} competitions"
                    )

        total_clubs_found = sum(data["clubs_count"] for data in city_data.values())
        self.assertGreater(
            total_clubs_found, 0, "Should find clubs in at least one city"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
