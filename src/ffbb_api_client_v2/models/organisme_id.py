from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_str


@dataclass
class OrganismeId:
    """Simple organisme ID reference."""

    id: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> OrganismeId:
        assert isinstance(obj, dict)
        return OrganismeId(id=from_str(obj, "id"))

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        return result
