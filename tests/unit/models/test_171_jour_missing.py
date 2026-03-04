"""Unit tests for JourEnum enum _missing_ branch coverage."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.models.jour_enum import JourEnum


class TestJourMissing(unittest.TestCase):
    def test_case_insensitive_lookup(self) -> None:
        self.assertEqual(JourEnum("Lundi"), JourEnum.MONDAY)
        self.assertEqual(JourEnum("DIMANCHE"), JourEnum.SUNDAY)

    def test_exact_value(self) -> None:
        self.assertEqual(JourEnum("vendredi"), JourEnum.FRIDAY)

    def test_nonexistent_string_raises(self) -> None:
        with self.assertRaises(ValueError):
            JourEnum("nonexistent_value")

    def test_non_string_raises(self) -> None:
        with self.assertRaises(ValueError):
            JourEnum(123)


if __name__ == "__main__":
    unittest.main()
