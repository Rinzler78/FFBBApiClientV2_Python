from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_str


@dataclass
class TypeAssociation:
    libelle: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> TypeAssociation:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        libelle = from_str(obj, "libelle")
        return TypeAssociation(libelle=libelle)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.libelle is not None:
            result["libelle"] = self.libelle
        return result
