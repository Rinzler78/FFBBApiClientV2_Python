"""
Unit tests for get_saisons_response.py
"""

import unittest
from datetime import datetime

from ffbb_api_client_v2.directus_ffbb.models.get_saisons_response import (
    GetSaisonsResponse,
)


class TestGetSaisonsResponse(unittest.TestCase):
    """Tests pour la classe GetSaisonsResponse"""

    def test_001_from_dict_none(self):
        """Test from_dict avec None"""
        result = GetSaisonsResponse.from_dict(None)  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_002_from_dict_empty_dict(self):
        """Test from_dict avec dict vide"""
        result = GetSaisonsResponse.from_dict({})
        self.assertIsNone(result)

    def test_003_from_dict_non_dict(self):
        """Test from_dict avec non-dict"""
        result = GetSaisonsResponse.from_dict("string")  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_004_from_dict_with_errors(self):
        """Test from_dict avec clé errors"""
        data = {"errors": [{"message": "Not found"}]}
        result = GetSaisonsResponse.from_dict(data)
        self.assertIsNone(result)

    def test_005_from_dict_minimal(self):
        """Test from_dict avec seulement id"""
        data = {"id": "42"}
        result = GetSaisonsResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "42")
        self.assertIsNone(result.actif)
        self.assertIsNone(result.debut)
        self.assertIsNone(result.fin)
        self.assertIsNone(result.code)
        self.assertIsNone(result.libelle)
        self.assertIsNone(result.enCours)
        self.assertIsNone(result.date_created)
        self.assertIsNone(result.date_updated)

    def test_006_from_dict_full(self):
        """Test from_dict avec toutes les clés"""
        data = {
            "id": "123",
            "actif": True,
            "debut": "2024-09-01",
            "fin": "2025-06-30",
            "code": "2024-2025",
            "libelle": "Saison 2024-2025",
            "enCours": False,
            "date_created": "2024-01-01T10:00:00Z",
            "date_updated": "2024-01-02T11:00:00Z",
        }
        result = GetSaisonsResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "123")
        self.assertTrue(result.actif)
        self.assertEqual(result.debut, "2024-09-01")
        self.assertEqual(result.fin, "2025-06-30")
        self.assertEqual(result.code, "2024-2025")
        self.assertEqual(result.libelle, "Saison 2024-2025")
        self.assertFalse(result.enCours)
        self.assertIsInstance(result.date_created, datetime)
        self.assertIsInstance(result.date_updated, datetime)

    def test_007_from_dict_partial_fields(self):
        """Test from_dict avec champs partiels"""
        data = {
            "id": "456",
            "actif": False,
            "code": "test-code",
            "enCours": True,
        }
        result = GetSaisonsResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "456")
        self.assertFalse(result.actif)
        self.assertEqual(result.code, "test-code")
        self.assertTrue(result.enCours)
        # Autres champs None
        self.assertIsNone(result.debut)
        self.assertIsNone(result.fin)
        self.assertIsNone(result.libelle)
        self.assertIsNone(result.date_created)
        self.assertIsNone(result.date_updated)

    def test_008_from_dict_empty_strings(self):
        """Test from_dict avec chaînes vides — from_str preserves empty strings, from_datetime returns None"""
        data = {
            "id": "789",
            "debut": "",
            "fin": "",
            "code": "",
            "libelle": "",
            "date_created": "",
            "date_updated": "",
        }
        result = GetSaisonsResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "789")
        self.assertEqual(result.debut, "")
        self.assertEqual(result.fin, "")
        self.assertEqual(result.code, "")
        self.assertEqual(result.libelle, "")
        self.assertIsNone(result.date_created)
        self.assertIsNone(result.date_updated)

    def test_009_from_list_empty(self):
        """Test from_list avec liste vide"""
        result = GetSaisonsResponse.from_list([])
        self.assertEqual(result, [])

    def test_010_from_list_none(self):
        """Test from_list avec None"""
        result = GetSaisonsResponse.from_list(None)  # type: ignore[arg-type]
        self.assertEqual(result, [])

    def test_011_from_list_valid_items(self):
        """Test from_list avec items valides"""
        data_list = [
            {"id": "1", "libelle": "Saison 1"},
            {"id": "2", "libelle": "Saison 2", "actif": True},
        ]
        result = GetSaisonsResponse.from_list(data_list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[0].libelle, "Saison 1")
        self.assertEqual(result[1].id, "2")
        self.assertEqual(result[1].libelle, "Saison 2")
        self.assertTrue(result[1].actif)

    def test_012_from_list_mixed_items(self):
        """Test from_list avec mélange d'items valides/invalides"""
        data_list = [
            {"id": "1", "libelle": "Saison 1"},
            None,  # Invalid
            {"errors": [{"message": "error"}]},  # Invalid
            {},  # Invalid (no id)
            {"id": "2", "libelle": "Saison 2"},
        ]
        result = GetSaisonsResponse.from_list(data_list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[1].id, "2")

    def test_013_from_dict_id_conversion(self):
        """Test que id est toujours converti en string"""
        data = {"id": 123}
        result = GetSaisonsResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "123")  # Converted to string


if __name__ == "__main__":
    unittest.main()
