from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_obj, from_str
from .logo import Logo


@dataclass
class IDOrganismeEquipe:
    id: str | None = None
    nom: str | None = None
    nom_simple: str | None = None
    code: str | None = None
    nom_club_pro: str | None = None
    logo: Logo | None = None

    @staticmethod
    def from_dict(obj: Any) -> IDOrganismeEquipe:
        assert isinstance(obj, dict)
        id = from_str(obj, "id")
        nom = from_str(obj, "nom")
        nom_simple = from_str(obj, "nom_simple")
        code = from_str(obj, "code")
        nom_club_pro = from_str(obj, "nomClubPro")
        logo = from_obj(Logo.from_dict, obj, "logo")
        return IDOrganismeEquipe(
            id=id,
            nom=nom,
            nom_simple=nom_simple,
            code=code,
            nom_club_pro=nom_club_pro,
            logo=logo,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.nom is not None:
            result["nom"] = self.nom
        if self.nom_simple is not None:
            result["nom_simple"] = self.nom_simple
        if self.code is not None:
            result["code"] = self.code
        if self.nom_club_pro is not None:
            result["nomClubPro"] = self.nom_club_pro
        if self.logo is not None:
            result["logo"] = self.logo.to_dict()
        return result
