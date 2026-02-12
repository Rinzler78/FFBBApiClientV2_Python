import os
import unittest

from dotenv import load_dotenv

from ffbb_api_client_v2 import ApiFFBBAppClient


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

    def test_000_lives(self):
        result = self.api_client.get_lives()
        self.assertIsNotNone(result)

    def test_001_get_saisons(self):
        result = self.api_client.get_saisons()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)

    def test_002_get_organisme(self):
        organisme_id = 12186  # SENAS BASKET BALL
        result = self.api_client.get_organisme(organisme_id)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, str(organisme_id))

    def _get_valid_competition_id(self) -> int:
        """Helper method to get a valid competition ID dynamically."""
        competitions = self.api_client.list_competitions(limit=1)
        self.assertIsNotNone(competitions)
        self.assertGreater(len(competitions), 0, "No competitions found")
        return int(competitions[0].id)

    def test_003_list_competitions(self):
        result = self.api_client.list_competitions(limit=5)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_004_get_competition(self):
        competition_id = self._get_valid_competition_id()
        result = self.api_client.get_competition(competition_id)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, str(competition_id))
        self.assertIsNotNone(result.phases)

    def test_005_get_poule(self):
        poule_id = 200000002967008
        result = self.api_client.get_poule(poule_id)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, str(poule_id))
        self.assertIsNotNone(result.rencontres)

    def test_006_get_saisons_with_detailed_field_set(self):
        from ffbb_api_client_v2.models.field_set import FieldSet

        result = self.api_client.get_saisons(field_set=FieldSet.DETAILED)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        if result:
            first_item = result[0]
            self.assertIsNotNone(first_item.id)

    def test_007_get_competition_with_basic_field_set(self):
        from ffbb_api_client_v2.models.field_set import FieldSet

        competition_id = self._get_valid_competition_id()
        result = self.api_client.get_competition(
            competition_id, field_set=FieldSet.BASIC
        )
        self.assertIsNotNone(result)
        self.assertEqual(result.id, str(competition_id))
        self.assertIsNotNone(result.nom)
