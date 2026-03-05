from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ..utils.converter_utils import (
    from_str,
    from_uuid,
)


@dataclass
class Folder:
    id: UUID | None = None
    name: str | None = None
    parent: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> Folder:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        id = from_uuid(obj, "id")
        name = from_str(obj, "name")
        parent = from_str(obj, "parent")
        return Folder(id=id, name=name, parent=parent)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = str(self.id)
        if self.name is not None:
            result["name"] = self.name
        if self.parent is not None:
            result["parent"] = self.parent
        return result
