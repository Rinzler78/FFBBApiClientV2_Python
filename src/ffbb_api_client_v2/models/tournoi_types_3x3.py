from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ..utils.converter_utils import from_enum, from_int, from_uuid
from .tournoi_types_3x3_libelle_enum import TournoiTypes3x3LibelleEnum
from .type_league_enum import TypeLeagueEnum


@dataclass
class TournoiTypes3X3:
    libelle: TournoiTypes3x3LibelleEnum | None = None
    logo: UUID | None = None
    type_league: TypeLeagueEnum | None = None
    type_tournois: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> TournoiTypes3X3:
        assert isinstance(obj, dict)
        libelle = from_enum(TournoiTypes3x3LibelleEnum, obj, "libelle")
        logo = from_uuid(obj, "logo")
        type_league = from_enum(TypeLeagueEnum, obj, "type_league")
        type_tournois = from_int(obj, "type_tournois")
        return TournoiTypes3X3(
            libelle=libelle,
            logo=logo,
            type_league=type_league,
            type_tournois=type_tournois,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.libelle is not None:
            result["libelle"] = self.libelle.value
        if self.logo is not None:
            result["logo"] = str(self.logo)
        if self.type_league is not None:
            result["type_league"] = self.type_league.value
        if self.type_tournois is not None:
            result["type_tournois"] = str(self.type_tournois)
        return result
