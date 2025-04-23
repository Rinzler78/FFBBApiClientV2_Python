from typing import Any, Optional

from .converters import from_int, from_none, from_union


class CompetitionIDSexe:
    féminin: Optional[int] = None
    masculin: Optional[int] = None
    mixte: Optional[int] = None

    def __init__(
        self, féminin: Optional[int], masculin: Optional[int], mixte: Optional[int]
    ) -> None:
        self.féminin = féminin
        self.masculin = masculin
        self.mixte = mixte

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionIDSexe":
        assert isinstance(obj, dict)
        féminin = from_union([from_int, from_none], obj.get("Féminin"))
        masculin = from_union([from_int, from_none], obj.get("Masculin"))
        mixte = from_union([from_int, from_none], obj.get("Mixte"))
        return CompetitionIDSexe(féminin, masculin, mixte)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.féminin is not None:
            result["Féminin"] = from_union([from_int, from_none], self.féminin)
        if self.masculin is not None:
            result["Masculin"] = from_union([from_int, from_none], self.masculin)
        if self.mixte is not None:
            result["Mixte"] = from_union([from_int, from_none], self.mixte)
        return result
