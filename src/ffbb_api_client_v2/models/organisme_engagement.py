from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_obj, from_str
from .competition_ref import CompetitionRef
from .id_poule import IDPoule


@dataclass
class OrganismeEngagement:
    id: str | None = None
    id_poule: IDPoule | None = None
    id_competition: CompetitionRef | None = None

    @staticmethod
    def from_dict(obj: Any) -> OrganismeEngagement:
        assert isinstance(obj, dict)
        return OrganismeEngagement(
            id=from_str(obj, "id"),
            id_poule=from_obj(IDPoule.from_dict, obj, "idPoule"),
            id_competition=from_obj(CompetitionRef.from_dict, obj, "idCompetition"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.id_poule is not None:
            result["idPoule"] = self.id_poule.to_dict()
        if self.id_competition is not None:
            result["idCompetition"] = self.id_competition.to_dict()
        return result
