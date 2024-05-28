from dataclasses import dataclass
from typing import Any, Optional

from .competition_type import CompetitionType, extract_competition_type
from .converters import from_none, from_str, from_union
from .sex import Sex


@dataclass
class Competition:
    code: Optional[str] = None
    nom: Optional[str] = None
    sexe: Optional[Sex] = None
    type_competition: Optional[CompetitionType] = None

    @staticmethod
    def from_dict(obj: Any) -> "Competition":
        """
        Convert a dictionary object to a Competition object.

        Args:
            obj (Any): The dictionary object to convert.

        Returns:
            Competition: The converted Competition object.
        """
        assert isinstance(obj, dict)
        code = from_union([from_str, from_none], obj.get("code"))
        nom = from_union([from_str, from_none], obj.get("nom"))
        sexe = from_union([from_str, from_none], obj.get("sexe"))
        type_competition = from_union(
            [extract_competition_type, from_none], obj.get("typeCompetition")
        )
        return Competition(code, nom, sexe, type_competition)

    def to_dict(self) -> dict:
        """
        Convert the Competition object to a dictionary.

        Returns:
            dict: The converted dictionary object.
        """
        result: dict = {}
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.sexe is not None:
            result["sexe"] = from_union([from_str, from_none], self.sexe)
        if self.type_competition is not None:
            result["typeCompetition"] = (
                self.type_competition.value
                if self.type_competition is not None
                else None
            )
        return result
