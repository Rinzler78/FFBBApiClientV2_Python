from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_int


@dataclass
class TypeClass:
    groupement: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> TypeClass:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        groupement = from_int(obj, "Groupement")
        return TypeClass(groupement=groupement)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.groupement is not None:
            result["Groupement"] = self.groupement
        return result
