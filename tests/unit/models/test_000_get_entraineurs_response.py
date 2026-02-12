"""Tests for GetEntraineursResponse model."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.get_entraineurs_response import GetEntraineursResponse

SAMPLE_DATA: dict[str, Any] = {
    "idLicence": "0078-654321",
    "nom": "LEFEVRE",
    "prenom": "Marie",
    "adresse1": "12 Rue du Panier",
    "adresse2": "Batiment C",
    "commune": {
        "id": "c1d2e3f4-0000-1111-2222-333344445555",
        "libelle": "MANTES-LA-JOLIE",
        "codePostal": "78200",
    },
    "email": "m.lefevre@basket78.fr",
    "telephoneDomicile": "0134567890",
    "telephonePortable": "0612345678",
    "telephoneTravail": "0145678901",
    "date_created": "2024-03-10T09:15:00.000Z",
    "date_updated": "2025-12-01T11:00:00.000Z",
}


class TestGetEntraineursResponse(unittest.TestCase):
    def test_000_from_dict_valid(self) -> None:
        result = GetEntraineursResponse.from_dict(SAMPLE_DATA)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.idLicence, "0078-654321")
        self.assertEqual(result.nom, "LEFEVRE")
        self.assertEqual(result.prenom, "Marie")
        self.assertEqual(result.adresse1, "12 Rue du Panier")
        self.assertEqual(result.adresse2, "Batiment C")
        self.assertIsInstance(result.commune, dict)
        self.assertEqual(result.commune["libelle"], "MANTES-LA-JOLIE")  # type: ignore[index]
        self.assertEqual(result.email, "m.lefevre@basket78.fr")
        self.assertEqual(result.telephoneDomicile, "0134567890")
        self.assertEqual(result.telephonePortable, "0612345678")
        self.assertEqual(result.telephoneTravail, "0145678901")
        self.assertEqual(result.date_created, "2024-03-10T09:15:00.000Z")
        self.assertEqual(result.date_updated, "2025-12-01T11:00:00.000Z")

    def test_001_from_dict_none(self) -> None:
        result = GetEntraineursResponse.from_dict(None)  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_002_from_dict_empty(self) -> None:
        result = GetEntraineursResponse.from_dict({})
        self.assertIsNone(result)

    def test_003_from_dict_errors(self) -> None:
        result = GetEntraineursResponse.from_dict({"errors": [{"message": "err"}]})
        self.assertIsNone(result)

    def test_004_from_dict_not_dict(self) -> None:
        result = GetEntraineursResponse.from_dict("not a dict")  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_005_from_dict_minimal(self) -> None:
        """Only required field 'idLicence' present; optional fields default to None."""
        result = GetEntraineursResponse.from_dict({"idLicence": "0092-111111"})
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.idLicence, "0092-111111")
        self.assertIsNone(result.nom)
        self.assertIsNone(result.prenom)
        self.assertIsNone(result.adresse1)
        self.assertIsNone(result.adresse2)
        self.assertIsNone(result.commune)
        self.assertIsNone(result.email)
        self.assertIsNone(result.telephoneDomicile)
        self.assertIsNone(result.telephonePortable)
        self.assertIsNone(result.telephoneTravail)
        self.assertIsNone(result.date_created)
        self.assertIsNone(result.date_updated)

    def test_006_from_dict_commune_none(self) -> None:
        """commune can be None when not provided."""
        data = {**SAMPLE_DATA, "commune": None}
        result = GetEntraineursResponse.from_dict(data)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertIsNone(result.commune)

    def test_007_from_list_valid(self) -> None:
        result = GetEntraineursResponse.from_list([SAMPLE_DATA, SAMPLE_DATA])
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], GetEntraineursResponse)
        self.assertIsInstance(result[1], GetEntraineursResponse)

    def test_008_from_list_empty(self) -> None:
        result = GetEntraineursResponse.from_list([])
        self.assertEqual(result, [])

    def test_009_from_list_filters_none_items(self) -> None:
        """from_list skips items that produce None (empty dicts, errors)."""
        data_list: list[dict[str, Any]] = [
            SAMPLE_DATA,
            {},
            {"errors": [{"message": "err"}]},
        ]
        result = GetEntraineursResponse.from_list(data_list)
        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
