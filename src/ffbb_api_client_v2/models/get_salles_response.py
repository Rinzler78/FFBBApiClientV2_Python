from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_int, from_str


@dataclass
class GetSallesResponse:
    id: str
    libelle: str | None = None
    libelle2: str | None = None
    adresse: str | None = None
    adresseComplement: str | None = None
    numero: str | None = None
    telephone: str | None = None
    mail: str | None = None
    capaciteSpectateur: int | None = None
    commune: dict[str, Any] | None = None
    cartographie: dict[str, Any] | None = None
    date_created: str | None = None
    date_updated: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetSallesResponse | None:
        """Convert dictionary to GetSallesResponse instance."""
        if not data:
            return None
        if not isinstance(data, dict):
            return None
        if "errors" in data:
            return None

        return cls(
            id=from_str(data, "id") or "",
            libelle=from_str(data, "libelle"),
            libelle2=from_str(data, "libelle2"),
            adresse=from_str(data, "adresse"),
            adresseComplement=from_str(data, "adresseComplement"),
            numero=from_str(data, "numero"),
            telephone=from_str(data, "telephone"),
            mail=from_str(data, "mail"),
            capaciteSpectateur=from_int(data, "capaciteSpectateur"),
            commune=data.get("commune"),
            cartographie=data.get("cartographie"),
            date_created=from_str(data, "date_created"),
            date_updated=from_str(data, "date_updated"),
        )

    @classmethod
    def from_list(cls, data_list: list[dict[str, Any]]) -> list[GetSallesResponse]:
        """Convert list of dictionaries to list of instances."""
        if not data_list:
            return []
        return [
            result
            for item in data_list
            if item
            for result in [cls.from_dict(item)]
            if result is not None
        ]
