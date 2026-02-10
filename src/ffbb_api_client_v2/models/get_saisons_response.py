from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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
            id=str(data.get("id", "")),
            actif=bool(data.get("actif", False)) if "actif" in data else None,
            debut=str(data.get("debut", "")) if data.get("debut") else None,
            fin=str(data.get("fin", "")) if data.get("fin") else None,
            code=str(data.get("code", "")) if data.get("code") else None,
            libelle=str(data.get("libelle", "")) if data.get("libelle") else None,
            enCours=bool(data.get("enCours", False)) if "enCours" in data else None,
            date_created=(
                str(data.get("date_created", "")) if data.get("date_created") else None
            ),
            date_updated=(
                str(data.get("date_updated", "")) if data.get("date_updated") else None
            ),
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
