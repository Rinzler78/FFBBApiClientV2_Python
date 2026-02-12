"""Round-trip tests for CompetitionOrigine."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.competition_origine import CompetitionOrigine


class Test029CompetitionOrigine(unittest.TestCase):
    def _assert_stable(self, model_class: type, input_data: dict[str, Any]) -> None:
        obj1 = model_class.from_dict(input_data)
        dict1 = obj1.to_dict()
        obj2 = model_class.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2, f"{model_class.__name__} round-trip not stable")

    def test_000_round_trip_full(self) -> None:
        self._assert_stable(
            CompetitionOrigine,
            {
                "id": "comp-orig-001",
                "code": "D1M",
                "nom": "Championnat D1 Masculine",
                "typeCompetition": "DIV",
                "categorie": {"ordre": 1},
                "typeCompetitionGenerique": {
                    "logo": {"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}
                },
            },
        )

    def test_001_round_trip_coupe(self) -> None:
        self._assert_stable(
            CompetitionOrigine,
            {
                "id": "comp-orig-002",
                "code": "CDF",
                "nom": "Coupe de France",
                "typeCompetition": "COUPE",
                "categorie": None,
                "typeCompetitionGenerique": None,
            },
        )

    def test_002_round_trip_minimal(self) -> None:
        self._assert_stable(CompetitionOrigine, {"id": "comp-orig-003"})


if __name__ == "__main__":
    unittest.main()
