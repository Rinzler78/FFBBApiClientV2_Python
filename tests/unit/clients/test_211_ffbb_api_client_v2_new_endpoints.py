"""Unit tests for FFBBAPIClientV2 facade delegation of new Directus endpoints."""

import unittest
from unittest.mock import Mock

from ffbb_api_client_v2 import FFBBAPIClientV2
from ffbb_api_client_v2.clients.api_ffbb_app_client import ApiFFBBAppClient
from ffbb_api_client_v2.clients.meilisearch_ffbb_client import MeilisearchFFBBClient


class Test211FFBBAPIClientV2NewEndpointsRencontres(unittest.TestCase):
    """Tests for rencontres facade delegation on FFBBAPIClientV2."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_api_client = Mock(spec=ApiFFBBAppClient)
        self.mock_meilisearch_client = Mock(spec=MeilisearchFFBBClient)
        self.client = FFBBAPIClientV2(
            api_ffbb_client=self.mock_api_client,
            meilisearch_ffbb_client=self.mock_meilisearch_client,
        )

    def test_000_get_rencontre_delegates(self):
        """Test get_rencontre delegates to api_ffbb_client."""
        mock_result = Mock()
        self.mock_api_client.get_rencontre.return_value = mock_result
        result = self.client.get_rencontre(123)
        self.mock_api_client.get_rencontre.assert_called_once()
        self.assertEqual(result, mock_result)

    def test_001_list_rencontres_delegates(self):
        """Test list_rencontres delegates to api_ffbb_client."""
        mock_result = [Mock(), Mock()]
        self.mock_api_client.list_rencontres.return_value = mock_result
        result = self.client.list_rencontres(limit=10)
        self.mock_api_client.list_rencontres.assert_called_once()
        self.assertEqual(result, mock_result)


class Test211FFBBAPIClientV2NewEndpointsSalles(unittest.TestCase):
    """Tests for salles facade delegation on FFBBAPIClientV2."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_api_client = Mock(spec=ApiFFBBAppClient)
        self.mock_meilisearch_client = Mock(spec=MeilisearchFFBBClient)
        self.client = FFBBAPIClientV2(
            api_ffbb_client=self.mock_api_client,
            meilisearch_ffbb_client=self.mock_meilisearch_client,
        )

    def test_002_get_salle_delegates(self):
        """Test get_salle delegates to api_ffbb_client."""
        mock_result = Mock()
        self.mock_api_client.get_salle.return_value = mock_result
        result = self.client.get_salle(456)
        self.mock_api_client.get_salle.assert_called_once()
        self.assertEqual(result, mock_result)

    def test_003_list_salles_delegates(self):
        """Test list_salles delegates to api_ffbb_client."""
        mock_result = [Mock(), Mock()]
        self.mock_api_client.list_salles.return_value = mock_result
        result = self.client.list_salles(limit=10)
        self.mock_api_client.list_salles.assert_called_once()
        self.assertEqual(result, mock_result)


class Test211FFBBAPIClientV2NewEndpointsTerrains(unittest.TestCase):
    """Tests for terrains facade delegation on FFBBAPIClientV2."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_api_client = Mock(spec=ApiFFBBAppClient)
        self.mock_meilisearch_client = Mock(spec=MeilisearchFFBBClient)
        self.client = FFBBAPIClientV2(
            api_ffbb_client=self.mock_api_client,
            meilisearch_ffbb_client=self.mock_meilisearch_client,
        )

    def test_004_get_terrain_delegates(self):
        """Test get_terrain delegates to api_ffbb_client."""
        mock_result = Mock()
        self.mock_api_client.get_terrain.return_value = mock_result
        result = self.client.get_terrain(789)
        self.mock_api_client.get_terrain.assert_called_once()
        self.assertEqual(result, mock_result)

    def test_005_list_terrains_delegates(self):
        """Test list_terrains delegates to api_ffbb_client."""
        mock_result = [Mock(), Mock()]
        self.mock_api_client.list_terrains.return_value = mock_result
        result = self.client.list_terrains(limit=10)
        self.mock_api_client.list_terrains.assert_called_once()
        self.assertEqual(result, mock_result)


class Test211FFBBAPIClientV2NewEndpointsTournois(unittest.TestCase):
    """Tests for tournois facade delegation on FFBBAPIClientV2."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_api_client = Mock(spec=ApiFFBBAppClient)
        self.mock_meilisearch_client = Mock(spec=MeilisearchFFBBClient)
        self.client = FFBBAPIClientV2(
            api_ffbb_client=self.mock_api_client,
            meilisearch_ffbb_client=self.mock_meilisearch_client,
        )

    def test_006_get_tournoi_delegates(self):
        """Test get_tournoi delegates to api_ffbb_client."""
        mock_result = Mock()
        self.mock_api_client.get_tournoi.return_value = mock_result
        result = self.client.get_tournoi(101)
        self.mock_api_client.get_tournoi.assert_called_once()
        self.assertEqual(result, mock_result)

    def test_007_list_tournois_delegates(self):
        """Test list_tournois delegates to api_ffbb_client."""
        mock_result = [Mock(), Mock()]
        self.mock_api_client.list_tournois.return_value = mock_result
        result = self.client.list_tournois(limit=10)
        self.mock_api_client.list_tournois.assert_called_once()
        self.assertEqual(result, mock_result)


