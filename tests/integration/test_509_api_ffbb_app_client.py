import os
import unittest

from dotenv import load_dotenv

from ffbb_api_client_v2 import ApiFFBBAppClient
from ffbb_api_client_v2.directus.exceptions import DirectusAuthError


class Test000ApiFfbbAppClient(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        api_token = os.getenv("API_FFBB_APP_BEARER_TOKEN")
        if not api_token:
            self.skipTest("API_FFBB_APP_BEARER_TOKEN environment variable not set")

        # NOTE: Set debug=True for detailed logging if needed during debugging
        self.api_client = ApiFFBBAppClient(
            bearer_token=api_token,
            debug=False,
        )

    def setup_method(self, method):
        self.setUp()

    def _skip_if_auth_error(self, func, *args, **kwargs):
        """Call func and skip test if auth/permission error occurs."""
        try:
            return func(*args, **kwargs)
        except DirectusAuthError:
            self.skipTest("API token expired or insufficient permissions")

    def test_000_lives(self):
        result = self._skip_if_auth_error(self.api_client.get_lives)
        self.assertIsNotNone(result)

    def test_001_get_saisons(self):
        result = self._skip_if_auth_error(self.api_client.get_saisons)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)

    def test_002_get_organisme(self):
        organisme_id = 12186  # SENAS BASKET BALL
        result = self._skip_if_auth_error(self.api_client.get_organisme, organisme_id)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, str(organisme_id))

    def _get_valid_competition_id(self) -> int:
        """Helper method to get a valid competition ID dynamically."""
        competitions = self._skip_if_auth_error(
            self.api_client.list_competitions, limit=1
        )
        self.assertIsNotNone(competitions)
        self.assertGreater(len(competitions), 0, "No competitions found")
        return int(competitions[0].id)

    def _get_valid_poule_id(self) -> int:
        """Helper method to get a valid poule ID dynamically from a competition."""
        competition_id = self._get_valid_competition_id()
        competition = self._skip_if_auth_error(
            self.api_client.get_competition, competition_id
        )
        self.assertIsNotNone(competition)
        self.assertIsNotNone(competition.poules, "Competition has no poules")
        self.assertGreater(len(competition.poules), 0, "Competition poules list empty")
        return int(competition.poules[0])

    def test_003_list_competitions(self):
        result = self._skip_if_auth_error(self.api_client.list_competitions, limit=5)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_004_get_competition(self):
        competition_id = self._get_valid_competition_id()
        result = self._skip_if_auth_error(
            self.api_client.get_competition, competition_id
        )
        self.assertIsNotNone(result)
        self.assertEqual(result.id, str(competition_id))
        self.assertIsNotNone(result.phases)

    def test_005_get_poule(self):
        poule_id = self._get_valid_poule_id()
        result = self._skip_if_auth_error(self.api_client.get_poule, poule_id)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, str(poule_id))
        self.assertIsNotNone(result.rencontres)

    def test_006_get_saisons_with_detailed_field_set(self):
        result = self._skip_if_auth_error(self.api_client.get_saisons)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        if result:
            first_item = result[0]
            self.assertIsNotNone(first_item.id)

    def test_007_get_competition_with_basic_field_set(self):
        competition_id = self._get_valid_competition_id()
        result = self._skip_if_auth_error(
            self.api_client.get_competition, competition_id
        )
        self.assertIsNotNone(result)
        self.assertEqual(result.id, str(competition_id))
        self.assertIsNotNone(result.nom)
