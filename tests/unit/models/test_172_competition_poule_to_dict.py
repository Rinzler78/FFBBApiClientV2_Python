"""Unit tests for CompetitionPoule to_dict branch coverage."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.models.competition_poule import CompetitionPoule


class TestCompetitionPouleToDict(unittest.TestCase):
    def test_all_none_and_empty_returns_empty(self) -> None:
        poule = CompetitionPoule()
        self.assertEqual(poule.to_dict(), {})

    def test_none_id_none_nom(self) -> None:
        poule = CompetitionPoule(id=None, nom=None)
        d = poule.to_dict()
        self.assertNotIn("id", d)
        self.assertNotIn("nom", d)

    def test_with_id_and_nom(self) -> None:
        poule = CompetitionPoule(id="123", nom="Poule A")
        d = poule.to_dict()
        self.assertEqual(d["id"], "123")
        self.assertEqual(d["nom"], "Poule A")

    def test_empty_lists_not_in_dict(self) -> None:
        poule = CompetitionPoule(id="1", nom="P", rencontres=[], engagements=[])
        d = poule.to_dict()
        self.assertNotIn("rencontres", d)
        self.assertNotIn("engagements", d)

    def test_from_dict_missing_lists(self) -> None:
        poule = CompetitionPoule.from_dict({"id": "1", "nom": "A"})
        self.assertEqual(poule.rencontres, [])
        self.assertEqual(poule.engagements, [])


if __name__ == "__main__":
    unittest.main()
