"""Tests for GetCommunesResponse model."""

from __future__ import annotations

import unittest
from datetime import datetime
from typing import Any

from ffbb_api_client_v2.directus_ffbb.models.get_communes_response import (
    GetCommunesResponse,
)

SAMPLE_DATA: dict[str, Any] = {
    "id": "a1b2c3d4-5678-9012-abcd-ef0123456789",
    "codeInsee": "75056",
    "codePostal": "75013",
    "departement": "75",
    "libelle": "PARIS 13EME ARRONDISSEMENT",
    "date_created": "2024-01-15T10:30:00.000Z",
    "date_updated": "2024-06-20T14:45:00.000Z",
}


class TestGetCommunesResponse(unittest.TestCase):
    def test_000_from_dict_valid(self) -> None:
        result = GetCommunesResponse.from_dict(SAMPLE_DATA)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.id, "a1b2c3d4-5678-9012-abcd-ef0123456789")
        self.assertEqual(result.codeInsee, "75056")
        self.assertEqual(result.codePostal, "75013")
        self.assertEqual(result.departement, "75")
        self.assertEqual(result.libelle, "PARIS 13EME ARRONDISSEMENT")
        self.assertIsInstance(result.date_created, datetime)
        self.assertIsInstance(result.date_updated, datetime)

    def test_001_from_dict_none(self) -> None:
        result = GetCommunesResponse.from_dict(None)  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_002_from_dict_empty(self) -> None:
        result = GetCommunesResponse.from_dict({})
        self.assertIsNone(result)

    def test_003_from_dict_errors(self) -> None:
        result = GetCommunesResponse.from_dict({"errors": [{"message": "err"}]})
        self.assertIsNone(result)

    def test_004_from_dict_not_dict(self) -> None:
        result = GetCommunesResponse.from_dict("not a dict")  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_005_from_dict_minimal(self) -> None:
        """Only required field 'id' present; optional fields default to None."""
        result = GetCommunesResponse.from_dict({"id": "123"})
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.id, "123")
        self.assertIsNone(result.codeInsee)
        self.assertIsNone(result.codePostal)
        self.assertIsNone(result.departement)
        self.assertIsNone(result.libelle)
        self.assertIsNone(result.date_created)
        self.assertIsNone(result.date_updated)

    def test_006_from_list_valid(self) -> None:
        result = GetCommunesResponse.from_list([SAMPLE_DATA, SAMPLE_DATA])
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], GetCommunesResponse)
        self.assertIsInstance(result[1], GetCommunesResponse)

    def test_007_from_list_empty(self) -> None:
        result = GetCommunesResponse.from_list([])
        self.assertEqual(result, [])

    def test_008_from_list_filters_none_items(self) -> None:
        """from_list skips items that produce None (empty dicts, errors)."""
        data_list: list[dict[str, Any]] = [
            SAMPLE_DATA,
            {},
            {"errors": [{"message": "err"}]},
        ]
        result = GetCommunesResponse.from_list(data_list)
        self.assertEqual(len(result), 1)

    def test_009_id_coerced_to_string(self) -> None:
        """Numeric id should be coerced to string."""
        result = GetCommunesResponse.from_dict({"id": 42})
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.id, "42")


if __name__ == "__main__":
    unittest.main()
