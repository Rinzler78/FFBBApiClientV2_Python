from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_obj, from_str
from .logo import Logo


@dataclass
class EngagementEquipe:
    """Team engagement in a competition rencontre."""

    nom: str | None = None
    id: str | None = None
    nom_officiel: str | None = None
    nom_usuel: str | None = None
    code_abrege: str | None = None
    logo: Logo | None = None

    @staticmethod
    def from_dict(obj: Any) -> EngagementEquipe:
        assert isinstance(obj, dict)
        return EngagementEquipe(
            nom=from_str(obj, "nom"),
            id=from_str(obj, "id"),
            nom_officiel=from_str(obj, "nomOfficiel"),
            nom_usuel=from_str(obj, "nomUsuel"),
            code_abrege=from_str(obj, "codeAbrege"),
            logo=from_obj(Logo.from_dict, obj, "logo"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom is not None:
            result["nom"] = self.nom
        if self.id is not None:
            result["id"] = self.id
        if self.nom_officiel is not None:
            result["nomOfficiel"] = self.nom_officiel
        if self.nom_usuel is not None:
            result["nomUsuel"] = self.nom_usuel
        if self.code_abrege is not None:
            result["codeAbrege"] = self.code_abrege
        if self.logo is not None:
            result["logo"] = self.logo.to_dict()
        return result
