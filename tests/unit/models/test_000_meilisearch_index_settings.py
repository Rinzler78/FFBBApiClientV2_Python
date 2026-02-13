"""Tests for MeilisearchIndexSettings model."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.meilisearch.models.meilisearch_index_settings import (
    MeilisearchIndexSettings,
)


class Test124MeilisearchIndexSettings(unittest.TestCase):
    """Tests for MeilisearchIndexSettings from_dict and to_dict."""

    def test_000_from_dict_full(self) -> None:
        """Test from_dict with all fields populated."""
        data = {
            "filterableAttributes": ["type", "commune.codePostal"],
            "sortableAttributes": ["nom"],
            "searchableAttributes": ["nom", "code"],
            "displayedAttributes": ["*"],
            "rankingRules": ["words", "typo"],
            "stopWords": ["le", "la"],
            "synonyms": {"basket": ["basketball"]},
            "distinctAttribute": "id",
            "pagination": {"maxTotalHits": 1000},
            "faceting": {"maxValuesPerFacet": 100},
        }
        settings = MeilisearchIndexSettings.from_dict(data)

        self.assertEqual(settings.filterable_attributes, ["type", "commune.codePostal"])
        self.assertEqual(settings.sortable_attributes, ["nom"])
        self.assertEqual(settings.searchable_attributes, ["nom", "code"])
        self.assertEqual(settings.displayed_attributes, ["*"])
        self.assertEqual(settings.ranking_rules, ["words", "typo"])
        self.assertEqual(settings.stop_words, ["le", "la"])
        self.assertEqual(settings.synonyms, {"basket": ["basketball"]})
        self.assertEqual(settings.distinct_attribute, "id")
        self.assertEqual(settings.pagination, {"maxTotalHits": 1000})
        self.assertEqual(settings.faceting, {"maxValuesPerFacet": 100})

    def test_001_from_dict_empty(self) -> None:
        """Test from_dict with empty dict."""
        settings = MeilisearchIndexSettings.from_dict({})

        self.assertEqual(settings.filterable_attributes, [])
        self.assertEqual(settings.sortable_attributes, [])
        self.assertEqual(settings.searchable_attributes, [])
        self.assertEqual(settings.displayed_attributes, [])
        self.assertEqual(settings.ranking_rules, [])
        self.assertEqual(settings.stop_words, [])
        self.assertEqual(settings.synonyms, {})
        self.assertIsNone(settings.distinct_attribute)
        self.assertEqual(settings.pagination, {})
        self.assertEqual(settings.faceting, {})

    def test_002_to_dict_full(self) -> None:
        """Test to_dict with all fields populated."""
        settings = MeilisearchIndexSettings(
            filterable_attributes=["type"],
            sortable_attributes=["nom"],
            searchable_attributes=["nom"],
            displayed_attributes=["*"],
            ranking_rules=["words"],
            stop_words=["le"],
            synonyms={"a": ["b"]},
            distinct_attribute="id",
            pagination={"maxTotalHits": 1000},
            faceting={"maxValuesPerFacet": 100},
        )
        result = settings.to_dict()

        self.assertEqual(result["filterableAttributes"], ["type"])
        self.assertEqual(result["sortableAttributes"], ["nom"])
        self.assertEqual(result["searchableAttributes"], ["nom"])
        self.assertEqual(result["displayedAttributes"], ["*"])
        self.assertEqual(result["rankingRules"], ["words"])
        self.assertEqual(result["stopWords"], ["le"])
        self.assertEqual(result["synonyms"], {"a": ["b"]})
        self.assertEqual(result["distinctAttribute"], "id")
        self.assertEqual(result["pagination"], {"maxTotalHits": 1000})
        self.assertEqual(result["faceting"], {"maxValuesPerFacet": 100})

    def test_003_to_dict_empty(self) -> None:
        """Test to_dict with empty/default settings."""
        settings = MeilisearchIndexSettings()
        result = settings.to_dict()
        self.assertEqual(result, {})

    def test_004_roundtrip(self) -> None:
        """Test from_dict -> to_dict roundtrip."""
        data = {
            "filterableAttributes": ["type", "_geo"],
            "sortableAttributes": ["nom"],
            "searchableAttributes": ["nom", "code"],
            "displayedAttributes": ["*"],
            "rankingRules": ["words", "typo", "proximity"],
            "stopWords": [],
            "synonyms": {},
            "distinctAttribute": None,
            "pagination": {},
            "faceting": {},
        }
        settings = MeilisearchIndexSettings.from_dict(data)
        result = settings.to_dict()

        # Only non-empty/non-None values are included in to_dict output
        self.assertEqual(result["filterableAttributes"], ["type", "_geo"])
        self.assertEqual(result["sortableAttributes"], ["nom"])
        self.assertEqual(result["searchableAttributes"], ["nom", "code"])
        self.assertEqual(result["displayedAttributes"], ["*"])
        self.assertEqual(result["rankingRules"], ["words", "typo", "proximity"])

    def test_005_from_dict_invalid_type(self) -> None:
        """Test from_dict raises AssertionError for non-dict input."""
        with self.assertRaises(AssertionError):
            MeilisearchIndexSettings.from_dict("invalid")

    def test_006_from_dict_partial(self) -> None:
        """Test from_dict with partial data."""
        data = {
            "filterableAttributes": ["type"],
            "distinctAttribute": "id",
        }
        settings = MeilisearchIndexSettings.from_dict(data)
        self.assertEqual(settings.filterable_attributes, ["type"])
        self.assertEqual(settings.distinct_attribute, "id")
        self.assertEqual(settings.sortable_attributes, [])


if __name__ == "__main__":
    unittest.main()
