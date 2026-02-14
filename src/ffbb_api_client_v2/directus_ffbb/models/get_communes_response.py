from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ...utils.converter_utils import from_datetime, from_str


@dataclass
class GetCommunesResponse:
    id: str
    codeInsee: str | None = None
    codePostal: str | None = None
    departement: str | None = None
    libelle: str | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetCommunesResponse | None:
        """Convert dictionary to GetCommunesResponse instance."""
        if not data:
            return None
        if not isinstance(data, dict):
            return None
        if "errors" in data:
            return None

        return cls(
            id=from_str(data, "id") or "",
            codeInsee=from_str(data, "codeInsee"),
            codePostal=from_str(data, "codePostal"),
            departement=from_str(data, "departement"),
            libelle=from_str(data, "libelle"),
            date_created=from_datetime(data, "date_created"),
            date_updated=from_datetime(data, "date_updated"),
        )

    @classmethod
    def from_list(cls, data_list: list[dict[str, Any]]) -> list[GetCommunesResponse]:
        """Convert list of dictionaries to list of GetCommunesResponse instances."""
        if not data_list:
            return []
        return [
            result
            for item in data_list
            if item
            for result in [cls.from_dict(item)]
            if result is not None
        ]
