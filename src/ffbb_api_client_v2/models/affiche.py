from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ..utils.converter_utils import (
    from_int,
    from_str,
    from_uuid,
)


@dataclass
class Affiche:
    affiche_id: UUID | None = None
    gradient_color: str | None = None
    width: int | None = None
    height: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> Affiche:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        affiche_id = from_uuid(obj, "id")
        gradient_color = from_str(obj, "gradient_color")
        width = from_int(obj, "width")
        height = from_int(obj, "height")
        return Affiche(
            affiche_id=affiche_id,
            gradient_color=gradient_color,
            width=width,
            height=height,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.affiche_id is not None:
            result["id"] = str(self.affiche_id)
        if self.gradient_color is not None:
            result["gradient_color"] = self.gradient_color
        if self.width is not None:
            result["width"] = self.width
        if self.height is not None:
            result["height"] = self.height
        return result
