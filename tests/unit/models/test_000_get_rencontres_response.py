"""Tests for GetRencontresResponse model."""

from __future__ import annotations

import unittest
from datetime import datetime
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
    # FK-only fields (int IDs)
    "competitionId": 2800001,
    "idOrganismeEquipe1": 1100001,
    "idOrganismeEquipe2": 1100002,
    "idPoule": 3000001,
    "saison": 10,
    "salle": 4000001,
    "idEngagementEquipe1": 5001,
    "idEngagementEquipe2": 5002,
    # Embedded
    "gsId": None,
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
        # FK-only fields
        self.assertEqual(result.competitionId, 2800001)
        self.assertEqual(result.idOrganismeEquipe1, 1100001)
        self.assertEqual(result.idOrganismeEquipe2, 1100002)
        self.assertEqual(result.idPoule, 3000001)
        self.assertEqual(result.saison, 10)
        self.assertEqual(result.salle, 4000001)
        self.assertIsNone(result.gsId)
        self.assertIsInstance(result.officiels, list)
        self.assertEqual(len(result.officiels), 2)
        self.assertIsInstance(result.date_created, datetime)
        self.assertIsInstance(result.date_updated, datetime)

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

    def test_006_from_dict_fk_fields_are_ints(self) -> None:
        """FK-only fields are parsed as ints."""
        result = GetRencontresResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.competitionId, int)
        self.assertIsInstance(result.idOrganismeEquipe1, int)
        self.assertIsInstance(result.idOrganismeEquipe2, int)
        self.assertIsInstance(result.idPoule, int)
        self.assertIsInstance(result.saison, int)
        self.assertIsInstance(result.salle, int)

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
