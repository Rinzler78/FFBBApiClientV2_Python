from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class GetCommunesResponse:
    id: str
    codeInsee: str | None = None
    codePostal: str | None = None
    departement: str | None = None
    libelle: str | None = None
    date_created: str | None = None
    date_updated: str | None = None

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
            id=str(data.get("id", "")),
            codeInsee=(
                str(data.get("codeInsee", "")) if data.get("codeInsee") else None
            ),
            codePostal=(
                str(data.get("codePostal", "")) if data.get("codePostal") else None
            ),
            departement=(
                str(data.get("departement", "")) if data.get("departement") else None
            ),
            libelle=(str(data.get("libelle", "")) if data.get("libelle") else None),
            date_created=(
                str(data.get("date_created", "")) if data.get("date_created") else None
            ),
            date_updated=(
                str(data.get("date_updated", "")) if data.get("date_updated") else None
            ),
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
