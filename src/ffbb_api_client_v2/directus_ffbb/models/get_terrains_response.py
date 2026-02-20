from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ...models.cartographie import Cartographie
from ...models.nature_sol import NatureSol
from ...utils.converter_utils import (
    from_bool,
    from_datetime,
    from_float,
    from_int,
    from_obj,
    from_str,
)


@dataclass
class GetTerrainsResponse:
    id: str
    nom: str | None = None
    rue: str | None = None
    numero: int | None = None
    largeur: float | None = None
    longueur: float | None = None
    accesLibre: bool | None = None
    natureSol: NatureSol | None = None
    commune: int | None = None
    cartographie: Cartographie | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetTerrainsResponse | None:
        """Convert dictionary to GetTerrainsResponse instance."""
        if not data:
            return None
        if not isinstance(data, dict):
            return None
        if "errors" in data:
            return None

        return cls(
            id=from_str(data, "id") or "",
            nom=from_str(data, "nom"),
            rue=from_str(data, "rue"),
            numero=from_int(data, "numero"),
            largeur=from_float(data, "largeur"),
            longueur=from_float(data, "longueur"),
            accesLibre=from_bool(data, "accesLibre"),
            natureSol=from_obj(NatureSol.from_dict, data, "natureSol"),
            commune=from_int(data, "commune"),
            cartographie=from_obj(Cartographie.from_dict, data, "cartographie"),
            date_created=from_datetime(data, "date_created"),
            date_updated=from_datetime(data, "date_updated"),
        )

    @classmethod
    def from_list(cls, data_list: list[dict[str, Any]]) -> list[GetTerrainsResponse]:
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
