"""Tests for RencontresHit new fields (16 fields)."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.meilisearch_ffbb.models.rencontres_hit import RencontresHit


class TestRencontresHitNewFields(unittest.TestCase):
    """Test new fields added to RencontresHit from discover_types report."""

    FULL_DATA: dict = {
        "id": "200000013828659",
        "competition_orgine": "Qualifications Coupe du Monde - 2026",
        "competition_origine": None,
        "handicap1": 14,
        "handicap2": None,
        "horaire": "20:30:00",
        "joue": True,
        "logo": None,
        "nomExtended": "|QCM||DIV|Féminin|9|International",
        "officiels_string": "CASSE David, ABBAD Habiba",
        "pro": True,
        "resultatEquipe1": "71",
        "resultatEquipe2": "27",
        "sexe": "Féminin",
        "typeCompetitionGenerique": None,
        "uniqueKey": "200000003017758_10_46",
        "url_competition": "/ligues/han/comites/0099/competitions/enat/match/200000013828659",
    }

    def test_from_dict_with_all_new_fields(self) -> None:
        hit = RencontresHit.from_dict(self.FULL_DATA)
        self.assertEqual(hit.competition_orgine, "Qualifications Coupe du Monde - 2026")
        self.assertIsNone(hit.competition_origine)
        self.assertEqual(hit.handicap1, 14)
        self.assertIsNone(hit.handicap2)
        self.assertEqual(hit.horaire, "20:30:00")
        self.assertIs(hit.joue, True)
        self.assertIsNone(hit.logo)
        self.assertEqual(hit.nom_extended, "|QCM||DIV|Féminin|9|International")
        self.assertEqual(hit.officiels_string, "CASSE David, ABBAD Habiba")
        self.assertIs(hit.pro, True)
        self.assertEqual(hit.resultat_equipe1, "71")
        self.assertEqual(hit.resultat_equipe2, "27")
        self.assertEqual(hit.sexe, "Féminin")
        self.assertIsNone(hit.type_competition_generique)
        self.assertEqual(hit.unique_key, "200000003017758_10_46")
        self.assertIn("/ligues/han", hit.url_competition or "")

    def test_from_dict_missing_new_fields_returns_none(self) -> None:
        hit = RencontresHit.from_dict({"id": "r1"})
        self.assertIsNone(hit.competition_orgine)
        self.assertIsNone(hit.competition_origine)
        self.assertIsNone(hit.handicap1)
        self.assertIsNone(hit.handicap2)
        self.assertIsNone(hit.horaire)
        self.assertIsNone(hit.joue)
        self.assertIsNone(hit.logo)
        self.assertIsNone(hit.nom_extended)
        self.assertIsNone(hit.officiels_string)
        self.assertIsNone(hit.pro)
        self.assertIsNone(hit.resultat_equipe1)
        self.assertIsNone(hit.resultat_equipe2)
        self.assertIsNone(hit.sexe)
        self.assertIsNone(hit.type_competition_generique)
        self.assertIsNone(hit.unique_key)
        self.assertIsNone(hit.url_competition)

    def test_to_dict_includes_new_fields(self) -> None:
        hit = RencontresHit.from_dict(self.FULL_DATA)
        d = hit.to_dict()
        self.assertEqual(
            d["competition_orgine"], "Qualifications Coupe du Monde - 2026"
        )
        self.assertEqual(d["handicap1"], 14)
        self.assertEqual(d["horaire"], "20:30:00")
        self.assertIs(d["joue"], True)
        self.assertEqual(d["nomExtended"], "|QCM||DIV|Féminin|9|International")
        self.assertEqual(d["officiels_string"], "CASSE David, ABBAD Habiba")
        self.assertIs(d["pro"], True)
        self.assertEqual(d["resultatEquipe1"], "71")
        self.assertEqual(d["resultatEquipe2"], "27")
        self.assertEqual(d["sexe"], "Féminin")
        self.assertEqual(d["uniqueKey"], "200000003017758_10_46")
        self.assertIn("/ligues/han", d["url_competition"])

    def test_to_dict_excludes_none_fields(self) -> None:
        hit = RencontresHit.from_dict({"id": "r1"})
        d = hit.to_dict()
        for key in [
            "competition_orgine",
            "competition_origine",
            "handicap1",
            "handicap2",
            "horaire",
            "joue",
            "logo",
            "nomExtended",
            "officiels_string",
            "pro",
            "resultatEquipe1",
            "resultatEquipe2",
            "sexe",
            "typeCompetitionGenerique",
            "uniqueKey",
            "url_competition",
        ]:
            self.assertNotIn(key, d)


if __name__ == "__main__":
    unittest.main()
