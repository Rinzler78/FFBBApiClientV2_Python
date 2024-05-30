from dataclasses import dataclass
from typing import Any, Optional
from uuid import UUID

from ffbb_api_client_v2.converters import from_none, from_union, to_enum
from ffbb_api_client_v2.multi_search_result_terrains import Name


@dataclass
class Folder:
    id: Optional[UUID] = None
    name: Optional[Name] = None
    parent: None

    @staticmethod
    def from_dict(obj: Any) -> "Folder":
        assert isinstance(obj, dict)
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        name = from_union([Name, from_none], obj.get("name"))
        parent = from_none(obj.get("parent"))
        return Folder(id, name, parent)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([lambda x: str(x), from_none], self.id)
        if self.name is not None:
            result["name"] = from_union(
                [lambda x: to_enum(Name, x), from_none], self.name
            )
        if self.parent is not None:
            result["parent"] = from_none(self.parent)
        return result
