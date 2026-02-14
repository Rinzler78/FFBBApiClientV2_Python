"""Tests for GetEngagementsResponse model."""

from __future__ import annotations

import unittest
from datetime import datetime
from typing import Any

from ffbb_api_client_v2.directus_ffbb.models.get_engagements_response import (
    GetEngagementsResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_entraineurs_response import (
    GetEntraineursResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_poule_response import (
    GetPouleResponse,
)
from ffbb_api_client_v2.models.categorie import Categorie
from ffbb_api_client_v2.models.document_flyer import DocumentFlyer
from ffbb_api_client_v2.models.organisateur import Organisateur

SAMPLE_DATA: dict[str, Any] = {
    "id": "200000005137866",
    "nom": "Pre nationale feminine Poule A",
    "nomEquipe": "Equipe 1",
    "nomUsuel": "CA MANTES",
    "nomOfficiel": "CA MANTES LA VILLE BASKET",
    "numeroEquipe": "1",
    "codeAbrege": "MAN",
    "clubPro": False,
    "position": 3,
    "logo": {
        "id": "d4e5f6a7-b8c9-0123-4567-89abcdef0123",
        "filename_download": "ca_mantes_logo.png",
        "type": "image/png",
    },
    "idCompetition": {
        "id": "200000002872432",
        "nom": "Pre nationale feminine",
        "code": "PNF",
    },
    "idOrganisme": {
        "id": "200000000123456",
        "nom": "CA MANTES LA VILLE",
        "code": "IDF0078020",
    },
    "idPoule": {"id": "200000003017520", "nom": "Poule A"},
    "niveau": {"code": "SEN", "libelle": "Seniors"},
    "classement": {
        "victoires": 12,
        "defaites": 4,
        "nuls": 0,
        "points": 28,
    },
    "entraineur": {
        "idLicence": "ENT-001",
        "nom": "Dupont",
        "prenom": "Jean",
    },
    "entraineurAdjoint": {
        "idLicence": "ENT-002",
        "nom": "Martin",
        "prenom": "Sophie",
    },
    "positionVariation": -1,
    "position_n1": 2,
    "positions": [
        {"journee": 1, "position": 1},
        {"journee": 2, "position": 2},
        {"journee": 3, "position": 3},
    ],
    "rencontres_domiciles": [
        {"id": "REN-001", "scoreEquipeDomicile": 72, "scoreEquipeVisiteur": 65},
    ],
    "rencontres_exterieur": [
        {"id": "REN-002", "scoreEquipeDomicile": 80, "scoreEquipeVisiteur": 68},
    ],
    "date_created": "2024-10-01T08:00:00.000Z",
    "date_updated": "2025-04-12T20:15:00.000Z",
}


class TestGetEngagementsResponse(unittest.TestCase):
    def test_000_from_dict_valid(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        self.assertIsNotNone(result)

    def test_001_from_dict_none(self) -> None:
        result = GetEngagementsResponse.from_dict(None)  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_002_from_dict_empty(self) -> None:
        result = GetEngagementsResponse.from_dict({})
        self.assertIsNone(result)

    def test_003_from_dict_errors(self) -> None:
        result = GetEngagementsResponse.from_dict({"errors": [{"message": "err"}]})
        self.assertIsNone(result)

    def test_004_from_dict_not_dict(self) -> None:
        result = GetEngagementsResponse.from_dict("not a dict")  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_005_from_list_valid(self) -> None:
        result = GetEngagementsResponse.from_list([SAMPLE_DATA, SAMPLE_DATA])
        self.assertEqual(len(result), 2)

    def test_006_from_list_empty(self) -> None:
        result = GetEngagementsResponse.from_list([])
        self.assertEqual(result, [])

    def test_007_field_id(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.id, "200000005137866")

    def test_008_field_nom(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.nom, "Pre nationale feminine Poule A")

    def test_009_field_nom_equipe(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.nomEquipe, "Equipe 1")

    def test_010_field_nom_usuel(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.nomUsuel, "CA MANTES")

    def test_011_field_nom_officiel(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.nomOfficiel, "CA MANTES LA VILLE BASKET")

    def test_012_field_numero_equipe(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.numeroEquipe, "1")

    def test_013_field_code_abrege(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.codeAbrege, "MAN")

    def test_014_field_club_pro(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertFalse(result.clubPro)

    def test_015_field_position(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.position, 3)

    def test_016_field_logo(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.logo, DocumentFlyer)
        assert isinstance(result.logo, DocumentFlyer)
        self.assertEqual(result.logo.filename_download, "ca_mantes_logo.png")

    def test_017_field_id_competition(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.idCompetition, dict)
        self.assertEqual(result.idCompetition["code"], "PNF")  # type: ignore[index]

    def test_018_field_id_organisme(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.idOrganisme, Organisateur)
        assert isinstance(result.idOrganisme, Organisateur)
        self.assertEqual(result.idOrganisme.code, "IDF0078020")

    def test_019_field_id_poule(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.idPoule, GetPouleResponse)
        assert isinstance(result.idPoule, GetPouleResponse)
        self.assertEqual(result.idPoule.nom, "Poule A")

    def test_020_field_niveau(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.niveau, Categorie)
        assert isinstance(result.niveau, Categorie)
        self.assertEqual(result.niveau.libelle, "Seniors")

    def test_021_field_classement(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.classement, dict)
        self.assertEqual(result.classement["victoires"], 12)  # type: ignore[index]

    def test_022_field_entraineur(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.entraineur, GetEntraineursResponse)
        assert isinstance(result.entraineur, GetEntraineursResponse)
        self.assertEqual(result.entraineur.nom, "Dupont")

    def test_023_field_entraineur_adjoint(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.entraineurAdjoint, GetEntraineursResponse)
        assert isinstance(result.entraineurAdjoint, GetEntraineursResponse)
        self.assertEqual(result.entraineurAdjoint.nom, "Martin")

    def test_024_field_positions(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.positions, list)
        self.assertEqual(len(result.positions), 3)

    def test_025_field_rencontres_domiciles(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.rencontres_domiciles, list)
        self.assertEqual(len(result.rencontres_domiciles), 1)

    def test_026_field_rencontres_exterieur(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.rencontres_exterieur, list)
        self.assertEqual(len(result.rencontres_exterieur), 1)

    def test_027_field_date_created(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.date_created, datetime)

    def test_028_field_date_updated(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.date_updated, datetime)

    def test_029_nullable_bool_none(self) -> None:
        data = {**SAMPLE_DATA, "clubPro": None}
        result = GetEngagementsResponse.from_dict(data)
        assert result is not None
        self.assertIsNone(result.clubPro)

    def test_030_nullable_int_none(self) -> None:
        data = {**SAMPLE_DATA, "position": None}
        result = GetEngagementsResponse.from_dict(data)
        assert result is not None
        self.assertIsNone(result.position)

    def test_031_nullable_dicts_none(self) -> None:
        data = {
            **SAMPLE_DATA,
            "logo": None,
            "idCompetition": None,
            "idOrganisme": None,
            "idPoule": None,
            "niveau": None,
            "classement": None,
            "entraineur": None,
            "entraineurAdjoint": None,
        }
        result = GetEngagementsResponse.from_dict(data)
        assert result is not None
        self.assertIsNone(result.logo)
        self.assertIsNone(result.idCompetition)
        self.assertIsNone(result.idOrganisme)
        self.assertIsNone(result.idPoule)
        self.assertIsNone(result.niveau)
        self.assertIsNone(result.classement)
        self.assertIsNone(result.entraineur)
        self.assertIsNone(result.entraineurAdjoint)

    def test_032_lists_default_to_empty(self) -> None:
        data = {
            **SAMPLE_DATA,
            "positions": None,
            "rencontres_domiciles": None,
            "rencontres_exterieur": None,
        }
        result = GetEngagementsResponse.from_dict(data)
        assert result is not None
        self.assertEqual(result.positions, [])
        self.assertEqual(result.rencontres_domiciles, [])
        self.assertEqual(result.rencontres_exterieur, [])

    def test_033_from_list_filters_none_items(self) -> None:
        result = GetEngagementsResponse.from_list([SAMPLE_DATA, {}, SAMPLE_DATA])
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
