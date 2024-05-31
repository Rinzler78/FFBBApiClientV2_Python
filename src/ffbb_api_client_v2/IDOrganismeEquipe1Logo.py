from typing import Any, Optional
from uuid import UUID

from .converters import from_none, from_str, from_union


class IDOrganismeEquipe1Logo:
    id: Optional[UUID] = None
    gradient_color: Optional[str] = None

    def __init__(self, id: Optional[UUID], gradient_color: Optional[str]) -> None:
        self.id = id
        self.gradient_color = gradient_color

    @staticmethod
    def from_dict(obj: Any) -> "IDOrganismeEquipe1Logo":
        assert isinstance(obj, dict)
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        gradient_color = from_union([from_str, from_none], obj.get("gradient_color"))
        return IDOrganismeEquipe1Logo(id, gradient_color)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([lambda x: str(x), from_none], self.id)
        if self.gradient_color is not None:
            result["gradient_color"] = from_union(
                [from_str, from_none], self.gradient_color
            )
        return result
