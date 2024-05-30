from dataclasses import dataclass
from typing import Any, Optional
from uuid import UUID

from ffbb_api_client_v2.converters import from_none, from_str, from_union


@dataclass
class Logo:
    id: Optional[UUID] = None
    gradient_color: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Logo":
        assert isinstance(obj, dict)
        id = from_union([from_none, lambda x: UUID(x)], obj.get("id"))
        gradient_color = from_union([from_str, from_none], obj.get("gradient_color"))
        return Logo(id, gradient_color)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_none, lambda x: str(x)], self.id)
        if self.gradient_color is not None:
            result["gradient_color"] = from_union(
                [from_str, from_none], self.gradient_color
            )
        return result
