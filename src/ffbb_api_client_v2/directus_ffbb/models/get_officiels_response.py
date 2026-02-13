from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...utils.converter_utils import from_str


@dataclass
class GetOfficielsResponse:
    nom: str
    prenom: str | None = None
    numeroNational: str | None = None
    date_created: str | None = None
    date_updated: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetOfficielsResponse | None:
        """Convert dictionary to GetOfficielsResponse instance."""
        if not data:
            return None
        if not isinstance(data, dict):
            return None
        if "errors" in data:
            return None

        return cls(
            nom=from_str(data, "nom") or "",
            prenom=from_str(data, "prenom"),
            numeroNational=from_str(data, "numeroNational"),
            date_created=from_str(data, "date_created"),
            date_updated=from_str(data, "date_updated"),
        )

    @classmethod
    def from_list(cls, data_list: list[dict[str, Any]]) -> list[GetOfficielsResponse]:
        """Convert list of dictionaries to list of GetOfficielsResponse instances."""
        if not data_list:
            return []
        return [
            result
            for item in data_list
            if item
            for result in [cls.from_dict(item)]
            if result is not None
        ]
