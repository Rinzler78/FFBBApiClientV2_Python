from __future__ import annotations

from typing import Any

from ...meilisearch.models.facet_stats import FacetStats


class CompetitionsFacetStats(FacetStats):
    @staticmethod
    def from_dict(obj: Any) -> CompetitionsFacetStats:
        return CompetitionsFacetStats()

    def to_dict(self) -> dict:
        return super().to_dict()
