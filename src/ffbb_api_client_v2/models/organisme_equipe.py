from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ..utils.converter_utils import from_str, from_uuid


@dataclass
class OrganismeEquipe:
    id: str | None = None
    nom: str | None = None
    nom_simple: str | None = None
    code: str | None = None
    nom_club_pro: str | None = None
    logo: UUID | None = None

    @staticmethod
    def from_dict(obj: Any) -> OrganismeEquipe:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        return OrganismeEquipe(
            id=from_str(obj, "id"),
            nom=from_str(obj, "nom"),
            nom_simple=from_str(obj, "nom_simple"),
            code=from_str(obj, "code"),
            nom_club_pro=from_str(obj, "nomClubPro"),
            logo=from_uuid(obj, "logo"),
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
            result["logo"] = str(self.logo)
        return result
