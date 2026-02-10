from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MeilisearchIndexSettings:
    """Settings for a Meilisearch index."""

    filterable_attributes: list[str] = field(default_factory=list)
    sortable_attributes: list[str] = field(default_factory=list)
    searchable_attributes: list[str] = field(default_factory=list)
    displayed_attributes: list[str] = field(default_factory=list)
    ranking_rules: list[str] = field(default_factory=list)
    stop_words: list[str] = field(default_factory=list)
    synonyms: dict[str, list[str]] = field(default_factory=dict)
    distinct_attribute: str | None = None
    pagination: dict[str, Any] = field(default_factory=dict)
    faceting: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_dict(obj: Any) -> MeilisearchIndexSettings:
        assert isinstance(obj, dict)
        return MeilisearchIndexSettings(
            filterable_attributes=obj.get("filterableAttributes", []),
            sortable_attributes=obj.get("sortableAttributes", []),
            searchable_attributes=obj.get("searchableAttributes", []),
            displayed_attributes=obj.get("displayedAttributes", []),
            ranking_rules=obj.get("rankingRules", []),
            stop_words=obj.get("stopWords", []),
            synonyms=obj.get("synonyms", {}),
            distinct_attribute=obj.get("distinctAttribute"),
            pagination=obj.get("pagination", {}),
            faceting=obj.get("faceting", {}),
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.filterable_attributes:
            result["filterableAttributes"] = self.filterable_attributes
        if self.sortable_attributes:
            result["sortableAttributes"] = self.sortable_attributes
        if self.searchable_attributes:
            result["searchableAttributes"] = self.searchable_attributes
        if self.displayed_attributes:
            result["displayedAttributes"] = self.displayed_attributes
        if self.ranking_rules:
            result["rankingRules"] = self.ranking_rules
        if self.stop_words:
            result["stopWords"] = self.stop_words
        if self.synonyms:
            result["synonyms"] = self.synonyms
        if self.distinct_attribute is not None:
            result["distinctAttribute"] = self.distinct_attribute
        if self.pagination:
            result["pagination"] = self.pagination
        if self.faceting:
            result["faceting"] = self.faceting
        return result
