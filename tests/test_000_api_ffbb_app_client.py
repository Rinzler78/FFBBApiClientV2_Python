import os
import unittest

from dotenv import load_dotenv

from ffbb_api_client_v2 import ApiFFBBAppClient


class Test000ApiFfbbAppClient(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        # NOTE: Set debug=True for detailed logging if needed during debugging
        self.api_client = ApiFFBBAppClient(
            bearer_token=os.getenv("API_FFBB_APP_BEARER_TOKEN"),
            debug=False,
        )

    def setup_method(self, method):
        self.setUp()

    def test_lives(self):
        result = self.api_client.get_lives()
        self.assertIsNotNone(result)

    def test_get_saisons(self):
        result = self.api_client.get_saisons()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)

    def test_get_organisme(self):
        organisme_id = 12186  # SENAS BASKET BALL
        result = self.api_client.get_organisme(organisme_id)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, str(organisme_id))

    def test_get_competition(self):
        competition_id = 200000002845137  # Régionale féminine seniors - Division 2
        result = self.api_client.get_competition(competition_id)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, str(competition_id))
        self.assertIsNotNone(result.phases)

    def test_get_poule(self):
        poule_id = 200000002967008
        result = self.api_client.get_poule(poule_id)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, str(poule_id))
        self.assertIsNotNone(result.rencontres)

    def test_get_saisons_with_custom_fields(self):
        fields = ["id", "libelle", "code"]
        result = self.api_client.get_saisons(fields=fields)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        if result:
            first_item = result[0]
            self.assertIsNotNone(first_item.id)

    def test_get_competition_with_custom_fields(self):
        competition_id = 200000002845137
        fields = ["id", "nom", "sexe", "saison"]
        result = self.api_client.get_competition(competition_id, fields=fields)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, str(competition_id))
        self.assertIsNotNone(result.nom)
        self.assertIsNotNone(result.sexe)
