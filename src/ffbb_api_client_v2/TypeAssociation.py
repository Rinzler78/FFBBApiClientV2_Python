from dataclasses import dataclass
from typing import Any, Optional

from ffbb_api_client_v2.converters import from_none, from_str, from_union


@dataclass
class TypeAssociation:
    libelle: Optional[str] = None

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
