"""Unit tests for PouleRencontreItemModel."""

from __future__ import annotations

import unittest
from datetime import datetime

from ffbb_api_client_v2.directus_ffbb.models.poule_rencontre_item_model import (
    PouleRencontreItemModel,
)


class TestPouleRencontreItemModelFromDict(unittest.TestCase):
    def test_full_data(self) -> None:
        data = {
            "id": "abc-123",
            "numero": "5",
            "numeroJournee": 3,
            "idPoule": "poule-1",
            "competitionId": "comp-42",
            "resultatEquipe1": 78,
            "resultatEquipe2": 65,
            "joue": True,
            "nomEquipe1": "Club A",
            "nomEquipe2": "Club B",
            "date_rencontre": "2025-12-15T20:00:00Z",
        }
        item = PouleRencontreItemModel.from_dict(data)
        self.assertEqual(item.id, "abc-123")
        self.assertEqual(item.numero, "5")
        self.assertEqual(item.numeroJournee, 3)
        self.assertEqual(item.idPoule, "poule-1")
        self.assertEqual(item.competitionId, "comp-42")
        self.assertEqual(item.resultatEquipe1, 78)
        self.assertEqual(item.resultatEquipe2, 65)
        self.assertTrue(item.joue)
        self.assertEqual(item.nomEquipe1, "Club A")
        self.assertEqual(item.nomEquipe2, "Club B")
        self.assertIsInstance(item.date_rencontre, datetime)

    def test_missing_fields_use_defaults(self) -> None:
        item = PouleRencontreItemModel.from_dict({})
        self.assertEqual(item.id, "")
        self.assertEqual(item.numero, "")
        self.assertEqual(item.numeroJournee, 0)
        self.assertEqual(item.idPoule, "")
        self.assertEqual(item.competitionId, "")
        self.assertEqual(item.resultatEquipe1, 0)
        self.assertEqual(item.resultatEquipe2, 0)
        self.assertFalse(item.joue)
        self.assertEqual(item.nomEquipe1, "")
        self.assertEqual(item.nomEquipe2, "")
        self.assertEqual(item.date_rencontre, datetime(1970, 1, 1))

    def test_partial_data(self) -> None:
        data = {
            "id": "x",
            "numero": "1",
            "joue": False,
        }
        item = PouleRencontreItemModel.from_dict(data)
        self.assertEqual(item.id, "x")
        self.assertEqual(item.numero, "1")
        self.assertFalse(item.joue)
        self.assertEqual(item.nomEquipe1, "")


if __name__ == "__main__":
    unittest.main()
