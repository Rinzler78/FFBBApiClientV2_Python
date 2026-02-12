"""Round-trip tests for CompetitionOrigineCategorie."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.competition_origine_categorie import (
    CompetitionOrigineCategorie,
)


class Test027CompetitionOrigineCategorie(unittest.TestCase):
    def _assert_stable(self, model_class: type, input_data: dict[str, Any]) -> None:
        obj1 = model_class.from_dict(input_data)
        dict1 = obj1.to_dict()
        obj2 = model_class.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2, f"{model_class.__name__} round-trip not stable")

    def test_000_round_trip(self) -> None:
        self._assert_stable(CompetitionOrigineCategorie, {"ordre": 1})

    def test_001_round_trip_none(self) -> None:
        self._assert_stable(CompetitionOrigineCategorie, {"ordre": None})


if __name__ == "__main__":
    unittest.main()
