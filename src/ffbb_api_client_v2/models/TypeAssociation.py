from typing import Any, Optional

from .converters import from_none, from_str, from_union


class TypeAssociation:
    libelle: Optional[str] = None

    def __init__(self, libelle: Optional[str] = None):
        self.libelle = libelle

    @staticmethod
    def from_dict(obj: Any) -> "TypeAssociation":
        assert isinstance(obj, dict)
        libelle = from_union([from_str, from_none], obj.get("libelle"))
        return TypeAssociation(libelle)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.libelle is not None:
            result["libelle"] = from_union([from_str, from_none], self.libelle)
        return result
