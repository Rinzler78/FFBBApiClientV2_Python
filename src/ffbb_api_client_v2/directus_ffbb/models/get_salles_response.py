from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ...models.cartographie import Cartographie
from ...utils.converter_utils import from_datetime, from_int, from_obj, from_str


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
    commune: int | None = None
    cartographie: Cartographie | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None

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
            commune=from_int(data, "commune"),
            cartographie=from_obj(Cartographie.from_dict, data, "cartographie"),
            date_created=from_datetime(data, "date_created"),
            date_updated=from_datetime(data, "date_updated"),
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
