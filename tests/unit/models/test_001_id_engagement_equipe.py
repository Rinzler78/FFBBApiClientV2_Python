"""Round-trip tests for EngagementEquipe (validates bug fix 1b)."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.engagement_equipe import EngagementEquipe


class Test030IdEngagementEquipe(unittest.TestCase):
    def _assert_stable(self, model_class: type, input_data: dict[str, Any]) -> None:
        obj1 = model_class.from_dict(input_data)
        dict1 = obj1.to_dict()
        obj2 = model_class.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2, f"{model_class.__name__} round-trip not stable")

    def test_000_round_trip_with_logo(self) -> None:
        self._assert_stable(
            EngagementEquipe,
            {
                "id": "eng-001",
                "nomUsuel": "Paris BC",
                "logo": {
                    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                    "gradient_color": "#FF0000",
                },
            },
        )

    def test_001_round_trip_no_logo(self) -> None:
        self._assert_stable(
            EngagementEquipe,
            {"id": "eng-002", "nomUsuel": "Lyon BC", "logo": None},
        )

    def test_002_round_trip_minimal(self) -> None:
        self._assert_stable(EngagementEquipe, {"id": "eng-003"})


if __name__ == "__main__":
    unittest.main()
