from __future__ import annotations

from typing import Any
from uuid import UUID

from ..utils.converter_utils import from_int, from_none, from_str, from_union


class Affiche:
    affiche_id: UUID | None = None
    gradient_color: str | None = None
    width: int | None = None
    height: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> Affiche:
        assert isinstance(obj, dict)
        affiche_id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        gradient_color = from_union([from_none, from_str], obj.get("gradient_color"))
        width = from_union([from_int, from_none], obj.get("width"))
        height = from_union([from_int, from_none], obj.get("height"))
        return Affiche(affiche_id, gradient_color, width, height)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.affiche_id is not None:
            result["id"] = from_union([lambda x: str(x), from_none], self.affiche_id)
        if self.gradient_color is not None:
            result["gradient_color"] = from_union(
                [from_none, from_str], self.gradient_color
            )
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        return result
