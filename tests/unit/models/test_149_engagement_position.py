"""Tests for EngagementPosition model."""

from __future__ import annotations

import unittest
from datetime import datetime
from typing import Any

from ffbb_api_client_v2.models.engagement_position import EngagementPosition

SAMPLE_DATA: dict[str, Any] = {
    "position": "5",
    "key": "5_0_0_0_0_0_0",
    "date": "2025-08-08T03:18:28.606Z",
}


class TestEngagementPosition(unittest.TestCase):
    def test_000_from_dict_valid(self) -> None:
        result = EngagementPosition.from_dict(SAMPLE_DATA)
        self.assertIsNotNone(result)
        self.assertEqual(result.position, "5")
        self.assertEqual(result.key, "5_0_0_0_0_0_0")
        self.assertIsInstance(result.date, datetime)

    def test_001_from_dict_not_dict_raises(self) -> None:
        with self.assertRaises(TypeError):
            EngagementPosition.from_dict(None)

    def test_002_from_dict_minimal(self) -> None:
        result = EngagementPosition.from_dict({})
        self.assertIsNone(result.position)
        self.assertIsNone(result.key)
        self.assertIsNone(result.date)

    def test_003_to_dict_full(self) -> None:
        result = EngagementPosition.from_dict(SAMPLE_DATA)
        d = result.to_dict()
        self.assertEqual(d["position"], "5")
        self.assertEqual(d["key"], "5_0_0_0_0_0_0")
        self.assertIn("date", d)
        self.assertIsInstance(d["date"], str)

    def test_004_to_dict_empty(self) -> None:
        result = EngagementPosition()
        d = result.to_dict()
        self.assertEqual(d, {})

    def test_005_roundtrip(self) -> None:
        original = EngagementPosition.from_dict(SAMPLE_DATA)
        d = original.to_dict()
        restored = EngagementPosition.from_dict(d)
        self.assertEqual(restored.position, original.position)
        self.assertEqual(restored.key, original.key)
        self.assertIsInstance(restored.date, datetime)

    def test_006_date_none(self) -> None:
        data = {"position": "1", "key": "1_0", "date": None}
        result = EngagementPosition.from_dict(data)
        self.assertEqual(result.position, "1")
        self.assertIsNone(result.date)

    def test_007_position_numeric_coerced_to_str(self) -> None:
        data = {"position": 13, "key": "13_1_0_1_0_1_-21"}
        result = EngagementPosition.from_dict(data)
        self.assertEqual(result.position, "13")


if __name__ == "__main__":
    unittest.main()
