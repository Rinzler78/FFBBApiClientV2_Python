from __future__ import annotations

from enum import Enum
from typing import Any

from ..utils.converter_utils import (
    from_bool,
    from_datetime,
    from_dict,
    from_int,
    from_list,
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
from .Labellisation import Labellisation
from .logo import Logo
from .OrganismeIDPere import OrganismeIDPere
from .TypeAssociation import TypeAssociation
from .TypeAssociationLibelle import TypeAssociationLibelle
from .TypeClass import TypeClass


class OrganismesFacetDistribution(FacetDistribution):
    labellisation: Labellisation | None = None
    offres_pratiques: dict[str, int] | None = None
    type: TypeClass | None = None
    type_association_libelle: TypeAssociationLibelle | None = None

    def __init__(
        self,
        labellisation: Labellisation | None,
        offres_pratiques: dict[str, int] | None,
        type: TypeClass | None,
        type_association_libelle: TypeAssociationLibelle | None,
    ) -> None:
        self.labellisation = labellisation
        self.offres_pratiques = offres_pratiques
        self.type = type
        self.type_association_libelle = type_association_libelle

    @staticmethod
    def from_dict(obj: Any) -> OrganismesFacetDistribution:
        assert isinstance(obj, dict)
        labellisation = from_union(
            [Labellisation.from_dict, from_none], obj.get("labellisation")
        )
        offres_pratiques = from_union(
            [lambda x: from_dict(from_int, x), from_none], obj.get("offresPratiques")
        )
        type = from_union([TypeClass.from_dict, from_none], obj.get("type"))
        type_association_libelle = from_union(
            [TypeAssociationLibelle.from_dict, from_none],
            obj.get("type_association.libelle"),
        )
        return OrganismesFacetDistribution(
            labellisation, offres_pratiques, type, type_association_libelle
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.labellisation is not None:
            result["labellisation"] = from_union(
                [lambda x: to_class(Labellisation, x), from_none], self.labellisation
            )
        if self.offres_pratiques is not None:
            result["offresPratiques"] = from_union(
                [lambda x: from_dict(from_int, x), from_none], self.offres_pratiques
            )
        if self.type is not None:
            result["type"] = from_union(
                [lambda x: to_class(TypeClass, x), from_none], self.type
            )
        if self.type_association_libelle is not None:
            result["type_association.libelle"] = from_union(
                [lambda x: to_class(TypeAssociationLibelle, x), from_none],
                self.type_association_libelle,
            )
        return result


class HitType(Enum):
    BASKET_INCLUSIF = "Basket Inclusif"
    BASKET_SANTÉ = "Basket Santé"
    BASKET_TONIK = "Basket Tonik"
    CENTRE_GÉNÉRATION_BASKET = "Centre Génération Basket"
    MICRO_BASKET = "Micro Basket"


class OrganismesHit(Hit):
    nom_club_pro: str | None = None
    nom: str | None = None
    adresse: str | None = None
    adresse_club_pro: None
    code: str | None = None
    id: str | None = None
    engagements_noms: str | None = None
    mail: str | None = None
    telephone: str | None = None
    type: str | None = None
    url_site_web: str | None = None
    nom_simple: None
    date_affiliation: None
    saison_en_cours: bool | None = None
    offres_pratiques: list[str] | None = None
    labellisation: list[str] | None = None
    cartographie: Cartographie | None = None
    organisme_id_pere: OrganismeIDPere | None = None
    commune: Commune | None = None
    commune_club_pro: None
    type_association: TypeAssociation | None = None
    logo: Logo | None = None
    geo: Geo | None = None
    thumbnail: str | None = None

    def __init__(
        self,
        nom_club_pro: str | None,
        nom: str | None,
        adresse: str | None,
        adresse_club_pro: None,
        code: str | None,
        id: str | None,
        engagements_noms: str | None,
        mail: str | None,
        telephone: str | None,
        type: str | None,
        url_site_web: str | None,
        nom_simple: None,
        date_affiliation: None,
        saison_en_cours: bool | None,
        offres_pratiques: list[str] | None,
        labellisation: list[str] | None,
        cartographie: Cartographie | None,
        organisme_id_pere: OrganismeIDPere | None,
        commune: Commune | None,
        commune_club_pro: None,
        type_association: TypeAssociation | None,
        logo: Logo | None,
        geo: Geo | None,
        thumbnail: str | None,
    ) -> None:
        self.nom_club_pro = nom_club_pro
        self.lower_nom_club_pro = nom_club_pro.lower() if nom_club_pro else None

        self.nom = nom
        self.lower_nom = nom.lower() if nom else None

        self.adresse = adresse
        self.adresse_club_pro = adresse_club_pro
        self.code = code
        self.id = id
        self.engagements_noms = engagements_noms
        self.lower_engagements_noms = (
            self.engagements_noms.lower() if self.engagements_noms else None
        )

        self.mail = mail
        self.telephone = telephone
        self.type = type
        self.url_site_web = url_site_web
        self.nom_simple = nom_simple
        self.date_affiliation = date_affiliation
        self.saison_en_cours = saison_en_cours
        self.offres_pratiques = offres_pratiques
        self.labellisation = labellisation
        self.cartographie = cartographie
        self.organisme_id_pere = organisme_id_pere
        self.commune = commune
        self.commune_club_pro = commune_club_pro
        self.type_association = type_association
        self.logo = logo
        self.geo = geo
        self.thumbnail = thumbnail

    @staticmethod
    def from_dict(obj: Any) -> Hit:
        try:
            assert isinstance(obj, dict)
            nom_club_pro = from_union([from_str, from_none], obj.get("nomClubPro"))
            nom = from_union([from_str, from_none], obj.get("nom"))
            adresse = from_union([from_str, from_none], obj.get("adresse"))
            adresse_club_pro = from_none(obj.get("adresseClubPro"))
            code = from_union([from_str, from_none], obj.get("code"))
            id = from_union([from_str, from_none], obj.get("id"))
            engagements_noms = from_union(
                [from_str, from_none], obj.get("engagements_noms")
            )
            mail = from_union([from_str, from_none], obj.get("mail"))
            telephone = from_union([from_str, from_none], obj.get("telephone"))
            type = from_union([from_str, from_none], obj.get("type"))
            url_site_web = from_union([from_str, from_none], obj.get("urlSiteWeb"))
            nom_simple = from_union([from_str, from_none], obj.get("nom_simple"))
            date_affiliation = from_union(
                [from_datetime, from_none], obj.get("dateAffiliation")
            )
            saison_en_cours = from_union(
                [from_bool, from_none], obj.get("saison_en_cours")
            )
            offres_pratiques = from_union(
                [lambda x: from_list(from_str, x), from_none],
                obj.get("offresPratiques"),
            )
            labellisation = from_union(
                [lambda x: from_list(from_str, x), from_none], obj.get("labellisation")
            )
            cartographie = from_union(
                [Cartographie.from_dict, from_none], obj.get("cartographie")
            )
            organisme_id_pere = from_union(
                [OrganismeIDPere.from_dict, from_none], obj.get("organisme_id_pere")
            )
            commune = from_union([Commune.from_dict, from_none], obj.get("commune"))
            commune_club_pro = from_union(
                [Commune.from_dict, from_none], obj.get("communeClubPro")
            )
            type_association = from_union(
                [TypeAssociation.from_dict, from_none], obj.get("type_association")
            )
            logo = from_union([Logo.from_dict, from_none], obj.get("logo"))
            geo = from_union([Geo.from_dict, from_none], obj.get("_geo"))
            thumbnail = from_union([from_none, from_str], obj.get("thumbnail"))
            return OrganismesHit(
                nom_club_pro,
                nom,
                adresse,
                adresse_club_pro,
                code,
                id,
                engagements_noms,
                mail,
                telephone,
                type,
                url_site_web,
                nom_simple,
                date_affiliation,
                saison_en_cours,
                offres_pratiques,
                labellisation,
                cartographie,
                organisme_id_pere,
                commune,
                commune_club_pro,
                type_association,
                logo,
                geo,
                thumbnail,
            )
        except Exception as e:
            raise ValueError(f"Invalid `OrganismesHit` object: {e}")

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom_club_pro is not None:
            result["nomClubPro"] = from_union([from_str, from_none], self.nom_club_pro)
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.adresse is not None:
            result["adresse"] = from_union([from_str, from_none], self.adresse)
        if self.adresse_club_pro is not None:
            result["adresseClubPro"] = from_none(self.adresse_club_pro)
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.engagements_noms is not None:
            result["engagements_noms"] = from_union(
                [from_str, from_none], self.engagements_noms
            )
        if self.mail is not None:
            result["mail"] = from_union([from_str, from_none], self.mail)
        if self.telephone is not None:
            result["telephone"] = from_union([from_str, from_none], self.telephone)
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        if self.url_site_web is not None:
            result["urlSiteWeb"] = from_union([from_str, from_none], self.url_site_web)
        if self.nom_simple is not None:
            result["nom_simple"] = from_none(self.nom_simple)
        if self.date_affiliation is not None:
            result["dateAffiliation"] = from_none(self.date_affiliation)
        if self.saison_en_cours is not None:
            result["saison_en_cours"] = from_union(
                [from_bool, from_none], self.saison_en_cours
            )
        if self.offres_pratiques is not None:
            result["offresPratiques"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.offres_pratiques
            )
        if self.labellisation is not None:
            result["labellisation"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.labellisation
            )
        if self.cartographie is not None:
            result["cartographie"] = from_union(
                [lambda x: to_class(Cartographie, x), from_none], self.cartographie
            )
        if self.organisme_id_pere is not None:
            result["organisme_id_pere"] = from_union(
                [lambda x: to_class(OrganismeIDPere, x), from_none],
                self.organisme_id_pere,
            )
        if self.commune is not None:
            result["commune"] = from_union(
                [lambda x: to_class(Commune, x), from_none], self.commune
            )
        if self.commune_club_pro is not None:
            result["communeClubPro"] = from_union(
                [lambda x: to_class(Commune, x), from_none], self.commune_club_pro
            )
        if self.type_association is not None:
            result["type_association"] = from_union(
                [lambda x: to_class(TypeAssociation, x), from_none],
                self.type_association,
            )
        if self.logo is not None:
            result["logo"] = from_union(
                [lambda x: to_class(Logo, x), from_none], self.logo
            )
        if self.geo is not None:
            result["_geo"] = from_union(
                [lambda x: to_class(Geo, x), from_none], self.geo
            )
        if self.thumbnail is not None:
            result["thumbnail"] = from_union([from_none, from_str], self.thumbnail)
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return (
            not query
            or (self.lower_nom and query in self.lower_nom)
            or (self.lower_nom_club_pro and query in self.lower_nom_club_pro)
            or (self.lower_engagements_noms and query in self.lower_engagements_noms)
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


class OrganismesFacetStats(FacetStats):
    @staticmethod
    def from_dict(obj: Any) -> OrganismesFacetStats:
        return OrganismesFacetStats()

    def to_dict(self) -> dict:
        super().to_dict()
