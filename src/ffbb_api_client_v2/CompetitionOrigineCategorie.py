from dataclasses import dataclass
from typing import Any, Optional

from ffbb_api_client_v2.converters import from_int, from_none, from_union


@dataclass
class CompetitionOrigineCategorie:
    ordre: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionOrigineCategorie":
        assert isinstance(obj, dict)
        ordre = from_union([from_int, from_none], obj.get("ordre"))
        return CompetitionOrigineCategorie(ordre)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.ordre is not None:
            result["ordre"] = from_union([from_int, from_none], self.ordre)
        return result
