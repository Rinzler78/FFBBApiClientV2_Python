from typing import Any, Optional

from .converters import from_int, from_none, from_union


class CompetitionIDTypeCompetition:
    championnat: Optional[int] = None
    coupe: Optional[int] = None

    def __init__(self, championnat: Optional[int], coupe: Optional[int]) -> None:
        self.championnat = championnat
        self.coupe = coupe

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionIDTypeCompetition":
        assert isinstance(obj, dict)
        championnat = from_union([from_int, from_none], obj.get("Championnat"))
        coupe = from_union([from_int, from_none], obj.get("Coupe"))
        return CompetitionIDTypeCompetition(championnat, coupe)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.championnat is not None:
            result["Championnat"] = from_union([from_int, from_none], self.championnat)
        if self.coupe is not None:
            result["Coupe"] = from_union([from_int, from_none], self.coupe)
        return result
