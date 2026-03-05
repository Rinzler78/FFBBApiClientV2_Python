from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_int


@dataclass
class TypeAssociationLibelle:
    club: int | None = None
    coopération_territoriale_club: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> TypeAssociationLibelle:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        club = from_int(obj, "Club")
        coopération_territoriale_club = from_int(obj, "Coopération Territoriale Club")
        return TypeAssociationLibelle(
            club=club,
            coopération_territoriale_club=coopération_territoriale_club,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.club is not None:
            result["Club"] = self.club
        if self.coopération_territoriale_club is not None:
            result["Coopération Territoriale Club"] = self.coopération_territoriale_club
        return result
