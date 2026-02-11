"""Tests for GetTerrainsResponse model."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.get_terrains_response import GetTerrainsResponse

SAMPLE_DATA: dict[str, Any] = {
    "id": "200000001234567",
    "nom": "Gymnase Pierre de Coubertin",
    "rue": "12 Avenue du Général de Gaulle",
    "numero": "T-75013-001",
    "largeur": 15.0,
    "longueur": 28.0,
    "accesLibre": True,
    "natureSol": {"id": "1", "libelle": "Parquet"},
    "commune": {
        "id": "75113",
        "nom": "PARIS 13EME ARRONDISSEMENT",
        "codePostal": "75013",
    },
    "cartographie": {"latitude": 48.8322, "longitude": 2.3561},
    "date_created": "2024-09-15T10:30:00.000Z",
    "date_updated": "2025-01-20T14:45:00.000Z",
}


class TestGetTerrainsResponse(unittest.TestCase):
    def test_from_dict_valid(self) -> None:
        result = GetTerrainsResponse.from_dict(SAMPLE_DATA)
        self.assertIsNotNone(result)

    def test_from_dict_none(self) -> None:
        result = GetTerrainsResponse.from_dict(None)  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_from_dict_empty(self) -> None:
        result = GetTerrainsResponse.from_dict({})
        self.assertIsNone(result)

    def test_from_dict_errors(self) -> None:
        result = GetTerrainsResponse.from_dict({"errors": [{"message": "err"}]})
        self.assertIsNone(result)

    def test_from_dict_not_dict(self) -> None:
        result = GetTerrainsResponse.from_dict("not a dict")  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_from_list_valid(self) -> None:
        result = GetTerrainsResponse.from_list([SAMPLE_DATA, SAMPLE_DATA])
        self.assertEqual(len(result), 2)

    def test_from_list_empty(self) -> None:
        result = GetTerrainsResponse.from_list([])
        self.assertEqual(result, [])

    def test_field_id(self) -> None:
        result = GetTerrainsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.id, "200000001234567")

    def test_field_nom(self) -> None:
        result = GetTerrainsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.nom, "Gymnase Pierre de Coubertin")

    def test_field_rue(self) -> None:
        result = GetTerrainsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.rue, "12 Avenue du Général de Gaulle")

    def test_field_numero(self) -> None:
        result = GetTerrainsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.numero, "T-75013-001")

    def test_field_largeur(self) -> None:
        result = GetTerrainsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.largeur, 15.0)

    def test_field_longueur(self) -> None:
        result = GetTerrainsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.longueur, 28.0)

    def test_field_acces_libre(self) -> None:
        result = GetTerrainsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertTrue(result.accesLibre)

    def test_field_nature_sol(self) -> None:
        result = GetTerrainsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.natureSol, dict)
        self.assertEqual(result.natureSol["libelle"], "Parquet")  # type: ignore[index]

    def test_field_commune(self) -> None:
        result = GetTerrainsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.commune, dict)
        self.assertEqual(result.commune["nom"], "PARIS 13EME ARRONDISSEMENT")  # type: ignore[index]

    def test_field_cartographie(self) -> None:
        result = GetTerrainsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.cartographie, dict)
        self.assertAlmostEqual(result.cartographie["latitude"], 48.8322)  # type: ignore[index]

    def test_field_date_created(self) -> None:
        result = GetTerrainsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.date_created, "2024-09-15T10:30:00.000Z")

    def test_field_date_updated(self) -> None:
        result = GetTerrainsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.date_updated, "2025-01-20T14:45:00.000Z")

    def test_nullable_floats_none(self) -> None:
        data = {**SAMPLE_DATA, "largeur": None, "longueur": None}
        result = GetTerrainsResponse.from_dict(data)
        assert result is not None
        self.assertIsNone(result.largeur)
        self.assertIsNone(result.longueur)

    def test_nullable_bool_none(self) -> None:
        data = {**SAMPLE_DATA, "accesLibre": None}
        result = GetTerrainsResponse.from_dict(data)
        assert result is not None
        self.assertIsNone(result.accesLibre)

    def test_nullable_dicts_none(self) -> None:
        data = {
            **SAMPLE_DATA,
            "natureSol": None,
            "commune": None,
            "cartographie": None,
        }
        result = GetTerrainsResponse.from_dict(data)
        assert result is not None
        self.assertIsNone(result.natureSol)
        self.assertIsNone(result.commune)
        self.assertIsNone(result.cartographie)

    def test_from_list_filters_none_items(self) -> None:
        result = GetTerrainsResponse.from_list([SAMPLE_DATA, {}, SAMPLE_DATA])
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
