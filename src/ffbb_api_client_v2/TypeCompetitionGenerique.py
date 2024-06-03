from typing import Any, Optional

from .converters import from_none, from_str, from_union, to_class
from .logo import Logo


class TypeCompetitionGenerique:
    id: Optional[str] = None
    logo: Optional[Logo] = None

    def __init__(self, id: Optional[str], logo: Optional[Logo]) -> None:
        self.id = id
        self.logo = logo

    @staticmethod
    def from_dict(obj: Any) -> "TypeCompetitionGenerique":
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        logo = from_union([Logo.from_dict, from_none], obj.get("logo"))
        return TypeCompetitionGenerique(id, logo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.logo is not None:
            result["logo"] = from_union(
                [lambda x: to_class(Logo, x), from_none], self.logo
            )
        return result
