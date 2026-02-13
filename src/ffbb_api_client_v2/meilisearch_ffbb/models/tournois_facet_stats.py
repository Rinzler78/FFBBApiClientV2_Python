from __future__ import annotations

from typing import Any

from ...meilisearch.models.facet_stats import FacetStats


class TournoisFacetStats(FacetStats):
    @staticmethod
    def from_dict(obj: Any) -> TournoisFacetStats:
        return TournoisFacetStats()

    def to_dict(self) -> dict:
        return super().to_dict()
