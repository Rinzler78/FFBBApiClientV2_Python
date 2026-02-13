from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ...meilisearch.models.hit import Hit
from ...models.cartographie import Cartographie
from ...models.commune import Commune
from ...models.geo import Geo
from ...models.nature_sol import NatureSol
from ...models.tournois_hit_type import HitType
from ...utils.converter_utils import (
    from_bool,
    from_datetime,
    from_enum,
    from_int,
    from_obj,
    from_str,
)


@dataclass
class TerrainsHit(Hit):
    nom: str | None = None
    rue: str | None = None
    id: int | None = None
    acces_libre: bool | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    largeur: int | None = None
    longueur: int | None = None
    numero: int | None = None
    cartographie: Cartographie | None = None
    commune: Commune | None = None
    nature_sol: NatureSol | None = None
    geo: Geo | None = None
    thumbnail: str | None = None
    type: HitType | None = None
    lower_nom: str | None = field(init=False, default=None, repr=False)
    lower_rue: str | None = field(init=False, default=None, repr=False)

    def __post_init__(self) -> None:
        self.lower_nom = self.nom.lower() if self.nom else None
        self.lower_rue = self.rue.lower() if self.rue else None

    @staticmethod
    def from_dict(obj: Any) -> TerrainsHit:
        assert isinstance(obj, dict)
        nom = from_str(obj, "nom")
        rue = from_str(obj, "rue")
        id = from_int(obj, "id")
        acces_libre = from_bool(obj, "accesLibre")
        date_created = from_datetime(obj, "date_created")
        date_updated = from_datetime(obj, "date_updated")
        largeur = from_int(obj, "largeur")
        longueur = from_int(obj, "longueur")
        numero = from_int(obj, "numero")
        cartographie = from_obj(Cartographie.from_dict, obj, "cartographie")
        commune = from_obj(Commune.from_dict, obj, "commune")
        nature_sol = from_obj(NatureSol.from_dict, obj, "natureSol")
        geo = from_obj(Geo.from_dict, obj, "_geo")
        thumbnail = from_str(obj, "thumbnail")
        type = from_enum(HitType, obj, "type")
        return TerrainsHit(
            nom=nom,
            rue=rue,
            id=id,
            acces_libre=acces_libre,
            date_created=date_created,
            date_updated=date_updated,
            largeur=largeur,
            longueur=longueur,
            numero=numero,
            cartographie=cartographie,
            commune=commune,
            nature_sol=nature_sol,
            geo=geo,
            thumbnail=thumbnail,
            type=type,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom is not None:
            result["nom"] = self.nom
        if self.rue is not None:
            result["rue"] = self.rue
        if self.id is not None:
            result["id"] = str(self.id)
        if self.acces_libre is not None:
            result["accesLibre"] = self.acces_libre
        if self.date_created is not None:
            result["date_created"] = self.date_created.isoformat()
        if self.date_updated is not None:
            result["date_updated"] = self.date_updated.isoformat()
        if self.largeur is not None:
            result["largeur"] = self.largeur
        if self.longueur is not None:
            result["longueur"] = self.longueur
        if self.numero is not None:
            result["numero"] = self.numero
        if self.cartographie is not None:
            result["cartographie"] = self.cartographie.to_dict()
        if self.commune is not None:
            result["commune"] = self.commune.to_dict()
        if self.nature_sol is not None:
            result["natureSol"] = self.nature_sol.to_dict()
        if self.geo is not None:
            result["_geo"] = self.geo.to_dict()
        if self.thumbnail is not None:
            result["thumbnail"] = self.thumbnail
        if self.type is not None:
            result["type"] = self.type.value
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return bool(
            not query
            or (self.lower_nom and query in self.lower_nom)
            or (self.lower_rue and query in self.lower_rue)
            or (
                self.commune
                and (
                    (self.commune.lower_libelle and query in self.commune.lower_libelle)
                    or (
                        self.commune.lower_departement
                        and query in self.commune.lower_departement
                    )
                )
            )
        )
