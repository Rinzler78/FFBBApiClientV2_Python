from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_none, from_str, from_union


class TypeAssociation:
    libelle: str | None = None

    def __init__(self, libelle: str | None = None):
        self.libelle = libelle

    @staticmethod
    def from_dict(obj: Any) -> TypeAssociation:
        assert isinstance(obj, dict)
        libelle = from_union([from_str, from_none], obj.get("libelle"))
        return TypeAssociation(libelle)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.libelle is not None:
            result["libelle"] = from_union([from_str, from_none], self.libelle)
        return result
