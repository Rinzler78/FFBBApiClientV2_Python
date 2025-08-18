from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_int, from_none, from_union


class TypeAssociationLibelle:
    club: int | None = None
    coopération_territoriale_club: int | None = None

    def __init__(
        self, club: int | None, coopération_territoriale_club: int | None
    ) -> None:
        self.club = club
        self.coopération_territoriale_club = coopération_territoriale_club

    @staticmethod
    def from_dict(obj: Any) -> TypeAssociationLibelle:
        assert isinstance(obj, dict)
        club = from_union([from_int, from_none], obj.get("Club"))
        coopération_territoriale_club = from_union(
            [from_int, from_none], obj.get("Coopération Territoriale Club")
        )
        return TypeAssociationLibelle(club, coopération_territoriale_club)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.club is not None:
            result["Club"] = from_union([from_int, from_none], self.club)
        if self.coopération_territoriale_club is not None:
            result["Coopération Territoriale Club"] = from_union(
                [from_int, from_none], self.coopération_territoriale_club
            )
        return result
