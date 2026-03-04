from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_str


@dataclass
class OrganismeEngagement:
    id: str | None = None
    id_poule: str | None = None
    id_competition: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> OrganismeEngagement:
        assert isinstance(obj, dict)
        return OrganismeEngagement(
            id=from_str(obj, "id"),
            id_poule=from_str(obj, "idPoule"),
            id_competition=from_str(obj, "idCompetition"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.id_poule is not None:
            result["idPoule"] = self.id_poule
        if self.id_competition is not None:
            result["idCompetition"] = self.id_competition
        return result
