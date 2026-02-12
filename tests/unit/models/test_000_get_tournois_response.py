"""Tests for GetTournoisResponse model."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.get_tournois_response import GetTournoisResponse

SAMPLE_DATA: dict[str, Any] = {
    "id": "200000004567890",
    "nom": "Tournoi de la Pentecote 3x3",
    "code": "TRN-2025-IDF-042",
    "sexe": "Mixte",
    "debut": "2025-06-07T08:00:00.000Z",
    "fin": "2025-06-08T18:00:00.000Z",
    "description": "Tournoi 3x3 ouvert a toutes categories, organise par le club de Levallois.",
    "adresse": "15 Rue Aristide Briand",
    "adresseComplement": "Gymnase Marcel Cerdan",
    "mailOrganisateur": "contact@levallois-basket.fr",
    "nomOrganisateur": "LEVALLOIS SPORTING CLUB BASKET",
    "telephoneOrganisateur": "01 47 37 12 34",
    "urlOrganisateur": "https://www.levallois-basket.fr",
    "siteChoisi": "Gymnase Marcel Cerdan - Levallois-Perret",
    "nbParticipantPrevu": 24,
    "tarifOrganisateur": "15 EUR par equipe",
    "ageMin": 12,
    "ageMax": 18,
    "tournoiType": {"id": "3", "libelle": "3x3"},
    "commune": {
        "id": "92044",
        "nom": "LEVALLOIS-PERRET",
        "codePostal": "92300",
    },
    "cartographie": {"latitude": 48.8938, "longitude": 2.2882},
    "tournoiTypes3x3": [
        {"id": "1", "libelle": "U13"},
        {"id": "2", "libelle": "U15"},
    ],
    "document_flyer": {"id": "abc-123", "filename": "flyer_tournoi.pdf"},
    "categorieChampionnat3x3Id": "CAT-3X3-001",
    "categorieChampionnat3x3Libelle": "Championnat 3x3 U15",
    "date_created": "2025-03-01T09:00:00.000Z",
    "date_updated": "2025-05-15T16:30:00.000Z",
}


class TestGetTournoisResponse(unittest.TestCase):
    def test_000_from_dict_valid(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        self.assertIsNotNone(result)

    def test_001_from_dict_none(self) -> None:
        result = GetTournoisResponse.from_dict(None)  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_002_from_dict_empty(self) -> None:
        result = GetTournoisResponse.from_dict({})
        self.assertIsNone(result)

    def test_003_from_dict_errors(self) -> None:
        result = GetTournoisResponse.from_dict({"errors": [{"message": "err"}]})
        self.assertIsNone(result)

    def test_004_from_dict_not_dict(self) -> None:
        result = GetTournoisResponse.from_dict("not a dict")  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_005_from_list_valid(self) -> None:
        result = GetTournoisResponse.from_list([SAMPLE_DATA, SAMPLE_DATA])
        self.assertEqual(len(result), 2)

    def test_006_from_list_empty(self) -> None:
        result = GetTournoisResponse.from_list([])
        self.assertEqual(result, [])

    def test_007_field_id(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.id, "200000004567890")

    def test_008_field_nom(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.nom, "Tournoi de la Pentecote 3x3")

    def test_009_field_code(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.code, "TRN-2025-IDF-042")

    def test_010_field_sexe(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.sexe, "Mixte")

    def test_011_field_debut_fin(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.debut, "2025-06-07T08:00:00.000Z")
        self.assertEqual(result.fin, "2025-06-08T18:00:00.000Z")

    def test_012_field_description(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("Levallois", result.description)  # type: ignore[operator]

    def test_013_field_adresse(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.adresse, "15 Rue Aristide Briand")
        self.assertEqual(result.adresseComplement, "Gymnase Marcel Cerdan")

    def test_014_field_organisateur(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.mailOrganisateur, "contact@levallois-basket.fr")
        self.assertEqual(result.nomOrganisateur, "LEVALLOIS SPORTING CLUB BASKET")
        self.assertEqual(result.telephoneOrganisateur, "01 47 37 12 34")
        self.assertEqual(result.urlOrganisateur, "https://www.levallois-basket.fr")

    def test_015_field_site_choisi(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.siteChoisi, "Gymnase Marcel Cerdan - Levallois-Perret")

    def test_016_field_nb_participant_prevu(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.nbParticipantPrevu, 24)

    def test_017_field_tarif(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.tarifOrganisateur, "15 EUR par equipe")

    def test_018_field_age_min_max(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.ageMin, 12)
        self.assertEqual(result.ageMax, 18)

    def test_019_field_tournoi_type(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.tournoiType, dict)
        self.assertEqual(result.tournoiType["libelle"], "3x3")  # type: ignore[index]

    def test_020_field_commune(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.commune, dict)
        self.assertEqual(result.commune["nom"], "LEVALLOIS-PERRET")  # type: ignore[index]

    def test_021_field_cartographie(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.cartographie, dict)
        self.assertAlmostEqual(result.cartographie["latitude"], 48.8938)  # type: ignore[index]

    def test_022_field_tournoi_types_3x3(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.tournoiTypes3x3, list)
        self.assertEqual(len(result.tournoiTypes3x3), 2)
        self.assertEqual(result.tournoiTypes3x3[0]["libelle"], "U13")

    def test_023_field_document_flyer(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.document_flyer, dict)
        self.assertEqual(result.document_flyer["filename"], "flyer_tournoi.pdf")  # type: ignore[index]

    def test_024_field_categorie_championnat_3x3(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.categorieChampionnat3x3Id, "CAT-3X3-001")
        self.assertEqual(result.categorieChampionnat3x3Libelle, "Championnat 3x3 U15")

    def test_025_field_date_created(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.date_created, "2025-03-01T09:00:00.000Z")

    def test_026_field_date_updated(self) -> None:
        result = GetTournoisResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.date_updated, "2025-05-15T16:30:00.000Z")

    def test_027_nullable_dicts_none(self) -> None:
        data = {
            **SAMPLE_DATA,
            "tournoiType": None,
            "commune": None,
            "cartographie": None,
        }
        result = GetTournoisResponse.from_dict(data)
        assert result is not None
        self.assertIsNone(result.tournoiType)
        self.assertIsNone(result.commune)
        self.assertIsNone(result.cartographie)

    def test_028_tournoi_types_3x3_defaults_to_empty_list(self) -> None:
        data = {**SAMPLE_DATA, "tournoiTypes3x3": None}
        result = GetTournoisResponse.from_dict(data)
        assert result is not None
        self.assertEqual(result.tournoiTypes3x3, [])

    def test_029_from_list_filters_none_items(self) -> None:
        result = GetTournoisResponse.from_list([SAMPLE_DATA, {}, SAMPLE_DATA])
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
