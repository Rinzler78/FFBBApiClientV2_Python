from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import (
    from_obj,
    from_str,
)
from .competition_origine_categorie import CompetitionOrigineCategorie
from .competition_origine_type_competition_enum import (
    CompetitionOrigineTypeCompetitionEnum,
)
from .type_competition_generique import (
    TypeCompetitionGenerique,
)


@dataclass
class CompetitionOrigine:
    id: str | None = None
    code: str | None = None
    nom: str | None = None
    type_competition: CompetitionOrigineTypeCompetitionEnum | None = None
    categorie: CompetitionOrigineCategorie | None = None
    type_competition_generique: TypeCompetitionGenerique | None = None

    @staticmethod
    def from_dict(obj: Any) -> CompetitionOrigine:
        assert isinstance(obj, dict)
        id = from_str(obj, "id")
        code = from_str(obj, "code")
        nom = from_str(obj, "nom")
        tc_val = obj.get("typeCompetition")
        type_competition = (
            CompetitionOrigineTypeCompetitionEnum.parse(tc_val)
            if tc_val is not None
            else None
        )
        categorie = from_obj(CompetitionOrigineCategorie.from_dict, obj, "categorie")
        type_competition_generique = from_obj(
            TypeCompetitionGenerique.from_dict,
            obj,
            "typeCompetitionGenerique",
        )
        return CompetitionOrigine(
            id=id,
            code=code,
            nom=nom,
            type_competition=type_competition,
            categorie=categorie,
            type_competition_generique=type_competition_generique,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.code is not None:
            result["code"] = self.code
        if self.nom is not None:
            result["nom"] = self.nom
        if self.type_competition is not None:
            result["typeCompetition"] = self.type_competition.value
        if self.categorie is not None:
            result["categorie"] = self.categorie.to_dict()
        if self.type_competition_generique is not None:
            result["typeCompetitionGenerique"] = (
                self.type_competition_generique.to_dict()
            )
        return result
