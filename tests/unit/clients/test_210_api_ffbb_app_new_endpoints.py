"""Unit tests for ApiFFBBAppClient new Directus endpoints."""

import unittest
from unittest.mock import Mock, patch

from requests_cache import CachedSession

from ffbb_api_client_v2.clients.api_ffbb_app_client import ApiFFBBAppClient


class Test210ApiFFBBAppNewEndpointsRencontres(unittest.TestCase):
    """Tests for rencontres endpoints on ApiFFBBAppClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_000_get_rencontre_success(self, mock_http):
        """Test get_rencontre returns a rencontre object on success."""
        mock_http.return_value = {
            "data": {"id": "123", "nomEquipe1": "Paris", "nomEquipe2": "Lyon"}
        }
        result = self.client.get_rencontre(123)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "123")
        self.assertEqual(result.nomEquipe1, "Paris")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_001_get_rencontre_empty(self, mock_http):
        """Test get_rencontre returns None when data is None."""
        mock_http.return_value = {"data": None}
        result = self.client.get_rencontre(999)
        self.assertIsNone(result)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_002_list_rencontres_success(self, mock_http):
        """Test list_rencontres returns a list of rencontre objects."""
        mock_http.return_value = {
            "data": [{"id": "1", "nomEquipe1": "A"}, {"id": "2", "nomEquipe1": "B"}]
        }
        result = self.client.list_rencontres(limit=10)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[1].id, "2")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_003_list_rencontres_empty(self, mock_http):
        """Test list_rencontres returns empty list when data is empty."""
        mock_http.return_value = {"data": []}
        result = self.client.list_rencontres(limit=10)
        self.assertEqual(result, [])


class Test210ApiFFBBAppNewEndpointsSalles(unittest.TestCase):
    """Tests for salles endpoints on ApiFFBBAppClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_004_get_salle_success(self, mock_http):
        """Test get_salle returns a salle object on success."""
        mock_http.return_value = {"data": {"id": "456", "libelle": "Salle Omnisports"}}
        result = self.client.get_salle(456)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "456")
        self.assertEqual(result.libelle, "Salle Omnisports")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_005_get_salle_empty(self, mock_http):
        """Test get_salle returns None when data is None."""
        mock_http.return_value = {"data": None}
        result = self.client.get_salle(999)
        self.assertIsNone(result)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_006_list_salles_success(self, mock_http):
        """Test list_salles returns a list of salle objects."""
        mock_http.return_value = {
            "data": [
                {"id": "1", "libelle": "Salle A"},
                {"id": "2", "libelle": "Salle B"},
            ]
        }
        result = self.client.list_salles(limit=10)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[1].id, "2")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_007_list_salles_empty(self, mock_http):
        """Test list_salles returns empty list when data is empty."""
        mock_http.return_value = {"data": []}
        result = self.client.list_salles(limit=10)
        self.assertEqual(result, [])


