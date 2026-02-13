from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...utils.converter_utils import from_bool, from_float, from_str


@dataclass
class GetTerrainsResponse:
    id: str
    nom: str | None = None
    rue: str | None = None
    numero: str | None = None
    largeur: float | None = None
    longueur: float | None = None
    accesLibre: bool | None = None
    natureSol: dict[str, Any] | None = None
    commune: dict[str, Any] | None = None
    cartographie: dict[str, Any] | None = None
    date_created: str | None = None
    date_updated: str | None = None

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
            numero=from_str(data, "numero"),
            largeur=from_float(data, "largeur"),
            longueur=from_float(data, "longueur"),
            accesLibre=from_bool(data, "accesLibre"),
            natureSol=data.get("natureSol"),
            commune=data.get("commune"),
            cartographie=data.get("cartographie"),
            date_created=from_str(data, "date_created"),
            date_updated=from_str(data, "date_updated"),
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
