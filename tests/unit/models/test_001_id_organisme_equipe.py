"""Round-trip tests for OrganismeEquipe."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.organisme_equipe import OrganismeEquipe


class Test031IdOrganismeEquipe(unittest.TestCase):
    def _assert_stable(self, model_class: type, input_data: dict[str, Any]) -> None:
        obj1 = model_class.from_dict(input_data)
        dict1 = obj1.to_dict()
        obj2 = model_class.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2, f"{model_class.__name__} round-trip not stable")

    def test_000_round_trip_full(self) -> None:
        self._assert_stable(
            OrganismeEquipe,
            {
                "id": "org-001",
                "nom": "Club Paris",
                "nom_simple": None,
                "code": "0750001",
                "nomClubPro": None,
                "logo": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            },
        )

    def test_001_round_trip_minimal(self) -> None:
        self._assert_stable(
            OrganismeEquipe,
            {"id": "org-002", "nom": "Club Lyon", "nom_simple": None},
        )

    def test_002_round_trip_with_code(self) -> None:
        self._assert_stable(
            OrganismeEquipe,
            {
                "id": "org-003",
                "nom": "Club Marseille",
                "nom_simple": None,
                "code": "0130001",
                "nomClubPro": "OM Basket",
                "logo": None,
            },
        )


if __name__ == "__main__":
    unittest.main()
