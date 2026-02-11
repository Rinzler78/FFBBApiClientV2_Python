from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_str


@dataclass
class Fonction:
    libelle: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> Fonction:
        assert isinstance(obj, dict)
        return Fonction(libelle=from_str(obj, "libelle"))

    def to_dict(self) -> dict:
        result: dict = {}
        if self.libelle is not None:
            result["libelle"] = self.libelle
        return result
