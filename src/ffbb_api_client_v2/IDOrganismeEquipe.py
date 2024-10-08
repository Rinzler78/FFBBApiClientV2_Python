from typing import Any, Optional

from .converters import from_none, from_str, from_union, to_class
from .IDOrganismeEquipe1Logo import IDOrganismeEquipe1Logo


class IDOrganismeEquipe:
    id: Optional[str] = None
    nom: Optional[str] = None
    nom_simple: None
    code: Optional[str] = None
    nom_club_pro: Optional[str] = None
    logo: Optional[IDOrganismeEquipe1Logo] = None

    def __init__(
        self,
        id: Optional[str],
        nom: Optional[str],
        nom_simple: None,
        code: Optional[str],
        nom_club_pro: Optional[str],
        logo: Optional[IDOrganismeEquipe1Logo],
    ) -> None:
        self.id = id
        self.nom = nom
        self.nom_simple = nom_simple
        self.code = code
        self.nom_club_pro = nom_club_pro
        self.logo = logo

    @staticmethod
    def from_dict(obj: Any) -> "IDOrganismeEquipe":
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        nom = from_union([from_str, from_none], obj.get("nom"))
        nom_simple = from_union([from_str, from_none], obj.get("nom_simple"))
        code = from_union([from_str, from_none], obj.get("code"))
        nom_club_pro = from_union([from_str, from_none], obj.get("nomClubPro"))
        logo = from_union(
            [IDOrganismeEquipe1Logo.from_dict, from_none], obj.get("logo")
        )
        return IDOrganismeEquipe(id, nom, nom_simple, code, nom_club_pro, logo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.nom_simple is not None:
            result["nom_simple"] = from_none(self.nom_simple)
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.nom_club_pro is not None:
            result["nomClubPro"] = from_union([from_str, from_none], self.nom_club_pro)
        if self.logo is not None:
            result["logo"] = from_union(
                [lambda x: to_class(IDOrganismeEquipe1Logo, x), from_none], self.logo
            )
        return result
