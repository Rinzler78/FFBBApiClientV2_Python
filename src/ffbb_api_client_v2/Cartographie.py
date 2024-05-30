from dataclasses import dataclass
from typing import Any, Optional

from ffbb_api_client_v2.converters import (
    from_float,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
    to_float,
)
from ffbb_api_client_v2.Coordonnees import Coordonnees


@dataclass
class Cartographie:
    adresse: Optional[str] = None
    code_postal: Optional[int] = None
    coordonnees: Optional[Coordonnees] = None
    date_created: None
    date_updated: None
    id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    title: Optional[str] = None
    ville: Optional[str] = None
    status: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Cartographie":
        assert isinstance(obj, dict)
        adresse = from_union([from_str, from_none], obj.get("adresse"))
        code_postal = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("codePostal")
        )
        coordonnees = from_union(
            [Coordonnees.from_dict, from_none], obj.get("coordonnees")
        )
        date_created = from_none(obj.get("date_created"))
        date_updated = from_none(obj.get("date_updated"))
        id = from_union([from_str, from_none], obj.get("id"))
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
            id,
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
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
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
