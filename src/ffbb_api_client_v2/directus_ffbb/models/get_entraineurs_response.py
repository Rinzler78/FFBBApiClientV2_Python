from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...utils.converter_utils import from_str


@dataclass
class GetEntraineursResponse:
    idLicence: str
    nom: str | None = None
    prenom: str | None = None
    adresse1: str | None = None
    adresse2: str | None = None
    commune: dict[str, Any] | None = None
    email: str | None = None
    telephoneDomicile: str | None = None
    telephonePortable: str | None = None
    telephoneTravail: str | None = None
    date_created: str | None = None
    date_updated: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetEntraineursResponse | None:
        """Convert dictionary to GetEntraineursResponse instance."""
        if not data:
            return None
        if not isinstance(data, dict):
            return None
        if "errors" in data:
            return None

        return cls(
            idLicence=from_str(data, "idLicence") or "",
            nom=from_str(data, "nom"),
            prenom=from_str(data, "prenom"),
            adresse1=from_str(data, "adresse1"),
            adresse2=from_str(data, "adresse2"),
            commune=data.get("commune"),
            email=from_str(data, "email"),
            telephoneDomicile=from_str(data, "telephoneDomicile"),
            telephonePortable=from_str(data, "telephonePortable"),
            telephoneTravail=from_str(data, "telephoneTravail"),
            date_created=from_str(data, "date_created"),
            date_updated=from_str(data, "date_updated"),
        )

    @classmethod
    def from_list(cls, data_list: list[dict[str, Any]]) -> list[GetEntraineursResponse]:
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