class Test211FFBBAPIClientV2NewEndpointsEngagements(unittest.TestCase):
    """Tests for engagements facade delegation on FFBBAPIClientV2."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_api_client = Mock(spec=ApiFFBBAppClient)
        self.mock_meilisearch_client = Mock(spec=MeilisearchFFBBClient)
        self.client = FFBBAPIClientV2(
            api_ffbb_client=self.mock_api_client,
            meilisearch_ffbb_client=self.mock_meilisearch_client,
        )

    def test_008_get_engagement_delegates(self):
        """Test get_engagement delegates to api_ffbb_client."""
        mock_result = Mock()
        self.mock_api_client.get_engagement.return_value = mock_result
        result = self.client.get_engagement(200)
        self.mock_api_client.get_engagement.assert_called_once()
        self.assertEqual(result, mock_result)

    def test_009_list_engagements_delegates(self):
        """Test list_engagements delegates to api_ffbb_client."""
        mock_result = [Mock(), Mock()]
        self.mock_api_client.list_engagements.return_value = mock_result
        result = self.client.list_engagements(limit=10)
        self.mock_api_client.list_engagements.assert_called_once()
        self.assertEqual(result, mock_result)


class Test211FFBBAPIClientV2NewEndpointsFormations(unittest.TestCase):
    """Tests for formations facade delegation on FFBBAPIClientV2."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_api_client = Mock(spec=ApiFFBBAppClient)
        self.mock_meilisearch_client = Mock(spec=MeilisearchFFBBClient)
        self.client = FFBBAPIClientV2(
            api_ffbb_client=self.mock_api_client,
            meilisearch_ffbb_client=self.mock_meilisearch_client,
        )

    def test_010_get_formation_delegates(self):
        """Test get_formation delegates to api_ffbb_client."""
        mock_result = Mock()
        self.mock_api_client.get_formation.return_value = mock_result
        result = self.client.get_formation("f-001")
        self.mock_api_client.get_formation.assert_called_once()
        self.assertEqual(result, mock_result)

    def test_011_list_formations_delegates(self):
        """Test list_formations delegates to api_ffbb_client."""
        mock_result = [Mock(), Mock()]
        self.mock_api_client.list_formations.return_value = mock_result
        result = self.client.list_formations(limit=10)
        self.mock_api_client.list_formations.assert_called_once()
        self.assertEqual(result, mock_result)


class Test211FFBBAPIClientV2NewEndpointsEntraineurs(unittest.TestCase):
    """Tests for entraineurs facade delegation on FFBBAPIClientV2."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_api_client = Mock(spec=ApiFFBBAppClient)
        self.mock_meilisearch_client = Mock(spec=MeilisearchFFBBClient)
        self.client = FFBBAPIClientV2(
            api_ffbb_client=self.mock_api_client,
            meilisearch_ffbb_client=self.mock_meilisearch_client,
        )

    def test_012_get_entraineur_delegates(self):
        """Test get_entraineur delegates to api_ffbb_client."""
        mock_result = Mock()
        self.mock_api_client.get_entraineur.return_value = mock_result
        result = self.client.get_entraineur(300)
        self.mock_api_client.get_entraineur.assert_called_once()
        self.assertEqual(result, mock_result)

    def test_013_list_entraineurs_delegates(self):
        """Test list_entraineurs delegates to api_ffbb_client."""
        mock_result = [Mock(), Mock()]
        self.mock_api_client.list_entraineurs.return_value = mock_result
        result = self.client.list_entraineurs(limit=10)
        self.mock_api_client.list_entraineurs.assert_called_once()
        self.assertEqual(result, mock_result)


class Test211FFBBAPIClientV2NewEndpointsCommunes(unittest.TestCase):
    """Tests for communes facade delegation on FFBBAPIClientV2."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_api_client = Mock(spec=ApiFFBBAppClient)
        self.mock_meilisearch_client = Mock(spec=MeilisearchFFBBClient)
        self.client = FFBBAPIClientV2(
            api_ffbb_client=self.mock_api_client,
            meilisearch_ffbb_client=self.mock_meilisearch_client,
        )

    def test_014_list_communes_delegates(self):
        """Test list_communes delegates to api_ffbb_client."""
        mock_result = [Mock(), Mock()]
        self.mock_api_client.list_communes.return_value = mock_result
        result = self.client.list_communes(limit=10)
        self.mock_api_client.list_communes.assert_called_once()
        self.assertEqual(result, mock_result)


