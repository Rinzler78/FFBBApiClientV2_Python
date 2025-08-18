from __future__ import annotations

from datetime import datetime
from typing import Any

from ..utils.converter_utils import (
    from_datetime,
    from_none,
    from_str,
    from_union,
    is_type,
)


class Commune:
    code_insee: None
    code_postal: int | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    commune_id: int | None = None
    libelle: str | None = None
    departement: str | None = None

    def __init__(
        self,
        code_insee: None,
        code_postal: int | None,
        date_created: datetime | None,
        date_updated: datetime | None,
        id: int | None,
        libelle: str | None,
        departement: str | None,
    ):
        self.code_insee = code_insee
        self.code_postal = code_postal
        self.date_created = date_created
        self.date_updated = date_updated
        self.commune_id = id
        self.libelle = libelle
        self.lower_libelle = libelle.lower() if libelle else None

        self.departement = departement
        self.lower_departement = departement.lower() if departement else None

    @staticmethod
    def from_dict(obj: Any) -> Commune:
        assert isinstance(obj, dict)
        code_insee = from_none(obj.get("codeInsee"))
        code_postal = from_union(
            [lambda x: int(from_str(x)), from_none], obj.get("codePostal")
        )
        date_created = from_union([from_datetime, from_none], obj.get("date_created"))
        date_updated = from_union([from_datetime, from_none], obj.get("date_updated"))
        commune_id = from_union([lambda x: int(from_str(x)), from_none], obj.get("id"))
        libelle = from_union([from_str, from_none], obj.get("libelle"))
        departement = from_union([from_str, from_none], obj.get("departement"))
        return Commune(
            code_insee,
            code_postal,
            date_created,
            date_updated,
            commune_id,
            libelle,
            departement,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code_insee is not None:
            result["codeInsee"] = from_none(self.code_insee)
        if self.code_postal is not None:
            result["codePostal"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.code_postal,
            )
        if self.date_created is not None:
            result["date_created"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_created
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_updated
            )
        if self.commune_id is not None:
            result["id"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.commune_id,
            )
        if self.libelle is not None:
            result["libelle"] = from_union([from_str, from_none], self.libelle)
        if self.departement is not None:
            result["departement"] = from_union([from_str, from_none], self.departement)
        return result
