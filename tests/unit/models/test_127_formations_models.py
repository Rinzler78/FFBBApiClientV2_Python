"""Tests for Formations index models (hit, facet_distribution, facet_stats, result)."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.meilisearch_ffbb.models.formations_facet_distribution import (
    FormationsFacetDistribution,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.formations_facet_stats import (
    FormationsFacetStats,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.formations_hit import FormationsHit
from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_formations import (
    FormationsMultiSearchResult,
)

SAMPLE_HIT: dict[str, Any] = {
    "id": "5faa8064-93a7-4817-9187-dc87c567dc1c",
    "title": "DIPLOME DE PREPARATEUR PHYSIQUE EN BASKETBALL",
    "mode": "in_person",
    "duration_hours": None,
    "goals": "DIPLOME DE PREPARATEUR PHYSIQUE EN BASKETBALL",
    "public": None,
    "prerequisites": None,
    "content": None,
    "pedagogy": None,
    "certification": None,
    "results": None,
    "description": None,
    "modalities": None,
    "level": None,
    "reference": "FEDE",
    "programIdFbi": None,
    "sessions": [],
    "files": [],
    "theme": "DIPLOME DE PREPARATEUR PHYSIQUE EN BASKETBALL",
    "domain": "Transversales",
    "image": None,
    "thumbnail": None,
    "mode_hidden": "Présentielle",
    "type": "formation",
    "postal_codes": [],
    "places": [],
    "id_origin_hash": "aTeHNOrTPV8jXC9appqLTQ%3D%3D",
}


class TestFormationsHit(unittest.TestCase):
    def test_000_from_dict_full(self) -> None:
        hit = FormationsHit.from_dict(SAMPLE_HIT)
        self.assertEqual(hit.id, "5faa8064-93a7-4817-9187-dc87c567dc1c")
        self.assertEqual(hit.title, "DIPLOME DE PREPARATEUR PHYSIQUE EN BASKETBALL")
        self.assertEqual(hit.mode, "in_person")
        self.assertEqual(hit.domain, "Transversales")
        self.assertEqual(hit.type, "formation")
        self.assertEqual(hit.reference, "FEDE")
        self.assertEqual(hit.sessions, [])
        self.assertEqual(hit.files, [])
        self.assertEqual(hit.postal_codes, [])
        self.assertEqual(hit.places, [])

    def test_013_from_dict_empty(self) -> None:
        hit = FormationsHit.from_dict({})
        self.assertIsNone(hit.id)
        self.assertIsNone(hit.title)

    def test_009_to_dict_roundtrip(self) -> None:
        hit = FormationsHit.from_dict(SAMPLE_HIT)
        d = hit.to_dict()
        self.assertEqual(d["id"], "5faa8064-93a7-4817-9187-dc87c567dc1c")
        self.assertEqual(d["type"], "formation")
        self.assertEqual(d["domain"], "Transversales")
        self.assertIn("mode_hidden", d)

    def test_010_to_dict_empty(self) -> None:
        self.assertEqual(FormationsHit().to_dict(), {})

    def test_004_is_valid_for_query_title(self) -> None:
        hit = FormationsHit.from_dict(SAMPLE_HIT)
        self.assertTrue(hit.is_valid_for_query("diplome"))
        self.assertTrue(hit.is_valid_for_query("transversales"))
        self.assertFalse(hit.is_valid_for_query("xyz_not_found"))

    def test_005_is_valid_for_query_empty(self) -> None:
        hit = FormationsHit.from_dict(SAMPLE_HIT)
        self.assertTrue(hit.is_valid_for_query(""))

    def test_006_duration_hours_parsed(self) -> None:
        data = {**SAMPLE_HIT, "duration_hours": 40}
        hit = FormationsHit.from_dict(data)
        self.assertEqual(hit.duration_hours, 40)


class TestFormationsFacetDistribution(unittest.TestCase):
    def test_013_from_dict_empty(self) -> None:
        fd = FormationsFacetDistribution.from_dict({})
        self.assertIsNone(fd.domain)
        self.assertIsNone(fd.mode)

    def test_008_from_dict_with_data(self) -> None:
        data = {
            "domain": {"Dirigeant": 4, "Officiel": 15, "Technicien": 68},
            "mode": {"in_person": 58, "mixed": 29, "remote": 1},
            "theme": {"Bénévole": 25, "DEFB": 2},
            "type": {"formation": 55, "session": 35},
        }
        fd = FormationsFacetDistribution.from_dict(data)
        self.assertEqual(fd.domain, {"Dirigeant": 4, "Officiel": 15, "Technicien": 68})
        self.assertEqual(fd.mode, {"in_person": 58, "mixed": 29, "remote": 1})
        self.assertEqual(fd.theme, {"Bénévole": 25, "DEFB": 2})
        self.assertEqual(fd.type, {"formation": 55, "session": 35})

    def test_009_to_dict_roundtrip(self) -> None:
        data = {
            "domain": {"Technicien": 68},
            "place": {"PARIS": 2},
            "postal_code": {"75000": 1},
        }
        fd = FormationsFacetDistribution.from_dict(data)
        d = fd.to_dict()
        self.assertEqual(d["domain"], {"Technicien": 68})
        self.assertEqual(d["place"], {"PARIS": 2})
        self.assertEqual(d["postal_code"], {"75000": 1})

    def test_010_to_dict_empty(self) -> None:
        self.assertEqual(FormationsFacetDistribution().to_dict(), {})


class TestFormationsFacetStats(unittest.TestCase):
    def test_011_from_dict_and_to_dict(self) -> None:
        stats = FormationsFacetStats.from_dict({})
        self.assertIsInstance(stats, FormationsFacetStats)
        self.assertEqual(stats.to_dict(), {})


class TestFormationsMultiSearchResult(unittest.TestCase):
    def test_012_from_dict_with_hits(self) -> None:
        data = {
            "indexUid": "ffbbserver_formations",
            "hits": [SAMPLE_HIT],
            "query": "diplome",
            "processingTimeMs": 3,
            "limit": 10,
            "offset": 0,
            "estimatedTotalHits": 1,
        }
        result = FormationsMultiSearchResult.from_dict(data)
        self.assertEqual(result.index_uid, "ffbbserver_formations")
        self.assertIsNotNone(result.hits)
        assert result.hits is not None
        self.assertEqual(len(result.hits), 1)
        self.assertIsInstance(result.hits[0], FormationsHit)

    def test_013_from_dict_empty(self) -> None:
        result = FormationsMultiSearchResult.from_dict({})
        self.assertIsNone(result.hits)


if __name__ == "__main__":
    unittest.main()
