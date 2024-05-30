from dataclasses import dataclass
from typing import Any, Optional

from ffbb_api_client_v2.converters import from_none, from_union, to_class
from ffbb_api_client_v2.PurpleLogo import PurpleLogo


@dataclass
class CompetitionOrigineTypeCompetitionGenerique:
    logo: Optional[PurpleLogo] = None

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionOrigineTypeCompetitionGenerique":
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
