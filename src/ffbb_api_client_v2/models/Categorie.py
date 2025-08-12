from __future__ import annotations

from datetime import datetime
from typing import Any

from ..utils.converter_utils import (
    from_datetime,
    from_int,
    from_none,
    from_str,
    from_union,
)


class Categorie:
    code: str | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    categorie_id: str | None = None
    libelle: str | None = None
    ordre: int | None = None

    def __init__(
        self,
        code: str | None = None,
        date_created: datetime | None = None,
        date_updated: datetime | None = None,
        id: str | None = None,
        libelle: str | None = None,
        ordre: int | None = None,
    ) -> None:
        self.code = code
        self.date_created = date_created
        self.date_updated = date_updated
        self.categorie_id = id
        self.libelle = libelle
        self.ordre = ordre

    @staticmethod
    def from_dict(obj: Any) -> Categorie:
        assert isinstance(obj, dict)
        code = from_union([from_str, from_none], obj.get("code"))
        date_created = from_union([from_datetime, from_none], obj.get("date_created"))
        date_updated = from_union([from_datetime, from_none], obj.get("date_updated"))
        categorie_id = from_union([from_str, from_none], obj.get("id"))
        libelle = from_union([from_str, from_none], obj.get("libelle"))
        ordre = from_union([from_int, from_none], obj.get("ordre"))
        return Categorie(code, date_created, date_updated, categorie_id, libelle, ordre)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.date_created is not None:
            result["date_created"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_created
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_updated
            )
        if self.categorie_id is not None:
            result["id"] = from_union([from_str, from_none], self.categorie_id)
        if self.libelle is not None:
            result["libelle"] = from_union([from_str, from_none], self.libelle)
        if self.ordre is not None:
            result["ordre"] = from_union([from_int, from_none], self.ordre)
        return result
