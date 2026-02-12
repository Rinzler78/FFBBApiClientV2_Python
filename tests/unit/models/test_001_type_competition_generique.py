"""Round-trip tests for TypeCompetitionGenerique."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.type_competition_generique import (
    TypeCompetitionGenerique,
)


class Test039TypeCompetitionGenerique(unittest.TestCase):
    def _assert_stable(self, model_class: type, input_data: dict[str, Any]) -> None:
        obj1 = model_class.from_dict(input_data)
        dict1 = obj1.to_dict()
        obj2 = model_class.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2, f"{model_class.__name__} round-trip not stable")

    def test_000_round_trip_with_logo(self) -> None:
        self._assert_stable(
            TypeCompetitionGenerique,
            {
                "id": "tcg-001",
                "logo": {
                    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                    "gradient_color": "#003366",
                },
            },
        )

    def test_001_round_trip_no_logo(self) -> None:
        self._assert_stable(
            TypeCompetitionGenerique,
            {"id": "tcg-002", "logo": None},
        )

    def test_002_round_trip_minimal(self) -> None:
        self._assert_stable(TypeCompetitionGenerique, {"id": "tcg-003"})


if __name__ == "__main__":
    unittest.main()
