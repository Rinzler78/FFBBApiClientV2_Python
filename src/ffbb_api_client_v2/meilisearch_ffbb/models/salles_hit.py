from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ...meilisearch.models.hit import Hit
from ...models.cartographie import Cartographie
from ...models.commune import Commune
from ...models.geo import Geo
from ...models.type_association import TypeAssociation
from ...utils.converter_utils import (
    from_datetime,
    from_int,
    from_obj,
    from_str,
)


@dataclass
class SallesHit(Hit):
    libelle: str | None = None
    adresse: str | None = None
    id: str | None = None
    adresse_complement: str | None = None
    capacite_spectateur: int | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    libelle2: str | None = None
    mail: str | None = None
    numero: str | None = None
    telephone: str | None = None
    cartographie: Cartographie | None = None
    commune: Commune | None = None
    geo: Geo | None = None
    thumbnail: str | None = None
    type: str | None = None
    type_association: TypeAssociation | None = None
    lower_libelle: str | None = field(init=False, default=None, repr=False)
    lower_addresse: str | None = field(init=False, default=None, repr=False)
    lower_adresse_complement: str | None = field(init=False, default=None, repr=False)
    lower_libelle2: str | None = field(init=False, default=None, repr=False)

    def __post_init__(self) -> None:
        self.lower_libelle = self.libelle.lower() if self.libelle else None
        self.lower_addresse = self.adresse.lower() if self.adresse else None
        self.lower_adresse_complement = (
            self.adresse_complement.lower() if self.adresse_complement else None
        )
        self.lower_libelle2 = self.libelle2.lower() if self.libelle2 else None

    @staticmethod
    def from_dict(obj: Any) -> SallesHit:
        assert isinstance(obj, dict)
        libelle = from_str(obj, "libelle")
        adresse = from_str(obj, "adresse")
        id = from_str(obj, "id")
        adresse_complement = from_str(obj, "adresseComplement")
        capacite_spectateur = from_int(obj, "capaciteSpectateur")
        date_created = from_datetime(obj, "date_created")
        date_updated = from_datetime(obj, "date_updated")
        libelle2 = from_str(obj, "libelle2")
        mail = from_str(obj, "mail")
        numero = from_str(obj, "numero")
        telephone = from_str(obj, "telephone")
        cartographie = from_obj(Cartographie.from_dict, obj, "cartographie")
        commune = from_obj(Commune.from_dict, obj, "commune")
        geo = from_obj(Geo.from_dict, obj, "_geo")
        thumbnail = from_str(obj, "thumbnail")
        type = from_str(obj, "type")
        type_association = from_obj(TypeAssociation.from_dict, obj, "type_association")
        return SallesHit(
            libelle=libelle,
            adresse=adresse,
            id=id,
            adresse_complement=adresse_complement,
            capacite_spectateur=capacite_spectateur,
            date_created=date_created,
            date_updated=date_updated,
            libelle2=libelle2,
            mail=mail,
            numero=numero,
            telephone=telephone,
            cartographie=cartographie,
            commune=commune,
            geo=geo,
            thumbnail=thumbnail,
            type=type,
            type_association=type_association,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.libelle is not None:
            result["libelle"] = self.libelle
        if self.adresse is not None:
            result["adresse"] = self.adresse
        if self.id is not None:
            result["id"] = self.id
        if self.adresse_complement is not None:
            result["adresseComplement"] = self.adresse_complement
        if self.capacite_spectateur is not None:
            result["capaciteSpectateur"] = str(self.capacite_spectateur)
        if self.date_created is not None:
            result["date_created"] = self.date_created.isoformat()
        if self.date_updated is not None:
            result["date_updated"] = self.date_updated.isoformat()
        if self.libelle2 is not None:
            result["libelle2"] = self.libelle2
        if self.mail is not None:
            result["mail"] = self.mail
        if self.numero is not None:
            result["numero"] = self.numero
        if self.telephone is not None:
            result["telephone"] = self.telephone
        if self.cartographie is not None:
            result["cartographie"] = self.cartographie.to_dict()
        if self.commune is not None:
            result["commune"] = self.commune.to_dict()
        if self.geo is not None:
            result["_geo"] = self.geo.to_dict()
        if self.thumbnail is not None:
            result["thumbnail"] = self.thumbnail
        if self.type is not None:
            result["type"] = self.type
        if self.type_association is not None:
            result["type_association"] = self.type_association.to_dict()
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return bool(
            not query
            or (self.lower_addresse and query in self.lower_addresse)
            or (
                self.lower_adresse_complement and query in self.lower_adresse_complement
            )
            or (self.lower_libelle and query in self.lower_libelle)
            or (self.lower_libelle2 and query in self.lower_libelle2)
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
