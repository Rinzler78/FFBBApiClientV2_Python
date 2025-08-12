from __future__ import annotations

from typing import Any

from ..utils.converter_utils import (
    from_float,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
    to_float,
)
from .Coordonnees import Coordonnees


class Cartographie:
    adresse: str | None = None
    code_postal: int | None = None
    coordonnees: Coordonnees | None = None
    date_created: None
    date_updated: None
    cartographie_id: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    title: str | None = None
    ville: str | None = None
    status: str | None = None

    def __init__(
        self,
        adresse: str | None,
        code_postal: int | None,
        coordonnees: Coordonnees | None,
        date_created: None,
        date_updated: None,
        id: str | None,
        latitude: float | None,
        longitude: float | None,
        title: str | None,
        ville: str | None,
        status: str | None,
    ):
        self.adresse = adresse
        self.code_postal = code_postal
        self.coordonnees = coordonnees
        self.date_created = date_created
        self.date_updated = date_updated
        self.cartographie_id = id
        self.latitude = latitude
        self.longitude = longitude
        self.title = title
        self.ville = ville
        self.status = status

    @staticmethod
    def from_dict(obj: Any) -> Cartographie:
        assert isinstance(obj, dict)
        adresse = from_union([from_str, from_none], obj.get("adresse"))
        code_postal = from_union(
            [lambda x: int(from_str(x)), from_none], obj.get("codePostal")
        )
        coordonnees = from_union(
            [Coordonnees.from_dict, from_none], obj.get("coordonnees")
        )
        date_created = from_none(obj.get("date_created"))
        date_updated = from_none(obj.get("date_updated"))
        cartographie_id = from_union([from_str, from_none], obj.get("id"))
        latitude = from_union([from_float, from_none], obj.get("latitude"))
        longitude = from_union([from_float, from_none], obj.get("longitude"))
        title = from_union([from_str, from_none], obj.get("title"))
        ville = from_union([from_str, from_none], obj.get("ville"))
        status = from_union([from_str, from_none], obj.get("status"))
        return Cartographie(
            adresse,
            code_postal,
            coordonnees,
            date_created,
            date_updated,
            cartographie_id,
            latitude,
            longitude,
            title,
            ville,
            status,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.adresse is not None:
            result["adresse"] = from_union([from_str, from_none], self.adresse)
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
        if self.coordonnees is not None:
            result["coordonnees"] = from_union(
                [lambda x: to_class(Coordonnees, x), from_none], self.coordonnees
            )
        if self.date_created is not None:
            result["date_created"] = from_none(self.date_created)
        if self.date_updated is not None:
            result["date_updated"] = from_none(self.date_updated)
        if self.cartographie_id is not None:
            result["id"] = from_union([from_str, from_none], self.cartographie_id)
        if self.latitude is not None:
            result["latitude"] = from_union([to_float, from_none], self.latitude)
        if self.longitude is not None:
            result["longitude"] = from_union([to_float, from_none], self.longitude)
        if self.title is not None:
            result["title"] = from_union([from_str, from_none], self.title)
        if self.ville is not None:
            result["ville"] = from_union([from_str, from_none], self.ville)
        if self.status is not None:
            result["status"] = from_union([from_str, from_none], self.status)
        return result
