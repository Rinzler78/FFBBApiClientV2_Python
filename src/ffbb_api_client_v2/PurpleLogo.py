from typing import Any, Optional
from uuid import UUID

from .converters import from_none, from_union


class PurpleLogo:
    id: Optional[UUID] = None

    @staticmethod
    def from_dict(obj: Any) -> "PurpleLogo":
        assert isinstance(obj, dict)
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        return PurpleLogo(id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([lambda x: str(x), from_none], self.id)
        return result
