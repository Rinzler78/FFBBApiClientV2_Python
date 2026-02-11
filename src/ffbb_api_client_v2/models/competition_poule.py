from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..utils.converter_utils import from_list, from_str
from .competition_rencontre import CompetitionRencontre
from .phase_engagement import PhaseEngagement


@dataclass
class CompetitionPoule:
    id: str | None = None
    nom: str | None = None
    rencontres: list[CompetitionRencontre] = field(default_factory=list)
    engagements: list[PhaseEngagement] = field(default_factory=list)

    @staticmethod
    def from_dict(obj: Any) -> CompetitionPoule:
        assert isinstance(obj, dict)
        rencontres_raw = from_list(CompetitionRencontre.from_dict, obj, "rencontres")
        engagements_raw = from_list(PhaseEngagement.from_dict, obj, "engagements")
        return CompetitionPoule(
            id=from_str(obj, "id"),
            nom=from_str(obj, "nom"),
            rencontres=rencontres_raw if rencontres_raw is not None else [],
            engagements=engagements_raw if engagements_raw is not None else [],
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.nom is not None:
            result["nom"] = self.nom
        if self.rencontres:
            result["rencontres"] = [r.to_dict() for r in self.rencontres]
        if self.engagements:
            result["engagements"] = [e.to_dict() for e in self.engagements]
        return result
