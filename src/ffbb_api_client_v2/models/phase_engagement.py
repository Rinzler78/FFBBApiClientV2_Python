from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_str


@dataclass
class PhaseEngagement:
    """Engagement within a competition phase poule."""

    id: str | None = None
    id_organisme: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> PhaseEngagement:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        return PhaseEngagement(
            id=from_str(obj, "id"),
            id_organisme=from_str(obj, "idOrganisme"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.id_organisme is not None:
            result["idOrganisme"] = self.id_organisme
        return result
