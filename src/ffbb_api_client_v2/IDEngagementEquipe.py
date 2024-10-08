from typing import Any, Optional

from .converters import from_none, from_str, from_union
from .logo import Logo


class IDEngagementEquipe:
    id: Optional[str] = None
    nom_usuel: Optional[str] = None
    logo: Logo

    def __init__(self, id: Optional[str], nom_usuel: Optional[str], logo: Logo) -> None:
        self.id = id
        self.nom_usuel = nom_usuel
        self.logo = logo

    @staticmethod
    def from_dict(obj: Any) -> "IDEngagementEquipe":
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        nom_usuel = from_union([from_none, from_str], obj.get("nomUsuel"))
        logo = from_union([from_none, Logo.from_dict], obj.get("logo"))
        return IDEngagementEquipe(id, nom_usuel, logo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.nom_usuel is not None:
            result["nomUsuel"] = from_union([from_none, from_str], self.nom_usuel)
        if self.logo is not None:
            result["logo"] = from_union([from_none, Logo.from_dict], self.logo)
        return result
