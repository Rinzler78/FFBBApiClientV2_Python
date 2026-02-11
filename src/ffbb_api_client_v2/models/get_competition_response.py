from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..utils.converter_utils import from_bool, from_list, from_obj, from_str
from .categorie import Categorie
from .competition_phase import CompetitionPhase
from .id_poule import IDPoule
from .type_competition_generique import TypeCompetitionGenerique


@dataclass
class GetCompetitionResponse:
    id: str | None = None
    nom: str | None = None
    sexe: str | None = None
    saison: str | None = None
    code: str | None = None
    type_competition: str | None = None
    live_stat: bool | None = None
    competition_origine: str | None = None
    competition_origine_nom: str | None = None
    publication_internet: str | None = None
    categorie: Categorie | None = None
    type_competition_generique: TypeCompetitionGenerique | None = None
    logo: Any | None = None
    poules: list[IDPoule] = field(default_factory=list)
    phases: list[CompetitionPhase] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetCompetitionResponse | None:
        """Convert dictionary to GetCompetitionResponse instance."""
        if not data:
            return None
        if not isinstance(data, dict):
            return None
        if "errors" in data:
            return None

        poules_raw = from_list(IDPoule.from_dict, data, "poules")
        phases_raw = from_list(CompetitionPhase.from_dict, data, "phases")

        return cls(
            id=from_str(data, "id"),
            nom=from_str(data, "nom"),
            sexe=from_str(data, "sexe"),
            saison=from_str(data, "saison"),
            code=from_str(data, "code"),
            type_competition=from_str(data, "typeCompetition"),
            live_stat=from_bool(data, "liveStat"),
            competition_origine=from_str(data, "competition_origine"),
            competition_origine_nom=from_str(data, "competition_origine_nom"),
            publication_internet=from_str(data, "publicationInternet"),
            categorie=from_obj(Categorie.from_dict, data, "categorie"),
            type_competition_generique=from_obj(
                TypeCompetitionGenerique.from_dict, data, "typeCompetitionGenerique"
            ),
            logo=data.get("logo"),
            poules=poules_raw if poules_raw is not None else [],
            phases=phases_raw if phases_raw is not None else [],
        )
