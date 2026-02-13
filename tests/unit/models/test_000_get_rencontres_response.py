"""Tests for GetRencontresResponse model."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.directus_ffbb.models.get_rencontres_response import (
    GetRencontresResponse,
)

SAMPLE_DATA: dict[str, Any] = {
    "id": "200000012345678",
    "date": "2025-12-14",
    "date_rencontre": "2025-12-14T20:00:00",
    "horaire": "20:00",
    "numero": "J07-001",
    "numeroJournee": "7",
    "nomEquipe1": "PARIS BASKET 13",
    "nomEquipe2": "AS VILLEURBANNE",
    "resultatEquipe1": 78,
    "resultatEquipe2": 82,
    "joue": True,
    "etat": "TERMINE",
    "pratique": "5x5",
    "status": "published",
    "competitionId": {
        "id": "200000002800001",
        "nom": "Nationale Masculine 1",
        "code": "NM1",
    },
    "idOrganismeEquipe1": {
        "id": "200000001100001",
        "nom": "PARIS BASKET 13",
    },
    "idOrganismeEquipe2": {
        "id": "200000001100002",
        "nom": "AS VILLEURBANNE",
    },
    "idPoule": {"id": "200000003000001", "nom": "Poule unique"},
    "saison": {"id": "200000000000010", "nom": "2025-2026"},
    "salle": {
        "id": "200000004000001",
        "libelle": "Gymnase Marie Curie",
    },
    "gsId": {"id": "GS-12345"},
    "officiels": [
        {"nom": "DURAND", "prenom": "Luc", "role": "Arbitre 1"},
        {"nom": "MOREAU", "prenom": "Sophie", "role": "Arbitre 2"},
    ],
    "date_created": "2025-10-01T08:00:00.000Z",
    "date_updated": "2025-12-14T23:30:00.000Z",
}


class TestGetRencontresResponse(unittest.TestCase):
    def test_000_from_dict_valid(self) -> None:
        result = GetRencontresResponse.from_dict(SAMPLE_DATA)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.id, "200000012345678")
        self.assertEqual(result.date, "2025-12-14")
        self.assertEqual(result.date_rencontre, "2025-12-14T20:00:00")
        self.assertEqual(result.horaire, "20:00")
        self.assertEqual(result.numero, "J07-001")
        self.assertEqual(result.numeroJournee, "7")
        self.assertEqual(result.nomEquipe1, "PARIS BASKET 13")
        self.assertEqual(result.nomEquipe2, "AS VILLEURBANNE")
        self.assertEqual(result.resultatEquipe1, 78)
        self.assertEqual(result.resultatEquipe2, 82)
        self.assertTrue(result.joue)
        self.assertEqual(result.etat, "TERMINE")
        self.assertEqual(result.pratique, "5x5")
        self.assertEqual(result.status, "published")
        self.assertIsInstance(result.competitionId, dict)
        self.assertIsInstance(result.idOrganismeEquipe1, dict)
        self.assertIsInstance(result.idOrganismeEquipe2, dict)
        self.assertIsInstance(result.idPoule, dict)
        self.assertIsInstance(result.saison, dict)
        self.assertIsInstance(result.salle, dict)
        self.assertIsInstance(result.gsId, dict)
        self.assertIsInstance(result.officiels, list)
        self.assertEqual(len(result.officiels), 2)
        self.assertEqual(result.date_created, "2025-10-01T08:00:00.000Z")
        self.assertEqual(result.date_updated, "2025-12-14T23:30:00.000Z")

    def test_001_from_dict_none(self) -> None:
        result = GetRencontresResponse.from_dict(None)  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_002_from_dict_empty(self) -> None:
        result = GetRencontresResponse.from_dict({})
        self.assertIsNone(result)

    def test_003_from_dict_errors(self) -> None:
        result = GetRencontresResponse.from_dict({"errors": [{"message": "err"}]})
        self.assertIsNone(result)

    def test_004_from_dict_not_dict(self) -> None:
        result = GetRencontresResponse.from_dict("not a dict")  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_005_from_dict_minimal(self) -> None:
        """Only required field 'id' present; optional fields default to None or []."""
        result = GetRencontresResponse.from_dict({"id": "999"})
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.id, "999")
        self.assertIsNone(result.date)
        self.assertIsNone(result.date_rencontre)
        self.assertIsNone(result.horaire)
        self.assertIsNone(result.numero)
        self.assertIsNone(result.numeroJournee)
        self.assertIsNone(result.nomEquipe1)
        self.assertIsNone(result.nomEquipe2)
        self.assertIsNone(result.resultatEquipe1)
        self.assertIsNone(result.resultatEquipe2)
        self.assertIsNone(result.joue)
        self.assertIsNone(result.etat)
        self.assertIsNone(result.pratique)
        self.assertIsNone(result.status)
        self.assertIsNone(result.competitionId)
        self.assertIsNone(result.idOrganismeEquipe1)
        self.assertIsNone(result.idOrganismeEquipe2)
        self.assertIsNone(result.idPoule)
        self.assertIsNone(result.saison)
        self.assertIsNone(result.salle)
        self.assertIsNone(result.gsId)
        self.assertEqual(result.officiels, [])
        self.assertIsNone(result.date_created)
        self.assertIsNone(result.date_updated)

    def test_006_from_dict_nested_dicts_kept_raw(self) -> None:
        """Nested dict fields are kept as raw dicts, not deserialized."""
        result = GetRencontresResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.competitionId["nom"], "Nationale Masculine 1")  # type: ignore[index]
        self.assertEqual(result.idPoule["nom"], "Poule unique")  # type: ignore[index]
        self.assertEqual(result.saison["nom"], "2025-2026")  # type: ignore[index]

    def test_007_from_dict_officiels_empty_when_missing(self) -> None:
        """officiels defaults to empty list when key absent."""
        data = {k: v for k, v in SAMPLE_DATA.items() if k != "officiels"}
        result = GetRencontresResponse.from_dict(data)
        assert result is not None
        self.assertEqual(result.officiels, [])

    def test_008_from_list_valid(self) -> None:
        result = GetRencontresResponse.from_list([SAMPLE_DATA, SAMPLE_DATA])
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], GetRencontresResponse)
        self.assertIsInstance(result[1], GetRencontresResponse)

    def test_009_from_list_empty(self) -> None:
        result = GetRencontresResponse.from_list([])
        self.assertEqual(result, [])

    def test_010_from_list_filters_none_items(self) -> None:
        """from_list skips items that produce None (empty dicts, errors)."""
        data_list: list[dict[str, Any]] = [
            SAMPLE_DATA,
            {},
            {"errors": [{"message": "err"}]},
        ]
        result = GetRencontresResponse.from_list(data_list)
        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
