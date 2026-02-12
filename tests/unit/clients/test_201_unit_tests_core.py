"""Unit tests for FFBB API Client V2 core components."""

import unittest
from unittest.mock import Mock, patch

from requests_cache import CachedSession

from ffbb_api_client_v2 import FFBBAPIClientV2
from ffbb_api_client_v2.clients.api_ffbb_app_client import ApiFFBBAppClient
from ffbb_api_client_v2.clients.meilisearch_ffbb_client import MeilisearchFFBBClient


class Test001FfbbApiClientV2Core(unittest.TestCase):
    """Unit tests for the FFBB API Client V2 core module."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_api_client = Mock(spec=ApiFFBBAppClient)
        self.mock_meilisearch_client = Mock(spec=MeilisearchFFBBClient)
        self.client = FFBBAPIClientV2(
            api_ffbb_client=self.mock_api_client,
            meilisearch_ffbb_client=self.mock_meilisearch_client,
        )

    def test_000_init_with_valid_clients(self):
        """Test that client initializes correctly with valid clients."""
        self.assertIsNotNone(self.client)
        self.assertEqual(self.client.api_ffbb_client, self.mock_api_client)
        self.assertEqual(
            self.client.meilisearch_ffbb_client, self.mock_meilisearch_client
        )

    def test_001_create_factory_method_success(self):
        """Test factory method creates client successfully."""
        with patch(
            "ffbb_api_client_v2.clients.ffbb_api_client_v2.ApiFFBBAppClient"
        ) as mock_api_cls, patch(
            "ffbb_api_client_v2.clients.ffbb_api_client_v2.MeilisearchFFBBClient"
        ) as mock_ms_cls:

            mock_api_instance = Mock()
            mock_ms_instance = Mock()
            mock_api_cls.return_value = mock_api_instance
            mock_ms_cls.return_value = mock_ms_instance

            client = FFBBAPIClientV2.create(
                meilisearch_bearer_token="test_ms_token",
                api_bearer_token="test_api_token",
            )

            self.assertIsNotNone(client)
            mock_api_cls.assert_called_once()
            mock_ms_cls.assert_called_once()

    def test_002_create_factory_method_empty_api_token(self):
        """Test factory method raises error with empty API token."""
        with self.assertRaises(ValueError) as context:
            FFBBAPIClientV2.create(
                meilisearch_bearer_token="test_ms_token", api_bearer_token=""
            )
        self.assertIn(
            "api_bearer_token cannot be empty or whitespace-only",
            str(context.exception),
        )

    def test_003_create_factory_method_empty_meilisearch_token(self):
        """Test factory method raises error with empty Meilisearch token."""
        with self.assertRaises(ValueError) as context:
            FFBBAPIClientV2.create(
                meilisearch_bearer_token="",
                api_bearer_token="test_api_token_valid_length",
            )
        self.assertIn(
            "meilisearch_bearer_token cannot be empty or whitespace-only",
            str(context.exception),
        )

    def test_004_get_lives_delegates_to_api_client(self):
        """Test get_lives delegates correctly to API client."""
        mock_lives = ["mock_live_data"]
        self.mock_api_client.get_lives.return_value = mock_lives

        result = self.client.get_lives()

        self.mock_api_client.get_lives.assert_called_once_with(None)
        self.assertEqual(result, mock_lives)

    def test_005_multi_search_with_name(self):
        """Test multi_search with valid name parameter."""
        with patch(
            "ffbb_api_client_v2.clients.ffbb_api_client_v2.generate_queries"
        ) as mock_gen_queries:
            mock_queries = ["query1", "query2"]
            mock_gen_queries.return_value = mock_queries

            mock_result = Mock()
            mock_result.results = ["result1", "result2"]
            self.mock_meilisearch_client.recursive_smart_multi_search.return_value = (
                mock_result
            )

            result = self.client.multi_search("Paris")

            mock_gen_queries.assert_called_once_with("Paris")
            mock_call = self.mock_meilisearch_client.recursive_smart_multi_search
            mock_call.assert_called_once_with(mock_queries, cached_session=None)
            self.assertEqual(result, ["result1", "result2"])

    def test_006_multi_search_no_results(self):
        """Test multi_search returns None when no results found."""
        with patch(
            "ffbb_api_client_v2.clients.ffbb_api_client_v2.generate_queries"
        ) as mock_gen_queries:
            mock_gen_queries.return_value = ["query"]
            self.mock_meilisearch_client.recursive_smart_multi_search.return_value = (
                None
            )

            result = self.client.multi_search("NonExistent")

            self.assertIsNone(result)

    def test_007_search_organismes_with_name(self):
        """Test search_organismes with valid name parameter."""
        with patch.object(
            self.client, "search_multiple_organismes"
        ) as mock_search_multiple:
            mock_result = Mock()
            mock_search_multiple.return_value = [mock_result]

            result = self.client.search_organismes("Paris")

            mock_search_multiple.assert_called_once_with(
                ["Paris"],
                filter=None,
                sort=None,
                limit=10,
                cached_session=None,
            )
            self.assertEqual(result, mock_result)

    def test_008_search_organismes_no_results(self):
        """Test search_organismes returns None when no results found."""
        with patch.object(
            self.client, "search_multiple_organismes"
        ) as mock_search_multiple:
            mock_search_multiple.return_value = None

            result = self.client.search_organismes("NonExistent")

            self.assertIsNone(result)

    def test_009_search_multiple_organismes_empty_names(self):
        """Test search_multiple_organismes returns None for empty names."""
        result = self.client.search_multiple_organismes(None)
        self.assertIsNone(result)

    def test_010_search_multiple_organismes_with_names(self):
        """Test search_multiple_organismes with valid names list."""
        mock_result = Mock()
        mock_result.results = ["result1", "result2"]
        self.mock_meilisearch_client.recursive_smart_multi_search.return_value = (
            mock_result
        )

        result = self.client.search_multiple_organismes(["Paris", "Lyon"])

        self.assertEqual(result, ["result1", "result2"])

    def test_011_cached_session_parameter_propagation(self):
        """Test cached_session parameter is propagated correctly."""
        custom_session = Mock(spec=CachedSession)

        self.client.get_lives(cached_session=custom_session)

        self.mock_api_client.get_lives.assert_called_once_with(custom_session)


class Test001ApiFfbbAppCore(unittest.TestCase):
    """Unit tests for the API FFBB App Client module."""

    def setUp(self):
        """Set up test fixtures."""
        self.bearer_token = "test_token"
        # NOTE: Set debug=True for detailed logging if needed during debugging
        self.client = ApiFFBBAppClient(bearer_token=self.bearer_token, debug=False)

    def test_012_init_with_valid_token(self):
        """Test client initializes correctly with valid token."""
        self.assertEqual(self.client.bearer_token, self.bearer_token)
        self.assertEqual(self.client.url, "https://api.ffbb.app/")
        self.assertFalse(self.client.debug)
        self.assertEqual(
            self.client.headers,
            {
                "Authorization": f"Bearer {self.bearer_token}",
                "user-agent": "okhttp/4.12.0",
            },
        )

    def test_013_init_with_empty_token(self):
        """Test client raises error with empty token."""
        with self.assertRaises(ValueError) as context:
            ApiFFBBAppClient(bearer_token="")
        self.assertIn(
            "bearer_token cannot be None, empty, or whitespace-only",
            str(context.exception),
        )

    def test_014_init_with_none_token(self):
        """Test client raises error with None token."""
        with self.assertRaises(ValueError) as context:
            ApiFFBBAppClient(bearer_token=None)
        self.assertIn("bearer_token cannot be None", str(context.exception))

    def test_015_init_with_custom_url(self):
        """Test client initializes with custom URL."""
        custom_url = "https://custom.api.url/"
        client = ApiFFBBAppClient(bearer_token=self.bearer_token, url=custom_url)
        self.assertEqual(client.url, custom_url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.lives_from_dict")
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_016_get_lives_success(self, mock_http_get, mock_lives_from_dict):
        """Test get_lives returns live data successfully."""
        mock_data = {"lives": [{"id": "1", "team1": "A", "team2": "B"}]}
        mock_http_get.return_value = mock_data
        mock_lives = ["mock_live_object"]
        mock_lives_from_dict.return_value = mock_lives

        result = self.client.get_lives()

        mock_http_get.assert_called_once()
        mock_lives_from_dict.assert_called_once_with(mock_data)
        self.assertEqual(result, mock_lives)

    @patch(
        "ffbb_api_client_v2.models.get_competition_response.GetCompetitionResponse.from_dict"
    )
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_017_get_competition_success(self, mock_http_get, mock_from_dict):
        """Test get_competition returns competition model with default fields."""
        mock_inner_data = {"id": 123, "nom": "Test Competition"}
        mock_data = {"data": mock_inner_data}  # Wrap in API response structure
        mock_http_get.return_value = mock_data

        mock_competition_obj = Mock()
        mock_from_dict.return_value = mock_competition_obj

        # Test without fields (should use defaults)
        result = self.client.get_competition(competition_id=123)

        mock_http_get.assert_called_once()
        # Verify that default fields are used in the URL
        call_args = mock_http_get.call_args
        self.assertIn("fields%5B%5D", call_args[0][0])  # URL should contain fields[]
        mock_from_dict.assert_called_once_with(mock_inner_data)
        self.assertEqual(result, mock_competition_obj)

    @patch(
        "ffbb_api_client_v2.models.get_competition_response.GetCompetitionResponse.from_dict"
    )
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_018_006b_get_competition_with_basic_field_set(
        self, mock_http_get, mock_from_dict
    ):
        """Test get_competition with BASIC field_set."""
        mock_inner_data = {"id": 123, "nom": "Test Competition", "sexe": "M"}
        mock_data = {"data": mock_inner_data}
        mock_http_get.return_value = mock_data

        mock_competition_obj = Mock()
        mock_from_dict.return_value = mock_competition_obj

        from ffbb_api_client_v2.models.field_set import FieldSet
        from ffbb_api_client_v2.models.query_fields_manager import QueryFieldsManager

        basic_fields = QueryFieldsManager.get_competition_fields(FieldSet.BASIC)
        result = self.client.get_competition(
            competition_id=123, field_set=FieldSet.BASIC
        )

        mock_http_get.assert_called_once()
        # Verify that basic fields are in the URL
        call_args = mock_http_get.call_args
        url = call_args[0][0]
        for field in basic_fields:
            self.assertIn(field.replace("[", "%5B").replace("]", "%5D"), url)
        mock_from_dict.assert_called_once_with(mock_inner_data)
        self.assertEqual(result, mock_competition_obj)

    @patch("ffbb_api_client_v2.models.poules_models.GetPouleResponse.from_dict")
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_019_get_poule_with_default_fields(self, mock_http_get, mock_from_dict):
        """Test get_poule without fields uses default fields."""
        mock_inner_data = {"id": 456, "nom": "Test Poule"}
        mock_data = {"data": mock_inner_data}
        mock_http_get.return_value = mock_data

        mock_poule_obj = Mock()
        mock_from_dict.return_value = mock_poule_obj

        # Test without fields (should use defaults)
        result = self.client.get_poule(poule_id=456)

        mock_http_get.assert_called_once()
        # Verify that fields are in the URL
        call_args = mock_http_get.call_args
        self.assertIn("fields%5B%5D", call_args[0][0])
        mock_from_dict.assert_called_once_with(mock_inner_data)
        self.assertEqual(result, mock_poule_obj)

    @patch("ffbb_api_client_v2.models.poules_models.GetPouleResponse.from_dict")
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_020_007b_get_poule_with_basic_field_set(
        self, mock_http_get, mock_from_dict
    ):
        """Test get_poule with BASIC field_set."""
        mock_inner_data = {"id": 456, "nom": "Test Poule", "rencontres": []}
        mock_data = {"data": mock_inner_data}
        mock_http_get.return_value = mock_data

        mock_poule_obj = Mock()
        mock_from_dict.return_value = mock_poule_obj

        from ffbb_api_client_v2.models.field_set import FieldSet

        result = self.client.get_poule(poule_id=456, field_set=FieldSet.BASIC)

        mock_http_get.assert_called_once()
        # Verify fields in URL
        call_args = mock_http_get.call_args
        url = call_args[0][0]
        self.assertIn("fields%5B%5D", url)
        mock_from_dict.assert_called_once_with(mock_inner_data)
        self.assertEqual(result, mock_poule_obj)

    @patch("ffbb_api_client_v2.models.saisons_models.GetSaisonsResponse.from_list")
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_021_get_saisons_with_filter(self, mock_http_get, mock_from_list):
        """Test get_saisons with filter returns saisons list successfully."""
        mock_inner_data = [{"id": 2024, "nom": "Saison 2024"}]
        mock_data = {"data": mock_inner_data}  # Wrap in API response structure
        mock_http_get.return_value = mock_data

        mock_saisons_list = [Mock()]
        mock_from_list.return_value = mock_saisons_list

        filter_criteria = '{"id":{"_eq":2024}}'
        result = self.client.get_saisons(filter_criteria=filter_criteria)

        mock_http_get.assert_called_once()
        mock_from_list.assert_called_once_with(
            mock_inner_data
        )  # Should be called with inner data
        self.assertEqual(result, mock_saisons_list)

    @patch(
        "ffbb_api_client_v2.models.get_organisme_response.GetOrganismeResponse.from_dict"
    )
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_022_get_organisme_with_default_fields(self, mock_http_get, mock_from_dict):
        """Test get_organisme without fields uses default fields."""
        mock_inner_data = {
            "id": 789,
            "nom": "Test Club",
            "engagements": [{"id": "eng1"}, {"id": "eng2"}],
        }
        mock_data = {"data": mock_inner_data}
        mock_http_get.return_value = mock_data

        mock_organisme_obj = Mock()
        mock_from_dict.return_value = mock_organisme_obj

        # Test without fields (should use defaults)
        result = self.client.get_organisme(organisme_id=789)

        mock_http_get.assert_called_once()
        # Verify default fields in URL
        call_args = mock_http_get.call_args
        self.assertIn("fields%5B%5D", call_args[0][0])
        mock_from_dict.assert_called_once_with(mock_inner_data)
        self.assertEqual(result, mock_organisme_obj)

    @patch(
        "ffbb_api_client_v2.models.get_organisme_response.GetOrganismeResponse.from_dict"
    )
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_023_009b_get_organisme_with_basic_field_set(
        self, mock_http_get, mock_from_dict
    ):
        """Test get_organisme with BASIC field_set."""
        mock_inner_data = {"id": 789, "nom": "Test Club", "code": "TEST"}
        mock_data = {"data": mock_inner_data}
        mock_http_get.return_value = mock_data

        mock_organisme_obj = Mock()
        mock_from_dict.return_value = mock_organisme_obj

        from ffbb_api_client_v2.models.field_set import FieldSet

        result = self.client.get_organisme(organisme_id=789, field_set=FieldSet.BASIC)

        mock_http_get.assert_called_once()
        # Verify basic fields in URL
        call_args = mock_http_get.call_args
        url = call_args[0][0]
        self.assertIn("nom", url)
        self.assertIn("code", url)
        mock_from_dict.assert_called_once_with(mock_inner_data)
        self.assertEqual(result, mock_organisme_obj)

    @patch(
        "ffbb_api_client_v2.models.get_organisme_response.GetOrganismeResponse.from_dict"
    )
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_024_009c_get_organisme_with_detailed_field_set(
        self, mock_http_get, mock_from_dict
    ):
        """Test get_organisme with DETAILED field_set (default)."""
        mock_inner_data = {
            "id": 789,
            "nom": "Test Club",
            "engagements": [{"id": "eng1", "idCompetition": {"id": "comp1"}}],
        }
        mock_data = {"data": mock_inner_data}
        mock_http_get.return_value = mock_data

        mock_organisme_obj = Mock()
        mock_from_dict.return_value = mock_organisme_obj

        # Default field_set is DETAILED, so no need to pass it
        result = self.client.get_organisme(organisme_id=789)

        mock_http_get.assert_called_once()
        # Verify detailed fields in URL
        call_args = mock_http_get.call_args
        url = call_args[0][0]
        self.assertIn("engagements.idCompetition.id", url)
        mock_from_dict.assert_called_once_with(mock_inner_data)
        self.assertEqual(result, mock_organisme_obj)


class Test001QueryFieldsCounts(unittest.TestCase):
    """Regression tests for query field counts after API discovery alignment."""

    def test_025_organisme_field_counts(self):
        """Verify OrganismeFields counts after API discovery alignment."""
        from ffbb_api_client_v2.models.organisme_fields import OrganismeFields

        basic = OrganismeFields.get_basic_fields()
        default = OrganismeFields.get_default_fields()
        detailed = OrganismeFields.get_detailed_fields()

        self.assertEqual(len(basic), 6)
        self.assertEqual(len(default), 68)
        self.assertEqual(len(detailed), 76)
        self.assertGreater(len(default), len(basic))
        self.assertGreater(len(detailed), len(default))
        # No duplicates
        self.assertEqual(len(default), len(set(default)))
        self.assertEqual(len(detailed), len(set(detailed)))

    def test_026_competition_field_counts(self):
        """Verify CompetitionFields counts after API discovery alignment."""
        from ffbb_api_client_v2.models.competition_fields import CompetitionFields

        basic = CompetitionFields.get_basic_fields()
        default = CompetitionFields.get_default_fields()
        detailed = CompetitionFields.get_detailed_fields()

        self.assertEqual(len(basic), 5)
        self.assertEqual(len(default), 80)
        self.assertEqual(len(detailed), 80)
        self.assertGreater(len(default), len(basic))
        # No duplicates
        self.assertEqual(len(default), len(set(default)))

    def test_027_poule_field_counts(self):
        """Verify PouleFields counts — no duplicates in detailed."""
        from ffbb_api_client_v2.models.poule_fields import PouleFields

        basic = PouleFields.get_basic_fields()
        default = PouleFields.get_default_fields()
        detailed = PouleFields.get_detailed_fields()

        self.assertEqual(len(basic), 3)
        self.assertEqual(len(default), 104)
        self.assertEqual(len(detailed), 104)
        # No duplicates
        self.assertEqual(len(default), len(set(default)))

    def test_028_saison_field_counts(self):
        """Verify SaisonFields counts after API discovery alignment."""
        from ffbb_api_client_v2.models.saison_fields import SaisonFields

        default = SaisonFields.get_default_fields()
        detailed = SaisonFields.get_detailed_fields()

        self.assertEqual(len(default), 8)
        self.assertEqual(len(detailed), 10)
        self.assertGreater(len(detailed), len(default))
        # No duplicates
        self.assertEqual(len(default), len(set(default)))
        self.assertEqual(len(detailed), len(set(detailed)))


class Test001QueryFieldsManagerFieldSets(unittest.TestCase):
    """Tests that QueryFieldsManager returns valid field lists for all FieldSet values."""

    def test_029_organisme_all_field_sets(self):
        """Validate organisme fields for BASIC, DEFAULT, DETAILED."""
        from ffbb_api_client_v2.models.field_set import FieldSet
        from ffbb_api_client_v2.models.query_fields_manager import QueryFieldsManager

        basic = QueryFieldsManager.get_organisme_fields(FieldSet.BASIC)
        default = QueryFieldsManager.get_organisme_fields(FieldSet.DEFAULT)
        detailed = QueryFieldsManager.get_organisme_fields(FieldSet.DETAILED)

        # All return non-empty lists
        self.assertIsInstance(basic, list)
        self.assertGreater(len(basic), 0)
        self.assertIsInstance(default, list)
        self.assertGreater(len(default), 0)
        self.assertIsInstance(detailed, list)
        self.assertGreater(len(detailed), 0)
        # Ordering: basic < default <= detailed
        self.assertGreater(len(default), len(basic))
        self.assertGreaterEqual(len(detailed), len(default))
        # All basic fields are in default
        for f in basic:
            self.assertIn(f, default)
        # All default fields are in detailed
        for f in default:
            self.assertIn(f, detailed)

    def test_030_competition_all_field_sets(self):
        """Validate competition fields for BASIC, DEFAULT, DETAILED."""
        from ffbb_api_client_v2.models.field_set import FieldSet
        from ffbb_api_client_v2.models.query_fields_manager import QueryFieldsManager

        basic = QueryFieldsManager.get_competition_fields(FieldSet.BASIC)
        default = QueryFieldsManager.get_competition_fields(FieldSet.DEFAULT)
        detailed = QueryFieldsManager.get_competition_fields(FieldSet.DETAILED)

        self.assertIsInstance(basic, list)
        self.assertGreater(len(basic), 0)
        self.assertIsInstance(default, list)
        self.assertGreater(len(default), 0)
        self.assertIsInstance(detailed, list)
        self.assertGreater(len(detailed), 0)
        self.assertGreater(len(default), len(basic))
        self.assertGreaterEqual(len(detailed), len(default))
        for f in basic:
            self.assertIn(f, default)
        for f in default:
            self.assertIn(f, detailed)

    def test_031_poule_all_field_sets(self):
        """Validate poule fields for BASIC, DEFAULT, DETAILED."""
        from ffbb_api_client_v2.models.field_set import FieldSet
        from ffbb_api_client_v2.models.query_fields_manager import QueryFieldsManager

        basic = QueryFieldsManager.get_poule_fields(FieldSet.BASIC)
        default = QueryFieldsManager.get_poule_fields(FieldSet.DEFAULT)
        detailed = QueryFieldsManager.get_poule_fields(FieldSet.DETAILED)

        self.assertIsInstance(basic, list)
        self.assertGreater(len(basic), 0)
        self.assertIsInstance(default, list)
        self.assertGreater(len(default), 0)
        self.assertIsInstance(detailed, list)
        self.assertGreater(len(detailed), 0)
        self.assertGreater(len(default), len(basic))
        self.assertGreaterEqual(len(detailed), len(default))
        for f in basic:
            self.assertIn(f, default)
        for f in default:
            self.assertIn(f, detailed)

    def test_032_saison_all_field_sets(self):
        """Validate saison fields for all FieldSet values.

        Note: Saison has no BASIC, so BASIC falls through to DEFAULT.
        """
        from ffbb_api_client_v2.models.field_set import FieldSet
        from ffbb_api_client_v2.models.query_fields_manager import QueryFieldsManager

        basic = QueryFieldsManager.get_saison_fields(FieldSet.BASIC)
        default = QueryFieldsManager.get_saison_fields(FieldSet.DEFAULT)
        detailed = QueryFieldsManager.get_saison_fields(FieldSet.DETAILED)

        # BASIC falls through to default for saisons
        self.assertEqual(basic, default)
        self.assertIsInstance(default, list)
        self.assertGreater(len(default), 0)
        self.assertIsInstance(detailed, list)
        self.assertGreater(len(detailed), len(default))
        for f in default:
            self.assertIn(f, detailed)

    def test_033_organisme_query_with_default_fields(self):
        """Test get_organisme uses default fields in URL."""
        from ffbb_api_client_v2.models.organisme_fields import OrganismeFields
        from ffbb_api_client_v2.models.query_fields_manager import QueryFieldsManager

        fields = QueryFieldsManager.get_organisme_fields()
        # Verify key fields are present
        self.assertIn(OrganismeFields.ID, fields)
        self.assertIn(OrganismeFields.NOM, fields)
        self.assertIn(OrganismeFields.CARTOGRAPHIE_LATITUDE, fields)
        self.assertIn(OrganismeFields.LOGO_ID, fields)
        self.assertIn(OrganismeFields.SALLE_ID, fields)
        self.assertIn(OrganismeFields.OFFRES_PRATIQUES_ID, fields)
        self.assertIn(OrganismeFields.LABELLISATION_ID, fields)

    def test_034_competition_query_with_default_fields(self):
        """Test get_competition default fields include GameStats and Officiels."""
        from ffbb_api_client_v2.models.competition_fields import CompetitionFields
        from ffbb_api_client_v2.models.query_fields_manager import QueryFieldsManager

        fields = QueryFieldsManager.get_competition_fields()
        # GameStats should be in default now
        self.assertIn(CompetitionFields.PHASES_POULES_RENCONTRES_GSID_MATCH_ID, fields)
        self.assertIn(
            CompetitionFields.PHASES_POULES_RENCONTRES_GSID_CURRENT_STATUS, fields
        )
        # Officiels should be in default now
        self.assertIn(
            CompetitionFields.PHASES_POULES_RENCONTRES_OFFICIELS_ORDRE, fields
        )
        self.assertIn(
            CompetitionFields.PHASES_POULES_RENCONTRES_OFFICIELS_OFFICIEL_NOM, fields
        )
        # New engagement equipe fields
        self.assertIn(
            CompetitionFields.PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE1_ID, fields
        )
        self.assertIn(CompetitionFields.PHASES_POULES_RENCONTRES_SALLE_ID, fields)

    def test_035_saison_query_with_default_fields(self):
        """Test saison default fields include new API-discovered fields."""
        from ffbb_api_client_v2.models.query_fields_manager import QueryFieldsManager
        from ffbb_api_client_v2.models.saison_fields import SaisonFields

        fields = QueryFieldsManager.get_saison_fields()
        self.assertIn(SaisonFields.ID, fields)
        self.assertIn(SaisonFields.NOM, fields)
        self.assertIn(SaisonFields.CODE, fields)
        self.assertIn(SaisonFields.LIBELLE, fields)
        self.assertIn(SaisonFields.EN_COURS, fields)
        # date_created/date_updated only in detailed
        self.assertNotIn(SaisonFields.DATE_CREATED, fields)
        self.assertNotIn(SaisonFields.DATE_UPDATED, fields)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    @patch(
        "ffbb_api_client_v2.models.get_organisme_response.GetOrganismeResponse.from_dict"
    )
    def test_036_get_organisme_with_each_field_set(self, mock_from_dict, mock_http_get):
        """Test get_organisme works with BASIC, DEFAULT, and DETAILED field sets."""
        from ffbb_api_client_v2.clients.api_ffbb_app_client import ApiFFBBAppClient
        from ffbb_api_client_v2.models.field_set import FieldSet

        mock_inner_data = {"id": 1, "nom": "Test"}
        mock_http_get.return_value = {"data": mock_inner_data}
        mock_from_dict.return_value = Mock()

        client = ApiFFBBAppClient(bearer_token="test_token", debug=False)

        for fs in [FieldSet.BASIC, FieldSet.DEFAULT, FieldSet.DETAILED]:
            mock_http_get.reset_mock()
            mock_from_dict.reset_mock()

            result = client.get_organisme(organisme_id=1, field_set=fs)

            self.assertIsNotNone(result)
            mock_http_get.assert_called_once()
            url = mock_http_get.call_args[0][0]
            # URL must contain fields[] encoded
            self.assertIn("fields%5B%5D", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    @patch(
        "ffbb_api_client_v2.models.get_competition_response.GetCompetitionResponse.from_dict"
    )
    def test_037_get_competition_with_each_field_set(
        self, mock_from_dict, mock_http_get
    ):
        """Test get_competition works with BASIC, DEFAULT, and DETAILED field sets."""
        from ffbb_api_client_v2.clients.api_ffbb_app_client import ApiFFBBAppClient
        from ffbb_api_client_v2.models.field_set import FieldSet

        mock_inner_data = {"id": 1, "nom": "Test"}
        mock_http_get.return_value = {"data": mock_inner_data}
        mock_from_dict.return_value = Mock()

        client = ApiFFBBAppClient(bearer_token="test_token", debug=False)

        for fs in [FieldSet.BASIC, FieldSet.DEFAULT, FieldSet.DETAILED]:
            mock_http_get.reset_mock()
            mock_from_dict.reset_mock()

            result = client.get_competition(competition_id=1, field_set=fs)

            self.assertIsNotNone(result)
            mock_http_get.assert_called_once()
            url = mock_http_get.call_args[0][0]
            self.assertIn("fields%5B%5D", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    @patch("ffbb_api_client_v2.models.poules_models.GetPouleResponse.from_dict")
    def test_038_get_poule_with_each_field_set(self, mock_from_dict, mock_http_get):
        """Test get_poule works with BASIC, DEFAULT, and DETAILED field sets."""
        from ffbb_api_client_v2.clients.api_ffbb_app_client import ApiFFBBAppClient
        from ffbb_api_client_v2.models.field_set import FieldSet

        mock_inner_data = {"id": 1, "nom": "Test"}
        mock_http_get.return_value = {"data": mock_inner_data}
        mock_from_dict.return_value = Mock()

        client = ApiFFBBAppClient(bearer_token="test_token", debug=False)

        for fs in [FieldSet.BASIC, FieldSet.DEFAULT, FieldSet.DETAILED]:
            mock_http_get.reset_mock()
            mock_from_dict.reset_mock()

            result = client.get_poule(poule_id=1, field_set=fs)

            self.assertIsNotNone(result)
            mock_http_get.assert_called_once()
            url = mock_http_get.call_args[0][0]
            self.assertIn("fields%5B%5D", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    @patch("ffbb_api_client_v2.models.saisons_models.GetSaisonsResponse.from_list")
    def test_039_get_saisons_with_each_field_set(self, mock_from_list, mock_http_get):
        """Test get_saisons works with BASIC, DEFAULT, and DETAILED field sets."""
        from ffbb_api_client_v2.clients.api_ffbb_app_client import ApiFFBBAppClient
        from ffbb_api_client_v2.models.field_set import FieldSet

        mock_http_get.return_value = {"data": [{"id": "2024"}]}
        mock_from_list.return_value = [Mock()]

        client = ApiFFBBAppClient(bearer_token="test_token", debug=False)

        for fs in [FieldSet.BASIC, FieldSet.DEFAULT, FieldSet.DETAILED]:
            mock_http_get.reset_mock()
            mock_from_list.reset_mock()
            mock_from_list.return_value = [Mock()]

            result = client.get_saisons(field_set=fs)

            self.assertIsNotNone(result)
            mock_http_get.assert_called_once()
            url = mock_http_get.call_args[0][0]
            self.assertIn("fields%5B%5D", url)


class Test001MeilisearchFfbbCore(unittest.TestCase):
    """Unit tests for the Meilisearch FFBB Client module."""

    def setUp(self):
        """Set up test fixtures."""
        self.bearer_token = "test_ms_token"

    def test_040_init_with_default_url(self):
        """Test client initializes with default URL."""
        mock_path = (
            "ffbb_api_client_v2.clients.meilisearch_ffbb_client."
            "MeilisearchClientExtension.__init__"
        )
        with patch(mock_path) as mock_super_init:
            MeilisearchFFBBClient(bearer_token=self.bearer_token)
            mock_super_init.assert_called_once_with(
                self.bearer_token,
                "https://meilisearch-prod.ffbb.app/",
                False,
                unittest.mock.ANY,
            )

    def test_041_init_with_custom_url(self):
        """Test client initializes with custom URL."""
        custom_url = "https://custom.meilisearch.url/"
        mock_path = (
            "ffbb_api_client_v2.clients.meilisearch_ffbb_client."
            "MeilisearchClientExtension.__init__"
        )
        with patch(mock_path) as mock_super_init:
            MeilisearchFFBBClient(bearer_token=self.bearer_token, url=custom_url)
            mock_super_init.assert_called_once_with(
                self.bearer_token, custom_url, False, unittest.mock.ANY
            )


if __name__ == "__main__":
    unittest.main()
