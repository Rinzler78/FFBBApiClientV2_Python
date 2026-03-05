from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_int


@dataclass
class NiveauClass:
    départemental: int | None = None
    régional: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> NiveauClass:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        départemental = from_int(obj, "Départemental")
        régional = from_int(obj, "Régional")
        return NiveauClass(départemental=départemental, régional=régional)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.départemental is not None:
            result["Départemental"] = self.départemental
        if self.régional is not None:
            result["Régional"] = self.régional
        return result
