"""Round-trip tests for Organisateur."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.organisateur import Organisateur


class Test043Organisateur(unittest.TestCase):
    def _assert_stable(self, model_class: type, input_data: dict[str, Any]) -> None:
        obj1 = model_class.from_dict(input_data)
        dict1 = obj1.to_dict()
        obj2 = model_class.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2, f"{model_class.__name__} round-trip not stable")

    def test_000_round_trip_full(self) -> None:
        self._assert_stable(
            Organisateur,
            {
                "adresse": "1 rue Federation",
                "adresseClubPro": None,
                "cartographie": "carto-123",
                "code": "0750001",
                "commune": "12345",
                "communeClubPro": None,
                "id": "9999",
                "mail": "contact@club.fr",
                "nom": "Club Paris",
                "nomClubPro": "Paris BC Pro",
                "organisme_id_pere": None,
                "salle": None,
                "telephone": "0100000000",
                "type": "ASS",
                "type_association": None,
                "urlSiteWeb": "https://club.fr",
                "logo": "d4e5f6a7-b8c9-0123-4567-89abcdef0123",
                "nom_simple": "Paris",
                "dateAffiliation": None,
                "saison_en_cours": True,
                "entreprise": False,
                "handibasket": False,
                "omnisport": False,
                "horsAssociation": False,
                "offresPratiques": ["Basket Santé", "Micro Basket"],
                "engagements": ["eng-1", "eng-2"],
                "labellisation": ["Label Or"],
                "membres": ["101", "102"],
                "date_created": "2024-01-01T00:00:00",
                "date_updated": "2024-06-01T00:00:00",
                "logo_base64": None,
                "competitions": ["comp-1", "comp-2"],
                "organismes_fils": ["201", "202"],
            },
        )

    def test_001_round_trip_minimal(self) -> None:
        self._assert_stable(
            Organisateur,
            {
                "id": "8888",
                "nom": "Club Lyon",
                "adresseClubPro": None,
                "communeClubPro": None,
                "salle": None,
                "type_association": None,
                "dateAffiliation": None,
                "logo_base64": None,
            },
        )


if __name__ == "__main__":
    unittest.main()
