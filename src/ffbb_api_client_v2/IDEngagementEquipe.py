from dataclasses import dataclass
from typing import Any, Optional

from ffbb_api_client_v2.converters import from_none, from_str, from_union


@dataclass
class IDEngagementEquipe:
    id: Optional[str] = None
    nom_usuel: Optional[str] = None
    logo: None

    @staticmethod
    def from_dict(obj: Any) -> "IDEngagementEquipe":
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        nom_usuel = from_union([from_none, from_str], obj.get("nomUsuel"))
        logo = from_none(obj.get("logo"))
        return IDEngagementEquipe(id, nom_usuel, logo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.nom_usuel is not None:
            result["nomUsuel"] = from_union([from_none, from_str], self.nom_usuel)
        if self.logo is not None:
            result["logo"] = from_none(self.logo)
        return result
