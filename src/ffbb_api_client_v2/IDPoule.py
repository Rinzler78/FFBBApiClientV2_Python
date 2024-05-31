from typing import Any, Optional

from .converters import from_none, from_str, from_union


class IDPoule:
    id: Optional[str] = None
    nom: Optional[str] = None

    def __init__(self, id: Optional[str], nom: Optional[str] = None) -> None:
        self.id = id
        self.nom = nom

    @staticmethod
    def from_dict(obj: Any) -> "IDPoule":
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
