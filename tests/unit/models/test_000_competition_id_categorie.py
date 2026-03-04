"""Round-trip tests for Categorie."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.categorie import Categorie


class Test023CompetitionIdCategorie(unittest.TestCase):
    def _assert_stable(self, model_class: type, input_data: dict[str, Any]) -> None:
        obj1 = model_class.from_dict(input_data)
        dict1 = obj1.to_dict()
        obj2 = model_class.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2, f"{model_class.__name__} round-trip not stable")

    def test_000_round_trip_full(self) -> None:
        self._assert_stable(
            Categorie,
            {"code": "U17", "libelle": "U17 Masculin", "ordre": 3},
        )

    def test_001_round_trip_minimal(self) -> None:
        self._assert_stable(Categorie, {"code": "SE"})

    def test_002_round_trip_none_fields(self) -> None:
        self._assert_stable(
            Categorie,
            {"code": None, "libelle": None, "ordre": None},
        )


if __name__ == "__main__":
    unittest.main()
