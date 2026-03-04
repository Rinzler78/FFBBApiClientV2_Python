"""Unit tests for models extracted from get_competition_response.py (Phase 2)."""

from __future__ import annotations

import unittest
from uuid import UUID

from ffbb_api_client_v2.directus_ffbb.models.get_competition_response import (
    GetCompetitionResponse,
)
from ffbb_api_client_v2.models.competition_phase import CompetitionPhase
from ffbb_api_client_v2.models.competition_poule import CompetitionPoule
from ffbb_api_client_v2.models.competition_rencontre import CompetitionRencontre
from ffbb_api_client_v2.models.engagement_equipe import EngagementEquipe
from ffbb_api_client_v2.models.fonction import Fonction
from ffbb_api_client_v2.models.id_organisme_equipe import IDOrganismeEquipe
from ffbb_api_client_v2.models.officiel import Officiel
from ffbb_api_client_v2.models.officiel_personne import OfficielPersonne
from ffbb_api_client_v2.models.phase_engagement import PhaseEngagement
from ffbb_api_client_v2.models.type_competition_enum import TypeCompetitionEnum

# Aliases for backward-compat in tests
OrganismeEquipe = IDOrganismeEquipe


class TestFonction(unittest.TestCase):
    """Tests for Fonction model."""

    def test_032_from_dict_full(self) -> None:
        f = Fonction.from_dict({"libelle": "Arbitre"})
        self.assertEqual(f.libelle, "Arbitre")

    def test_033_from_dict_empty(self) -> None:
        f = Fonction.from_dict({})
        self.assertIsNone(f.libelle)

    def test_002_to_dict(self) -> None:
        self.assertEqual(Fonction(libelle="Arbitre").to_dict(), {"libelle": "Arbitre"})

    def test_003_to_dict_skips_none(self) -> None:
        self.assertEqual(Fonction().to_dict(), {})

    def test_035_round_trip(self) -> None:
        data = {"libelle": "Marqueur"}
        obj1 = Fonction.from_dict(data)
        obj2 = Fonction.from_dict(obj1.to_dict())
        self.assertEqual(obj1.to_dict(), obj2.to_dict())


class TestOfficielPersonne(unittest.TestCase):
    """Tests for OfficielPersonne model."""

    def test_032_from_dict_full(self) -> None:
        p = OfficielPersonne.from_dict({"nom": "Dupont", "prenom": "Jean"})
        self.assertEqual(p.nom, "Dupont")
        self.assertEqual(p.prenom, "Jean")

    def test_033_from_dict_empty(self) -> None:
        p = OfficielPersonne.from_dict({})
        self.assertIsNone(p.nom)
        self.assertIsNone(p.prenom)

    def test_035_round_trip(self) -> None:
        data = {"nom": "Dupont", "prenom": "Jean"}
        obj1 = OfficielPersonne.from_dict(data)
        obj2 = OfficielPersonne.from_dict(obj1.to_dict())
        self.assertEqual(obj1.to_dict(), obj2.to_dict())


class TestOfficiel(unittest.TestCase):
    """Tests for Officiel model."""

    def test_032_from_dict_full(self) -> None:
        data = {
            "ordre": 1,
            "fonction": {"libelle": "Arbitre"},
            "officiel": {"nom": "Martin", "prenom": "Paul"},
        }
        off = Officiel.from_dict(data)
        self.assertEqual(off.ordre, 1)
        self.assertIsNotNone(off.fonction)
        self.assertEqual(off.fonction.libelle, "Arbitre")
        self.assertIsNotNone(off.officiel)
        self.assertEqual(off.officiel.nom, "Martin")

    def test_033_from_dict_empty(self) -> None:
        off = Officiel.from_dict({})
        self.assertIsNone(off.ordre)
        self.assertIsNone(off.fonction)
        self.assertIsNone(off.officiel)

    def test_035_round_trip(self) -> None:
        data = {
            "ordre": 1,
            "fonction": {"libelle": "Arbitre"},
            "officiel": {"nom": "Martin", "prenom": "Paul"},
        }
        obj1 = Officiel.from_dict(data)
        obj2 = Officiel.from_dict(obj1.to_dict())
        self.assertEqual(obj1.to_dict(), obj2.to_dict())


