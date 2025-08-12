from __future__ import annotations

from typing import Any
from uuid import UUID

from ..utils.converter_utils import from_none, from_str, from_union


class Logo:
    id: UUID | None = None
    gradient_color: str | None = None

    def __init__(self, id: UUID | None, gradient_color: str | None) -> None:
        self.id = id
        self.gradient_color = gradient_color

    @staticmethod
    def from_dict(obj: Any) -> Logo:
        assert isinstance(obj, dict)
        id = from_union([from_none, lambda x: UUID(x)], obj.get("id"))
        gradient_color = from_union([from_str, from_none], obj.get("gradient_color"))
        return Logo(id, gradient_color)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_none, lambda x: str(x)], self.id)
        if self.gradient_color is not None:
            result["gradient_color"] = from_union(
                [from_str, from_none], self.gradient_color
            )
        return result
