"""Tests for GetSallesResponse model."""

from __future__ import annotations

import unittest
from datetime import datetime
from typing import Any

from ffbb_api_client_v2.directus_ffbb.models.get_salles_response import (
    GetSallesResponse,
)
from ffbb_api_client_v2.models.cartographie import Cartographie

SAMPLE_DATA: dict[str, Any] = {
    "id": "200000004500123",
    "libelle": "Gymnase Pierre de Coubertin",
    "libelle2": "Salle principale",
    "adresse": "15 Avenue du General de Gaulle",
    "adresseComplement": "Entree cote parking",
    "numero": "SAL-78200-001",
    "telephone": "0134567899",
    "mail": "gymnase.coubertin@mairie-mantes.fr",
    "capaciteSpectateur": 1200,
    "commune": 78200,
    "cartographie": {
        "latitude": 48.9906,
        "longitude": 1.7169,
    },
    "date_created": "2023-06-15T12:00:00.000Z",
    "date_updated": "2025-09-30T18:00:00.000Z",
}


class TestGetSallesResponse(unittest.TestCase):
    def test_000_from_dict_valid(self) -> None:
        result = GetSallesResponse.from_dict(SAMPLE_DATA)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.id, "200000004500123")
        self.assertEqual(result.libelle, "Gymnase Pierre de Coubertin")
        self.assertEqual(result.libelle2, "Salle principale")
        self.assertEqual(result.adresse, "15 Avenue du General de Gaulle")
        self.assertEqual(result.adresseComplement, "Entree cote parking")
        self.assertEqual(result.numero, "SAL-78200-001")
        self.assertEqual(result.telephone, "0134567899")
        self.assertEqual(result.mail, "gymnase.coubertin@mairie-mantes.fr")
        self.assertEqual(result.capaciteSpectateur, 1200)
        self.assertEqual(result.commune, 78200)
        self.assertIsInstance(result.cartographie, Cartographie)
        assert isinstance(result.cartographie, Cartographie)
        self.assertIsNotNone(result.cartographie.latitude)
        self.assertAlmostEqual(result.cartographie.latitude, 48.9906)  # type: ignore[arg-type]
        self.assertIsInstance(result.date_created, datetime)
        self.assertIsInstance(result.date_updated, datetime)

    def test_001_from_dict_none(self) -> None:
        result = GetSallesResponse.from_dict(None)  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_002_from_dict_empty(self) -> None:
        result = GetSallesResponse.from_dict({})
        self.assertIsNone(result)

    def test_003_from_dict_errors(self) -> None:
        result = GetSallesResponse.from_dict({"errors": [{"message": "err"}]})
        self.assertIsNone(result)

    def test_004_from_dict_not_dict(self) -> None:
        result = GetSallesResponse.from_dict("not a dict")  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_005_from_dict_minimal(self) -> None:
        """Only required field 'id' present; optional fields default to None."""
        result = GetSallesResponse.from_dict({"id": "456"})
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.id, "456")
        self.assertIsNone(result.libelle)
        self.assertIsNone(result.libelle2)
        self.assertIsNone(result.adresse)
        self.assertIsNone(result.adresseComplement)
        self.assertIsNone(result.numero)
        self.assertIsNone(result.telephone)
        self.assertIsNone(result.mail)
        self.assertIsNone(result.capaciteSpectateur)
        self.assertIsNone(result.commune)
        self.assertIsNone(result.cartographie)
        self.assertIsNone(result.date_created)
        self.assertIsNone(result.date_updated)

    def test_006_from_dict_commune_none(self) -> None:
        """commune can be None when not provided."""
        data = {**SAMPLE_DATA, "commune": None}
        result = GetSallesResponse.from_dict(data)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertIsNone(result.commune)

    def test_007_from_dict_cartographie_none(self) -> None:
        """cartographie can be None when not provided."""
        data = {**SAMPLE_DATA, "cartographie": None}
        result = GetSallesResponse.from_dict(data)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertIsNone(result.cartographie)

    def test_008_from_list_valid(self) -> None:
        result = GetSallesResponse.from_list([SAMPLE_DATA, SAMPLE_DATA])
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], GetSallesResponse)
        self.assertIsInstance(result[1], GetSallesResponse)

    def test_009_from_list_empty(self) -> None:
        result = GetSallesResponse.from_list([])
        self.assertEqual(result, [])

    def test_010_from_list_filters_none_items(self) -> None:
        """from_list skips items that produce None (empty dicts, errors)."""
        data_list: list[dict[str, Any]] = [
            SAMPLE_DATA,
            {},
            {"errors": [{"message": "err"}]},
        ]
        result = GetSallesResponse.from_list(data_list)
        self.assertEqual(len(result), 1)

    def test_011_capacite_spectateur_integer(self) -> None:
        """capaciteSpectateur is kept as int."""
        result = GetSallesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.capaciteSpectateur, int)
        self.assertEqual(result.capaciteSpectateur, 1200)


if __name__ == "__main__":
    unittest.main()
