from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_int, from_obj, from_str
from .competition_base import CompetitionBase
from .niveau_models import NiveauInfo, get_niveau_from_idcompetition
from .organisateur import Organisateur
from .saison import Saison


@dataclass
class CompetitionDetail(CompetitionBase):
    """Competition detail as nested in organisme engagements."""

    competition_origine: str | None = None
    competition_origine_niveau: int | None = None
    saison: Saison | None = None
    id_competition_pere: str | None = None
    organisateur: Organisateur | None = None

    @property
    def niveau(self) -> NiveauInfo | None:
        """Extract level from competition name."""
        return get_niveau_from_idcompetition(self)

    @staticmethod
    def from_dict(obj: Any) -> CompetitionDetail:
        assert isinstance(obj, dict)
        base = CompetitionBase._parse_base(obj)
        return CompetitionDetail(
            **base,
            competition_origine=from_str(obj, "competition_origine"),
            competition_origine_niveau=from_int(obj, "competition_origine_niveau"),
            saison=from_obj(Saison.from_dict, obj, "saison"),
            id_competition_pere=from_str(obj, "idCompetitionPere"),
            organisateur=from_obj(Organisateur.from_dict, obj, "organisateur"),
        )

    def to_dict(self) -> dict:
        result = self._base_to_dict()
        if self.competition_origine is not None:
            result["competition_origine"] = self.competition_origine
        if self.competition_origine_niveau is not None:
            result["competition_origine_niveau"] = self.competition_origine_niveau
        if self.saison is not None:
            result["saison"] = self.saison.to_dict()
        if self.id_competition_pere is not None:
            result["idCompetitionPere"] = self.id_competition_pere
        if self.organisateur is not None:
            result["organisateur"] = self.organisateur.to_dict()
        return result
