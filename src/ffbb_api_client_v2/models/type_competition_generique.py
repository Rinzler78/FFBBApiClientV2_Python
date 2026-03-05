from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ..utils.converter_utils import from_str, from_uuid


@dataclass
class TypeCompetitionGenerique:
    type_competition_generique_id: str | None = None
    logo: UUID | None = None

    @staticmethod
    def from_dict(obj: Any) -> TypeCompetitionGenerique:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        return TypeCompetitionGenerique(
            type_competition_generique_id=from_str(obj, "id"),
            logo=from_uuid(obj, "logo"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type_competition_generique_id is not None:
            result["id"] = self.type_competition_generique_id
        if self.logo is not None:
            result["logo"] = str(self.logo)
        return result
