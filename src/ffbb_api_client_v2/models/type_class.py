from typing import Any, Optional

from .converters import from_int, from_none, from_union


class TypeClass:
    groupement: Optional[int] = None

    def __init__(self, groupement: Optional[int] = None):
        self.groupement = groupement

    @staticmethod
    def from_dict(obj: Any) -> "TypeClass":
        assert isinstance(obj, dict)
        groupement = from_union([from_int, from_none], obj.get("Groupement"))
        return TypeClass(groupement)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.groupement is not None:
            result["Groupement"] = from_union([from_int, from_none], self.groupement)
        return result
