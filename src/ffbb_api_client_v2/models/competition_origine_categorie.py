from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_int


@dataclass
class CompetitionOrigineCategorie:
    ordre: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> CompetitionOrigineCategorie:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        ordre = from_int(obj, "ordre")
        return CompetitionOrigineCategorie(ordre=ordre)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.ordre is not None:
            result["ordre"] = self.ordre
        return result
