from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_int


@dataclass
class SexeFacet:
    feminine: int | None = None
    masculine: int | None = None
    mixed: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> SexeFacet:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        feminine = from_int(obj, "Féminin")
        masculine = from_int(obj, "Masculin")
        mixed = from_int(obj, "Mixte")
        return SexeFacet(feminine=feminine, masculine=masculine, mixed=mixed)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.feminine is not None:
            result["Féminin"] = self.feminine
        if self.masculine is not None:
            result["Masculin"] = self.masculine
        if self.mixed is not None:
            result["Mixte"] = self.mixed
        return result
