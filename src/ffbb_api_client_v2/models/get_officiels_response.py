from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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
            nom=str(data.get("nom", "")),
            prenom=(str(data.get("prenom", "")) if data.get("prenom") else None),
            numeroNational=(
                str(data.get("numeroNational", ""))
                if data.get("numeroNational")
                else None
            ),
            date_created=(
                str(data.get("date_created", "")) if data.get("date_created") else None
            ),
            date_updated=(
                str(data.get("date_updated", "")) if data.get("date_updated") else None
            ),
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
