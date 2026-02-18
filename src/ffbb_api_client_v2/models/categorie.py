from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ..utils.converter_utils import (
    from_categorie_code,
    from_datetime,
    from_int,
    from_str,
)
from .categorie_code import CategorieCode


@dataclass
class Categorie:
    code: CategorieCode | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    categorie_id: str | None = None
    libelle: str | None = None
    ordre: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> Categorie:
        assert isinstance(obj, dict)
        code = from_categorie_code(obj, "code")
        date_created = from_datetime(obj, "date_created")
        date_updated = from_datetime(obj, "date_updated")
        categorie_id = from_str(obj, "id")
        libelle = from_str(obj, "libelle")
        ordre = from_int(obj, "ordre")
        return Categorie(
            code=code,
            date_created=date_created,
            date_updated=date_updated,
            categorie_id=categorie_id,
            libelle=libelle,
            ordre=ordre,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = self.code
        if self.date_created is not None:
            result["date_created"] = self.date_created.isoformat()
        if self.date_updated is not None:
            result["date_updated"] = self.date_updated.isoformat()
        if self.categorie_id is not None:
            result["id"] = self.categorie_id
        if self.libelle is not None:
            result["libelle"] = self.libelle
        if self.ordre is not None:
            result["ordre"] = self.ordre
        return result
