from dataclasses import dataclass
from typing import Any, Optional

from ffbb_api_client_v2.converters import from_int, from_none, from_union, to_enum
from ffbb_api_client_v2.multi_search_result_competitions import LibelleEnum


@dataclass
class CompetitionIDCategorie:
    code: Optional[LibelleEnum] = None
    libelle: Optional[LibelleEnum] = None
    ordre: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionIDCategorie":
        assert isinstance(obj, dict)
        code = from_union([LibelleEnum, from_none], obj.get("code"))
        libelle = from_union([LibelleEnum, from_none], obj.get("libelle"))
        ordre = from_union([from_int, from_none], obj.get("ordre"))
        return CompetitionIDCategorie(code, libelle, ordre)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = from_union(
                [lambda x: to_enum(LibelleEnum, x), from_none], self.code
            )
        if self.libelle is not None:
            result["libelle"] = from_union(
                [lambda x: to_enum(LibelleEnum, x), from_none], self.libelle
            )
        if self.ordre is not None:
            result["ordre"] = from_union([from_int, from_none], self.ordre)
        return result
