"""Tests for FormationSession model."""

from __future__ import annotations

import unittest
from datetime import datetime
from typing import Any

from ffbb_api_client_v2.meilisearch_ffbb.models.formation_session import (
    FormationSession,
)

SAMPLE_DATA: dict[str, Any] = {
    "id": "1baa9997-82fc-47f3-bd59-af009452b2dc",
    "title": "SEMINAIRE DE REVALIDATION DES ENTRAINEURS",
    "date_start": "2026-02-21T00:00:00",
    "date_end": "2026-02-22T00:00:00",
    "place": "CHALON-SUR-SAONE",
    "postal_code": "71100",
    "reference": "REF-001",
    "entity": "FFBB",
    "subscribeBtn": "https://example.com/subscribe",
}


class TestFormationSession(unittest.TestCase):
    def test_000_from_dict_valid(self) -> None:
        result = FormationSession.from_dict(SAMPLE_DATA)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "1baa9997-82fc-47f3-bd59-af009452b2dc")
        self.assertEqual(result.title, "SEMINAIRE DE REVALIDATION DES ENTRAINEURS")
        self.assertIsInstance(result.date_start, datetime)
        self.assertIsInstance(result.date_end, datetime)
        self.assertEqual(result.place, "CHALON-SUR-SAONE")
        self.assertEqual(result.postal_code, "71100")
        self.assertEqual(result.reference, "REF-001")
        self.assertEqual(result.entity, "FFBB")
        self.assertEqual(result.subscribe_btn, "https://example.com/subscribe")

    def test_001_from_dict_not_dict_raises(self) -> None:
        with self.assertRaises(TypeError):
            FormationSession.from_dict(None)

    def test_002_from_dict_minimal(self) -> None:
        result = FormationSession.from_dict({})
        self.assertIsNone(result.id)
        self.assertIsNone(result.title)
        self.assertIsNone(result.date_start)
        self.assertIsNone(result.date_end)
        self.assertIsNone(result.place)
        self.assertIsNone(result.postal_code)
        self.assertIsNone(result.reference)
        self.assertIsNone(result.entity)
        self.assertIsNone(result.subscribe_btn)

    def test_003_to_dict_full(self) -> None:
        result = FormationSession.from_dict(SAMPLE_DATA)
        d = result.to_dict()
        self.assertEqual(d["id"], "1baa9997-82fc-47f3-bd59-af009452b2dc")
        self.assertEqual(d["title"], "SEMINAIRE DE REVALIDATION DES ENTRAINEURS")
        self.assertIn("date_start", d)
        self.assertIn("date_end", d)
        self.assertEqual(d["place"], "CHALON-SUR-SAONE")
        self.assertEqual(d["postal_code"], "71100")
        self.assertEqual(d["reference"], "REF-001")
        self.assertEqual(d["entity"], "FFBB")
        self.assertEqual(d["subscribeBtn"], "https://example.com/subscribe")

    def test_004_to_dict_empty(self) -> None:
        result = FormationSession()
        d = result.to_dict()
        self.assertEqual(d, {})

    def test_005_roundtrip(self) -> None:
        original = FormationSession.from_dict(SAMPLE_DATA)
        d = original.to_dict()
        restored = FormationSession.from_dict(d)
        self.assertEqual(restored.id, original.id)
        self.assertEqual(restored.title, original.title)
        self.assertIsInstance(restored.date_start, datetime)
        self.assertIsInstance(restored.date_end, datetime)
        self.assertEqual(restored.place, original.place)
        self.assertEqual(restored.postal_code, original.postal_code)
        self.assertEqual(restored.reference, original.reference)
        self.assertEqual(restored.entity, original.entity)
        self.assertEqual(restored.subscribe_btn, original.subscribe_btn)

    def test_006_nullable_dates(self) -> None:
        data = {**SAMPLE_DATA, "date_start": None, "date_end": None}
        result = FormationSession.from_dict(data)
        self.assertIsNone(result.date_start)
        self.assertIsNone(result.date_end)

    def test_007_subscribe_btn_camel_case_mapping(self) -> None:
        """subscribeBtn in JSON maps to subscribe_btn in Python."""
        data = {"subscribeBtn": "https://example.com/sub"}
        result = FormationSession.from_dict(data)
        self.assertEqual(result.subscribe_btn, "https://example.com/sub")
        d = result.to_dict()
        self.assertEqual(d["subscribeBtn"], "https://example.com/sub")


if __name__ == "__main__":
    unittest.main()
