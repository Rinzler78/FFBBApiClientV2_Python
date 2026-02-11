from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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
            id=str(data.get("id", "")),
            libelle=(str(data.get("libelle", "")) if data.get("libelle") else None),
            libelle2=(str(data.get("libelle2", "")) if data.get("libelle2") else None),
            adresse=(str(data.get("adresse", "")) if data.get("adresse") else None),
            adresseComplement=data.get("adresseComplement"),
            numero=(str(data.get("numero", "")) if data.get("numero") else None),
            telephone=data.get("telephone"),
            mail=data.get("mail"),
            capaciteSpectateur=data.get("capaciteSpectateur"),
            commune=data.get("commune"),
            cartographie=data.get("cartographie"),
            date_created=(
                str(data.get("date_created", "")) if data.get("date_created") else None
            ),
            date_updated=(
                str(data.get("date_updated", "")) if data.get("date_updated") else None
            ),
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
