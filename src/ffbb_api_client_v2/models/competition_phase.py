from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..utils.converter_utils import from_bool, from_str
from .competition_poule import CompetitionPoule


@dataclass
class CompetitionPhase:
    id: str | None = None
    nom: str | None = None
    live_stat: bool | None = None
    phase_code: str | None = None
    poules: list[CompetitionPoule] = field(default_factory=list)

    @staticmethod
    def from_dict(obj: Any) -> CompetitionPhase:
        assert isinstance(obj, dict)
        raw_poules = obj.get("poules")
        poules: list[CompetitionPoule] = []
        if isinstance(raw_poules, list):
            for item in raw_poules:
                if isinstance(item, dict):
                    poules.append(CompetitionPoule.from_dict(item))
                elif item is not None:
                    poules.append(CompetitionPoule(id=str(item)))
        return CompetitionPhase(
            id=from_str(obj, "id"),
            nom=from_str(obj, "nom"),
            live_stat=from_bool(obj, "liveStat"),
            phase_code=from_str(obj, "phase_code"),
            poules=poules,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.nom is not None:
            result["nom"] = self.nom
        if self.live_stat is not None:
            result["liveStat"] = self.live_stat
        if self.phase_code is not None:
            result["phase_code"] = self.phase_code
        if self.poules:
            result["poules"] = [p.to_dict() for p in self.poules]
        return result
