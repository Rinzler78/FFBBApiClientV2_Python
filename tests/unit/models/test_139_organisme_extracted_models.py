"""Unit tests for models extracted from get_organisme_response.py (Phase 1)."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone
from typing import Any

from ffbb_api_client_v2.directus_ffbb.models.get_organisme_response import (
    GetOrganismeResponse,
)
from ffbb_api_client_v2.models.code_fonction import CodeFonction
from ffbb_api_client_v2.models.competition_ref import CompetitionRef
from ffbb_api_client_v2.models.labellisation_item import LabellisationItem
from ffbb_api_client_v2.models.labellisation_programme import LabellisationProgramme
from ffbb_api_client_v2.models.membre import Membre
from ffbb_api_client_v2.models.offre_pratique import OffrePratique, OffrePratiqueDetail
from ffbb_api_client_v2.models.organisme_engagement import OrganismeEngagement


class TestMembre(unittest.TestCase):
    """Tests for Membre model."""

    def _assert_stable(self, model_class: type, input_data: dict[str, Any]) -> None:
        obj1 = model_class.from_dict(input_data)
        dict1 = obj1.to_dict()
        obj2 = model_class.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2, f"{model_class.__name__} round-trip not stable")

    def test_026_from_dict_full(self) -> None:
        data = {
            "id": "m-001",
            "nom": "Dupont",
            "prenom": "Jean",
            "adresse1": "12 rue de la Paix",
            "adresse2": "Apt 3",
            "codePostal": "75001",
            "ville": "Paris",
            "mail": "jean@example.com",
            "telephoneFixe": "0102030405",
            "telephonePortable": "0607080910",
            "codeFonction": "PRES",
        }
        membre = Membre.from_dict(data)
        self.assertEqual(membre.id, "m-001")
        self.assertEqual(membre.nom, "Dupont")
        self.assertEqual(membre.prenom, "Jean")
        self.assertEqual(membre.code_postal, "75001")
        self.assertEqual(membre.ville, "Paris")
        self.assertEqual(membre.mail, "jean@example.com")
        self.assertEqual(membre.telephone_fixe, "0102030405")
        self.assertEqual(membre.telephone_portable, "0607080910")
        self.assertEqual(membre.code_fonction, "PRES")

    def test_027_from_dict_empty(self) -> None:
        membre = Membre.from_dict({})
        self.assertIsNone(membre.id)
        self.assertIsNone(membre.nom)
        self.assertIsNone(membre.prenom)

    def test_028_to_dict_camelcase_keys(self) -> None:
        membre = Membre(
            id="m-001",
            code_postal="75001",
            telephone_fixe="01",
            telephone_portable="06",
            code_fonction=CodeFonction.PRESIDENT,
        )
        d = membre.to_dict()
        self.assertEqual(d["codePostal"], "75001")
        self.assertEqual(d["telephoneFixe"], "01")
        self.assertEqual(d["telephonePortable"], "06")
        self.assertEqual(d["codeFonction"], "PRES")
        self.assertNotIn("code_postal", d)

    def test_003_to_dict_skips_none(self) -> None:
        membre = Membre(id="m-001")
        d = membre.to_dict()
        self.assertEqual(d, {"id": "m-001"})

    def test_004_round_trip_full(self) -> None:
        self._assert_stable(
            Membre,
            {
                "id": "m-001",
                "nom": "Dupont",
                "prenom": "Jean",
                "codePostal": "75001",
                "ville": "Paris",
                "codeFonction": "PRES",
            },
        )

    def test_005_round_trip_minimal(self) -> None:
        self._assert_stable(Membre, {"id": "m-002"})


class TestOffrePratiqueDetail(unittest.TestCase):
    """Tests for OffrePratiqueDetail model."""

    def test_026_from_dict_full(self) -> None:
        data = {
            "id": "op-001",
            "title": "Basketball Loisir",
            "categoriePratique": "Loisir",
            "typePratique": "Basket",
        }
        detail = OffrePratiqueDetail.from_dict(data)
        self.assertEqual(detail.id, "op-001")
        self.assertEqual(detail.title, "Basketball Loisir")
        self.assertEqual(detail.categorie_pratique, "Loisir")
        self.assertEqual(detail.type_pratique, "Basket")

    def test_027_from_dict_empty(self) -> None:
        detail = OffrePratiqueDetail.from_dict({})
        self.assertIsNone(detail.id)
        self.assertIsNone(detail.title)

    def test_028_to_dict_camelcase_keys(self) -> None:
        detail = OffrePratiqueDetail(
            id="op-001",
            categorie_pratique="Loisir",
            type_pratique="Basket",
        )
        d = detail.to_dict()
        self.assertEqual(d["categoriePratique"], "Loisir")
        self.assertEqual(d["typePratique"], "Basket")
        self.assertNotIn("categorie_pratique", d)

    def test_031_round_trip(self) -> None:
        data = {
            "id": "op-001",
            "title": "Basketball Loisir",
            "categoriePratique": "Loisir",
            "typePratique": "Basket",
        }
        obj1 = OffrePratiqueDetail.from_dict(data)
        obj2 = OffrePratiqueDetail.from_dict(obj1.to_dict())
        self.assertEqual(obj1.to_dict(), obj2.to_dict())


class TestOffrePratique(unittest.TestCase):
    """Tests for OffrePratique junction model."""

    def test_010_from_dict_with_detail(self) -> None:
        data = {
            "ffbbserver_offres_pratiques_id": {
                "id": "op-001",
                "title": "Basketball Loisir",
            }
        }
        offre = OffrePratique.from_dict(data)
        self.assertIsNotNone(offre.ffbbserver_offres_pratiques_id)
        self.assertEqual(offre.ffbbserver_offres_pratiques_id.id, "op-001")

    def test_027_from_dict_empty(self) -> None:
        offre = OffrePratique.from_dict({})
        self.assertIsNone(offre.ffbbserver_offres_pratiques_id)

    def test_031_round_trip(self) -> None:
        data = {
            "ffbbserver_offres_pratiques_id": {
                "id": "op-001",
                "title": "Basketball Loisir",
                "categoriePratique": "Loisir",
                "typePratique": "Basket",
            }
        }
        obj1 = OffrePratique.from_dict(data)
        obj2 = OffrePratique.from_dict(obj1.to_dict())
        self.assertEqual(obj1.to_dict(), obj2.to_dict())


class TestLabellisationProgramme(unittest.TestCase):
    """Tests for LabellisationProgramme model."""

    def test_026_from_dict_full(self) -> None:
        data = {
            "id": "lp-001",
            "libelle": "Label Ecole de Basket",
            "labellisationLabel": "OR",
            "logo_vertical": "https://ffbb.fr/images/label_or_vertical.png",
        }
        prog = LabellisationProgramme.from_dict(data)
        self.assertEqual(prog.id, "lp-001")
        self.assertEqual(prog.libelle, "Label Ecole de Basket")
        self.assertEqual(prog.labellisation_label, "OR")
        self.assertEqual(
            prog.logo_vertical, "https://ffbb.fr/images/label_or_vertical.png"
        )

    def test_027_from_dict_empty(self) -> None:
        prog = LabellisationProgramme.from_dict({})
        self.assertIsNone(prog.id)

    def test_028_to_dict_camelcase_keys(self) -> None:
        prog = LabellisationProgramme(
            id="lp-001",
            labellisation_label="OR",
        )
        d = prog.to_dict()
        self.assertEqual(d["labellisationLabel"], "OR")
        self.assertNotIn("labellisation_label", d)

    def test_031_round_trip(self) -> None:
        data = {
            "id": "lp-001",
            "libelle": "Label Ecole de Basket",
            "labellisationLabel": "OR",
        }
        obj1 = LabellisationProgramme.from_dict(data)
        obj2 = LabellisationProgramme.from_dict(obj1.to_dict())
        self.assertEqual(obj1.to_dict(), obj2.to_dict())


class TestLabellisationItem(unittest.TestCase):
    """Tests for LabellisationItem model."""

    def test_026_from_dict_full(self) -> None:
        data = {
            "id": "li-001",
            "debut": "2024-09-01T00:00:00+00:00",
            "fin": "2025-08-31T23:59:59+00:00",
            "idLabellisationProgramme": {
                "id": "lp-001",
                "libelle": "Label OR",
            },
        }
        item = LabellisationItem.from_dict(data)
        self.assertEqual(item.id, "li-001")
        self.assertIsInstance(item.debut, datetime)
        self.assertIsInstance(item.fin, datetime)
        self.assertIsNotNone(item.id_labellisation_programme)
        self.assertEqual(item.id_labellisation_programme.id, "lp-001")

    def test_027_from_dict_empty(self) -> None:
        item = LabellisationItem.from_dict({})
        self.assertIsNone(item.id)
        self.assertIsNone(item.debut)
        self.assertIsNone(item.fin)

    def test_019_to_dict_serializes_datetime(self) -> None:
        dt = datetime(2024, 9, 1, tzinfo=timezone.utc)
        item = LabellisationItem(id="li-001", debut=dt)
        d = item.to_dict()
        self.assertEqual(d["debut"], dt.isoformat())

    def test_028_to_dict_camelcase_keys(self) -> None:
        item = LabellisationItem(
            id="li-001",
            id_labellisation_programme=LabellisationProgramme(id="lp-001"),
        )
        d = item.to_dict()
        self.assertIn("idLabellisationProgramme", d)
        self.assertNotIn("id_labellisation_programme", d)

    def test_031_round_trip(self) -> None:
        data = {
            "id": "li-001",
            "debut": "2024-09-01T00:00:00+00:00",
            "fin": "2025-08-31T23:59:59+00:00",
            "idLabellisationProgramme": {
                "id": "lp-001",
                "libelle": "Label OR",
                "labellisationLabel": "OR",
            },
        }
        obj1 = LabellisationItem.from_dict(data)
        obj2 = LabellisationItem.from_dict(obj1.to_dict())
        self.assertEqual(obj1.to_dict(), obj2.to_dict())


class TestOrganismeEngagement(unittest.TestCase):
    """Tests for OrganismeEngagement model."""

    def test_026_from_dict_full(self) -> None:
        data = {
            "id": "eng-001",
            "idPoule": {"id": "poule-001"},
            "idCompetition": {
                "id": "comp-001",
                "nom": "Regionale 2 Masculine",
                "code": "R2M",
            },
        }
        eng = OrganismeEngagement.from_dict(data)
        self.assertEqual(eng.id, "eng-001")
        self.assertIsNotNone(eng.id_poule)
        self.assertEqual(eng.id_poule.id, "poule-001")
        self.assertIsNotNone(eng.id_competition)
        self.assertEqual(eng.id_competition.nom, "Regionale 2 Masculine")

    def test_027_from_dict_empty(self) -> None:
        eng = OrganismeEngagement.from_dict({})
        self.assertIsNone(eng.id)
        self.assertIsNone(eng.id_poule)
        self.assertIsNone(eng.id_competition)

    def test_028_to_dict_camelcase_keys(self) -> None:
        eng = OrganismeEngagement(id="eng-001")
        d = eng.to_dict()
        self.assertEqual(d, {"id": "eng-001"})

    def test_031_round_trip(self) -> None:
        data = {
            "id": "eng-001",
            "idPoule": {"id": "poule-001"},
            "idCompetition": {
                "id": "comp-001",
                "nom": "Regionale 2",
                "code": "R2",
            },
        }
        obj1 = OrganismeEngagement.from_dict(data)
        obj2 = OrganismeEngagement.from_dict(obj1.to_dict())
        self.assertEqual(obj1.to_dict(), obj2.to_dict())


class TestCompetitionRef(unittest.TestCase):
    """Tests for CompetitionRef model."""

    def test_026_from_dict_full(self) -> None:
        data = {
            "id": "comp-001",
            "nom": "Regionale 2 Masculine",
            "code": "R2M",
            "sexe": "M",
            "competition_origine": "orig-001",
            "competition_origine_nom": "Championnat Regional",
            "competition_origine_niveau": 2,
            "typeCompetition": "Championnat",
            "logo": {"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"},
            "saison": {"code": "2024"},
            "idCompetitionPere": "comp-parent",
            "organisateur": {"type": "COMITE"},
            "typeCompetitionGenerique": {"logo": None},
            "categorie": {"code": "SEN", "ordre": 10},
        }
        ref = CompetitionRef.from_dict(data)
        self.assertEqual(ref.id, "comp-001")
        self.assertEqual(ref.nom, "Regionale 2 Masculine")
        self.assertEqual(ref.sexe, "M")
        self.assertEqual(ref.competition_origine_niveau, 2)
        self.assertEqual(ref.type_competition, "Championnat")
        self.assertIsNotNone(ref.logo)
        self.assertIsNotNone(ref.saison)
        self.assertEqual(ref.id_competition_pere, "comp-parent")
        self.assertIsNotNone(ref.organisateur)
        self.assertIsNotNone(ref.categorie)

    def test_027_from_dict_empty(self) -> None:
        ref = CompetitionRef.from_dict({})
        self.assertIsNone(ref.id)
        self.assertIsNone(ref.nom)

    def test_028_to_dict_camelcase_keys(self) -> None:
        ref = CompetitionRef(
            id="comp-001",
            type_competition="Championnat",
            competition_origine_niveau=2,
            id_competition_pere="comp-parent",
        )
        d = ref.to_dict()
        self.assertEqual(d["typeCompetition"], "Championnat")
        self.assertEqual(d["competition_origine_niveau"], 2)
        self.assertEqual(d["idCompetitionPere"], "comp-parent")
        self.assertNotIn("type_competition", d)

    def test_029_niveau_property(self) -> None:
        ref = CompetitionRef(nom="Regionale 2 Masculine")
        niveau = ref.niveau
        self.assertIsNotNone(niveau)

    def test_030_niveau_property_none_when_no_nom(self) -> None:
        ref = CompetitionRef()
        niveau = ref.niveau
        self.assertIsNone(niveau)

    def test_031_round_trip(self) -> None:
        data = {
            "id": "comp-001",
            "nom": "Regionale 2",
            "code": "R2",
            "sexe": "M",
            "typeCompetition": "Championnat",
        }
        obj1 = CompetitionRef.from_dict(data)
        obj2 = CompetitionRef.from_dict(obj1.to_dict())
        self.assertEqual(obj1.to_dict(), obj2.to_dict())


class TestGetOrganismeResponseExtracted(unittest.TestCase):
    """Tests for rewritten GetOrganismeResponse using extracted models."""

    def test_032_from_dict_with_members(self) -> None:
        data = {
            "id": "org-001",
            "nom": "Club Test",
            "code": "CT01",
            "membres": [
                {"id": "m-001", "nom": "Dupont", "prenom": "Jean"},
                {"id": "m-002", "nom": "Martin", "prenom": "Pierre"},
            ],
        }
        resp = GetOrganismeResponse.from_dict(data)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.id, "org-001")
        self.assertEqual(len(resp.membres), 2)
        self.assertIsInstance(resp.membres[0], Membre)
        self.assertEqual(resp.membres[0].nom, "Dupont")

    def test_033_from_dict_with_engagements(self) -> None:
        data = {
            "id": "org-001",
            "nom": "Club Test",
            "engagements": [101, 102, 103],
        }
        resp = GetOrganismeResponse.from_dict(data)
        self.assertIsNotNone(resp)
        self.assertEqual(len(resp.engagements), 3)
        self.assertEqual(resp.engagements[0], 101)

    def test_034_from_dict_with_offres_pratiques(self) -> None:
        data = {
            "id": "org-001",
            "nom": "Club Test",
            "offresPratiques": [
                {
                    "ffbbserver_offres_pratiques_id": {
                        "id": "op-001",
                        "title": "Basket Loisir",
                    }
                }
            ],
        }
        resp = GetOrganismeResponse.from_dict(data)
        self.assertIsNotNone(resp)
        self.assertEqual(len(resp.offres_pratiques), 1)
        self.assertIsInstance(resp.offres_pratiques[0], OffrePratique)

    def test_035_from_dict_with_labellisation(self) -> None:
        data = {
            "id": "org-001",
            "nom": "Club Test",
            "labellisation": [
                {
                    "id": "li-001",
                    "debut": "2024-09-01T00:00:00+00:00",
                    "fin": "2025-08-31T23:59:59+00:00",
                    "idLabellisationProgramme": {
                        "id": "lp-001",
                        "libelle": "Label OR",
                    },
                }
            ],
        }
        resp = GetOrganismeResponse.from_dict(data)
        self.assertIsNotNone(resp)
        self.assertEqual(len(resp.labellisation), 1)
        self.assertIsInstance(resp.labellisation[0], LabellisationItem)

    def test_036_from_dict_empty_returns_none(self) -> None:
        self.assertIsNone(GetOrganismeResponse.from_dict({}))

    def test_037_from_dict_errors_returns_none(self) -> None:
        self.assertIsNone(GetOrganismeResponse.from_dict({"errors": ["err"]}))

    def test_038_from_dict_snake_case_fields(self) -> None:
        data = {
            "id": "org-001",
            "urlSiteWeb": "https://example.com",
            "nomClubPro": "Pro Club",
            "adresseClubPro": "10 avenue Foch",
        }
        resp = GetOrganismeResponse.from_dict(data)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.url_site_web, "https://example.com")
        self.assertEqual(resp.nom_club_pro, "Pro Club")
        self.assertEqual(resp.adresse_club_pro, "10 avenue Foch")

    def test_039_from_dict_empty_lists_default(self) -> None:
        data = {"id": "org-001", "nom": "Club Test"}
        resp = GetOrganismeResponse.from_dict(data)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.membres, [])
        self.assertEqual(resp.engagements, [])
        self.assertEqual(resp.offres_pratiques, [])
        self.assertEqual(resp.labellisation, [])
        self.assertEqual(resp.competitions, [])
        self.assertEqual(resp.organismes_fils, [])


if __name__ == "__main__":
    unittest.main()
