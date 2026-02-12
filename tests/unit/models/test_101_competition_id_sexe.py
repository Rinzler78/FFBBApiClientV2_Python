"""Round-trip tests for SexeClass (formerly CompetitionIDSexe)."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.sexe_class import SexeClass


class Test024SexeClass(unittest.TestCase):
    def _assert_stable(self, model_class: type, input_data: dict[str, Any]) -> None:
        obj1 = model_class.from_dict(input_data)
        dict1 = obj1.to_dict()
        obj2 = model_class.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2, f"{model_class.__name__} round-trip not stable")

    def test_000_round_trip_full(self) -> None:
        self._assert_stable(
            SexeClass,
            {"Féminin": 5, "Masculin": 10, "Mixte": 2},
        )

    def test_001_round_trip_partial(self) -> None:
        self._assert_stable(SexeClass, {"Masculin": 8})

    def test_002_round_trip_none_fields(self) -> None:
        self._assert_stable(
            SexeClass,
            {"Féminin": None, "Masculin": None, "Mixte": None},
        )


if __name__ == "__main__":
    unittest.main()