class Test210ApiFFBBAppNewEndpointsTerrains(unittest.TestCase):
    """Tests for terrains endpoints on ApiFFBBAppClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_008_get_terrain_success(self, mock_http):
        """Test get_terrain returns a terrain object on success."""
        mock_http.return_value = {"data": {"id": "789", "nom": "Terrain Central"}}
        result = self.client.get_terrain(789)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "789")
        self.assertEqual(result.nom, "Terrain Central")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_009_get_terrain_empty(self, mock_http):
        """Test get_terrain returns None when data is None."""
        mock_http.return_value = {"data": None}
        result = self.client.get_terrain(999)
        self.assertIsNone(result)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_010_list_terrains_success(self, mock_http):
        """Test list_terrains returns a list of terrain objects."""
        mock_http.return_value = {
            "data": [{"id": "1", "nom": "Terrain A"}, {"id": "2", "nom": "Terrain B"}]
        }
        result = self.client.list_terrains(limit=10)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[1].id, "2")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_011_list_terrains_empty(self, mock_http):
        """Test list_terrains returns empty list when data is empty."""
        mock_http.return_value = {"data": []}
        result = self.client.list_terrains(limit=10)
        self.assertEqual(result, [])


class Test210ApiFFBBAppNewEndpointsTournois(unittest.TestCase):
    """Tests for tournois endpoints on ApiFFBBAppClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_012_get_tournoi_success(self, mock_http):
        """Test get_tournoi returns a tournoi object on success."""
        mock_http.return_value = {
            "data": {"id": "101", "nom": "Tournoi 3x3", "code": "T3X3"}
        }
        result = self.client.get_tournoi(101)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "101")
        self.assertEqual(result.nom, "Tournoi 3x3")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_013_get_tournoi_empty(self, mock_http):
        """Test get_tournoi returns None when data is None."""
        mock_http.return_value = {"data": None}
        result = self.client.get_tournoi(999)
        self.assertIsNone(result)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_014_list_tournois_success(self, mock_http):
        """Test list_tournois returns a list of tournoi objects."""
        mock_http.return_value = {
            "data": [{"id": "1", "nom": "T1"}, {"id": "2", "nom": "T2"}]
        }
        result = self.client.list_tournois(limit=10)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[1].id, "2")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_015_list_tournois_empty(self, mock_http):
        """Test list_tournois returns empty list when data is empty."""
        mock_http.return_value = {"data": []}
        result = self.client.list_tournois(limit=10)
        self.assertEqual(result, [])


class Test210ApiFFBBAppNewEndpointsEngagements(unittest.TestCase):
    """Tests for engagements endpoints on ApiFFBBAppClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_016_get_engagement_success(self, mock_http):
        """Test get_engagement returns an engagement object on success."""
        mock_http.return_value = {
            "data": {"id": "200", "nom": "Engagement A", "nomEquipe": "Equipe 1"}
        }
        result = self.client.get_engagement(200)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "200")
        self.assertEqual(result.nom, "Engagement A")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_017_get_engagement_empty(self, mock_http):
        """Test get_engagement returns None when data is None."""
        mock_http.return_value = {"data": None}
        result = self.client.get_engagement(999)
        self.assertIsNone(result)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_018_list_engagements_success(self, mock_http):
        """Test list_engagements returns a list of engagement objects."""
        mock_http.return_value = {
            "data": [{"id": "1", "nom": "E1"}, {"id": "2", "nom": "E2"}]
        }
        result = self.client.list_engagements(limit=10)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[1].id, "2")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_019_list_engagements_empty(self, mock_http):
        """Test list_engagements returns empty list when data is empty."""
        mock_http.return_value = {"data": []}
        result = self.client.list_engagements(limit=10)
        self.assertEqual(result, [])


class Test210ApiFFBBAppNewEndpointsFormations(unittest.TestCase):
    """Tests for formations endpoints on ApiFFBBAppClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_020_get_formation_success(self, mock_http):
        """Test get_formation returns a formation object on success."""
        mock_http.return_value = {"data": {"id": "f-001", "title": "Formation Arbitre"}}
        result = self.client.get_formation("f-001")
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "f-001")
        self.assertEqual(result.title, "Formation Arbitre")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_021_get_formation_empty(self, mock_http):
        """Test get_formation returns None when data is None."""
        mock_http.return_value = {"data": None}
        result = self.client.get_formation("nonexistent")
        self.assertIsNone(result)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_022_list_formations_success(self, mock_http):
        """Test list_formations returns a list of formation objects."""
        mock_http.return_value = {
            "data": [{"id": "f1", "title": "F1"}, {"id": "f2", "title": "F2"}]
        }
        result = self.client.list_formations(limit=10)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "f1")
        self.assertEqual(result[1].id, "f2")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_023_list_formations_empty(self, mock_http):
        """Test list_formations returns empty list when data is empty."""
        mock_http.return_value = {"data": []}
        result = self.client.list_formations(limit=10)
        self.assertEqual(result, [])


