from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ...utils.converter_utils import from_datetime, from_int, from_str


@dataclass
class GetOfficielsResponse:
    nom: str
    prenom: str | None = None
    numeroNational: int | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None

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
            numeroNational=from_int(data, "numeroNational"),
            date_created=from_datetime(data, "date_created"),
            date_updated=from_datetime(data, "date_updated"),
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
