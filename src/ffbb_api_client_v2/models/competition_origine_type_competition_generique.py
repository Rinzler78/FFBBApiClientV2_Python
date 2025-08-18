from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_none, from_union, to_class
from .PurpleLogo import PurpleLogo


class CompetitionOrigineTypeCompetitionGenerique:
    logo: PurpleLogo | None = None

    def __init__(self, logo: PurpleLogo | None) -> None:
        self.logo = logo

    @staticmethod
    def from_dict(obj: Any) -> CompetitionOrigineTypeCompetitionGenerique:
        assert isinstance(obj, dict)
        logo = from_union([PurpleLogo.from_dict, from_none], obj.get("logo"))
        return CompetitionOrigineTypeCompetitionGenerique(logo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.logo is not None:
            result["logo"] = from_union(
                [lambda x: to_class(PurpleLogo, x), from_none], self.logo
            )
        return result
