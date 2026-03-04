"""Round-trip tests for Salle."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.salle import Salle


class Test036Salle(unittest.TestCase):
    def _assert_stable(self, model_class: type, input_data: dict[str, Any]) -> None:
        obj1 = model_class.from_dict(input_data)
        dict1 = obj1.to_dict()
        obj2 = model_class.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2, f"{model_class.__name__} round-trip not stable")

    def test_000_round_trip_full(self) -> None:
        self._assert_stable(
            Salle,
            {
                "id": "salle-001",
                "libelle": "Gymnase Central",
                "adresse": "12 rue du Sport",
                "adresseComplement": "Batiment B",
                "cartographie": "carto-001",
            },
        )

    def test_001_round_trip_minimal(self) -> None:
        self._assert_stable(Salle, {"id": "salle-002", "libelle": "Gymnase A"})

    def test_002_round_trip_no_cartographie(self) -> None:
        self._assert_stable(
            Salle,
            {
                "id": "salle-003",
                "libelle": "Gymnase B",
                "adresse": "5 avenue Foch",
                "adresseComplement": None,
                "cartographie": None,
            },
        )


if __name__ == "__main__":
    unittest.main()
