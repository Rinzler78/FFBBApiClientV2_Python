from dataclasses import dataclass
from typing import Any, Optional

from ffbb_api_client_v2.converters import from_int, from_none, from_union


@dataclass
class TypeAssociationLibelle:
    club: Optional[int] = None
    coopération_territoriale_club: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "TypeAssociationLibelle":
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
