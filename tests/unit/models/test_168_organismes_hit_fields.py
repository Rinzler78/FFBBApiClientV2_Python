"""Tests for OrganismesHit new fields (engagements_codes, saison, url_competition)."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.meilisearch_ffbb.models.organismes_hit import OrganismesHit


class TestOrganismesHitNewFields(unittest.TestCase):
    """Test new fields added to OrganismesHit."""

    FULL_DATA: dict = {
        "nom": "Club Test",
        "code": "CL01",
        "id": "org-1",
        "engagements_codes": "IDU15MP1 | Interdep U15M Phase 1",
        "saison": None,
        "url_competition": "/ligues/cvl/comites/0045/clubs/cvl0045063",
    }

    def test_from_dict_with_new_fields(self) -> None:
        hit = OrganismesHit.from_dict(self.FULL_DATA)
        self.assertEqual(hit.engagements_codes, "IDU15MP1 | Interdep U15M Phase 1")
        self.assertIsNone(hit.saison)
        self.assertEqual(
            hit.url_competition, "/ligues/cvl/comites/0045/clubs/cvl0045063"
        )

    def test_from_dict_missing_new_fields(self) -> None:
        hit = OrganismesHit.from_dict({"nom": "Test", "id": "1"})
        self.assertIsNone(hit.engagements_codes)
        self.assertIsNone(hit.saison)
        self.assertIsNone(hit.url_competition)

    def test_to_dict_includes_new_fields(self) -> None:
        hit = OrganismesHit.from_dict(self.FULL_DATA)
        d = hit.to_dict()
        self.assertEqual(d["engagements_codes"], "IDU15MP1 | Interdep U15M Phase 1")
        self.assertEqual(
            d["url_competition"], "/ligues/cvl/comites/0045/clubs/cvl0045063"
        )
        # saison is None so should be excluded
        self.assertNotIn("saison", d)

    def test_to_dict_excludes_none_new_fields(self) -> None:
        hit = OrganismesHit.from_dict({"nom": "Test"})
        d = hit.to_dict()
        self.assertNotIn("engagements_codes", d)
        self.assertNotIn("saison", d)
        self.assertNotIn("url_competition", d)


if __name__ == "__main__":
    unittest.main()
