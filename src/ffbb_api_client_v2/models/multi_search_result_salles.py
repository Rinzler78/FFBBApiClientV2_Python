from __future__ import annotations

from datetime import datetime
from typing import Any

from ..utils.converter_utils import (
    from_datetime,
    from_none,
    from_str,
    from_union,
    to_class,
)
from .Cartographie import Cartographie
from .Commune import Commune
from .FacetDistribution import FacetDistribution
from .FacetStats import FacetStats
from .Geo import Geo
from .Hit import Hit
from .TypeAssociation import TypeAssociation

# class LibelleEnum(Enum):
#     SALLE = "Salle"


class SallesFacetDistribution(FacetDistribution):
    @staticmethod
    def from_dict(obj: Any) -> SallesFacetDistribution:
        return SallesFacetDistribution()

    def to_dict(self) -> dict:
        super().to_dict()


class SallesHit(Hit):
    libelle: str | None = None
    adresse: str | None = None
    id: str | None = None
    adresse_complement: str | None = None
    capacite_spectateur: str | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    libelle2: str | None = None
    mail: str | None = None
    numero: str | None = None
    telephone: str | None = None
    cartographie: Cartographie | None = None
    commune: Commune | None = None
    geo: Geo | None = None
    thumbnail: None
    type: str | None = None
    type_association: TypeAssociation | None = None

    def __init__(
        self,
        libelle: str | None,
        adresse: str | None,
        id: str | None,
        adresse_complement: str | None,
        capacite_spectateur: str | None,
        date_created: datetime | None,
        date_updated: datetime | None,
        libelle2: str | None,
        mail: str | None,
        numero: str | None,
        telephone: str | None,
        cartographie: Cartographie | None,
        commune: Commune | None,
        geo: Geo | None,
        thumbnail: None,
        type: str | None,
        type_association: TypeAssociation | None,
    ) -> None:
        self.libelle = libelle
        self.lower_libelle = libelle.lower() if libelle else None

        self.adresse = adresse
        self.lower_addresse = adresse.lower() if adresse else None

        self.id = id
        self.adresse_complement = adresse_complement
        self.lower_adresse_complement = (
            adresse_complement.lower() if adresse_complement else None
        )

        self.capacite_spectateur = capacite_spectateur
        self.date_created = date_created
        self.date_updated = date_updated
        self.libelle2 = libelle2
        self.lower_libelle2 = libelle2.lower() if libelle2 else None

        self.mail = mail
        self.numero = numero
        self.telephone = telephone
        self.cartographie = cartographie
        self.commune = commune
        self.geo = geo
        self.thumbnail = thumbnail
        self.type = type
        self.type_association = type_association

    @staticmethod
    def from_dict(obj: Any) -> SallesHit:
        assert isinstance(obj, dict)
        libelle = from_union([from_str, from_none], obj.get("libelle"))
        adresse = from_union([from_none, from_str], obj.get("adresse"))
        id = from_union([from_str, from_none], obj.get("id"))
        adresse_complement = from_union(
            [from_none, from_str], obj.get("adresseComplement")
        )
        capacite_spectateur = from_union(
            [from_none, from_str], obj.get("capaciteSpectateur")
        )
        date_created = from_union([from_datetime, from_none], obj.get("date_created"))
        date_updated = from_union([from_datetime, from_none], obj.get("date_updated"))
        libelle2 = from_union([from_none, from_str], obj.get("libelle2"))
        mail = from_union([from_none, from_str], obj.get("mail"))
        numero = from_union([from_str, from_none], obj.get("numero"))
        telephone = from_union([from_none, from_str], obj.get("telephone"))
        cartographie = from_union(
            [Cartographie.from_dict, from_none], obj.get("cartographie")
        )
        commune = from_union([Commune.from_dict, from_none], obj.get("commune"))
        geo = from_union([Geo.from_dict, from_none], obj.get("_geo"))
        thumbnail = from_none(obj.get("thumbnail"))
        type = from_union([from_str, from_none], obj.get("type"))
        type_association = from_union(
            [TypeAssociation.from_dict, from_none], obj.get("type_association")
        )
        return SallesHit(
            libelle,
            adresse,
            id,
            adresse_complement,
            capacite_spectateur,
            date_created,
            date_updated,
            libelle2,
            mail,
            numero,
            telephone,
            cartographie,
            commune,
            geo,
            thumbnail,
            type,
            type_association,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.libelle is not None:
            result["libelle"] = from_union([from_str, from_none], self.libelle)
        if self.adresse is not None:
            result["adresse"] = from_union([from_none, from_str], self.adresse)
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.adresse_complement is not None:
            result["adresseComplement"] = from_union(
                [from_none, from_str], self.adresse_complement
            )
        if self.capacite_spectateur is not None:
            result["capaciteSpectateur"] = from_union(
                [from_none, from_str], self.capacite_spectateur
            )
        if self.date_created is not None:
            result["date_created"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_created
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_updated
            )
        if self.libelle2 is not None:
            result["libelle2"] = from_union([from_none, from_str], self.libelle2)
        if self.mail is not None:
            result["mail"] = from_union([from_none, from_str], self.mail)
        if self.numero is not None:
            result["numero"] = from_union([from_str, from_none], self.numero)
        if self.telephone is not None:
            result["telephone"] = from_union([from_none, from_str], self.telephone)
        if self.cartographie is not None:
            result["cartographie"] = from_union(
                [lambda x: to_class(Cartographie, x), from_none], self.cartographie
            )
        if self.commune is not None:
            result["commune"] = from_union(
                [lambda x: to_class(Commune, x), from_none], self.commune
            )
        if self.geo is not None:
            result["_geo"] = from_union(
                [lambda x: to_class(Geo, x), from_none], self.geo
            )
        if self.thumbnail is not None:
            result["thumbnail"] = from_none(self.thumbnail)
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        if self.type_association is not None:
            result["type_association"] = from_union(
                [lambda x: to_class(TypeAssociation, x), from_none],
                self.type_association,
            )
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return (
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


class SallesFacetStats(FacetStats):
    @staticmethod
    def from_dict(obj: Any) -> SallesFacetStats:
        return SallesFacetStats()

    def to_dict(self) -> dict:
        super().to_dict()
