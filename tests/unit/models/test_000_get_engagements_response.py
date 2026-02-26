"""Tests for GetEngagementsResponse model."""

from __future__ import annotations

import unittest
from datetime import datetime
from typing import Any
from uuid import UUID

from ffbb_api_client_v2.directus_ffbb.models.get_engagements_response import (
    GetEngagementsResponse,
)
from ffbb_api_client_v2.models.categorie import Categorie
from ffbb_api_client_v2.models.engagement_position import EngagementPosition
from ffbb_api_client_v2.models.team_ranking import TeamRanking

SAMPLE_DATA: dict[str, Any] = {
    "id": "200000005137866",
    "nom": "Pre nationale feminine Poule A",
    "nomEquipe": "Equipe 1",
    "nomUsuel": "CA MANTES",
    "nomOfficiel": "CA MANTES LA VILLE BASKET",
    "numeroEquipe": "1",  # string in API, converted to int by from_int
    "codeAbrege": "MAN",
    "clubPro": False,
    "position": 3,
    "positionVariation": -1,
    "position_n1": 2,
    "pouleId": "P-001",
    # FK-only fields (int IDs)
    "idCompetition": 2872432,
    "idOrganisme": 123456,
    "idOrganismeCtc": 789012,
    "idPoule": 3017520,
    "entraineur": 1001,
    "entraineurAdjoint": 1002,
    # FK-only: Directus file UUIDs
    "logo": "d4e5f6a7-b8c9-0123-4567-89abcdef0123",
    "logo_genius": "a1b2c3d4-e5f6-7890-abcd-ef0123456789",
    "photo": "11223344-5566-7788-99aa-bbccddeeff00",
    # Embedded objects
    "niveau": {"code": "SEN", "libelle": "Seniors"},
    "classement": [
        {
            "id": "200000003017520-3",
            "position": "3",
            "points": "29",
            "matchJoues": "17",
            "gagnes": "12",
            "perdus": "5",
        },
    ],
    # Correspondant fields
    "adresseCorrespondantEquipe": "12 Rue du Stade",
    "emailCorrespondantEquipe": "contact@club.fr",
    "nomCorrespondantEquipe": "Durand",
    # CTC fields
    "nomCtc": "CTC Yvelines",
    "typeEntenteCtc": "Entente",
    # Other
    "toUpdate": False,
    "url_competition": "https://example.com/competition",
    "positions": [
        {"position": "5", "key": "5_0_0_0_0_0_0", "date": "2025-08-08T03:18:28.606Z"},
        {
            "position": "13",
            "key": "13_1_0_1_0_1_-21",
            "date": "2025-09-15T03:15:04.279Z",
        },
        {
            "position": "14",
            "key": "14_2_0_2_0_2_-42",
            "date": "2025-10-06T03:15:26.456Z",
        },
    ],
    # FK-only: lists
    "rencontres_domiciles": [101, 102, 103],
    "rencontres_exterieur": [201, 202],
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
        self.assertEqual(result.numeroEquipe, 1)

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
        self.assertIsInstance(result.logo, UUID)
        self.assertEqual(str(result.logo), "d4e5f6a7-b8c9-0123-4567-89abcdef0123")

    def test_017_field_id_competition(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.idCompetition, 2872432)

    def test_018_field_id_organisme(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.idOrganisme, 123456)

    def test_019_field_id_poule(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.idPoule, 3017520)

    def test_020_field_niveau(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.niveau, Categorie)
        assert isinstance(result.niveau, Categorie)
        self.assertEqual(result.niveau.libelle, "Seniors")

    def test_021_field_classement(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.classement, list)
        assert result.classement is not None
        self.assertEqual(len(result.classement), 1)
        self.assertIsInstance(result.classement[0], TeamRanking)
        self.assertEqual(result.classement[0].position, 3)
        self.assertEqual(result.classement[0].points, 29)

    def test_022_field_entraineur(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.entraineur, 1001)

    def test_023_field_entraineur_adjoint(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.entraineurAdjoint, 1002)

    def test_024_field_positions(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.positions, list)
        self.assertEqual(len(result.positions), 3)
        self.assertIsInstance(result.positions[0], EngagementPosition)
        self.assertEqual(result.positions[0].position, "5")

    def test_025_field_rencontres_domiciles(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.rencontres_domiciles, list)
        self.assertEqual(len(result.rencontres_domiciles), 3)

    def test_026_field_rencontres_exterieur(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.rencontres_exterieur, list)
        self.assertEqual(len(result.rencontres_exterieur), 2)

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

    def test_031_nullable_fk_fields_none(self) -> None:
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

    def test_034_field_poule_id(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.pouleId, "P-001")

    def test_035_field_correspondant(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.adresseCorrespondantEquipe, "12 Rue du Stade")
        self.assertEqual(result.emailCorrespondantEquipe, "contact@club.fr")
        self.assertEqual(result.nomCorrespondantEquipe, "Durand")

    def test_036_field_ctc(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.nomCtc, "CTC Yvelines")
        self.assertEqual(result.typeEntenteCtc, "Entente")

    def test_037_field_to_update(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertFalse(result.toUpdate)

    def test_038_field_url_competition(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.url_competition, "https://example.com/competition")

    def test_039_field_logo_genius(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.logo_genius, UUID)

    def test_040_field_photo(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.photo, UUID)

    def test_041_field_id_organisme_ctc(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.idOrganismeCtc, 789012)

    def test_042_field_position_variation(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.positionVariation, -1)

    def test_043_field_position_n1(self) -> None:
        result = GetEngagementsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.position_n1, 2)


if __name__ == "__main__":
    unittest.main()
