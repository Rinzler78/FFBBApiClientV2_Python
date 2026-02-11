from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_obj, from_str
from .organisme_id import OrganismeId


@dataclass
class PhaseEngagement:
    """Engagement within a competition phase poule."""

    id: str | None = None
    id_organisme: OrganismeId | None = None

    @staticmethod
    def from_dict(obj: Any) -> PhaseEngagement:
        assert isinstance(obj, dict)
        return PhaseEngagement(
            id=from_str(obj, "id"),
            id_organisme=from_obj(OrganismeId.from_dict, obj, "idOrganisme"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.id_organisme is not None:
            result["idOrganisme"] = self.id_organisme.to_dict()
        return result