class Test210ApiFFBBAppNewEndpointsEntraineurs(unittest.TestCase):
    """Tests for entraineurs endpoints on ApiFFBBAppClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_024_get_entraineur_success(self, mock_http):
        """Test get_entraineur returns an entraineur object on success."""
        mock_http.return_value = {
            "data": {"idLicence": "LIC001", "nom": "Dupont", "prenom": "Jean"}
        }
        result = self.client.get_entraineur(300)
        self.assertIsNotNone(result)
        self.assertEqual(result.idLicence, "LIC001")
        self.assertEqual(result.nom, "Dupont")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_025_get_entraineur_empty(self, mock_http):
        """Test get_entraineur returns None when data is None."""
        mock_http.return_value = {"data": None}
        result = self.client.get_entraineur(999)
        self.assertIsNone(result)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_026_list_entraineurs_success(self, mock_http):
        """Test list_entraineurs returns a list of entraineur objects."""
        mock_http.return_value = {
            "data": [
                {"idLicence": "L1", "nom": "A"},
                {"idLicence": "L2", "nom": "B"},
            ]
        }
        result = self.client.list_entraineurs(limit=10)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].idLicence, "L1")
        self.assertEqual(result[1].idLicence, "L2")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_027_list_entraineurs_empty(self, mock_http):
        """Test list_entraineurs returns empty list when data is empty."""
        mock_http.return_value = {"data": []}
        result = self.client.list_entraineurs(limit=10)
        self.assertEqual(result, [])


class Test210ApiFFBBAppNewEndpointsCommunes(unittest.TestCase):
    """Tests for communes endpoints on ApiFFBBAppClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_028_list_communes_success(self, mock_http):
        """Test list_communes returns a list of commune objects."""
        mock_http.return_value = {
            "data": [
                {"id": "1", "codeInsee": "75056", "libelle": "Paris"},
                {"id": "2", "codeInsee": "69123", "libelle": "Lyon"},
            ]
        }
        result = self.client.list_communes(limit=10)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[0].libelle, "Paris")
        self.assertEqual(result[1].id, "2")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_029_list_communes_empty(self, mock_http):
        """Test list_communes returns empty list when data is empty."""
        mock_http.return_value = {"data": []}
        result = self.client.list_communes(limit=10)
        self.assertEqual(result, [])


class Test210ApiFFBBAppNewEndpointsOfficiels(unittest.TestCase):
    """Tests for officiels endpoints on ApiFFBBAppClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_030_list_officiels_success(self, mock_http):
        """Test list_officiels returns a list of officiel objects."""
        mock_http.return_value = {
            "data": [
                {"nom": "Martin", "prenom": "Pierre"},
                {"nom": "Bernard", "prenom": "Marie"},
            ]
        }
        result = self.client.list_officiels(limit=10)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].nom, "Martin")
        self.assertEqual(result[1].nom, "Bernard")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_031_list_officiels_empty(self, mock_http):
        """Test list_officiels returns empty list when data is empty."""
        mock_http.return_value = {"data": []}
        result = self.client.list_officiels(limit=10)
        self.assertEqual(result, [])


class Test210ApiFFBBAppNewEndpointsPratiques(unittest.TestCase):
    """Tests for pratiques endpoints on ApiFFBBAppClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_032_list_pratiques_success(self, mock_http):
        """Test list_pratiques returns a list of pratique objects."""
        mock_http.return_value = {
            "data": [
                {"id": "1", "titre": "Baby Basket"},
                {"id": "2", "titre": "Micro Basket"},
            ]
        }
        result = self.client.list_pratiques(limit=10)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[0].titre, "Baby Basket")
        self.assertEqual(result[1].id, "2")

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_033_list_pratiques_empty(self, mock_http):
        """Test list_pratiques returns empty list when data is empty."""
        mock_http.return_value = {"data": []}
        result = self.client.list_pratiques(limit=10)
        self.assertEqual(result, [])


