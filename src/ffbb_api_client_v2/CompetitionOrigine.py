from typing import Any, Optional

from .CompetitionOrigineCategorie import CompetitionOrigineCategorie
from .CompetitionOrigineTypeCompetition import CompetitionOrigineTypeCompetition
from .CompetitionOrigineTypeCompetitionGenerique import (
    CompetitionOrigineTypeCompetitionGenerique,
)
from .converters import from_none, from_str, from_union, to_class, to_enum


class CompetitionOrigine:
    id: Optional[str] = None
    code: Optional[str] = None
    nom: Optional[str] = None
    type_competition: Optional[CompetitionOrigineTypeCompetition] = None
    categorie: Optional[CompetitionOrigineCategorie] = None
    type_competition_generique: Optional[CompetitionOrigineTypeCompetitionGenerique] = (
        None
    )

    def __init__(
        self,
        id: Optional[str],
        code: Optional[str],
        nom: Optional[str],
        type_competition: Optional[CompetitionOrigineTypeCompetition],
        categorie: Optional[CompetitionOrigineCategorie],
        type_competition_generique: Optional[
            CompetitionOrigineTypeCompetitionGenerique
        ],
    ) -> None:
        self.id = id
        self.code = code
        self.nom = nom
        self.type_competition = type_competition
        self.categorie = categorie
        self.type_competition_generique = type_competition_generique

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionOrigine":
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        code = from_union([from_str, from_none], obj.get("code"))
        nom = from_union([from_str, from_none], obj.get("nom"))
        type_competition = from_union(
            [CompetitionOrigineTypeCompetition.parse, from_none],
            obj.get("typeCompetition"),
        )
        categorie = from_union(
            [CompetitionOrigineCategorie.from_dict, from_none], obj.get("categorie")
        )
        type_competition_generique = from_union(
            [CompetitionOrigineTypeCompetitionGenerique.from_dict, from_none],
            obj.get("typeCompetitionGenerique"),
        )
        return CompetitionOrigine(
            id, code, nom, type_competition, categorie, type_competition_generique
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.type_competition is not None:
            result["typeCompetition"] = from_union(
                [lambda x: to_enum(CompetitionOrigineTypeCompetition, x), from_none],
                self.type_competition,
            )
        if self.categorie is not None:
            result["categorie"] = from_union(
                [lambda x: to_class(CompetitionOrigineCategorie, x), from_none],
                self.categorie,
            )
        if self.type_competition_generique is not None:
            result["typeCompetitionGenerique"] = from_union(
                [
                    lambda x: to_class(CompetitionOrigineTypeCompetitionGenerique, x),
                    from_none,
                ],
                self.type_competition_generique,
            )
        return result
