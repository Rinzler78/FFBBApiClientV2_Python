from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_int


@dataclass
class CompetitionTypeFacet:
    championnat: int | None = None
    coupe: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> CompetitionTypeFacet:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        championnat = from_int(obj, "Championnat")
        coupe = from_int(obj, "Coupe")
        return CompetitionTypeFacet(championnat=championnat, coupe=coupe)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.championnat is not None:
            result["Championnat"] = self.championnat
        if self.coupe is not None:
            result["Coupe"] = self.coupe
        return result
