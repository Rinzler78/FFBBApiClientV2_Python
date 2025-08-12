from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_none, from_str, from_union


class IDPoule:
    id: str | None = None
    nom: str | None = None

    def __init__(self, id: str | None, nom: str | None = None) -> None:
        self.id = id
        self.nom = nom

    @staticmethod
    def from_dict(obj: Any) -> IDPoule:
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        nom = from_union([from_str, from_none], obj.get("nom"))
        return IDPoule(id, nom)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        return result
