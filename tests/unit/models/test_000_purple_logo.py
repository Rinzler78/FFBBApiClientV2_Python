"""Round-trip tests for PurpleLogo."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.purple_logo import PurpleLogo


class Test035PurpleLogo(unittest.TestCase):
    def _assert_stable(self, model_class: type, input_data: dict[str, Any]) -> None:
        obj1 = model_class.from_dict(input_data)
        dict1 = obj1.to_dict()
        obj2 = model_class.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2, f"{model_class.__name__} round-trip not stable")

    def test_000_round_trip_with_id(self) -> None:
        self._assert_stable(
            PurpleLogo,
            {"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"},
        )

    def test_001_round_trip_none_id(self) -> None:
        self._assert_stable(PurpleLogo, {"id": None})


if __name__ == "__main__":
    unittest.main()