class Test211FFBBAPIClientV2NewEndpointsOfficiels(unittest.TestCase):
    """Tests for officiels facade delegation on FFBBAPIClientV2."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_api_client = Mock(spec=ApiFFBBAppClient)
        self.mock_meilisearch_client = Mock(spec=MeilisearchFFBBClient)
        self.client = FFBBAPIClientV2(
            api_ffbb_client=self.mock_api_client,
            meilisearch_ffbb_client=self.mock_meilisearch_client,
        )

    def test_015_list_officiels_delegates(self):
        """Test list_officiels delegates to api_ffbb_client."""
        mock_result = [Mock(), Mock()]
        self.mock_api_client.list_officiels.return_value = mock_result
        result = self.client.list_officiels(limit=10)
        self.mock_api_client.list_officiels.assert_called_once()
        self.assertEqual(result, mock_result)


class Test211FFBBAPIClientV2NewEndpointsPratiques(unittest.TestCase):
    """Tests for pratiques facade delegation on FFBBAPIClientV2."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_api_client = Mock(spec=ApiFFBBAppClient)
        self.mock_meilisearch_client = Mock(spec=MeilisearchFFBBClient)
        self.client = FFBBAPIClientV2(
            api_ffbb_client=self.mock_api_client,
            meilisearch_ffbb_client=self.mock_meilisearch_client,
        )

    def test_016_list_pratiques_delegates(self):
        """Test list_pratiques delegates to api_ffbb_client."""
        mock_result = [Mock(), Mock()]
        self.mock_api_client.list_pratiques.return_value = mock_result
        result = self.client.list_pratiques(limit=10)
        self.mock_api_client.list_pratiques.assert_called_once()
        self.assertEqual(result, mock_result)


class Test211FFBBAPIClientV2QueryParamsDelegation(unittest.TestCase):
    """Tests for query params delegation on all list_xxx methods."""

    def setUp(self):
        self.mock_api_client = Mock(spec=ApiFFBBAppClient)
        self.mock_meilisearch_client = Mock(spec=MeilisearchFFBBClient)
        self.client = FFBBAPIClientV2(
            api_ffbb_client=self.mock_api_client,
            meilisearch_ffbb_client=self.mock_meilisearch_client,
        )

    def test_017_list_rencontres_delegates_with_query_params(self):
        """Test list_rencontres passes query params."""
        self.mock_api_client.list_rencontres.return_value = []
        self.client.list_rencontres(
            filter_criteria='{"actif":{"_eq":true}}',
            sort=["date_rencontre"],
            offset=20,
            search="paris",
        )
        self.mock_api_client.list_rencontres.assert_called_once()
        kwargs = self.mock_api_client.list_rencontres.call_args[1]
        self.assertEqual(kwargs["filter_criteria"], '{"actif":{"_eq":true}}')
        self.assertEqual(kwargs["sort"], ["date_rencontre"])
        self.assertEqual(kwargs["offset"], 20)
        self.assertEqual(kwargs["search"], "paris")

    def test_018_list_salles_delegates_with_query_params(self):
        self.mock_api_client.list_salles.return_value = []
        self.client.list_salles(
            filter_criteria='{"actif":{"_eq":true}}',
            sort=["libelle"],
            offset=10,
            search="gym",
        )
        kwargs = self.mock_api_client.list_salles.call_args[1]
        self.assertEqual(kwargs["filter_criteria"], '{"actif":{"_eq":true}}')
        self.assertEqual(kwargs["sort"], ["libelle"])
        self.assertEqual(kwargs["offset"], 10)

    def test_019_list_terrains_delegates_with_query_params(self):
        self.mock_api_client.list_terrains.return_value = []
        self.client.list_terrains(sort=["nom"], offset=5)
        kwargs = self.mock_api_client.list_terrains.call_args[1]
        self.assertEqual(kwargs["sort"], ["nom"])
        self.assertEqual(kwargs["offset"], 5)

    def test_020_list_tournois_delegates_with_query_params(self):
        self.mock_api_client.list_tournois.return_value = []
        self.client.list_tournois(search="3x3")
        kwargs = self.mock_api_client.list_tournois.call_args[1]
        self.assertEqual(kwargs["search"], "3x3")

    def test_021_list_engagements_delegates_with_query_params(self):
        self.mock_api_client.list_engagements.return_value = []
        self.client.list_engagements(offset=0)
        kwargs = self.mock_api_client.list_engagements.call_args[1]
        self.assertEqual(kwargs["offset"], 0)

    def test_022_list_formations_delegates_with_query_params(self):
        self.mock_api_client.list_formations.return_value = []
        self.client.list_formations(filter_criteria='{"test":{"_eq":1}}')
        kwargs = self.mock_api_client.list_formations.call_args[1]
        self.assertEqual(kwargs["filter_criteria"], '{"test":{"_eq":1}}')

    def test_023_list_entraineurs_delegates_with_query_params(self):
        self.mock_api_client.list_entraineurs.return_value = []
        self.client.list_entraineurs(sort=["nom"], search="dupont")
        kwargs = self.mock_api_client.list_entraineurs.call_args[1]
        self.assertEqual(kwargs["sort"], ["nom"])
        self.assertEqual(kwargs["search"], "dupont")

    def test_024_list_communes_delegates_with_query_params(self):
        self.mock_api_client.list_communes.return_value = []
        self.client.list_communes(sort=["libelle"])
        kwargs = self.mock_api_client.list_communes.call_args[1]
        self.assertEqual(kwargs["sort"], ["libelle"])

    def test_025_list_officiels_delegates_with_query_params(self):
        self.mock_api_client.list_officiels.return_value = []
        self.client.list_officiels(offset=100)
        kwargs = self.mock_api_client.list_officiels.call_args[1]
        self.assertEqual(kwargs["offset"], 100)

    def test_026_list_pratiques_delegates_with_query_params(self):
        self.mock_api_client.list_pratiques.return_value = []
        self.client.list_pratiques(search="basket")
        kwargs = self.mock_api_client.list_pratiques.call_args[1]
        self.assertEqual(kwargs["search"], "basket")


