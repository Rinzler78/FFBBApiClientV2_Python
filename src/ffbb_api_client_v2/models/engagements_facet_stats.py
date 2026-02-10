from __future__ import annotations

from typing import Any

from .facet_stats import FacetStats


class EngagementsFacetStats(FacetStats):
    @staticmethod
    def from_dict(obj: Any) -> EngagementsFacetStats:
        return EngagementsFacetStats()

    def to_dict(self) -> dict:
        return super().to_dict()
