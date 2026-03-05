from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_str


@dataclass
class Fonction:
    libelle: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> Fonction:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        return Fonction(libelle=from_str(obj, "libelle"))

    def to_dict(self) -> dict:
        result: dict = {}
        if self.libelle is not None:
            result["libelle"] = self.libelle
        return result
