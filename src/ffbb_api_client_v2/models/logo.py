from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ..utils.converter_utils import from_str, from_uuid


@dataclass
class Logo:
    id: UUID | None = None
    gradient_color: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> Logo:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        id = from_uuid(obj, "id")
        gradient_color = from_str(obj, "gradient_color")
        return Logo(id=id, gradient_color=gradient_color)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = str(self.id)
        if self.gradient_color is not None:
            result["gradient_color"] = self.gradient_color
        return result
