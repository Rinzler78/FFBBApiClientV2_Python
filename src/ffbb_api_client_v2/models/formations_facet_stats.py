from __future__ import annotations

from typing import Any

from .facet_stats import FacetStats


class FormationsFacetStats(FacetStats):
    @staticmethod
    def from_dict(obj: Any) -> FormationsFacetStats:
        return FormationsFacetStats()

    def to_dict(self) -> dict:
        return super().to_dict()
