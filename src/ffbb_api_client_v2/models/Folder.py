from __future__ import annotations

from typing import Any
from uuid import UUID

from ..utils.converter_utils import from_none, from_str, from_union


class Folder:
    id: UUID | None = None
    name: str | None = None
    parent: None

    @staticmethod
    def from_dict(obj: Any) -> Folder:
        assert isinstance(obj, dict)
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        name = from_union([from_str, from_none], obj.get("name"))
        parent = from_none(obj.get("parent"))
        return Folder(id, name, parent)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([lambda x: str(x), from_none], self.id)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.parent is not None:
            result["parent"] = from_none(self.parent)
        return result
