"""Tests for EngagementsHit new field (gradient_color)."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.meilisearch_ffbb.models.engagements_hit import EngagementsHit


class TestEngagementsHitNewFields(unittest.TestCase):
    """Test gradient_color field added to EngagementsHit."""

    FULL_DATA: dict = {
        "id": "eng-1",
        "nom": "Equipe Test",
        "gradient_color": "#5e6e5e",
    }

    def test_from_dict_with_gradient_color(self) -> None:
        hit = EngagementsHit.from_dict(self.FULL_DATA)
        self.assertEqual(hit.gradient_color, "#5e6e5e")

    def test_from_dict_missing_gradient_color(self) -> None:
        hit = EngagementsHit.from_dict({"id": "eng-1", "nom": "Test"})
        self.assertIsNone(hit.gradient_color)

    def test_to_dict_includes_gradient_color(self) -> None:
        hit = EngagementsHit.from_dict(self.FULL_DATA)
        d = hit.to_dict()
        self.assertEqual(d["gradient_color"], "#5e6e5e")

    def test_to_dict_excludes_none_gradient_color(self) -> None:
        hit = EngagementsHit.from_dict({"id": "eng-1"})
        d = hit.to_dict()
        self.assertNotIn("gradient_color", d)


if __name__ == "__main__":
    unittest.main()
