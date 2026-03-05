from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_obj, from_str
from .logo import Logo


@dataclass
class TypeCompetitionGenerique:
    type_competition_generique_id: str | None = None
    logo: Logo | None = None

    @staticmethod
    def from_dict(obj: Any) -> TypeCompetitionGenerique:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        type_competition_generique_id = from_str(obj, "id")
        logo = from_obj(Logo.from_dict, obj, "logo")
        return TypeCompetitionGenerique(
            type_competition_generique_id=type_competition_generique_id,
            logo=logo,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type_competition_generique_id is not None:
            result["id"] = self.type_competition_generique_id
        if self.logo is not None:
            result["logo"] = self.logo.to_dict()
        return result
