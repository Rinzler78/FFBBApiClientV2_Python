"""Tests for CompetitionsHit new fields (age, code_comite, etc.)."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.meilisearch_ffbb.models.competitions_hit import CompetitionsHit


class TestCompetitionsHitNewFields(unittest.TestCase):
    """Test new fields added to CompetitionsHit from discover_types report."""

    FULL_DATA: dict = {
        "nom": "Championnat",
        "id": "200000001234",
        "age": "SE F",
        "codeComite": "IDF",
        "codeLigue": "IDF",
        "compare_old_site": False,
        "ordre": 2,
        "participants": "Club A | Club B",
        "slug": "pnf",
        "toUpdate": False,
    }

    def test_from_dict_with_all_new_fields(self) -> None:
        hit = CompetitionsHit.from_dict(self.FULL_DATA)
        self.assertEqual(hit.age, "SE F")
        self.assertEqual(hit.code_comite, "IDF")
        self.assertEqual(hit.code_ligue, "IDF")
        self.assertIs(hit.compare_old_site, False)
        self.assertEqual(hit.ordre, 2)
        self.assertEqual(hit.participants, "Club A | Club B")
        self.assertEqual(hit.slug, "pnf")
        self.assertIs(hit.to_update, False)

    def test_from_dict_missing_new_fields_returns_none(self) -> None:
        data = {"nom": "Test", "id": "123"}
        hit = CompetitionsHit.from_dict(data)
        self.assertIsNone(hit.age)
        self.assertIsNone(hit.code_comite)
        self.assertIsNone(hit.code_ligue)
        self.assertIsNone(hit.compare_old_site)
        self.assertIsNone(hit.ordre)
        self.assertIsNone(hit.participants)
        self.assertIsNone(hit.slug)
        self.assertIsNone(hit.to_update)

    def test_to_dict_includes_new_fields(self) -> None:
        hit = CompetitionsHit.from_dict(self.FULL_DATA)
        d = hit.to_dict()
        self.assertEqual(d["age"], "SE F")
        self.assertEqual(d["codeComite"], "IDF")
        self.assertEqual(d["codeLigue"], "IDF")
        self.assertIs(d["compare_old_site"], False)
        self.assertEqual(d["ordre"], 2)
        self.assertEqual(d["participants"], "Club A | Club B")
        self.assertEqual(d["slug"], "pnf")
        self.assertIs(d["toUpdate"], False)

    def test_to_dict_excludes_none_new_fields(self) -> None:
        hit = CompetitionsHit.from_dict({"nom": "Test"})
        d = hit.to_dict()
        self.assertNotIn("age", d)
        self.assertNotIn("codeComite", d)
        self.assertNotIn("codeLigue", d)
        self.assertNotIn("compare_old_site", d)
        self.assertNotIn("ordre", d)
        self.assertNotIn("participants", d)
        self.assertNotIn("slug", d)
        self.assertNotIn("toUpdate", d)

    def test_round_trip_new_fields(self) -> None:
        hit = CompetitionsHit.from_dict(self.FULL_DATA)
        d = hit.to_dict()
        hit2 = CompetitionsHit.from_dict(d)
        self.assertEqual(hit2.age, hit.age)
        self.assertEqual(hit2.code_comite, hit.code_comite)
        self.assertEqual(hit2.code_ligue, hit.code_ligue)
        self.assertEqual(hit2.compare_old_site, hit.compare_old_site)
        self.assertEqual(hit2.ordre, hit.ordre)
        self.assertEqual(hit2.participants, hit.participants)
        self.assertEqual(hit2.slug, hit.slug)
        self.assertEqual(hit2.to_update, hit.to_update)


if __name__ == "__main__":
    unittest.main()
