from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ..utils.converter_utils import (
    from_datetime,
    from_str,
)


@dataclass
class Commune:
    code_insee: str | None = None
    code_postal: str | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    commune_id: str | None = None
    libelle: str | None = None
    departement: str | None = None
    lower_libelle: str | None = field(init=False, default=None, repr=False)
    lower_departement: str | None = field(init=False, default=None, repr=False)

    def __post_init__(self) -> None:
        self.lower_libelle = self.libelle.lower() if self.libelle else None
        self.lower_departement = self.departement.lower() if self.departement else None

    @staticmethod
    def from_dict(obj: Any) -> Commune:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        code_insee = from_str(obj, "codeInsee")
        code_postal = from_str(obj, "codePostal")
        date_created = from_datetime(obj, "date_created")
        date_updated = from_datetime(obj, "date_updated")
        commune_id = from_str(obj, "id")
        libelle = from_str(obj, "libelle")
        departement = from_str(obj, "departement")
        return Commune(
            code_insee=code_insee,
            code_postal=code_postal,
            date_created=date_created,
            date_updated=date_updated,
            commune_id=commune_id,
            libelle=libelle,
            departement=departement,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code_insee is not None:
            result["codeInsee"] = self.code_insee
        if self.code_postal is not None:
            result["codePostal"] = self.code_postal
        if self.date_created is not None:
            result["date_created"] = self.date_created.isoformat()
        if self.date_updated is not None:
            result["date_updated"] = self.date_updated.isoformat()
        if self.commune_id is not None:
            result["id"] = self.commune_id
        if self.libelle is not None:
            result["libelle"] = self.libelle
        if self.departement is not None:
            result["departement"] = self.departement
        return result
