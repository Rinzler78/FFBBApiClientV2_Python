from typing import Any, Optional

from ..utils.converter_utils import from_int, from_none, from_union


class CompetitionIDSexe:
    feminine: Optional[int] = None
    masculine: Optional[int] = None
    mixed: Optional[int] = None

    def __init__(
        self, feminine: Optional[int], masculine: Optional[int], mixed: Optional[int]
    ) -> None:
        self.feminine = feminine
        self.masculine = masculine
        self.mixed = mixed

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionIDSexe":
        assert isinstance(obj, dict)
        feminine = from_union([from_int, from_none], obj.get("Féminin"))
        masculine = from_union([from_int, from_none], obj.get("Masculin"))
        mixed = from_union([from_int, from_none], obj.get("Mixte"))
        return CompetitionIDSexe(feminine, masculine, mixed)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.feminine is not None:
            result["Féminin"] = from_union([from_int, from_none], self.feminine)
        if self.masculine is not None:
            result["Masculin"] = from_union([from_int, from_none], self.masculine)
        if self.mixed is not None:
            result["Mixte"] = from_union([from_int, from_none], self.mixed)
        return result