class Test211FFBBAPIClientV2ListAllDelegation(unittest.TestCase):
    """Tests for list_all_xxx delegation on FFBBAPIClientV2."""

    def setUp(self):
        self.mock_api_client = Mock(spec=ApiFFBBAppClient)
        self.mock_meilisearch_client = Mock(spec=MeilisearchFFBBClient)
        self.client = FFBBAPIClientV2(
            api_ffbb_client=self.mock_api_client,
            meilisearch_ffbb_client=self.mock_meilisearch_client,
        )

    def test_027_list_all_rencontres_delegates(self):
        self.mock_api_client.list_all_rencontres.return_value = [Mock()]
        result = self.client.list_all_rencontres()
        self.mock_api_client.list_all_rencontres.assert_called_once()
        self.assertEqual(len(result), 1)

    def test_028_list_all_salles_delegates(self):
        self.mock_api_client.list_all_salles.return_value = [Mock()]
        result = self.client.list_all_salles()
        self.mock_api_client.list_all_salles.assert_called_once()
        self.assertEqual(len(result), 1)

    def test_029_list_all_terrains_delegates(self):
        self.mock_api_client.list_all_terrains.return_value = [Mock()]
        result = self.client.list_all_terrains()
        self.mock_api_client.list_all_terrains.assert_called_once()
        self.assertEqual(len(result), 1)

    def test_030_list_all_tournois_delegates(self):
        self.mock_api_client.list_all_tournois.return_value = [Mock()]
        result = self.client.list_all_tournois()
        self.mock_api_client.list_all_tournois.assert_called_once()
        self.assertEqual(len(result), 1)

    def test_031_list_all_engagements_delegates(self):
        self.mock_api_client.list_all_engagements.return_value = [Mock()]
        result = self.client.list_all_engagements()
        self.mock_api_client.list_all_engagements.assert_called_once()
        self.assertEqual(len(result), 1)

    def test_032_list_all_formations_delegates(self):
        self.mock_api_client.list_all_formations.return_value = [Mock()]
        result = self.client.list_all_formations()
        self.mock_api_client.list_all_formations.assert_called_once()
        self.assertEqual(len(result), 1)

    def test_033_list_all_entraineurs_delegates(self):
        self.mock_api_client.list_all_entraineurs.return_value = [Mock()]
        result = self.client.list_all_entraineurs()
        self.mock_api_client.list_all_entraineurs.assert_called_once()
        self.assertEqual(len(result), 1)

    def test_034_list_all_communes_delegates(self):
        self.mock_api_client.list_all_communes.return_value = [Mock()]
        result = self.client.list_all_communes()
        self.mock_api_client.list_all_communes.assert_called_once()
        self.assertEqual(len(result), 1)

    def test_035_list_all_officiels_delegates(self):
        self.mock_api_client.list_all_officiels.return_value = [Mock()]
        result = self.client.list_all_officiels()
        self.mock_api_client.list_all_officiels.assert_called_once()
        self.assertEqual(len(result), 1)

    def test_036_list_all_pratiques_delegates(self):
        self.mock_api_client.list_all_pratiques.return_value = [Mock()]
        result = self.client.list_all_pratiques()
        self.mock_api_client.list_all_pratiques.assert_called_once()
        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
