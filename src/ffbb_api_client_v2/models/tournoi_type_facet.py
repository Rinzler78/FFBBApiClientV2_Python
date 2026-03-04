from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_int


@dataclass
class TournoiTypeFacet:
    open_plus: int | None = None
    open_plus_access: int | None = None
    open_start: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> TournoiTypeFacet:
        assert isinstance(obj, dict)
        open_plus = from_int(obj, "Open Plus")
        open_plus_access = from_int(obj, "Open Plus Access")
        open_start = from_int(obj, "Open Start")
        return TournoiTypeFacet(
            open_plus=open_plus,
            open_plus_access=open_plus_access,
            open_start=open_start,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.open_plus is not None:
            result["Open Plus"] = self.open_plus
        if self.open_plus_access is not None:
            result["Open Plus Access"] = self.open_plus_access
        if self.open_start is not None:
            result["Open Start"] = self.open_start
        return result
