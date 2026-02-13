from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...meilisearch.models.facet_distribution import FacetDistribution


@dataclass
class FormationsFacetDistribution(FacetDistribution):
    domain: dict[str, int] | None = None
    mode: dict[str, int] | None = None
    theme: dict[str, int] | None = None
    type: dict[str, int] | None = None
    place: dict[str, int] | None = None
    places: dict[str, int] | None = None
    postal_code: dict[str, int] | None = None
    postal_codes: dict[str, int] | None = None
    date_start_formatted: dict[str, int] | None = None
    date_end_formatted: dict[str, int] | None = None

    @staticmethod
    def from_dict(obj: Any) -> FormationsFacetDistribution:
        assert isinstance(obj, dict)
        return FormationsFacetDistribution(
            domain=obj.get("domain"),
            mode=obj.get("mode"),
            theme=obj.get("theme"),
            type=obj.get("type"),
            place=obj.get("place"),
            places=obj.get("places"),
            postal_code=obj.get("postal_code"),
            postal_codes=obj.get("postal_codes"),
            date_start_formatted=obj.get("date_start_formatted"),
            date_end_formatted=obj.get("date_end_formatted"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.domain is not None:
            result["domain"] = self.domain
        if self.mode is not None:
            result["mode"] = self.mode
        if self.theme is not None:
            result["theme"] = self.theme
        if self.type is not None:
            result["type"] = self.type
        if self.place is not None:
            result["place"] = self.place
        if self.places is not None:
            result["places"] = self.places
        if self.postal_code is not None:
            result["postal_code"] = self.postal_code
        if self.postal_codes is not None:
            result["postal_codes"] = self.postal_codes
        if self.date_start_formatted is not None:
            result["date_start_formatted"] = self.date_start_formatted
        if self.date_end_formatted is not None:
            result["date_end_formatted"] = self.date_end_formatted
        return result
