from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_int, from_none, from_union


class TournoiTypeClass:
    open_plus: int | None = None
    open_plus_access: int | None = None
    open_start: int | None = None

    def __init__(
        self,
        open_plus: int | None = None,
        open_plus_access: int | None = None,
        open_start: int | None = None,
    ):
        self.open_plus = open_plus
        self.open_plus_access = open_plus_access
        self.open_start = open_start

    @staticmethod
    def from_dict(obj: Any) -> TournoiTypeClass:
        assert isinstance(obj, dict)
        open_plus = from_union([from_int, from_none], obj.get("Open Plus"))
        open_plus_access = from_union(
            [from_int, from_none], obj.get("Open Plus Access")
        )
        open_start = from_union([from_int, from_none], obj.get("Open Start"))
        return TournoiTypeClass(open_plus, open_plus_access, open_start)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.open_plus is not None:
            result["Open Plus"] = from_union([from_int, from_none], self.open_plus)
        if self.open_plus_access is not None:
            result["Open Plus Access"] = from_union(
                [from_int, from_none], self.open_plus_access
            )
        if self.open_start is not None:
            result["Open Start"] = from_union([from_int, from_none], self.open_start)
        return result