class TestOrganismeEquipe(unittest.TestCase):
    """Tests for IDOrganismeEquipe model."""

    def test_011_from_dict_with_logo(self) -> None:
        uuid_str = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        data = {"logo": {"id": uuid_str}}
        oe = OrganismeEquipe.from_dict(data)
        self.assertIsNotNone(oe.logo)
        self.assertEqual(oe.logo.id, UUID(uuid_str))

    def test_033_from_dict_empty(self) -> None:
        oe = OrganismeEquipe.from_dict({})
        self.assertIsNone(oe.logo)

    def test_035_round_trip(self) -> None:
        data = {"logo": {"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}}
        obj1 = OrganismeEquipe.from_dict(data)
        obj2 = OrganismeEquipe.from_dict(obj1.to_dict())
        self.assertEqual(obj1.to_dict(), obj2.to_dict())


class TestEngagementEquipe(unittest.TestCase):
    """Tests for EngagementEquipe model."""

    def test_032_from_dict_full(self) -> None:
        data = {
            "id": "ee-001",
            "nom": "CLUB TEST - 1",
            "nomOfficiel": "CLUB TEST OFFICIEL",
            "nomUsuel": "CT",
            "codeAbrege": "CT1",
            "logo": {"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"},
        }
        ee = EngagementEquipe.from_dict(data)
        self.assertEqual(ee.id, "ee-001")
        self.assertEqual(ee.nom, "CLUB TEST - 1")
        self.assertEqual(ee.nom_officiel, "CLUB TEST OFFICIEL")
        self.assertEqual(ee.nom_usuel, "CT")
        self.assertEqual(ee.code_abrege, "CT1")
        self.assertIsNotNone(ee.logo)

    def test_033_from_dict_empty(self) -> None:
        ee = EngagementEquipe.from_dict({})
        self.assertIsNone(ee.id)
        self.assertIsNone(ee.nom)

    def test_034_to_dict_camelcase_keys(self) -> None:
        ee = EngagementEquipe(
            id="ee-001",
            nom_officiel="Off",
            nom_usuel="Usu",
            code_abrege="CA",
        )
        d = ee.to_dict()
        self.assertEqual(d["nomOfficiel"], "Off")
        self.assertEqual(d["nomUsuel"], "Usu")
        self.assertEqual(d["codeAbrege"], "CA")
        self.assertNotIn("nom_officiel", d)
        self.assertNotIn("nom_usuel", d)
        self.assertNotIn("code_abrege", d)

    def test_035_round_trip(self) -> None:
        data = {
            "id": "ee-001",
            "nom": "CLUB TEST - 1",
            "nomOfficiel": "CLUB TEST OFFICIEL",
            "nomUsuel": "CT",
            "codeAbrege": "CT1",
        }
        obj1 = EngagementEquipe.from_dict(data)
        obj2 = EngagementEquipe.from_dict(obj1.to_dict())
        self.assertEqual(obj1.to_dict(), obj2.to_dict())


class TestOrganismeId(unittest.TestCase):
    """Tests for OrganismeId (removed - PhaseEngagement.id_organisme is now str)."""

    def test_018_phase_engagement_id_organisme_is_str(self) -> None:
        pe = PhaseEngagement.from_dict({"id": "pe-001", "idOrganisme": "org-001"})
        self.assertEqual(pe.id_organisme, "org-001")


class TestPhaseEngagement(unittest.TestCase):
    """Tests for PhaseEngagement model."""

    def test_032_from_dict_full(self) -> None:
        data = {
            "id": "pe-001",
            "idOrganisme": "org-001",
        }
        pe = PhaseEngagement.from_dict(data)
        self.assertEqual(pe.id, "pe-001")
        self.assertEqual(pe.id_organisme, "org-001")

    def test_033_from_dict_empty(self) -> None:
        pe = PhaseEngagement.from_dict({})
        self.assertIsNone(pe.id)
        self.assertIsNone(pe.id_organisme)

    def test_034_to_dict_camelcase_keys(self) -> None:
        pe = PhaseEngagement(
            id="pe-001",
            id_organisme="org-001",
        )
        d = pe.to_dict()
        self.assertIn("idOrganisme", d)
        self.assertNotIn("id_organisme", d)

    def test_035_round_trip(self) -> None:
        data = {
            "id": "pe-001",
            "idOrganisme": "org-001",
        }
        obj1 = PhaseEngagement.from_dict(data)
        obj2 = PhaseEngagement.from_dict(obj1.to_dict())
        self.assertEqual(obj1.to_dict(), obj2.to_dict())


class TestCompetitionRencontre(unittest.TestCase):
    """Tests for CompetitionRencontre model."""

    def test_032_from_dict_full(self) -> None:
        data = {
            "id": "ren-001",
            "numero": "42",
            "numeroJournee": "3",
            "idPoule": "poule-001",
            "competitionId": "comp-001",
            "resultatEquipe1": "78",
            "resultatEquipe2": "65",
            "joue": True,
            "nomEquipe1": "Club A",
            "nomEquipe2": "Club B",
            "date_rencontre": "2024-11-15T20:00:00+00:00",
            "idOrganismeEquipe1": {
                "logo": {"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}
            },
            "idOrganismeEquipe2": {
                "logo": {"id": "b2c3d4e5-f6a7-8901-bcde-f12345678901"}
            },
            "idEngagementEquipe1": {"id": "ee-001", "nom": "CLUB A"},
            "idEngagementEquipe2": {"id": "ee-002", "nom": "CLUB B"},
            "salle": {"id": "salle-001", "libelle": "Gymnase Central"},
            "officiels": [
                {
                    "ordre": 1,
                    "fonction": {"libelle": "Arbitre"},
                    "officiel": {"nom": "Ref", "prenom": "One"},
                }
            ],
        }
        ren = CompetitionRencontre.from_dict(data)
        self.assertEqual(ren.id, "ren-001")
        self.assertEqual(ren.numero, "42")
        self.assertEqual(ren.numero_journee, "3")
        self.assertEqual(ren.resultat_equipe1, 78)
        self.assertEqual(ren.resultat_equipe2, 65)
        self.assertEqual(ren.joue, True)
        self.assertEqual(ren.nom_equipe1, "Club A")
        self.assertIsNotNone(ren.date_rencontre)
        self.assertIsNotNone(ren.id_organisme_equipe1)
        self.assertIsNotNone(ren.id_engagement_equipe1)
        self.assertIsNotNone(ren.salle)
        self.assertEqual(len(ren.officiels), 1)
        self.assertIsInstance(ren.officiels[0], Officiel)

    def test_033_from_dict_empty(self) -> None:
        ren = CompetitionRencontre.from_dict({})
        self.assertIsNone(ren.id)
        self.assertEqual(ren.officiels, [])

    def test_034_to_dict_camelcase_keys(self) -> None:
        ren = CompetitionRencontre(
            id="ren-001",
            numero_journee="3",
            resultat_equipe1=78,
            resultat_equipe2=65,
            nom_equipe1="Club A",
            nom_equipe2="Club B",
        )
        d = ren.to_dict()
        self.assertEqual(d["numeroJournee"], "3")
        self.assertEqual(d["resultatEquipe1"], 78)
        self.assertEqual(d["nomEquipe1"], "Club A")
        self.assertNotIn("numero_journee", d)
        self.assertNotIn("resultat_equipe1", d)

    def test_028_round_trip_minimal(self) -> None:
        data = {
            "id": "ren-001",
            "numero": "42",
            "joue": True,
            "nomEquipe1": "Club A",
            "nomEquipe2": "Club B",
        }
        obj1 = CompetitionRencontre.from_dict(data)
        obj2 = CompetitionRencontre.from_dict(obj1.to_dict())
        self.assertEqual(obj1.to_dict(), obj2.to_dict())


class TestCompetitionPoule(unittest.TestCase):
    """Tests for CompetitionPoule model."""

    def test_032_from_dict_full(self) -> None:
        data = {
            "id": "poule-001",
            "nom": "Poule A",
            "rencontres": [
                {
                    "id": "ren-001",
                    "numero": "1",
                    "joue": True,
                    "nomEquipe1": "A",
                    "nomEquipe2": "B",
                },
            ],
            "engagements": [
                {"id": "pe-001", "idOrganisme": "org-001"},
            ],
        }
        poule = CompetitionPoule.from_dict(data)
        self.assertEqual(poule.id, "poule-001")
        self.assertEqual(poule.nom, "Poule A")
        self.assertEqual(len(poule.rencontres), 1)
        self.assertIsInstance(poule.rencontres[0], CompetitionRencontre)
        self.assertEqual(len(poule.engagements), 1)
        self.assertIsInstance(poule.engagements[0], PhaseEngagement)

    def test_033_from_dict_empty(self) -> None:
        poule = CompetitionPoule.from_dict({})
        self.assertIsNone(poule.id)
        self.assertEqual(poule.rencontres, [])
        self.assertEqual(poule.engagements, [])

    def test_035_round_trip(self) -> None:
        data = {
            "id": "poule-001",
            "nom": "Poule A",
            "engagements": [
                {"id": "pe-001", "idOrganisme": "org-001"},
            ],
        }
        obj1 = CompetitionPoule.from_dict(data)
        obj2 = CompetitionPoule.from_dict(obj1.to_dict())
        self.assertEqual(obj1.to_dict(), obj2.to_dict())


class TestCompetitionPhase(unittest.TestCase):
    """Tests for CompetitionPhase model."""

    def test_032_from_dict_full(self) -> None:
        data = {
            "id": "phase-001",
            "nom": "Phase Aller",
            "liveStat": True,
            "phase_code": "ALLER",
            "poules": [
                {"id": "poule-001", "nom": "Poule A"},
            ],
        }
        phase = CompetitionPhase.from_dict(data)
        self.assertEqual(phase.id, "phase-001")
        self.assertEqual(phase.nom, "Phase Aller")
        self.assertEqual(phase.live_stat, True)
        self.assertEqual(phase.phase_code, "ALLER")
        self.assertEqual(len(phase.poules), 1)
        self.assertIsInstance(phase.poules[0], CompetitionPoule)

    def test_033_from_dict_empty(self) -> None:
        phase = CompetitionPhase.from_dict({})
        self.assertIsNone(phase.id)
        self.assertEqual(phase.poules, [])

    def test_034_to_dict_camelcase_keys(self) -> None:
        phase = CompetitionPhase(id="phase-001", live_stat=True, phase_code="ALLER")
        d = phase.to_dict()
        self.assertEqual(d["liveStat"], True)
        self.assertEqual(d["phase_code"], "ALLER")
        self.assertNotIn("live_stat", d)

    def test_035_round_trip(self) -> None:
        data = {
            "id": "phase-001",
            "nom": "Phase Aller",
            "liveStat": True,
            "phase_code": "ALLER",
            "poules": [
                {"id": "poule-001", "nom": "Poule A"},
            ],
        }
        obj1 = CompetitionPhase.from_dict(data)
        obj2 = CompetitionPhase.from_dict(obj1.to_dict())
        self.assertEqual(obj1.to_dict(), obj2.to_dict())


class TestGetCompetitionResponseExtracted(unittest.TestCase):
    """Tests for rewritten GetCompetitionResponse using extracted models."""

    def test_036_from_dict_with_phases(self) -> None:
        data = {
            "id": "comp-001",
            "nom": "Regionale 2",
            "phases": [
                {
                    "id": "phase-001",
                    "nom": "Phase Aller",
                    "liveStat": True,
                    "phase_code": "ALLER",
                    "poules": [],
                }
            ],
        }
        resp = GetCompetitionResponse.from_dict(data)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.id, "comp-001")
        self.assertEqual(len(resp.phases), 1)
        from ffbb_api_client_v2.models.competition_phase import CompetitionPhase

        self.assertIsInstance(resp.phases[0], CompetitionPhase)

    def test_037_from_dict_with_poules(self) -> None:
        data = {
            "id": "comp-001",
            "nom": "Regionale 2",
            "poules": [{"id": "poule-001"}],
        }
        resp = GetCompetitionResponse.from_dict(data)
        self.assertIsNotNone(resp)
        self.assertEqual(len(resp.poules), 1)

    def test_038_from_dict_snake_case_fields(self) -> None:
        data = {
            "id": "comp-001",
            "typeCompetition": "Championnat",
            "liveStat": True,
            "publicationInternet": "O",
            "competition_origine": 42,
            "competition_origine_nom": "Championnat Regional",
        }
        resp = GetCompetitionResponse.from_dict(data)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.type_competition, TypeCompetitionEnum.CHAMPIONNAT)
        self.assertEqual(resp.live_stat, True)
        self.assertEqual(resp.publication_internet, "O")
        self.assertEqual(resp.competition_origine, 42)
        self.assertEqual(resp.competition_origine_nom, "Championnat Regional")

    def test_039_from_dict_with_categorie(self) -> None:
        data = {
            "id": "comp-001",
            "categorie": {"code": "SEN", "ordre": 10},
        }
        resp = GetCompetitionResponse.from_dict(data)
        self.assertIsNotNone(resp)
        self.assertIsNotNone(resp.categorie)

    def test_040_from_dict_empty_returns_none(self) -> None:
        self.assertIsNone(GetCompetitionResponse.from_dict({}))

    def test_041_from_dict_errors_returns_none(self) -> None:
        self.assertIsNone(GetCompetitionResponse.from_dict({"errors": ["err"]}))

    def test_042_from_dict_empty_lists_default(self) -> None:
        data = {"id": "comp-001", "nom": "Regionale 2"}
        resp = GetCompetitionResponse.from_dict(data)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.poules, [])
        self.assertEqual(resp.phases, [])


if __name__ == "__main__":
    unittest.main()
