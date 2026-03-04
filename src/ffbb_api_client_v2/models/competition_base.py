from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_enum, from_obj, from_str
from .categorie import Categorie
from .logo import Logo
from .type_competition_enum import TypeCompetitionEnum
from .type_competition_generique import TypeCompetitionGenerique


@dataclass
class CompetitionBase:
    """Shared fields between Competition and CompetitionDetail."""

    id: str | None = None
    nom: str | None = None
    code: str | None = None
    sexe: str | None = None
    competition_origine_nom: str | None = None
    type_competition: TypeCompetitionEnum | None = None
    logo: Logo | None = None
    categorie: Categorie | None = None
    type_competition_generique: TypeCompetitionGenerique | None = None

    @staticmethod
    def _parse_base(obj: dict[str, Any]) -> dict[str, Any]:
        """Parse the shared fields from a dict."""
        return {
            "id": from_str(obj, "id"),
            "nom": from_str(obj, "nom"),
            "code": from_str(obj, "code"),
            "sexe": from_str(obj, "sexe"),
            "competition_origine_nom": from_str(obj, "competition_origine_nom"),
            "type_competition": from_enum(TypeCompetitionEnum, obj, "typeCompetition"),
            "logo": from_obj(Logo.from_dict, obj, "logo"),
            "categorie": from_obj(Categorie.from_dict, obj, "categorie"),
            "type_competition_generique": from_obj(
                TypeCompetitionGenerique.from_dict,
                obj,
                "typeCompetitionGenerique",
            ),
        }

    def _base_to_dict(self) -> dict:
        """Serialize the shared fields to a dict."""
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.nom is not None:
            result["nom"] = self.nom
        if self.code is not None:
            result["code"] = self.code
        if self.sexe is not None:
            result["sexe"] = self.sexe
        if self.competition_origine_nom is not None:
            result["competition_origine_nom"] = self.competition_origine_nom
        if self.type_competition is not None:
            result["typeCompetition"] = self.type_competition.value
        if self.logo is not None:
            result["logo"] = self.logo.to_dict()
        if self.categorie is not None:
            result["categorie"] = self.categorie.to_dict()
        if self.type_competition_generique is not None:
            result["typeCompetitionGenerique"] = (
                self.type_competition_generique.to_dict()
            )
        return result
