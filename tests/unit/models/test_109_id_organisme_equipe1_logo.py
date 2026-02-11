"""Round-trip tests for Logo (formerly IDOrganismeEquipe1Logo)."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.logo import Logo


class Test032Logo(unittest.TestCase):
    def _assert_stable(self, model_class: type, input_data: dict[str, Any]) -> None:
        obj1 = model_class.from_dict(input_data)
        dict1 = obj1.to_dict()
        obj2 = model_class.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2, f"{model_class.__name__} round-trip not stable")

    def test_001_round_trip_full(self) -> None:
        self._assert_stable(
            Logo,
            {
                "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "gradient_color": "#0055AA",
            },
        )

    def test_002_round_trip_id_only(self) -> None:
        self._assert_stable(
            Logo,
            {"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"},
        )

    def test_003_round_trip_none_fields(self) -> None:
        self._assert_stable(
            Logo,
            {"id": None, "gradient_color": None},
        )


if __name__ == "__main__":
    unittest.main()
