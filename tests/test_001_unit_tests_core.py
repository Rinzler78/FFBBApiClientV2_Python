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

    def test_001_init_with_valid_clients(self):
        """Test that client initializes correctly with valid clients."""
        self.assertIsNotNone(self.client)
        self.assertEqual(self.client.api_ffbb_client, self.mock_api_client)
        self.assertEqual(
            self.client.meilisearch_ffbb_client, self.mock_meilisearch_client
        )

    def test_002_create_factory_method_success(self):
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

    def test_003_create_factory_method_empty_api_token(self):
        """Test factory method raises error with empty API token."""
        with self.assertRaises(ValueError) as context:
            FFBBAPIClientV2.create(
                meilisearch_bearer_token="test_ms_token", api_bearer_token=""
            )
        self.assertIn(
            "Api Bearer token cannot be None or empty", str(context.exception)
        )

    def test_004_create_factory_method_empty_meilisearch_token(self):
        """Test factory method raises error with empty Meilisearch token."""
        with self.assertRaises(ValueError) as context:
            FFBBAPIClientV2.create(
                meilisearch_bearer_token="", api_bearer_token="test_api_token"
            )
        self.assertIn(
            "Meilisearch Bearer token cannot be None or empty", str(context.exception)
        )

    def test_005_get_lives_delegates_to_api_client(self):
        """Test get_lives delegates correctly to API client."""
        mock_lives = ["mock_live_data"]
        self.mock_api_client.get_lives.return_value = mock_lives

        result = self.client.get_lives()

        self.mock_api_client.get_lives.assert_called_once_with(None)
        self.assertEqual(result, mock_lives)

    def test_006_multi_search_with_name(self):
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

    def test_007_multi_search_no_results(self):
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

    def test_008_search_organismes_with_name(self):
        """Test search_organismes with valid name parameter."""
        with patch.object(
            self.client, "search_multiple_organismes"
        ) as mock_search_multiple:
            mock_result = Mock()
            mock_search_multiple.return_value = [mock_result]

            result = self.client.search_organismes("Paris")

            mock_search_multiple.assert_called_once_with(["Paris"], None)
            self.assertEqual(result, mock_result)

    def test_009_search_organismes_no_results(self):
        """Test search_organismes returns empty result object when no results found."""
        with patch.object(
            self.client, "search_multiple_organismes"
        ) as mock_search_multiple:
            mock_search_multiple.return_value = None

            mock_path = (
                "ffbb_api_client_v2.clients.ffbb_api_client_v2."
                "OrganismesMultiSearchResult"
            )
            with patch(mock_path) as mock_result_class:
                mock_result_instance = Mock()
                mock_result_class.return_value = mock_result_instance

                result = self.client.search_organismes("NonExistent")

                self.assertEqual(result, mock_result_instance)

    def test_010_search_multiple_organismes_empty_names(self):
        """Test search_multiple_organismes returns None for empty names."""
        result = self.client.search_multiple_organismes(None)
        self.assertIsNone(result)

    def test_011_search_multiple_organismes_with_names(self):
        """Test search_multiple_organismes with valid names list."""
        mock_result = Mock()
        mock_result.results = ["result1", "result2"]
        self.mock_meilisearch_client.recursive_smart_multi_search.return_value = (
            mock_result
        )

        result = self.client.search_multiple_organismes(["Paris", "Lyon"])

        self.assertEqual(result, ["result1", "result2"])

    def test_012_cached_session_parameter_propagation(self):
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

    def test_001_init_with_valid_token(self):
        """Test client initializes correctly with valid token."""
        self.assertEqual(self.client.bearer_token, self.bearer_token)
        self.assertEqual(self.client.url, "https://api.ffbb.app/")
        self.assertFalse(self.client.debug)
        self.assertEqual(
            self.client.headers, {"Authorization": f"Bearer {self.bearer_token}"}
        )

    def test_002_init_with_empty_token(self):
        """Test client raises error with empty token."""
        with self.assertRaises(ValueError) as context:
            ApiFFBBAppClient(bearer_token="")
        self.assertIn("bearer_token cannot be None or empty", str(context.exception))

    def test_003_init_with_none_token(self):
        """Test client raises error with None token."""
        with self.assertRaises(ValueError) as context:
            ApiFFBBAppClient(bearer_token=None)
        self.assertIn("bearer_token cannot be None or empty", str(context.exception))

    def test_004_init_with_custom_url(self):
        """Test client initializes with custom URL."""
        custom_url = "https://custom.api.url/"
        client = ApiFFBBAppClient(bearer_token=self.bearer_token, url=custom_url)
        self.assertEqual(client.url, custom_url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.lives_from_dict")
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_005_get_lives_success(self, mock_http_get, mock_lives_from_dict):
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
        "ffbb_api_client_v2.models.competitions_models.GetCompetitionResponse.from_dict"
    )
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_006_get_competition_success(self, mock_http_get, mock_from_dict):
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
        "ffbb_api_client_v2.models.competitions_models.GetCompetitionResponse.from_dict"
    )
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_006b_get_competition_with_basic_fields(
        self, mock_http_get, mock_from_dict
    ):
        """Test get_competition with basic fields."""
        mock_inner_data = {"id": 123, "nom": "Test Competition", "sexe": "M"}
        mock_data = {"data": mock_inner_data}
        mock_http_get.return_value = mock_data

        mock_competition_obj = Mock()
        mock_from_dict.return_value = mock_competition_obj

        # Use basic fields explicitly
        from ffbb_api_client_v2.models.query_fields import FieldSet, QueryFieldsManager

        basic_fields = QueryFieldsManager.get_competition_fields(FieldSet.BASIC)
        result = self.client.get_competition(competition_id=123, fields=basic_fields)

        mock_http_get.assert_called_once()
        # Verify that basic fields are in the URL
        call_args = mock_http_get.call_args
        url = call_args[0][0]
        for field in basic_fields:
            self.assertIn(field.replace("[", "%5B").replace("]", "%5D"), url)
        mock_from_dict.assert_called_once_with(mock_inner_data)
        self.assertEqual(result, mock_competition_obj)

    @patch(
        "ffbb_api_client_v2.models.competitions_models.GetCompetitionResponse.from_dict"
    )
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_006c_get_competition_with_custom_fields(
        self, mock_http_get, mock_from_dict
    ):
        """Test get_competition with custom fields."""
        mock_inner_data = {"id": 123, "custom": "value"}
        mock_data = {"data": mock_inner_data}
        mock_http_get.return_value = mock_data

        mock_competition_obj = Mock()
        mock_from_dict.return_value = mock_competition_obj

        # Use custom fields
        custom_fields = ["id", "custom_field1", "nested.field"]
        result = self.client.get_competition(competition_id=123, fields=custom_fields)

        mock_http_get.assert_called_once()
        # Verify that custom fields are in the URL
        call_args = mock_http_get.call_args
        url = call_args[0][0]
        for field in custom_fields:
            self.assertIn(
                field.replace("[", "%5B").replace("]", "%5D").replace(".", "."), url
            )
        mock_from_dict.assert_called_once_with(mock_inner_data)
        self.assertEqual(result, mock_competition_obj)

    @patch("ffbb_api_client_v2.models.poules_models.GetPouleResponse.from_dict")
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_007_get_poule_with_default_fields(self, mock_http_get, mock_from_dict):
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
    def test_007b_get_poule_with_custom_fields(self, mock_http_get, mock_from_dict):
        """Test get_poule with custom fields."""
        mock_inner_data = {"id": 456, "nom": "Test Poule", "rencontres": []}
        mock_data = {"data": mock_inner_data}
        mock_http_get.return_value = mock_data

        mock_poule_obj = Mock()
        mock_from_dict.return_value = mock_poule_obj

        # Use custom fields
        custom_fields = ["id", "nom", "rencontres.id", "rencontres.numero"]
        result = self.client.get_poule(poule_id=456, fields=custom_fields)

        mock_http_get.assert_called_once()
        # Verify custom fields in URL
        call_args = mock_http_get.call_args
        url = call_args[0][0]
        self.assertIn("rencontres.id", url)
        mock_from_dict.assert_called_once_with(mock_inner_data)
        self.assertEqual(result, mock_poule_obj)

    @patch("ffbb_api_client_v2.models.saisons_models.GetSaisonsResponse.from_list")
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_008_get_saisons_with_filter(self, mock_http_get, mock_from_list):
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

    @patch("ffbb_api_client_v2.models.organismes_models.GetOrganismeResponse.from_dict")
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_009_get_organisme_with_default_fields(self, mock_http_get, mock_from_dict):
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

    @patch("ffbb_api_client_v2.models.organismes_models.GetOrganismeResponse.from_dict")
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_009b_get_organisme_with_basic_fields(self, mock_http_get, mock_from_dict):
        """Test get_organisme with basic fields."""
        mock_inner_data = {"id": 789, "nom": "Test Club", "code": "TEST"}
        mock_data = {"data": mock_inner_data}
        mock_http_get.return_value = mock_data

        mock_organisme_obj = Mock()
        mock_from_dict.return_value = mock_organisme_obj

        # Use basic fields
        from ffbb_api_client_v2.models.query_fields import FieldSet, QueryFieldsManager

        basic_fields = QueryFieldsManager.get_organisme_fields(FieldSet.BASIC)
        result = self.client.get_organisme(organisme_id=789, fields=basic_fields)

        mock_http_get.assert_called_once()
        # Verify basic fields in URL
        call_args = mock_http_get.call_args
        url = call_args[0][0]
        self.assertIn("nom", url)
        self.assertIn("code", url)
        mock_from_dict.assert_called_once_with(mock_inner_data)
        self.assertEqual(result, mock_organisme_obj)

    @patch("ffbb_api_client_v2.models.organismes_models.GetOrganismeResponse.from_dict")
    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_009c_get_organisme_with_detailed_fields(
        self, mock_http_get, mock_from_dict
    ):
        """Test get_organisme with detailed fields."""
        mock_inner_data = {
            "id": 789,
            "nom": "Test Club",
            "engagements": [{"id": "eng1", "idCompetition": {"id": "comp1"}}],
        }
        mock_data = {"data": mock_inner_data}
        mock_http_get.return_value = mock_data

        mock_organisme_obj = Mock()
        mock_from_dict.return_value = mock_organisme_obj

        # Use detailed fields
        from ffbb_api_client_v2.models.query_fields import OrganismeFields

        detailed_fields = OrganismeFields.get_detailed_fields()

        result = self.client.get_organisme(organisme_id=789, fields=detailed_fields)

        mock_http_get.assert_called_once()
        # Verify detailed fields in URL
        call_args = mock_http_get.call_args
        url = call_args[0][0]
        self.assertIn("engagements.idCompetition.id", url)
        mock_from_dict.assert_called_once_with(mock_inner_data)
        self.assertEqual(result, mock_organisme_obj)


class Test001MeilisearchFfbbCore(unittest.TestCase):
    """Unit tests for the Meilisearch FFBB Client module."""

    def setUp(self):
        """Set up test fixtures."""
        self.bearer_token = "test_ms_token"

    def test_001_init_with_default_url(self):
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

    def test_002_init_with_custom_url(self):
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
