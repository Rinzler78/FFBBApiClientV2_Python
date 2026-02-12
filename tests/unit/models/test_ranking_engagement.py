"""
Unit tests for ranking_engagement.py
"""

import unittest

from ffbb_api_client_v2.models.ranking_engagement import RankingEngagement


class TestRankingEngagement(unittest.TestCase):
    """Tests pour la classe RankingEngagement"""

    def test_001_from_dict_none(self):
        """Test from_dict avec None"""
        result = RankingEngagement.from_dict(None)  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_002_from_dict_empty_dict(self):
        """Test from_dict avec dict vide"""
        result = RankingEngagement.from_dict({})
        self.assertIsNone(result)

    def test_003_from_dict_minimal(self):
        """Test from_dict avec seulement id et nom requis"""
        data = {"id": "eng-001", "nom": "Club Test"}
        result = RankingEngagement.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "eng-001")
        self.assertEqual(result.nom, "Club Test")
        self.assertIsNone(result.nom_usuel)
        self.assertIsNone(result.code_abrege)
        self.assertIsNone(result.numero_equ)
        self.assertIsNone(result.numero_equipe)
        self.assertIsNone(result.logo_id)
        self.assertIsNone(result.logo_gradient)

    def test_004_from_dict_full(self):
        """Test from_dict avec toutes les clés"""
        data = {
            "id": "eng-002",
            "nom": "Club Paris BC",
            "nomUsuel": "Paris BC",
            "codeAbrege": "PBC",
            "numeroEqu": "1",
            "numeroEquipe": "001",
            "logo": {"id": "logo-123", "gradient_color": "#FF0000"},
        }
        result = RankingEngagement.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "eng-002")
        self.assertEqual(result.nom, "Club Paris BC")
        self.assertEqual(result.nom_usuel, "Paris BC")
        self.assertEqual(result.code_abrege, "PBC")
        self.assertEqual(result.numero_equ, "1")
        self.assertEqual(result.numero_equipe, "001")
        self.assertEqual(result.logo_id, "logo-123")
        self.assertEqual(result.logo_gradient, "#FF0000")

    def test_005_from_dict_logo_none(self):
        """Test from_dict avec logo = None"""
        data = {
            "id": "eng-003",
            "nom": "Club Lyon",
            "logo": None,
        }
        result = RankingEngagement.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "eng-003")
        self.assertEqual(result.nom, "Club Lyon")
        self.assertIsNone(result.logo_id)
        self.assertIsNone(result.logo_gradient)

    def test_006_from_dict_logo_not_dict(self):
        """Test from_dict avec logo qui n'est pas un dict"""
        data = {
            "id": "eng-004",
            "nom": "Club Marseille",
            "logo": "invalid_logo",
        }
        result = RankingEngagement.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "eng-004")
        self.assertEqual(result.nom, "Club Marseille")
        self.assertIsNone(result.logo_id)
        self.assertIsNone(result.logo_gradient)

    def test_007_from_dict_logo_empty_dict(self):
        """Test from_dict avec logo = {}"""
        data = {
            "id": "eng-005",
            "nom": "Club Nice",
            "logo": {},
        }
        result = RankingEngagement.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "eng-005")
        self.assertEqual(result.nom, "Club Nice")
        self.assertIsNone(result.logo_id)
        self.assertIsNone(result.logo_gradient)

    def test_008_from_dict_logo_partial(self):
        """Test from_dict avec logo partiel (seulement id)"""
        data = {
            "id": "eng-006",
            "nom": "Club Toulouse",
            "logo": {"id": "logo-456"},
        }
        result = RankingEngagement.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "eng-006")
        self.assertEqual(result.nom, "Club Toulouse")
        self.assertEqual(result.logo_id, "logo-456")
        self.assertIsNone(result.logo_gradient)

    def test_009_from_dict_logo_partial_gradient_only(self):
        """Test from_dict avec logo partiel (seulement gradient_color)"""
        data = {
            "id": "eng-007",
            "nom": "Club Bordeaux",
            "logo": {"gradient_color": "#00FF00"},
        }
        result = RankingEngagement.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "eng-007")
        self.assertEqual(result.nom, "Club Bordeaux")
        self.assertIsNone(result.logo_id)
        self.assertEqual(result.logo_gradient, "#00FF00")

    def test_010_from_dict_id_conversion(self):
        """Test que id est converti en string"""
        data = {"id": 123, "nom": "Club Test"}
        result = RankingEngagement.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "123")

    def test_011_from_dict_nom_conversion(self):
        """Test que nom est converti en string"""
        data = {"id": "eng-008", "nom": 456}
        result = RankingEngagement.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.nom, "456")


if __name__ == "__main__":
    unittest.main()
