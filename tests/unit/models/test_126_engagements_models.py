"""Tests for Engagements index models (hit, facet_distribution, facet_stats, result)."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.meilisearch_ffbb.models.engagements_facet_distribution import (
    EngagementsFacetDistribution,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.engagements_facet_stats import (
    EngagementsFacetStats,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.engagements_hit import EngagementsHit
from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_engagements import (
    EngagementsMultiSearchResult,
)

SAMPLE_HIT: dict[str, Any] = {
    "id": "200000005137866",
    "nom": "Pré nationale féminine Poule A",
    "age": "SE F | SEF | Seniors F",
    "sexe": "Féminin",
    "clubPro": False,
    "codeAbrege": "",
    "codeClub": "IDF0078020",
    "codeComite": "0078",
    "codeLigue": "IDF",
    "competitionsUrl": "/ligues/idf/comites/0078/clubs/IDF0078020/equipes/200000005137866",
    "idCompetition": {
        "id": "200000002872432",
        "nom": "Pré nationale féminine",
        "code": "PNF",
        "sexe": "Féminin",
    },
    "idPoule": {"id": "200000003017520", "nom": "Poule A"},
    "logo": None,
    "niveau": {"code": "PNF", "libelle": "PNF"},
    "categorie": {"code": "SE", "libelle": "Seniors"},
    "nomClub": "CA MANTES LA VILLE",
    "nomClubPro": "",
    "nomComite": "COMITE DES YVELINES",
    "nomCtc": None,
    "nomEquipe": None,
    "nomLigue": "LIGUE IDF",
    "nomOfficiel": "",
    "nomOrganisme": "CA MANTES LA VILLE",
    "nomUsuel": "",
    "numeroEquipe": "1",
    "thumbnail": None,
    "_geo": {"lat": 48.978, "lng": 1.71424},
}


class TestEngagementsHit(unittest.TestCase):
    def test_000_from_dict_full(self) -> None:
        hit = EngagementsHit.from_dict(SAMPLE_HIT)
        self.assertEqual(hit.id, "200000005137866")
        self.assertEqual(hit.nom, "Pré nationale féminine Poule A")
        self.assertEqual(hit.sexe, "Féminin")
        self.assertFalse(hit.club_pro)
        self.assertEqual(hit.code_club, "IDF0078020")
        self.assertIsNotNone(hit.id_competition)
        self.assertIsNotNone(hit.id_poule)
        self.assertIsNotNone(hit.niveau)
        self.assertIsNotNone(hit.geo)

    def test_013_from_dict_empty(self) -> None:
        hit = EngagementsHit.from_dict({})
        self.assertIsNone(hit.id)
        self.assertIsNone(hit.nom)

    def test_009_to_dict_roundtrip(self) -> None:
        hit = EngagementsHit.from_dict(SAMPLE_HIT)
        d = hit.to_dict()
        self.assertEqual(d["id"], "200000005137866")
        self.assertEqual(d["clubPro"], False)
        self.assertIn("idCompetition", d)
        self.assertIn("_geo", d)

    def test_010_to_dict_empty(self) -> None:
        self.assertEqual(EngagementsHit().to_dict(), {})

    def test_004_is_valid_for_query_nom(self) -> None:
        hit = EngagementsHit.from_dict(SAMPLE_HIT)
        self.assertTrue(hit.is_valid_for_query("pré nationale"))
        self.assertTrue(hit.is_valid_for_query("mantes"))
        self.assertFalse(hit.is_valid_for_query("xyz_not_found"))

    def test_005_is_valid_for_query_empty(self) -> None:
        hit = EngagementsHit.from_dict(SAMPLE_HIT)
        self.assertTrue(hit.is_valid_for_query(""))

    def test_006_nested_dicts_deserialized(self) -> None:
        """idCompetition, idPoule, niveau, categorie are deserialized to typed models."""
        from ffbb_api_client_v2.models.categorie import (
            Categorie,
        )
        from ffbb_api_client_v2.models.competition_origine import CompetitionOrigine
        from ffbb_api_client_v2.models.id_poule import IDPoule

        hit = EngagementsHit.from_dict(SAMPLE_HIT)
        self.assertIsInstance(hit.id_competition, CompetitionOrigine)
        self.assertIsInstance(hit.id_poule, IDPoule)
        self.assertIsInstance(hit.niveau, Categorie)
        self.assertIsInstance(hit.categorie, Categorie)


class TestEngagementsFacetDistribution(unittest.TestCase):
    def test_013_from_dict_empty(self) -> None:
        fd = EngagementsFacetDistribution.from_dict({})
        self.assertIsNone(fd.club_pro)
        self.assertIsNone(fd.id_competition_sexe)

    def test_008_from_dict_with_data(self) -> None:
        data = {
            "clubPro": {"false": 100, "true": 10},
            "idCompetition.categorie.code": {"SE": 50, "U13": 30},
            "idCompetition.sexe": {"Féminin": 40, "Masculin": 60},
            "niveau.code": {"PNF": 20},
        }
        fd = EngagementsFacetDistribution.from_dict(data)
        self.assertEqual(fd.club_pro, {"false": 100, "true": 10})
        self.assertEqual(fd.id_competition_categorie_code, {"SE": 50, "U13": 30})
        self.assertIsNotNone(fd.id_competition_sexe)
        self.assertEqual(fd.niveau_code, {"PNF": 20})

    def test_009_to_dict_roundtrip(self) -> None:
        data = {
            "clubPro": {"false": 100},
            "idPoule.nom": {"Poule A": 5},
        }
        fd = EngagementsFacetDistribution.from_dict(data)
        d = fd.to_dict()
        self.assertEqual(d["clubPro"], {"false": 100})
        self.assertEqual(d["idPoule.nom"], {"Poule A": 5})

    def test_010_to_dict_empty(self) -> None:
        self.assertEqual(EngagementsFacetDistribution().to_dict(), {})


class TestEngagementsFacetStats(unittest.TestCase):
    def test_011_from_dict_and_to_dict(self) -> None:
        stats = EngagementsFacetStats.from_dict({})
        self.assertIsInstance(stats, EngagementsFacetStats)
        self.assertEqual(stats.to_dict(), {})


class TestEngagementsMultiSearchResult(unittest.TestCase):
    def test_012_from_dict_with_hits(self) -> None:
        data = {
            "indexUid": "ffbbserver_engagements",
            "hits": [SAMPLE_HIT],
            "query": "mantes",
            "processingTimeMs": 5,
            "limit": 10,
            "offset": 0,
            "estimatedTotalHits": 1,
        }
        result = EngagementsMultiSearchResult.from_dict(data)
        self.assertEqual(result.index_uid, "ffbbserver_engagements")
        self.assertIsNotNone(result.hits)
        assert result.hits is not None
        self.assertEqual(len(result.hits), 1)
        self.assertIsInstance(result.hits[0], EngagementsHit)

    def test_013_from_dict_empty(self) -> None:
        result = EngagementsMultiSearchResult.from_dict({})
        self.assertIsNone(result.hits)


if __name__ == "__main__":
    unittest.main()
