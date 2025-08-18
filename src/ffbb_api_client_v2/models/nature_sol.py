from __future__ import annotations

from datetime import datetime
from typing import Any

from ..utils.converter_utils import (
    from_datetime,
    from_none,
    from_str,
    from_stringified_bool,
    from_union,
    is_type,
    to_enum,
)
from .Code import Code

# from .multi_search_result_tournois import Libelle


class NatureSol:
    code: Code | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    id: str | None = None
    libelle: str | None = None
    terrain: bool | None = None

    @staticmethod
    def from_dict(obj: Any) -> NatureSol:
        assert isinstance(obj, dict)
        code = from_union([Code, from_none], obj.get("code"))
        date_created = from_union([from_datetime, from_none], obj.get("date_created"))
        date_updated = from_union([from_datetime, from_none], obj.get("date_updated"))
        id = from_union([from_str, from_none], obj.get("id"))
        libelle = from_union([from_str, from_none], obj.get("libelle"))
        terrain = from_union(
            [from_none, lambda x: from_stringified_bool(from_str(x))],
            obj.get("terrain"),
        )
        return NatureSol(code, date_created, date_updated, id, libelle, terrain)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = from_union(
                [lambda x: to_enum(Code, x), from_none], self.code
            )
        if self.date_created is not None:
            result["date_created"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_created
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_updated
            )
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.libelle is not None:
            result["libelle"] = from_union([from_str, from_none], self.libelle)
        if self.terrain is not None:
            result["terrain"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x)
                    ),
                ],
                self.terrain,
            )
        return result
