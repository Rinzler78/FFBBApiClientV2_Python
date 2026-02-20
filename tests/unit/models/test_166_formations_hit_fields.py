"""Tests for FormationsHit new fields (18 denormalized fields)."""

from __future__ import annotations

import unittest
from datetime import datetime
from uuid import UUID

from ffbb_api_client_v2.meilisearch_ffbb.models.formations_hit import FormationsHit


class TestFormationsHitNewFields(unittest.TestCase):
    """Test new denormalized fields added to FormationsHit."""

    FULL_DATA: dict = {
        "id": "formation-1",
        "title": "Stage National",
        "date_end": "2026-04-06T00:00:00",
        "date_end_formatted": 20260406,
        "date_start": "2026-04-02T00:00:00",
        "date_start_formatted": 20260402,
        "entity": "FEDE",
        "formation_domain": "Officiel",
        "formation_duration_hours": "7h00",
        "formation_id": "13142e30-bcc4-4321-a3f3-0f2751286096",
        "formation_image": "https://api.ffbb.com/assets/test.png",
        "formation_mode": "in_person",
        "formation_theme": "Gestion des acteurs",
        "formation_thumbnail": "https://api.ffbb.com/assets/test.png?height=500",
        "formation_title": "Stage National Arbitres",
        "place": "CHOLET",
        "postal_code": "49300",
        "reference_hidden": "ref 1750",
        "subscribeBtn": "https://extranet.ffbb.com/subscribe",
        "subscribe_button": "https://extranet.ffbb.com/subscribe2",
    }

    def test_from_dict_with_all_new_fields(self) -> None:
        hit = FormationsHit.from_dict(self.FULL_DATA)
        self.assertIsInstance(hit.date_end, datetime)
        self.assertEqual(hit.date_end_formatted, 20260406)
        self.assertIsInstance(hit.date_start, datetime)
        self.assertEqual(hit.date_start_formatted, 20260402)
        self.assertEqual(hit.entity, "FEDE")
        self.assertEqual(hit.formation_domain, "Officiel")
        self.assertEqual(hit.formation_duration_hours, "7h00")
        self.assertEqual(hit.formation_id, UUID("13142e30-bcc4-4321-a3f3-0f2751286096"))
        self.assertEqual(hit.formation_image, "https://api.ffbb.com/assets/test.png")
        self.assertEqual(hit.formation_mode, "in_person")
        self.assertEqual(hit.formation_theme, "Gestion des acteurs")
        self.assertIsNotNone(hit.formation_thumbnail)
        self.assertEqual(hit.formation_title, "Stage National Arbitres")
        self.assertEqual(hit.place, "CHOLET")
        self.assertEqual(hit.postal_code, "49300")
        self.assertEqual(hit.reference_hidden, "ref 1750")
        self.assertEqual(hit.subscribe_btn, "https://extranet.ffbb.com/subscribe")
        self.assertEqual(hit.subscribe_button, "https://extranet.ffbb.com/subscribe2")

    def test_from_dict_missing_new_fields_returns_none(self) -> None:
        hit = FormationsHit.from_dict({"id": "f1"})
        self.assertIsNone(hit.date_end)
        self.assertIsNone(hit.date_end_formatted)
        self.assertIsNone(hit.date_start)
        self.assertIsNone(hit.date_start_formatted)
        self.assertIsNone(hit.entity)
        self.assertIsNone(hit.formation_domain)
        self.assertIsNone(hit.formation_duration_hours)
        self.assertIsNone(hit.formation_id)
        self.assertIsNone(hit.formation_image)
        self.assertIsNone(hit.formation_mode)
        self.assertIsNone(hit.formation_theme)
        self.assertIsNone(hit.formation_thumbnail)
        self.assertIsNone(hit.formation_title)
        self.assertIsNone(hit.place)
        self.assertIsNone(hit.postal_code)
        self.assertIsNone(hit.reference_hidden)
        self.assertIsNone(hit.subscribe_btn)
        self.assertIsNone(hit.subscribe_button)

    def test_to_dict_includes_new_fields(self) -> None:
        hit = FormationsHit.from_dict(self.FULL_DATA)
        d = hit.to_dict()
        self.assertIn("date_end", d)
        self.assertEqual(d["date_end_formatted"], 20260406)
        self.assertIn("date_start", d)
        self.assertEqual(d["date_start_formatted"], 20260402)
        self.assertEqual(d["entity"], "FEDE")
        self.assertEqual(d["formation_domain"], "Officiel")
        self.assertEqual(d["formation_duration_hours"], "7h00")
        self.assertEqual(d["formation_id"], "13142e30-bcc4-4321-a3f3-0f2751286096")
        self.assertEqual(d["formation_image"], "https://api.ffbb.com/assets/test.png")
        self.assertEqual(d["formation_mode"], "in_person")
        self.assertEqual(d["formation_theme"], "Gestion des acteurs")
        self.assertIn("formation_thumbnail", d)
        self.assertEqual(d["formation_title"], "Stage National Arbitres")
        self.assertEqual(d["place"], "CHOLET")
        self.assertEqual(d["postal_code"], "49300")
        self.assertEqual(d["reference_hidden"], "ref 1750")
        self.assertEqual(d["subscribeBtn"], "https://extranet.ffbb.com/subscribe")
        self.assertEqual(d["subscribe_button"], "https://extranet.ffbb.com/subscribe2")

    def test_to_dict_excludes_none_new_fields(self) -> None:
        hit = FormationsHit.from_dict({"id": "f1"})
        d = hit.to_dict()
        for key in [
            "date_end",
            "date_end_formatted",
            "date_start",
            "date_start_formatted",
            "entity",
            "formation_domain",
            "formation_duration_hours",
            "formation_id",
            "formation_image",
            "formation_mode",
            "formation_theme",
            "formation_thumbnail",
            "formation_title",
            "place",
            "postal_code",
            "reference_hidden",
            "subscribeBtn",
            "subscribe_button",
        ]:
            self.assertNotIn(key, d)


if __name__ == "__main__":
    unittest.main()
