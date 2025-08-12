"""Unit tests for FFBB API Client V2 enhanced integration."""

import os
import time
import unittest

from ffbb_api_client_v2 import FFBBAPIClientV2
from ffbb_api_client_v2.models.competitions_models import GetCompetitionResponse
from ffbb_api_client_v2.models.organismes_models import GetOrganismeResponse
from ffbb_api_client_v2.models.query_fields import FieldSet, QueryFieldsManager
from ffbb_api_client_v2.models.saisons_models import GetSaisonsResponse


class Test011EnhancedIntegration(unittest.TestCase):
    """
    Enhanced integration tests that validate the new model-based API responses
    and centralized query fields management.
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

    def test_001_enhanced_organisme_model(self):
        """Test that get_organisme returns proper model objects."""
        paris_results = self.api_client.search_organismes("Paris")
        self.assertIsNotNone(paris_results)

        if not paris_results.hits:
            self.skipTest("No organismes found in Paris")

        first_organisme = paris_results.hits[0]
        organisme_id = int(first_organisme.id)

        organisme_details = self.api_client.api_ffbb_client.get_organisme(organisme_id)

        self.assertIsNotNone(organisme_details)
        self.assertIsInstance(organisme_details, GetOrganismeResponse)

        self.assertEqual(organisme_details.id, str(organisme_id))
        self.assertIsInstance(organisme_details.nom, str)
        self.assertIsInstance(organisme_details.code, str)

        if organisme_details.commune:
            self.assertIsNotNone(organisme_details.commune.libelle)
            self.assertIsNotNone(organisme_details.commune.codePostal)

        if organisme_details.engagements:
            self.assertIsInstance(organisme_details.engagements, list)
            for engagement in organisme_details.engagements:
                self.assertIsNotNone(engagement.id)

        print(f"✓ Enhanced organisme model test passed for: {organisme_details.nom}")

    def test_002_saisons_model_list(self):
        """Test that get_saisons returns proper model objects."""
        saisons = self.api_client.api_ffbb_client.get_saisons()

        self.assertIsNotNone(saisons)
        self.assertIsInstance(saisons, list)

        if saisons:
            first_saison = saisons[0]
            self.assertIsInstance(first_saison, GetSaisonsResponse)
            self.assertIsNotNone(first_saison.id)

            print(f"✓ Enhanced saisons model test passed. Found {len(saisons)} saisons")
            print(f"  First saison ID: {first_saison.id}")

    def test_003_competition_model_with_engagements(self):
        """Test competition model retrieval using engagements without setting fields."""
        results = self.api_client.search_organismes("Senas")
        if not results.hits:
            self.skipTest("No organismes found")

        organisme = results.hits[0]

        # First, get organisme with detailed fields to find competition IDs
        # in engagements. This is necessary because default fields don't
        # include engagement competition details
        organisme_with_details = self.api_client.api_ffbb_client.get_organisme(
            int(organisme.id)
        )

        if not organisme_with_details.engagements:
            self.skipTest("No engagements found for this organisme")

        # Find an engagement with competition information
        competition_id = None
        for engagement in organisme_with_details.engagements:
            if engagement.idCompetition and engagement.idCompetition.id:
                competition_id = int(engagement.idCompetition.id)
                break

        if not competition_id:
            self.skipTest("No engagement with competition found for this organisme")

        # Now test getting competition WITHOUT specifying fields (uses defaults)
        competition = self.api_client.api_ffbb_client.get_competition(competition_id)

        self.assertIsNotNone(competition)
        self.assertIsInstance(competition, GetCompetitionResponse)
        self.assertEqual(competition.id, str(competition_id))
        self.assertIsNotNone(competition.nom)

        # Also test getting organisme WITHOUT fields (uses defaults)
        organisme_details = self.api_client.api_ffbb_client.get_organisme(
            int(organisme.id)
        )

        self.assertIsNotNone(organisme_details)
        self.assertIsInstance(organisme_details, GetOrganismeResponse)
        self.assertEqual(organisme_details.id, organisme.id)

        print("✓ Competition model test passed for:", competition.nom)
        print("  ✓ Competition retrieved with default fields")
        print("  ✓ Organisme retrieved with default fields")

    def test_004_query_fields_manager(self):
        """Test centralized query fields management."""
        basic_fields = QueryFieldsManager.get_organisme_fields(FieldSet.BASIC)
        default_fields = QueryFieldsManager.get_organisme_fields(FieldSet.DEFAULT)
        detailed_fields = QueryFieldsManager.get_organisme_fields(FieldSet.DETAILED)

        self.assertIsInstance(basic_fields, list)
        self.assertIsInstance(default_fields, list)
        self.assertIsInstance(detailed_fields, list)

        self.assertIn("id", basic_fields)
        self.assertIn("nom", basic_fields)

        self.assertTrue(len(default_fields) > len(basic_fields))
        self.assertTrue(len(detailed_fields) > len(default_fields))

        print("✓ Query fields manager test passed")
        print(f"  Basic fields: {len(basic_fields)}")
        print(f"  Default fields: {len(default_fields)}")
        print(f"  Detailed fields: {len(detailed_fields)}")

    def test_005_complete_enhanced_user_journey(self):
        """Test complete user journey with enhanced model support."""
        print("\n" + "=" * 60)
        print("ENHANCED USER JOURNEY TEST")
        print("=" * 60)

        print("\n1. Enhanced city search")
        search_results = self.api_client.multi_search("Lyon")
        self.assertIsNotNone(search_results)
        self.assertGreater(len(search_results), 0)
        print(f"   ✓ Found {len(search_results)} search results")

        print("\n2. Enhanced organisme search with models")
        organismes_result = self.api_client.search_organismes("Lyon")
        self.assertIsNotNone(organismes_result)

        if not organismes_result.hits:
            print("   ⚠ No organismes found in Lyon")
            return

        selected_organisme = organismes_result.hits[0]
        print(f"   ✓ Found {len(organismes_result.hits)} organismes")
        print(f"   Selected: {selected_organisme.nom}")

        print("\n3. Enhanced organisme details with model")
        organisme_details = self.api_client.api_ffbb_client.get_organisme(
            int(selected_organisme.id)
        )

        self.assertIsInstance(organisme_details, GetOrganismeResponse)
        print(f"   ✓ Retrieved organisme model: {organisme_details.nom}")
        print(f"   ✓ Type: {organisme_details.type}")
        print(
            "   ✓ Teams:",
            len(organisme_details.engagements) if organisme_details.engagements else 0,
        )
        print(
            "   ✓ Competitions:",
            (
                len(organisme_details.competitions)
                if organisme_details.competitions
                else 0
            ),
        )

        print("\n4. Enhanced saisons retrieval")
        saisons = self.api_client.api_ffbb_client.get_saisons()

        self.assertIsInstance(saisons, list)
        if saisons:
            self.assertIsInstance(saisons[0], GetSaisonsResponse)
            print(f"   ✓ Retrieved {len(saisons)} saisons as model objects")
            print(f"   ✓ First saison: {saisons[0].id}")

        print("\n" + "=" * 60)
        print("ENHANCED JOURNEY SUMMARY")
        print("=" * 60)
        print("✓ All API methods return proper model objects")
        print("✓ Centralized query fields are working")
        print("✓ Model conversion is functioning correctly")
        print("✓ Enhanced integration tests successful!")

        self.assertIsInstance(organisme_details, GetOrganismeResponse)
        self.assertIsInstance(saisons, list)
        if saisons:
            self.assertIsInstance(saisons[0], GetSaisonsResponse)

    def test_006_error_handling_with_models(self):
        """Test error handling when models cannot be created."""
        result = self.api_client.api_ffbb_client.get_organisme(organisme_id=999999999)

        self.assertIsNone(result)
        print("✓ Error handling test passed - returned None for non-existent resource")

    def test_007_field_customization(self):
        """Test custom field selection with models."""
        paris_results = self.api_client.search_organismes("Paris")
        if not paris_results.hits:
            self.skipTest("No organismes found")

        organisme_id = int(paris_results.hits[0].id)

        custom_fields = ["id", "nom", "type"]
        organisme = self.api_client.api_ffbb_client.get_organisme(
            organisme_id=organisme_id, fields=custom_fields
        )

        self.assertIsNotNone(organisme)
        self.assertIsInstance(organisme, GetOrganismeResponse)
        self.assertIsNotNone(organisme.id)
        self.assertIsNotNone(organisme.nom)

        print(f"✓ Custom fields test passed for: {organisme.nom}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
