from typing import Any, Optional

from .converters import from_int, from_none, from_union


class NiveauClass:
    départemental: Optional[int] = None
    régional: Optional[int] = None

    def __init__(self, départemental: Optional[int], régional: Optional[int]) -> None:
        self.départemental = départemental
        self.régional = régional

    @staticmethod
    def from_dict(obj: Any) -> "NiveauClass":
        assert isinstance(obj, dict)
        départemental = from_union([from_int, from_none], obj.get("Départemental"))
        régional = from_union([from_int, from_none], obj.get("Régional"))
        return NiveauClass(départemental, régional)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.départemental is not None:
            result["Départemental"] = from_union(
                [from_int, from_none], self.départemental
            )
        if self.régional is not None:
            result["Régional"] = from_union([from_int, from_none], self.régional)
        return result
