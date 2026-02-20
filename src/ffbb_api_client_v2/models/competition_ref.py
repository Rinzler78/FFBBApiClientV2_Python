from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_enum, from_int, from_obj, from_str
from .categorie import Categorie
from .logo import Logo
from .niveau_models import NiveauInfo, get_niveau_from_idcompetition
from .organisateur import Organisateur
from .saison import Saison
from .type_competition import TypeCompetition
from .type_competition_generique import TypeCompetitionGenerique


@dataclass
class CompetitionRef:
    """Reference to a competition, as nested in organisme engagements."""

    id: str | None = None
    nom: str | None = None
    code: str | None = None
    sexe: str | None = None
    competition_origine: str | None = None
    competition_origine_nom: str | None = None
    competition_origine_niveau: int | None = None
    type_competition: TypeCompetition | None = None
    logo: Logo | None = None
    saison: Saison | None = None
    id_competition_pere: str | None = None
    organisateur: Organisateur | None = None
    type_competition_generique: TypeCompetitionGenerique | None = None
    categorie: Categorie | None = None

    @property
    def niveau(self) -> NiveauInfo | None:
        """Extract level from competition name."""
        return get_niveau_from_idcompetition(self)

    @staticmethod
    def from_dict(obj: Any) -> CompetitionRef:
        assert isinstance(obj, dict)
        return CompetitionRef(
            id=from_str(obj, "id"),
            nom=from_str(obj, "nom"),
            code=from_str(obj, "code"),
            sexe=from_str(obj, "sexe"),
            competition_origine=from_str(obj, "competition_origine"),
            competition_origine_nom=from_str(obj, "competition_origine_nom"),
            competition_origine_niveau=from_int(obj, "competition_origine_niveau"),
            type_competition=from_enum(TypeCompetition, obj, "typeCompetition"),
            logo=from_obj(Logo.from_dict, obj, "logo"),
            saison=from_obj(Saison.from_dict, obj, "saison"),
            id_competition_pere=from_str(obj, "idCompetitionPere"),
            organisateur=from_obj(Organisateur.from_dict, obj, "organisateur"),
            type_competition_generique=from_obj(
                TypeCompetitionGenerique.from_dict, obj, "typeCompetitionGenerique"
            ),
            categorie=from_obj(Categorie.from_dict, obj, "categorie"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.nom is not None:
            result["nom"] = self.nom
        if self.code is not None:
            result["code"] = self.code
        if self.sexe is not None:
            result["sexe"] = self.sexe
        if self.competition_origine is not None:
            result["competition_origine"] = self.competition_origine
        if self.competition_origine_nom is not None:
            result["competition_origine_nom"] = self.competition_origine_nom
        if self.competition_origine_niveau is not None:
            result["competition_origine_niveau"] = self.competition_origine_niveau
        if self.type_competition is not None:
            result["typeCompetition"] = self.type_competition.value
        if self.logo is not None:
            result["logo"] = self.logo.to_dict()
        if self.saison is not None:
            result["saison"] = self.saison.to_dict()
        if self.id_competition_pere is not None:
            result["idCompetitionPere"] = self.id_competition_pere
        if self.organisateur is not None:
            result["organisateur"] = self.organisateur.to_dict()
        if self.type_competition_generique is not None:
            result["typeCompetitionGenerique"] = (
                self.type_competition_generique.to_dict()
            )
        if self.categorie is not None:
            result["categorie"] = self.categorie.to_dict()
        return result
