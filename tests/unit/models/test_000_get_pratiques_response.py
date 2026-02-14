"""Tests for GetPratiquesResponse model."""

from __future__ import annotations

import unittest
from datetime import datetime
from typing import Any

from ffbb_api_client_v2.directus_ffbb.models.get_pratiques_response import (
    GetPratiquesResponse,
)

SAMPLE_DATA: dict[str, Any] = {
    "id": "200000007890123",
    "titre": "Basket Sante Bien-Etre",
    "type": "basket_sante",
    "label": "Labellise FFBB",
    "description": "Seances de basket adapte pour adultes et seniors, axees sur le bien-etre et la sante.",
    "code": "BS-IDF-2025-001",
    "adresse": "25 Rue de la Republique, 93100 Montreuil",
    "email": "basket-sante@montreuil-basket.fr",
    "telephone": "01 48 58 12 34",
    "date_debut": "2025-09-01T00:00:00.000Z",
    "date_fin": "2026-06-30T00:00:00.000Z",
    "horaires_seances": "Mardi 18h-19h30 / Jeudi 10h-11h30",
    "jours": "Mardi, Jeudi",
    "nom_structure": "MONTREUIL BASKET CLUB",
    "adresse_structure": "25 Rue de la Republique",
    "mail_structure": "contact@montreuil-basket.fr",
    "nom_salle": "Gymnase Jean Jaures",
    "adresse_salle": "25 Rue de la Republique",
    "cp_salle": "93100",
    "ville_salle": "MONTREUIL",
    "cartographie": {"latitude": 48.8634, "longitude": 2.4433},
    "latitude": 48.8634,
    "longitude": 2.4433,
    "nombre_personnes": 30,
    "nombre_seances": 60,
    "public": "Adultes et seniors",
    "objectif": "Ameliorer la condition physique par le basketball adapte",
    "site_web": "https://www.montreuil-basket.fr",
    "facebook": "https://facebook.com/montreuilbasket",
    "twitter": "https://twitter.com/montreuilbasket",
    "date_created": "2025-07-15T10:00:00.000Z",
    "date_updated": "2025-08-20T16:45:00.000Z",
}


class TestGetPratiquesResponse(unittest.TestCase):
    def test_000_from_dict_valid(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        self.assertIsNotNone(result)

    def test_001_from_dict_none(self) -> None:
        result = GetPratiquesResponse.from_dict(None)  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_002_from_dict_empty(self) -> None:
        result = GetPratiquesResponse.from_dict({})
        self.assertIsNone(result)

    def test_003_from_dict_errors(self) -> None:
        result = GetPratiquesResponse.from_dict({"errors": [{"message": "err"}]})
        self.assertIsNone(result)

    def test_004_from_dict_not_dict(self) -> None:
        result = GetPratiquesResponse.from_dict("not a dict")  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_005_from_list_valid(self) -> None:
        result = GetPratiquesResponse.from_list([SAMPLE_DATA, SAMPLE_DATA])
        self.assertEqual(len(result), 2)

    def test_006_from_list_empty(self) -> None:
        result = GetPratiquesResponse.from_list([])
        self.assertEqual(result, [])

    def test_007_field_id(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.id, "200000007890123")

    def test_008_field_titre(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.titre, "Basket Sante Bien-Etre")

    def test_009_field_type(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.type, "basket_sante")

    def test_010_field_label(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.label, "Labellise FFBB")

    def test_011_field_description(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("basket adapte", result.description)  # type: ignore[operator]

    def test_012_field_code(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.code, "BS-IDF-2025-001")

    def test_013_field_adresse(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("Montreuil", result.adresse)  # type: ignore[operator]

    def test_014_field_email(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.email, "basket-sante@montreuil-basket.fr")

    def test_015_field_telephone(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.telephone, "01 48 58 12 34")

    def test_016_field_date_debut_fin(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.date_debut, "2025-09-01T00:00:00.000Z")
        self.assertEqual(result.date_fin, "2026-06-30T00:00:00.000Z")

    def test_017_field_horaires_seances(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("Mardi", result.horaires_seances)  # type: ignore[operator]

    def test_018_field_jours(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.jours, "Mardi, Jeudi")

    def test_019_field_nom_structure(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.nom_structure, "MONTREUIL BASKET CLUB")

    def test_020_field_adresse_structure(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.adresse_structure, "25 Rue de la Republique")

    def test_021_field_mail_structure(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.mail_structure, "contact@montreuil-basket.fr")

    def test_022_field_nom_salle(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.nom_salle, "Gymnase Jean Jaures")

    def test_023_field_adresse_salle(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.adresse_salle, "25 Rue de la Republique")

    def test_024_field_cp_salle(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.cp_salle, "93100")

    def test_025_field_ville_salle(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.ville_salle, "MONTREUIL")

    def test_026_field_cartographie(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        from ffbb_api_client_v2.models.cartographie import Cartographie

        self.assertIsInstance(result.cartographie, Cartographie)
        assert isinstance(result.cartographie, Cartographie)
        self.assertIsNotNone(result.cartographie.latitude)
        self.assertAlmostEqual(result.cartographie.latitude, 48.8634)  # type: ignore[arg-type]

    def test_027_field_latitude(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertAlmostEqual(result.latitude, 48.8634)  # type: ignore[arg-type]

    def test_028_field_longitude(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertAlmostEqual(result.longitude, 2.4433)  # type: ignore[arg-type]

    def test_029_field_date_created(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.date_created, datetime)

    def test_030_field_date_updated(self) -> None:
        result = GetPratiquesResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.date_updated, datetime)

    def test_031_nullable_floats_none(self) -> None:
        data = {**SAMPLE_DATA, "latitude": None, "longitude": None}
        result = GetPratiquesResponse.from_dict(data)
        assert result is not None
        self.assertIsNone(result.latitude)
        self.assertIsNone(result.longitude)

    def test_032_nullable_cartographie_none(self) -> None:
        data = {**SAMPLE_DATA, "cartographie": None}
        result = GetPratiquesResponse.from_dict(data)
        assert result is not None
        self.assertIsNone(result.cartographie)

    def test_033_from_list_filters_none_items(self) -> None:
        result = GetPratiquesResponse.from_list([SAMPLE_DATA, {}, SAMPLE_DATA])
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
