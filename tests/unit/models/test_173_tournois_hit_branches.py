"""Unit tests for TournoisHit from_dict/to_dict branch coverage."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.meilisearch_ffbb.models.tournois_hit import TournoisHit


class TestTournoisHitFromDictMinimal(unittest.TestCase):
    """from_dict with all optional fields missing."""

    def test_minimal_dict(self) -> None:
        hit = TournoisHit.from_dict({})
        self.assertIsNone(hit.nom)
        self.assertIsNone(hit.sexe)
        self.assertIsNone(hit.adresse)
        self.assertIsNone(hit.nom_organisateur)
        self.assertIsNone(hit.description)
        self.assertIsNone(hit.site_choisi)
        self.assertIsNone(hit.id)
        self.assertIsNone(hit.code)
        self.assertIsNone(hit.date_created)
        self.assertIsNone(hit.date_updated)
        self.assertIsNone(hit.age_max)
        self.assertIsNone(hit.age_min)
        self.assertIsNone(hit.categorie_championnat3_x3_id)
        self.assertIsNone(hit.categorie_championnat3_x3_libelle)
        self.assertIsNone(hit.debut)
        self.assertIsNone(hit.fin)
        self.assertIsNone(hit.mail_organisateur)
        self.assertIsNone(hit.nb_participant_prevu)
        self.assertIsNone(hit.tarif_organisateur)
        self.assertIsNone(hit.telephone_organisateur)
        self.assertIsNone(hit.url_organisateur)
        self.assertIsNone(hit.adresse_complement)
        self.assertIsNone(hit.tournoi_types3_x3)
        self.assertIsNone(hit.cartographie)
        self.assertIsNone(hit.commune)
        self.assertIsNone(hit.document_flyer)
        self.assertIsNone(hit.tournoi_type)
        self.assertIsNone(hit.geo)
        self.assertIsNone(hit.debut_timestamp)
        self.assertIsNone(hit.fin_timestamp)
        self.assertIsNone(hit.thumbnail)


class TestTournoisHitToDictAllNone(unittest.TestCase):
    """to_dict with all None fields returns empty dict."""

    def test_all_none_returns_empty(self) -> None:
        hit = TournoisHit()
        self.assertEqual(hit.to_dict(), {})


class TestTournoisHitFromDictFull(unittest.TestCase):
    """from_dict with all fields present."""

    def test_full_dict(self) -> None:
        data = {
            "nom": "Tournoi 3x3",
            "sexe": "M",
            "adresse": "12 rue du Sport",
            "nomOrganisateur": "Club ABC",
            "description": "Un tournoi",
            "siteChoisi": "Gymnase",
            "id": 42,
            "code": "T42",
            "date_created": "2025-01-15T10:00:00Z",
            "date_updated": "2025-01-16T10:00:00Z",
            "ageMax": 18,
            "ageMin": 12,
            "categorieChampionnat3x3Id": 1,
            "categorieChampionnat3x3Libelle": "U18M",
            "debut": "2025-06-01T09:00:00Z",
            "fin": "2025-06-01T18:00:00Z",
            "mailOrganisateur": "org@test.com",
            "nbParticipantPrevu": 16,
            "tarifOrganisateur": 10,
            "telephoneOrganisateur": "0601020304",
            "urlOrganisateur": "https://example.com",
            "adresseComplement": "Bâtiment B",
            "tournoiTypes3x3": [],
            "cartographie": {"lat": 48.8, "lng": 2.3},
            "commune": {"id": "75001", "nom": "Paris"},
            "tournoiType": "3x3",
            "debut_timestamp": 1748764800,
            "fin_timestamp": 1748797200,
            "thumbnail": "https://example.com/thumb.jpg",
        }
        hit = TournoisHit.from_dict(data)
        self.assertEqual(hit.nom, "Tournoi 3x3")
        self.assertEqual(hit.id, 42)
        self.assertEqual(hit.code, "T42")
        self.assertEqual(hit.age_max, 18)
        self.assertEqual(hit.age_min, 12)

    def test_full_to_dict_roundtrip(self) -> None:
        """Ensure to_dict produces keys for non-None fields."""
        data = {
            "nom": "Tournoi 3x3",
            "sexe": "M",
            "adresse": "rue",
            "nomOrganisateur": "Club",
            "description": "desc",
            "siteChoisi": "Gym",
            "id": 1,
            "code": "T1",
            "ageMax": 20,
            "ageMin": 10,
            "mailOrganisateur": "a@b.c",
            "telephoneOrganisateur": "0600",
            "urlOrganisateur": "http://x",
            "adresseComplement": "apt",
            "debut_timestamp": 100,
            "fin_timestamp": 200,
            "thumbnail": "thumb.jpg",
        }
        hit = TournoisHit.from_dict(data)
        d = hit.to_dict()
        self.assertEqual(d["nom"], "Tournoi 3x3")
        self.assertEqual(d["id"], "1")
        self.assertEqual(d["ageMax"], 20)
        self.assertEqual(d["ageMin"], 10)
        self.assertEqual(d["mailOrganisateur"], "a@b.c")
        self.assertEqual(d["telephoneOrganisateur"], "0600")
        self.assertEqual(d["urlOrganisateur"], "http://x")
        self.assertEqual(d["adresseComplement"], "apt")
        self.assertEqual(d["debut_timestamp"], 100)
        self.assertEqual(d["fin_timestamp"], 200)
        self.assertEqual(d["thumbnail"], "thumb.jpg")


class TestTournoisHitPostInit(unittest.TestCase):
    """__post_init__ lower_ fields with None strings."""

    def test_lower_fields_none_when_none(self) -> None:
        hit = TournoisHit()
        self.assertIsNone(hit.lower_nom)
        self.assertIsNone(hit.lower_addresse)
        self.assertIsNone(hit.lower_nom_organisateur)
        self.assertIsNone(hit.lower_description)
        self.assertIsNone(hit.lower_site_choisi)
        self.assertIsNone(hit.lower_code)

    def test_lower_fields_set_when_present(self) -> None:
        hit = TournoisHit(
            nom="ABC",
            adresse="DEF",
            nom_organisateur="GHI",
            description="JKL",
            site_choisi="MNO",
            code="PQR",
        )
        self.assertEqual(hit.lower_nom, "abc")
        self.assertEqual(hit.lower_addresse, "def")
        self.assertEqual(hit.lower_nom_organisateur, "ghi")
        self.assertEqual(hit.lower_description, "jkl")
        self.assertEqual(hit.lower_site_choisi, "mno")
        self.assertEqual(hit.lower_code, "pqr")


if __name__ == "__main__":
    unittest.main()
