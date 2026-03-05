"""Unit tests for FFBB API Client V2 core components."""

import unittest
from unittest.mock import Mock, patch

from requests_cache import CachedSession

from ffbb_api_client_v2 import FFBBAPIClientV2
from ffbb_api_client_v2.directus_ffbb.client import ApiFFBBAppClient
from ffbb_api_client_v2.meilisearch_ffbb.client import MeilisearchFFBBClient


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
            "ffbb_api_client_v2.facade.client.ApiFFBBAppClient"
        ) as mock_api_cls, patch(
            "ffbb_api_client_v2.facade.client.MeilisearchFFBBClient"
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
            "ffbb_api_client_v2.facade.client.generate_queries"
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
            "ffbb_api_client_v2.facade.client.generate_queries"
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
        self.assertIn("bearer_token", str(context.exception))

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

    @patch("ffbb_api_client_v2.directus_ffbb.client.lives_from_dict")
    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
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
        "ffbb_api_client_v2.directus_ffbb.models.get_competition_response.GetCompetitionResponse.from_dict"
    )
    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
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
        "ffbb_api_client_v2.directus_ffbb.models.poules_models.GetPouleResponse.from_dict"
    )
    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
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

    @patch(
        "ffbb_api_client_v2.directus_ffbb.models.saisons_models.GetSaisonsResponse.from_list"
    )
    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
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
        "ffbb_api_client_v2.directus_ffbb.models.get_organisme_response.GetOrganismeResponse.from_dict"
    )
    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
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


class Test001QueryFieldsCounts(unittest.TestCase):
    """Regression tests for query field counts after refactoring to get_fields()."""

    def test_025_organisme_field_counts(self):
        """Verify OrganismeFields.get_fields() count."""
        from ffbb_api_client_v2.directus_ffbb.models.organisme_fields import (
            OrganismeFields,
        )

        fields = OrganismeFields.get_fields()
        self.assertEqual(len(fields), 63)
        # No duplicates
        self.assertEqual(len(fields), len(set(fields)))

    def test_026_competition_field_counts(self):
        """Verify CompetitionFields.get_fields() count."""
        from ffbb_api_client_v2.directus_ffbb.models.competition_fields import (
            CompetitionFields,
        )

        fields = CompetitionFields.get_fields()
        self.assertEqual(len(fields), 38)
        # No duplicates
        self.assertEqual(len(fields), len(set(fields)))

    def test_027_poule_field_counts(self):
        """Verify PouleFields.get_fields() count — no duplicates."""
        from ffbb_api_client_v2.directus_ffbb.models.poule_fields import PouleFields

        fields = PouleFields.get_fields()
        self.assertEqual(len(fields), 30)
        # No duplicates
        self.assertEqual(len(fields), len(set(fields)))

    def test_028_saison_field_counts(self):
        """Verify SaisonFields.get_fields() count."""
        from ffbb_api_client_v2.directus_ffbb.models.saison_fields import SaisonFields

        fields = SaisonFields.get_fields()
        self.assertEqual(len(fields), 9)
        # No duplicates
        self.assertEqual(len(fields), len(set(fields)))


class Test001QueryFieldsManagerExplicit(unittest.TestCase):
    """Tests that *Fields.get_fields() returns explicit fields for deep entities."""

    def test_033_organisme_query_returns_explicit_fields(self):
        """Test OrganismeFields.get_fields() returns explicit field list."""
        from ffbb_api_client_v2.directus_ffbb.models.organisme_fields import (
            OrganismeFields,
        )

        fields = OrganismeFields.get_fields()
        self.assertIsInstance(fields, list)
        self.assertIn("id", fields)
        self.assertIn("nom", fields)

    def test_034_competition_query_returns_explicit_fields(self):
        """Test CompetitionFields.get_fields() returns explicit field list."""
        from ffbb_api_client_v2.directus_ffbb.models.competition_fields import (
            CompetitionFields,
        )

        fields = CompetitionFields.get_fields()
        self.assertIsInstance(fields, list)
        self.assertIn("id", fields)
        self.assertIn("nom", fields)

    def test_035_saison_query_returns_explicit_fields(self):
        """Test SaisonFields.get_fields() returns explicit fields."""
        from ffbb_api_client_v2.directus_ffbb.models.saison_fields import SaisonFields

        fields = SaisonFields.get_fields()
        self.assertIsInstance(fields, list)
        self.assertIn("id", fields)


class Test001MeilisearchFfbbCore(unittest.TestCase):
    """Unit tests for the Meilisearch FFBB Client module."""

    def setUp(self):
        """Set up test fixtures."""
        self.bearer_token = "test_ms_token"

    def test_040_init_with_default_url(self):
        """Test client initializes with default URL."""
        mock_path = (
            "ffbb_api_client_v2.meilisearch_ffbb.client."
            "MeilisearchClientExtension.__init__"
        )
        with patch(mock_path) as mock_super_init:
            MeilisearchFFBBClient(bearer_token=self.bearer_token)
            mock_super_init.assert_called_once_with(
                self.bearer_token,
                "https://meilisearch-prod.ffbb.app/",
                False,
                unittest.mock.ANY,
                None,
                None,
            )

    def test_041_init_with_custom_url(self):
        """Test client initializes with custom URL."""
        custom_url = "https://custom.meilisearch.url/"
        mock_path = (
            "ffbb_api_client_v2.meilisearch_ffbb.client."
            "MeilisearchClientExtension.__init__"
        )
        with patch(mock_path) as mock_super_init:
            MeilisearchFFBBClient(bearer_token=self.bearer_token, url=custom_url)
            mock_super_init.assert_called_once_with(
                self.bearer_token,
                custom_url,
                False,
                unittest.mock.ANY,
                None,
                None,
            )


if __name__ == "__main__":
    unittest.main()
