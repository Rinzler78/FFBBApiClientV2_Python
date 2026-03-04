from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_int


@dataclass
class NiveauFacet:
    départemental: int | None = None
    régional: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> NiveauFacet:
        assert isinstance(obj, dict)
        départemental = from_int(obj, "Départemental")
        régional = from_int(obj, "Régional")
        return NiveauFacet(départemental=départemental, régional=régional)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.départemental is not None:
            result["Départemental"] = self.départemental
        if self.régional is not None:
            result["Régional"] = self.régional
        return result