class Test210ApiFFBBAppQueryParamsRencontres(unittest.TestCase):
    """Tests for query params on list_rencontres."""

    def setUp(self):
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_034_list_rencontres_with_filter(self, mock_http):
        """Test list_rencontres passes filter param."""
        mock_http.return_value = {"data": []}
        self.client.list_rencontres(filter_criteria='{"actif":{"_eq":true}}')
        url = mock_http.call_args[0][0]
        self.assertIn("filter=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_035_list_rencontres_with_sort(self, mock_http):
        """Test list_rencontres passes sort param."""
        mock_http.return_value = {"data": []}
        self.client.list_rencontres(sort=["date_rencontre", "-id"])
        url = mock_http.call_args[0][0]
        self.assertIn("sort%5B%5D=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_036_list_rencontres_with_offset(self, mock_http):
        """Test list_rencontres passes offset param."""
        mock_http.return_value = {"data": []}
        self.client.list_rencontres(offset=20)
        url = mock_http.call_args[0][0]
        self.assertIn("offset=20", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_037_list_rencontres_with_search(self, mock_http):
        """Test list_rencontres passes search param."""
        mock_http.return_value = {"data": []}
        self.client.list_rencontres(search="paris")
        url = mock_http.call_args[0][0]
        self.assertIn("search=", url)


class Test210ApiFFBBAppQueryParamsSalles(unittest.TestCase):
    """Tests for query params on list_salles."""

    def setUp(self):
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_038_list_salles_with_filter(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_salles(filter_criteria='{"actif":{"_eq":true}}')
        url = mock_http.call_args[0][0]
        self.assertIn("filter=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_039_list_salles_with_sort(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_salles(sort=["libelle"])
        url = mock_http.call_args[0][0]
        self.assertIn("sort%5B%5D=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_040_list_salles_with_offset(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_salles(offset=20)
        url = mock_http.call_args[0][0]
        self.assertIn("offset=20", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_041_list_salles_with_search(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_salles(search="paris")
        url = mock_http.call_args[0][0]
        self.assertIn("search=", url)


class Test210ApiFFBBAppQueryParamsTerrains(unittest.TestCase):
    """Tests for query params on list_terrains."""

    def setUp(self):
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_042_list_terrains_with_filter(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_terrains(filter_criteria='{"actif":{"_eq":true}}')
        url = mock_http.call_args[0][0]
        self.assertIn("filter=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_043_list_terrains_with_sort(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_terrains(sort=["nom"])
        url = mock_http.call_args[0][0]
        self.assertIn("sort%5B%5D=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_044_list_terrains_with_offset(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_terrains(offset=20)
        url = mock_http.call_args[0][0]
        self.assertIn("offset=20", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_045_list_terrains_with_search(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_terrains(search="lyon")
        url = mock_http.call_args[0][0]
        self.assertIn("search=", url)


class Test210ApiFFBBAppQueryParamsTournois(unittest.TestCase):
    """Tests for query params on list_tournois."""

    def setUp(self):
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_046_list_tournois_with_filter(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_tournois(filter_criteria='{"actif":{"_eq":true}}')
        url = mock_http.call_args[0][0]
        self.assertIn("filter=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_047_list_tournois_with_sort(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_tournois(sort=["nom"])
        url = mock_http.call_args[0][0]
        self.assertIn("sort%5B%5D=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_048_list_tournois_with_offset(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_tournois(offset=20)
        url = mock_http.call_args[0][0]
        self.assertIn("offset=20", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_049_list_tournois_with_search(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_tournois(search="3x3")
        url = mock_http.call_args[0][0]
        self.assertIn("search=", url)


class Test210ApiFFBBAppQueryParamsEngagements(unittest.TestCase):
    """Tests for query params on list_engagements."""

    def setUp(self):
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_050_list_engagements_with_filter(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_engagements(filter_criteria='{"actif":{"_eq":true}}')
        url = mock_http.call_args[0][0]
        self.assertIn("filter=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_051_list_engagements_with_sort(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_engagements(sort=["nom"])
        url = mock_http.call_args[0][0]
        self.assertIn("sort%5B%5D=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_052_list_engagements_with_offset(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_engagements(offset=20)
        url = mock_http.call_args[0][0]
        self.assertIn("offset=20", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_053_list_engagements_with_search(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_engagements(search="equipe")
        url = mock_http.call_args[0][0]
        self.assertIn("search=", url)


class Test210ApiFFBBAppQueryParamsFormations(unittest.TestCase):
    """Tests for query params on list_formations."""

    def setUp(self):
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_054_list_formations_with_filter(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_formations(filter_criteria='{"actif":{"_eq":true}}')
        url = mock_http.call_args[0][0]
        self.assertIn("filter=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_055_list_formations_with_sort(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_formations(sort=["title"])
        url = mock_http.call_args[0][0]
        self.assertIn("sort%5B%5D=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_056_list_formations_with_offset(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_formations(offset=20)
        url = mock_http.call_args[0][0]
        self.assertIn("offset=20", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_057_list_formations_with_search(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_formations(search="arbitre")
        url = mock_http.call_args[0][0]
        self.assertIn("search=", url)


class Test210ApiFFBBAppQueryParamsEntraineurs(unittest.TestCase):
    """Tests for query params on list_entraineurs."""

    def setUp(self):
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_058_list_entraineurs_with_filter(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_entraineurs(filter_criteria='{"actif":{"_eq":true}}')
        url = mock_http.call_args[0][0]
        self.assertIn("filter=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_059_list_entraineurs_with_sort(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_entraineurs(sort=["nom"])
        url = mock_http.call_args[0][0]
        self.assertIn("sort%5B%5D=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_060_list_entraineurs_with_offset(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_entraineurs(offset=20)
        url = mock_http.call_args[0][0]
        self.assertIn("offset=20", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_061_list_entraineurs_with_search(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_entraineurs(search="dupont")
        url = mock_http.call_args[0][0]
        self.assertIn("search=", url)


class Test210ApiFFBBAppQueryParamsCommunes(unittest.TestCase):
    """Tests for query params on list_communes."""

    def setUp(self):
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_062_list_communes_with_filter(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_communes(filter_criteria='{"actif":{"_eq":true}}')
        url = mock_http.call_args[0][0]
        self.assertIn("filter=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_063_list_communes_with_sort(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_communes(sort=["libelle"])
        url = mock_http.call_args[0][0]
        self.assertIn("sort%5B%5D=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_064_list_communes_with_offset(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_communes(offset=20)
        url = mock_http.call_args[0][0]
        self.assertIn("offset=20", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_065_list_communes_with_search(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_communes(search="paris")
        url = mock_http.call_args[0][0]
        self.assertIn("search=", url)


class Test210ApiFFBBAppQueryParamsOfficiels(unittest.TestCase):
    """Tests for query params on list_officiels."""

    def setUp(self):
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_066_list_officiels_with_filter(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_officiels(filter_criteria='{"actif":{"_eq":true}}')
        url = mock_http.call_args[0][0]
        self.assertIn("filter=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_067_list_officiels_with_sort(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_officiels(sort=["nom"])
        url = mock_http.call_args[0][0]
        self.assertIn("sort%5B%5D=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_068_list_officiels_with_offset(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_officiels(offset=20)
        url = mock_http.call_args[0][0]
        self.assertIn("offset=20", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_069_list_officiels_with_search(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_officiels(search="martin")
        url = mock_http.call_args[0][0]
        self.assertIn("search=", url)


class Test210ApiFFBBAppQueryParamsPratiques(unittest.TestCase):
    """Tests for query params on list_pratiques."""

    def setUp(self):
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_070_list_pratiques_with_filter(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_pratiques(filter_criteria='{"actif":{"_eq":true}}')
        url = mock_http.call_args[0][0]
        self.assertIn("filter=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_071_list_pratiques_with_sort(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_pratiques(sort=["titre"])
        url = mock_http.call_args[0][0]
        self.assertIn("sort%5B%5D=", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_072_list_pratiques_with_offset(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_pratiques(offset=20)
        url = mock_http.call_args[0][0]
        self.assertIn("offset=20", url)

    @patch("ffbb_api_client_v2.clients.api_ffbb_app_client.http_get_json")
    def test_073_list_pratiques_with_search(self, mock_http):
        mock_http.return_value = {"data": []}
        self.client.list_pratiques(search="basket")
        url = mock_http.call_args[0][0]
        self.assertIn("search=", url)


if __name__ == "__main__":
    unittest.main()
