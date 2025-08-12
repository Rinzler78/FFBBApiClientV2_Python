from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_none, from_str, from_union, to_class
from .logo import Logo


class TypeCompetitionGenerique:
    type_competition_generique_id: str | None = None
    logo: Logo | None = None

    def __init__(self, id: str | None, logo: Logo | None) -> None:
        self.type_competition_generique_id = id
        self.logo = logo

    @staticmethod
    def from_dict(obj: Any) -> TypeCompetitionGenerique:
        assert isinstance(obj, dict)
        type_competition_generique_id = from_union([from_str, from_none], obj.get("id"))
        logo = from_union([Logo.from_dict, from_none], obj.get("logo"))
        return TypeCompetitionGenerique(type_competition_generique_id, logo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type_competition_generique_id is not None:
            result["id"] = from_union(
                [from_str, from_none], self.type_competition_generique_id
            )
        if self.logo is not None:
            result["logo"] = from_union(
                [lambda x: to_class(Logo, x), from_none], self.logo
            )
        return result
