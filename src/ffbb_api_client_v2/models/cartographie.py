from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ..utils.converter_utils import (
    from_datetime,
    from_float,
    from_obj,
    from_str,
)
from .coordonnees import Coordonnees


@dataclass
class Cartographie:
    adresse: str | None = None
    code_postal: str | None = None
    coordonnees: Coordonnees | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    cartographie_id: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    title: str | None = None
    ville: str | None = None
    status: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> Cartographie:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        adresse = from_str(obj, "adresse")
        code_postal = from_str(obj, "codePostal")
        coordonnees = from_obj(Coordonnees.from_dict, obj, "coordonnees")
        date_created = from_datetime(obj, "date_created")
        date_updated = from_datetime(obj, "date_updated")
        cartographie_id = from_str(obj, "id")
        latitude = from_float(obj, "latitude")
        longitude = from_float(obj, "longitude")
        title = from_str(obj, "title")
        ville = from_str(obj, "ville")
        status = from_str(obj, "status")
        return Cartographie(
            adresse=adresse,
            code_postal=code_postal,
            coordonnees=coordonnees,
            date_created=date_created,
            date_updated=date_updated,
            cartographie_id=cartographie_id,
            latitude=latitude,
            longitude=longitude,
            title=title,
            ville=ville,
            status=status,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.adresse is not None:
            result["adresse"] = self.adresse
        if self.code_postal is not None:
            result["codePostal"] = self.code_postal
        if self.coordonnees is not None:
            result["coordonnees"] = self.coordonnees.to_dict()
        if self.date_created is not None:
            result["date_created"] = self.date_created.isoformat()
        if self.date_updated is not None:
            result["date_updated"] = self.date_updated.isoformat()
        if self.cartographie_id is not None:
            result["id"] = self.cartographie_id
        if self.latitude is not None:
            result["latitude"] = self.latitude
        if self.longitude is not None:
            result["longitude"] = self.longitude
        if self.title is not None:
            result["title"] = self.title
        if self.ville is not None:
            result["ville"] = self.ville
        if self.status is not None:
            result["status"] = self.status
        return result
