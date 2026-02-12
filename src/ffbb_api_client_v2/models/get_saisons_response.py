from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_bool, from_str


@dataclass
class GetSaisonsResponse:
    id: str
    actif: bool | None = None
    debut: str | None = None
    fin: str | None = None
    code: str | None = None
    libelle: str | None = None
    enCours: bool | None = None
    date_created: str | None = None
    date_updated: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetSaisonsResponse | None:
        """Convert dictionary to GetSaisonsResponse instance."""
        if not data:
            return None

        # Handle case where data is not a dictionary
        if not isinstance(data, dict):
            return None

        # Handle API error responses
        if "errors" in data:
            return None

        return cls(
            id=from_str(data, "id") or "",
            actif=from_bool(data, "actif"),
            debut=from_str(data, "debut"),
            fin=from_str(data, "fin"),
            code=from_str(data, "code"),
            libelle=from_str(data, "libelle"),
            enCours=from_bool(data, "enCours"),
            date_created=from_str(data, "date_created"),
            date_updated=from_str(data, "date_updated"),
        )

    @classmethod
    def from_list(cls, data_list: list[dict[str, Any]]) -> list[GetSaisonsResponse]:
        """Convert list of dictionaries to list of SaisonsModel instances."""
        if not data_list:
            return []

        # Filter out None results from from_dict (invalid items)
        return [
            result
            for item in data_list
            if item
            for result in [cls.from_dict(item)]
            if result is not None
        ]
