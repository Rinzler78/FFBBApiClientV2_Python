from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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
            idLicence=str(data.get("idLicence", "")),
            nom=str(data.get("nom", "")) if data.get("nom") else None,
            prenom=str(data.get("prenom", "")) if data.get("prenom") else None,
            adresse1=(str(data.get("adresse1", "")) if data.get("adresse1") else None),
            adresse2=data.get("adresse2"),
            commune=data.get("commune"),
            email=str(data.get("email", "")) if data.get("email") else None,
            telephoneDomicile=data.get("telephoneDomicile"),
            telephonePortable=(
                str(data.get("telephonePortable", ""))
                if data.get("telephonePortable")
                else None
            ),
            telephoneTravail=data.get("telephoneTravail"),
            date_created=(
                str(data.get("date_created", "")) if data.get("date_created") else None
            ),
            date_updated=(
                str(data.get("date_updated", "")) if data.get("date_updated") else None
            ),
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
