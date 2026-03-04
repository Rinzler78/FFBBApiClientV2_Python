"""Round-trip tests for Competition (from competition.py)."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.competition import Competition


class Test044CompetitionId(unittest.TestCase):
    def _assert_stable(self, model_class: type, input_data: dict[str, Any]) -> None:
        obj1 = model_class.from_dict(input_data)
        dict1 = obj1.to_dict()
        obj2 = model_class.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2, f"{model_class.__name__} round-trip not stable")

    def test_000_round_trip_full(self) -> None:
        self._assert_stable(
            Competition,
            {
                "id": "comp-001",
                "nom": "D1 Masculine",
                "competition_origine_nom": "D1 Origine",
                "code": "D1M",
                "creationEnCours": False,
                "liveStat": True,
                "publicationInternet": "Affichée",
                "sexe": "Masculin",
                "typeCompetition": "Championnat",
                "pro": False,
                "logo": None,
                "categorie": {"code": "SE", "libelle": "Seniors", "ordre": 1},
                "typeCompetitionGenerique": {
                    "logo": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                },
                "competition_origine": "co-001",
                "nomExtended": "D1 Masculine Seniors",
            },
        )

    def test_001_round_trip_minimal(self) -> None:
        self._assert_stable(
            Competition,
            {"id": "comp-002", "nom": "Coupe", "code": "CDF"},
        )


if __name__ == "__main__":
    unittest.main()
