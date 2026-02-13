"""Tests for new Meilisearch search parameters in MultiSearchQuery."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.meilisearch.models.multi_search_query import MultiSearchQuery


class Test214MultiSearchQueryNewParams(unittest.TestCase):
    """Tests for advanced Meilisearch parameters added to MultiSearchQuery."""

    def test_000_default_limit_is_20(self) -> None:
        """Default limit should be 20 (aligned with Meilisearch default)."""
        q = MultiSearchQuery()
        self.assertEqual(q.limit, 20)

    def test_001_matching_strategy_to_dict(self) -> None:
        q = MultiSearchQuery(index_uid="test", q="hello", matching_strategy="all")
        d = q.to_dict()
        self.assertEqual(d["matchingStrategy"], "all")

    def test_002_matching_strategy_last(self) -> None:
        q = MultiSearchQuery(matching_strategy="last")
        d = q.to_dict()
        self.assertEqual(d["matchingStrategy"], "last")

    def test_003_matching_strategy_frequency(self) -> None:
        q = MultiSearchQuery(matching_strategy="frequency")
        d = q.to_dict()
        self.assertEqual(d["matchingStrategy"], "frequency")

    def test_004_matching_strategy_none_not_in_dict(self) -> None:
        q = MultiSearchQuery()
        d = q.to_dict()
        self.assertNotIn("matchingStrategy", d)

    def test_005_attributes_to_highlight(self) -> None:
        q = MultiSearchQuery(attributes_to_highlight=["*"])
        d = q.to_dict()
        self.assertEqual(d["attributesToHighlight"], ["*"])

    def test_006_highlight_tags(self) -> None:
        q = MultiSearchQuery(highlight_pre_tag="<em>", highlight_post_tag="</em>")
        d = q.to_dict()
        self.assertEqual(d["highlightPreTag"], "<em>")
        self.assertEqual(d["highlightPostTag"], "</em>")

    def test_007_attributes_to_crop(self) -> None:
        q = MultiSearchQuery(attributes_to_crop=["description"], crop_length=50)
        d = q.to_dict()
        self.assertEqual(d["attributesToCrop"], ["description"])
        self.assertEqual(d["cropLength"], 50)

    def test_008_crop_marker(self) -> None:
        q = MultiSearchQuery(crop_marker="...")
        d = q.to_dict()
        self.assertEqual(d["cropMarker"], "...")

    def test_009_show_matches_position(self) -> None:
        q = MultiSearchQuery(show_matches_position=True)
        d = q.to_dict()
        self.assertTrue(d["showMatchesPosition"])

    def test_010_show_ranking_score(self) -> None:
        q = MultiSearchQuery(show_ranking_score=True)
        d = q.to_dict()
        self.assertTrue(d["showRankingScore"])

    def test_011_show_ranking_score_details(self) -> None:
        q = MultiSearchQuery(show_ranking_score_details=True)
        d = q.to_dict()
        self.assertTrue(d["showRankingScoreDetails"])

    def test_012_ranking_score_threshold(self) -> None:
        q = MultiSearchQuery(ranking_score_threshold=0.5)
        d = q.to_dict()
        self.assertAlmostEqual(d["rankingScoreThreshold"], 0.5)

    def test_013_attributes_to_search_on(self) -> None:
        q = MultiSearchQuery(attributes_to_search_on=["nom", "adresse"])
        d = q.to_dict()
        self.assertEqual(d["attributesToSearchOn"], ["nom", "adresse"])

    def test_014_attributes_to_retrieve(self) -> None:
        q = MultiSearchQuery(attributes_to_retrieve=["id", "nom"])
        d = q.to_dict()
        self.assertEqual(d["attributesToRetrieve"], ["id", "nom"])

    def test_015_distinct(self) -> None:
        q = MultiSearchQuery(distinct="type_association.libelle")
        d = q.to_dict()
        self.assertEqual(d["distinct"], "type_association.libelle")

    def test_016_none_params_excluded_from_dict(self) -> None:
        """Parameters set to None should not appear in to_dict()."""
        q = MultiSearchQuery(index_uid="test", q="hello")
        d = q.to_dict()
        excluded_keys = [
            "matchingStrategy",
            "attributesToHighlight",
            "highlightPreTag",
            "highlightPostTag",
            "attributesToCrop",
            "cropLength",
            "cropMarker",
            "showMatchesPosition",
            "showRankingScore",
            "showRankingScoreDetails",
            "rankingScoreThreshold",
            "attributesToSearchOn",
            "attributesToRetrieve",
            "distinct",
        ]
        for key in excluded_keys:
            self.assertNotIn(key, d, f"{key} should not be in dict when None")

    def test_017_from_dict_with_new_params(self) -> None:
        raw = {
            "indexUid": "test",
            "q": "hello",
            "matchingStrategy": "all",
            "attributesToHighlight": ["*"],
            "highlightPreTag": "<b>",
            "highlightPostTag": "</b>",
            "attributesToCrop": ["desc"],
            "cropLength": 100,
            "cropMarker": "...",
            "showRankingScore": True,
            "showRankingScoreDetails": False,
            "rankingScoreThreshold": 0.3,
            "attributesToSearchOn": ["nom"],
            "attributesToRetrieve": ["id"],
            "distinct": "type",
        }
        q = MultiSearchQuery.from_dict(raw)
        self.assertEqual(q.matching_strategy, "all")
        self.assertEqual(q.attributes_to_highlight, ["*"])
        self.assertEqual(q.highlight_pre_tag, "<b>")
        self.assertEqual(q.highlight_post_tag, "</b>")
        self.assertEqual(q.attributes_to_crop, ["desc"])
        self.assertEqual(q.crop_length, 100)
        self.assertEqual(q.crop_marker, "...")
        self.assertTrue(q.show_ranking_score)
        self.assertFalse(q.show_ranking_score_details)
        self.assertAlmostEqual(q.ranking_score_threshold, 0.3)
        self.assertEqual(q.attributes_to_search_on, ["nom"])
        self.assertEqual(q.attributes_to_retrieve, ["id"])
        self.assertEqual(q.distinct, "type")

    def test_018_all_params_combined(self) -> None:
        """Test creating a query with all parameters set."""
        q = MultiSearchQuery(
            index_uid="ffbbserver_organismes",
            q="Paris",
            limit=10,
            offset=0,
            filter=["type_association.libelle = Club"],
            sort=["nom:asc"],
            matching_strategy="all",
            attributes_to_highlight=["nom"],
            ranking_score_threshold=0.3,
            distinct="type_association.libelle",
        )
        d = q.to_dict()
        self.assertEqual(d["indexUid"], "ffbbserver_organismes")
        self.assertEqual(d["q"], "Paris")
        self.assertEqual(d["matchingStrategy"], "all")
        self.assertEqual(d["attributesToHighlight"], ["nom"])
        self.assertAlmostEqual(d["rankingScoreThreshold"], 0.3)
        self.assertEqual(d["distinct"], "type_association.libelle")

    def test_019_roundtrip_to_dict_from_dict(self) -> None:
        """to_dict then from_dict should preserve all fields."""
        original = MultiSearchQuery(
            index_uid="test",
            q="hello",
            matching_strategy="frequency",
            attributes_to_highlight=["*"],
            ranking_score_threshold=0.7,
            distinct="field",
        )
        d = original.to_dict()
        restored = MultiSearchQuery.from_dict(d)
        self.assertEqual(restored.index_uid, original.index_uid)
        self.assertEqual(restored.matching_strategy, original.matching_strategy)
        self.assertEqual(
            restored.attributes_to_highlight, original.attributes_to_highlight
        )
        self.assertEqual(
            restored.ranking_score_threshold, original.ranking_score_threshold
        )
        self.assertEqual(restored.distinct, original.distinct)


if __name__ == "__main__":
    unittest.main()
