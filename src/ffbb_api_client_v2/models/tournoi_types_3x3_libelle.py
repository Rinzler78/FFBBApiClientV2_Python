from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_int


@dataclass
class TournoiTypes3X3Libelle:
    open_plus_junior_league_3_x3: int | None = None
    open_plus_super_league_3_x3: int | None = None
    open_plus_access_junior_league_3_x3: int | None = None
    open_plus_access_super_league_3_x3: int | None = None
    open_start_junior_league_3_x3: int | None = None
    open_start_super_league_3_x3: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> TournoiTypes3X3Libelle:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        open_plus_junior_league_3_x3 = from_int(obj, "Open Plus - Junior league 3x3")
        open_plus_super_league_3_x3 = from_int(obj, "Open Plus - Super league 3x3")
        open_plus_access_junior_league_3_x3 = from_int(
            obj, "Open Plus Access - Junior league 3x3"
        )
        open_plus_access_super_league_3_x3 = from_int(
            obj, "Open Plus Access - Super league 3x3"
        )
        open_start_junior_league_3_x3 = from_int(obj, "Open Start - Junior league 3x3")
        open_start_super_league_3_x3 = from_int(obj, "Open Start - Super league 3x3")
        return TournoiTypes3X3Libelle(
            open_plus_junior_league_3_x3=open_plus_junior_league_3_x3,
            open_plus_super_league_3_x3=open_plus_super_league_3_x3,
            open_plus_access_junior_league_3_x3=open_plus_access_junior_league_3_x3,
            open_plus_access_super_league_3_x3=open_plus_access_super_league_3_x3,
            open_start_junior_league_3_x3=open_start_junior_league_3_x3,
            open_start_super_league_3_x3=open_start_super_league_3_x3,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.open_plus_junior_league_3_x3 is not None:
            result["Open Plus - Junior league 3x3"] = self.open_plus_junior_league_3_x3
        if self.open_plus_super_league_3_x3 is not None:
            result["Open Plus - Super league 3x3"] = self.open_plus_super_league_3_x3
        if self.open_plus_access_junior_league_3_x3 is not None:
            result["Open Plus Access - Junior league 3x3"] = (
                self.open_plus_access_junior_league_3_x3
            )
        if self.open_plus_access_super_league_3_x3 is not None:
            result["Open Plus Access - Super league 3x3"] = (
                self.open_plus_access_super_league_3_x3
            )
        if self.open_start_junior_league_3_x3 is not None:
            result["Open Start - Junior league 3x3"] = (
                self.open_start_junior_league_3_x3
            )
        if self.open_start_super_league_3_x3 is not None:
            result["Open Start - Super league 3x3"] = self.open_start_super_league_3_x3
        return result
