from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_int, from_none, from_union


class CompetitionOrigineCategorie:
    ordre: int | None = None

    def __init__(self, ordre: int | None = None) -> None:
        self.ordre = ordre

    @staticmethod
    def from_dict(obj: Any) -> CompetitionOrigineCategorie:
        assert isinstance(obj, dict)
        ordre = from_union([from_int, from_none], obj.get("ordre"))
        return CompetitionOrigineCategorie(ordre)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.ordre is not None:
            result["ordre"] = from_union([from_int, from_none], self.ordre)
        return result
