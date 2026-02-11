"""Tests for GetOfficielsResponse model."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.get_officiels_response import GetOfficielsResponse

SAMPLE_DATA: dict[str, Any] = {
    "nom": "DUPONT",
    "prenom": "Jean-Pierre",
    "numeroNational": "0075123456",
    "date_created": "2023-09-01T08:00:00.000Z",
    "date_updated": "2025-11-15T16:30:00.000Z",
}


class TestGetOfficielsResponse(unittest.TestCase):
    def test_from_dict_valid(self) -> None:
        result = GetOfficielsResponse.from_dict(SAMPLE_DATA)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.nom, "DUPONT")
        self.assertEqual(result.prenom, "Jean-Pierre")
        self.assertEqual(result.numeroNational, "0075123456")
        self.assertEqual(result.date_created, "2023-09-01T08:00:00.000Z")
        self.assertEqual(result.date_updated, "2025-11-15T16:30:00.000Z")

    def test_from_dict_none(self) -> None:
        result = GetOfficielsResponse.from_dict(None)  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_from_dict_empty(self) -> None:
        result = GetOfficielsResponse.from_dict({})
        self.assertIsNone(result)

    def test_from_dict_errors(self) -> None:
        result = GetOfficielsResponse.from_dict({"errors": [{"message": "err"}]})
        self.assertIsNone(result)

    def test_from_dict_not_dict(self) -> None:
        result = GetOfficielsResponse.from_dict("not a dict")  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_from_dict_minimal(self) -> None:
        """Only required field 'nom' present; optional fields default to None."""
        result = GetOfficielsResponse.from_dict({"nom": "MARTIN"})
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.nom, "MARTIN")
        self.assertIsNone(result.prenom)
        self.assertIsNone(result.numeroNational)
        self.assertIsNone(result.date_created)
        self.assertIsNone(result.date_updated)

    def test_from_list_valid(self) -> None:
        result = GetOfficielsResponse.from_list([SAMPLE_DATA, SAMPLE_DATA])
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], GetOfficielsResponse)
        self.assertIsInstance(result[1], GetOfficielsResponse)

    def test_from_list_empty(self) -> None:
        result = GetOfficielsResponse.from_list([])
        self.assertEqual(result, [])

    def test_from_list_filters_none_items(self) -> None:
        """from_list skips items that produce None (empty dicts, errors)."""
        data_list: list[dict[str, Any]] = [
            SAMPLE_DATA,
            {},
            {"errors": [{"message": "err"}]},
        ]
        result = GetOfficielsResponse.from_list(data_list)
        self.assertEqual(len(result), 1)

    def test_nom_coerced_to_string(self) -> None:
        """Numeric nom should be coerced to string."""
        result = GetOfficielsResponse.from_dict({"nom": 123})
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.nom, "123")


if __name__ == "__main__":
    unittest.main()
