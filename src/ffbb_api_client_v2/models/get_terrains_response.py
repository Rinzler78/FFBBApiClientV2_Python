from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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
            id=str(data.get("id", "")),
            nom=str(data.get("nom", "")) if data.get("nom") else None,
            rue=str(data.get("rue", "")) if data.get("rue") else None,
            numero=(str(data.get("numero", "")) if data.get("numero") else None),
            largeur=data.get("largeur"),
            longueur=data.get("longueur"),
            accesLibre=data.get("accesLibre"),
            natureSol=data.get("natureSol"),
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
