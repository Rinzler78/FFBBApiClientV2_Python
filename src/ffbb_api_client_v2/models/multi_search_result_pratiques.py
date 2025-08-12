from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from ..utils.converter_utils import (
    from_datetime,
    from_dict,
    from_float,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
    to_enum,
    to_float,
)
from .FacetDistribution import FacetDistribution
from .FacetStats import FacetStats
from .Hit import Hit


class TypeClass:
    basket_inclusif: int | None = None
    basket_santé: int | None = None
    basket_tonik: int | None = None
    centre_génération_basket: int | None = None
    micro_basket: int | None = None

    def __init__(
        self,
        basket_inclusif: int | None,
        basket_santé: int | None,
        basket_tonik: int | None,
        centre_génération_basket: int | None,
        micro_basket: int | None = None,
    ) -> None:
        self.basket_inclusif = basket_inclusif
        self.basket_santé = basket_santé
        self.basket_tonik = basket_tonik
        self.centre_génération_basket = centre_génération_basket
        self.micro_basket = micro_basket

    @staticmethod
    def from_dict(obj: Any) -> TypeClass:
        assert isinstance(obj, dict)
        basket_inclusif = from_union([from_int, from_none], obj.get("Basket Inclusif"))
        basket_santé = from_union([from_int, from_none], obj.get("Basket Santé"))
        basket_tonik = from_union([from_int, from_none], obj.get("Basket Tonik"))
        centre_génération_basket = from_union(
            [from_int, from_none], obj.get("Centre Génération Basket")
        )
        micro_basket = from_union([from_int, from_none], obj.get("Micro Basket"))
        return TypeClass(
            basket_inclusif,
            basket_santé,
            basket_tonik,
            centre_génération_basket,
            micro_basket,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.basket_inclusif is not None:
            result["Basket Inclusif"] = from_union(
                [from_int, from_none], self.basket_inclusif
            )
        if self.basket_santé is not None:
            result["Basket Santé"] = from_union(
                [from_int, from_none], self.basket_santé
            )
        if self.basket_tonik is not None:
            result["Basket Tonik"] = from_union(
                [from_int, from_none], self.basket_tonik
            )
        if self.centre_génération_basket is not None:
            result["Centre Génération Basket"] = from_union(
                [from_int, from_none], self.centre_génération_basket
            )
        if self.micro_basket is not None:
            result["Micro Basket"] = from_union(
                [from_int, from_none], self.micro_basket
            )
        return result


class PratiquesFacetDistribution(FacetDistribution):
    label: dict[str, int] | None = None
    type: TypeClass | None = None

    def __init__(
        self, label: dict[str, int] | None, type: TypeClass | None = None
    ) -> None:
        self.label = label
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> PratiquesFacetDistribution:
        assert isinstance(obj, dict)
        label = from_union(
            [lambda x: from_dict(from_int, x), from_none], obj.get("label")
        )
        type = from_union([TypeClass.from_dict, from_none], obj.get("type"))
        return PratiquesFacetDistribution(label, type)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.label is not None:
            result["label"] = from_union(
                [lambda x: from_dict(from_int, x), from_none], self.label
            )
        if self.type is not None:
            result["type"] = from_union(
                [lambda x: to_class(TypeClass, x), from_none], self.type
            )
        return result


class PratiquesFacetStats(FacetStats):
    def __init__(self) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> PratiquesFacetStats:
        assert isinstance(obj, dict)
        return PratiquesFacetStats()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


class Affiche:
    id: UUID | None = None
    gradient_color: str | None = None
    width: int | None = None
    height: int | None = None

    def __init__(
        self,
        id: UUID | None,
        gradient_color: str | None,
        width: int | None,
        height: int | None = None,
    ) -> None:
        self.id = id
        self.gradient_color = gradient_color
        self.width = width
        self.height = height

    @staticmethod
    def from_dict(obj: Any) -> Affiche:
        assert isinstance(obj, dict)
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        gradient_color = from_union([from_none, from_str], obj.get("gradient_color"))
        width = from_union([from_int, from_none], obj.get("width"))
        height = from_union([from_int, from_none], obj.get("height"))
        return Affiche(id, gradient_color, width, height)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([lambda x: str(x), from_none], self.id)
        if self.gradient_color is not None:
            result["gradient_color"] = from_union(
                [from_none, from_str], self.gradient_color
            )
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        return result


class CoordonneesType(Enum):
    POINT = "Point"


class Coordonnees:
    type: CoordonneesType | None = None
    coordinates: list[float] | None = None

    def __init__(
        self, type: CoordonneesType | None, coordinates: list[float] | None = None
    ) -> None:
        self.type = type
        self.coordinates = coordinates

    @staticmethod
    def from_dict(obj: Any) -> Coordonnees:
        assert isinstance(obj, dict)
        type = from_union([CoordonneesType, from_none], obj.get("type"))
        coordinates = from_union(
            [lambda x: from_list(from_float, x), from_none], obj.get("coordinates")
        )
        return Coordonnees(type, coordinates)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["type"] = from_union(
                [lambda x: to_enum(CoordonneesType, x), from_none], self.type
            )
        if self.coordinates is not None:
            result["coordinates"] = from_union(
                [lambda x: from_list(to_float, x), from_none], self.coordinates
            )
        return result


class Status(Enum):
    DRAFT = "draft"


class Cartographie:
    adresse: str | None = None
    code_postal: str | None = None
    coordonnees: Coordonnees | None = None
    date_created: None
    date_updated: None
    id: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    title: str | None = None
    ville: str | None = None
    status: Status | None = None

    def __init__(
        self,
        adresse: str | None,
        code_postal: str | None,
        coordonnees: Coordonnees | None,
        date_created: None,
        date_updated: None,
        id: str | None,
        latitude: float | None,
        longitude: float | None,
        title: str | None,
        ville: str | None,
        status: Status | None = None,
    ) -> None:
        self.adresse = adresse
        self.code_postal = code_postal
        self.coordonnees = coordonnees
        self.date_created = date_created
        self.date_updated = date_updated
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.title = title
        self.ville = ville
        self.status = status

    @staticmethod
    def from_dict(obj: Any) -> Cartographie:
        assert isinstance(obj, dict)
        adresse = from_union([from_str, from_none], obj.get("adresse"))
        code_postal = from_union([from_str, from_none], obj.get("codePostal"))
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
        status = from_union([Status, from_none], obj.get("status"))
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
            result["codePostal"] = from_union([from_str, from_none], self.code_postal)
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
            result["status"] = from_union(
                [lambda x: to_enum(Status, x), from_none], self.status
            )
        return result


class Geo:
    lat: float | None = None
    lng: float | None = None

    def __init__(self, lat: float | None, lng: float | None = None) -> None:
        self.lat = lat
        self.lng = lng

    @staticmethod
    def from_dict(obj: Any) -> Geo:
        assert isinstance(obj, dict)
        lat = from_union([from_float, from_none], obj.get("lat"))
        lng = from_union([from_float, from_none], obj.get("lng"))
        return Geo(lat, lng)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.lat is not None:
            result["lat"] = from_union([to_float, from_none], self.lat)
        if self.lng is not None:
            result["lng"] = from_union([to_float, from_none], self.lng)
        return result


class Jour(Enum):
    SUNDAY = "dimanche"
    THURSDAY = "jeudi"
    MONDAY = "lundi"
    TUESDAY = "mardi"
    WEDNESDAY = "mercredi"
    SATURDAY = "samedi"
    FRIDAY = "vendredi"


class Label(Enum):
    BASKET_INCLUSIF = "Basket Inclusif"
    BASKET_SANTÉ_CONFORT = "Basket Santé Confort"
    BASKET_SANTÉ_DÉCOUVERTE = "Basket Santé Découverte"
    BASKET_SANTÉ_RÉSOLUTIONS = "Basket Santé Résolutions"
    BASKE_TONIK = "BaskeTonik"
    BASKE_TONIK_FORME = "BaskeTonik forme"
    DÉCOUVERTE_BASKET_INCLUSIF = "Découverte Basket Inclusif"
    DÉCOUVERTE_BASKE_TONIK = "Découverte BaskeTonik"
    DÉCOUVERTE_MICRO_BASKET = "Découverte Micro Basket"
    EMPTY = ""
    MICRO_BASKET = "Micro Basket"


class Objectif(Enum):
    ACCOMPAGNEMENT = "Accompagnement"
    CURATIF = "Curatif"
    PREVENTIVE = "Préventif"


class HitType(Enum):
    BASKET_INCLUSIF = "Basket Inclusif"
    BASKET_SANTÉ = "Basket Santé"
    BASKET_TONIK = "Basket Tonik"
    CENTRE_GÉNÉRATION_BASKET = "Centre Génération Basket"
    MICRO_BASKET = "Micro Basket"


class PratiquesHit(Hit):
    titre: str | None = None
    type: HitType | None = None
    adresse: str | None = None
    description: str | None = None
    id: int | None = None
    date_created: datetime | None = None
    date_debut: datetime | None = None
    date_demande: int | None = None
    date_fin: datetime | None = None
    date_updated: datetime | None = None
    facebook: None
    site_web: str | None = None
    twitter: None
    action: str | None = None
    adresse_salle: str | None = None
    adresse_structure: str | None = None
    assurance: str | None = None
    code: str | None = None
    cp_salle: str | None = None
    date_inscription: int | None = None
    email: str | None = None
    engagement: str | None = None
    horaires_seances: str | None = None
    inscriptions: str | None = None
    jours: list[Jour] | None = None
    label: Label | None = None
    latitude: None
    longitude: None
    mail_demandeur: str | None = None
    mail_structure: str | None = None
    nom_demandeur: str | None = None
    nom_salle: str | None = None
    nom_structure: str | None = None
    nombre_personnes: str | None = None
    nombre_seances: str | None = None
    objectif: Objectif | None = None
    prenom_demandeur: str | None = None
    public: str | None = None
    telephone: str | None = None
    ville_salle: str | None = None
    cartographie: Cartographie | None = None
    affiche: Affiche | None = None
    geo: Geo | None = None
    date_debut_timestamp: int | None = None
    date_fin_timestamp: int | None = None
    thumbnail: str | None = None

    def __init__(
        self,
        titre: str | None,
        type: HitType | None,
        adresse: str | None,
        description: str | None,
        id: int | None,
        date_created: datetime | None,
        date_debut: datetime | None,
        date_demande: int | None,
        date_fin: datetime | None,
        date_updated: datetime | None,
        facebook: None,
        site_web: str | None,
        twitter: None,
        action: str | None,
        adresse_salle: str | None,
        adresse_structure: str | None,
        assurance: str | None,
        code: str | None,
        cp_salle: str | None,
        date_inscription: int | None,
        email: str | None,
        engagement: str | None,
        horaires_seances: str | None,
        inscriptions: str | None,
        jours: list[Jour] | None,
        label: Label | None,
        latitude: None,
        longitude: None,
        mail_demandeur: str | None,
        mail_structure: str | None,
        nom_demandeur: str | None,
        nom_salle: str | None,
        nom_structure: str | None,
        nombre_personnes: str | None,
        nombre_seances: str | None,
        objectif: Objectif | None,
        prenom_demandeur: str | None,
        public: str | None,
        telephone: str | None,
        ville_salle: str | None,
        cartographie: Cartographie | None,
        affiche: Affiche | None,
        geo: Geo | None,
        date_debut_timestamp: int | None,
        date_fin_timestamp: int | None,
        thumbnail: str | None,
    ) -> None:
        self.titre = titre
        self.lower_titre = titre.lower() if titre else None

        self.type = type
        self.adresse = adresse
        self.lower_addresse = adresse.lower() if adresse else None

        self.description = description
        self.lower_description = description.lower() if description else None

        self.id = id
        self.date_created = date_created
        self.date_debut = date_debut
        self.date_demande = date_demande
        self.date_fin = date_fin
        self.date_updated = date_updated
        self.facebook = facebook
        self.site_web = site_web
        self.lower_site_web = site_web.lower() if site_web else None

        self.twitter = twitter
        self.action = action
        self.lower_action = action.lower() if action else None

        self.adresse_salle = adresse_salle
        self.lower_adresse_salle = adresse_salle.lower() if adresse_salle else None

        self.adresse_structure = adresse_structure
        self.lower_adresse_structure = (
            adresse_structure.lower() if adresse_structure else None
        )

        self.assurance = assurance
        self.code = code
        self.cp_salle = cp_salle
        self.date_inscription = date_inscription
        self.email = email
        self.engagement = engagement
        self.horaires_seances = horaires_seances
        self.inscriptions = inscriptions
        self.jours = jours
        self.label = label
        self.latitude = latitude
        self.longitude = longitude
        self.mail_demandeur = mail_demandeur
        self.mail_structure = mail_structure
        self.nom_demandeur = nom_demandeur
        self.nom_salle = nom_salle
        self.lower_nom_salle = nom_salle.lower() if nom_salle else None

        self.nom_structure = nom_structure
        self.lower_nom_structure = nom_structure.lower() if nom_structure else None

        self.nombre_personnes = nombre_personnes
        self.nombre_seances = nombre_seances
        self.objectif = objectif
        self.prenom_demandeur = prenom_demandeur
        self.public = public
        self.telephone = telephone
        self.ville_salle = ville_salle
        self.lower_ville_salle = ville_salle.lower() if ville_salle else None

        self.cartographie = cartographie
        self.affiche = affiche
        self.geo = geo
        self.date_debut_timestamp = date_debut_timestamp
        self.date_fin_timestamp = date_fin_timestamp
        self.thumbnail = thumbnail

    @staticmethod
    def from_dict(obj: Any) -> PratiquesHit:
        assert isinstance(obj, dict)
        titre = from_union([from_str, from_none], obj.get("titre"))
        type = from_union([HitType, from_none], obj.get("type"))
        adresse = from_union([from_str, from_none], obj.get("adresse"))
        description = from_union([from_none, from_str], obj.get("description"))
        id = from_union([from_none, lambda x: int(from_str(x))], obj.get("id"))
        date_created = from_union([from_datetime, from_none], obj.get("date_created"))
        date_debut = from_union([from_datetime, from_none], obj.get("date_debut"))
        date_demande = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("date_demande")
        )
        date_fin = from_union([from_datetime, from_none], obj.get("date_fin"))
        date_updated = from_union([from_datetime, from_none], obj.get("date_updated"))
        facebook = from_none(obj.get("facebook"))
        site_web = from_union([from_none, from_str], obj.get("site_web"))
        twitter = from_none(obj.get("twitter"))
        action = from_union([from_str, from_none], obj.get("action"))
        adresse_salle = from_union([from_str, from_none], obj.get("adresse_salle"))
        adresse_structure = from_union(
            [from_none, from_str], obj.get("adresse_structure")
        )
        assurance = from_union([from_none, from_str], obj.get("assurance"))
        code = from_union([from_none, from_str], obj.get("code"))
        cp_salle = from_union([from_str, from_none], obj.get("cp_salle"))
        date_inscription = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("date_inscription")
        )
        email = from_union([from_none, from_str], obj.get("email"))
        engagement = from_union([from_none, from_str], obj.get("engagement"))
        horaires_seances = from_union(
            [from_none, from_str], obj.get("horaires_seances")
        )
        inscriptions = from_union([from_none, from_str], obj.get("inscriptions"))
        jours = from_union([lambda x: from_list(Jour, x), from_none], obj.get("jours"))
        label = from_union([Label, from_none], obj.get("label"))
        latitude = from_none(obj.get("latitude"))
        longitude = from_none(obj.get("longitude"))
        mail_demandeur = from_union([from_none, from_str], obj.get("mail_demandeur"))
        mail_structure = from_union([from_none, from_str], obj.get("mail_structure"))
        nom_demandeur = from_union([from_none, from_str], obj.get("nom_demandeur"))
        nom_salle = from_union([from_str, from_none], obj.get("nom_salle"))
        nom_structure = from_union([from_none, from_str], obj.get("nom_structure"))
        nombre_personnes = from_union(
            [from_none, from_str], obj.get("nombre_personnes")
        )
        nombre_seances = from_union([from_none, from_str], obj.get("nombre_seances"))
        objectif = from_union([from_none, Objectif], obj.get("objectif"))
        prenom_demandeur = from_union(
            [from_none, from_str], obj.get("prenom_demandeur")
        )
        public = from_union([from_none, from_str], obj.get("public"))
        telephone = from_union([from_none, from_str], obj.get("telephone"))
        ville_salle = from_union([from_str, from_none], obj.get("ville_salle"))
        cartographie = from_union(
            [Cartographie.from_dict, from_none], obj.get("cartographie")
        )
        affiche = from_union([from_none, Affiche.from_dict], obj.get("affiche"))
        geo = from_union([Geo.from_dict, from_none], obj.get("_geo"))
        date_debut_timestamp = from_union(
            [from_int, from_none], obj.get("date_debut_timestamp")
        )
        date_fin_timestamp = from_union(
            [from_int, from_none], obj.get("date_fin_timestamp")
        )
        thumbnail = from_union([from_none, from_str], obj.get("thumbnail"))
        return PratiquesHit(
            titre,
            type,
            adresse,
            description,
            id,
            date_created,
            date_debut,
            date_demande,
            date_fin,
            date_updated,
            facebook,
            site_web,
            twitter,
            action,
            adresse_salle,
            adresse_structure,
            assurance,
            code,
            cp_salle,
            date_inscription,
            email,
            engagement,
            horaires_seances,
            inscriptions,
            jours,
            label,
            latitude,
            longitude,
            mail_demandeur,
            mail_structure,
            nom_demandeur,
            nom_salle,
            nom_structure,
            nombre_personnes,
            nombre_seances,
            objectif,
            prenom_demandeur,
            public,
            telephone,
            ville_salle,
            cartographie,
            affiche,
            geo,
            date_debut_timestamp,
            date_fin_timestamp,
            thumbnail,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.titre is not None:
            result["titre"] = from_union([from_str, from_none], self.titre)
        if self.type is not None:
            result["type"] = from_union(
                [lambda x: to_enum(HitType, x), from_none], self.type
            )
        if self.adresse is not None:
            result["adresse"] = from_union([from_str, from_none], self.adresse)
        if self.description is not None:
            result["description"] = from_union([from_none, from_str], self.description)
        if self.id is not None:
            result["id"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.id,
            )
        if self.date_created is not None:
            result["date_created"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_created
            )
        if self.date_debut is not None:
            result["date_debut"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_debut
            )
        if self.date_demande is not None:
            result["date_demande"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.date_demande,
            )
        if self.date_fin is not None:
            result["date_fin"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_fin
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_updated
            )
        if self.facebook is not None:
            result["facebook"] = from_none(self.facebook)
        if self.site_web is not None:
            result["site_web"] = from_union([from_none, from_str], self.site_web)
        if self.twitter is not None:
            result["twitter"] = from_none(self.twitter)
        if self.action is not None:
            result["action"] = from_union([from_str, from_none], self.action)
        if self.adresse_salle is not None:
            result["adresse_salle"] = from_union(
                [from_str, from_none], self.adresse_salle
            )
        if self.adresse_structure is not None:
            result["adresse_structure"] = from_union(
                [from_none, from_str], self.adresse_structure
            )
        if self.assurance is not None:
            result["assurance"] = from_union([from_none, from_str], self.assurance)
        if self.code is not None:
            result["code"] = from_union([from_none, from_str], self.code)
        if self.cp_salle is not None:
            result["cp_salle"] = from_union([from_str, from_none], self.cp_salle)
        if self.date_inscription is not None:
            result["date_inscription"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.date_inscription,
            )
        if self.email is not None:
            result["email"] = from_union([from_none, from_str], self.email)
        if self.engagement is not None:
            result["engagement"] = from_union([from_none, from_str], self.engagement)
        if self.horaires_seances is not None:
            result["horaires_seances"] = from_union(
                [from_none, from_str], self.horaires_seances
            )
        if self.inscriptions is not None:
            result["inscriptions"] = from_union(
                [from_none, from_str], self.inscriptions
            )
        if self.jours is not None:
            result["jours"] = from_union(
                [lambda x: from_list(lambda x: to_enum(Jour, x), x), from_none],
                self.jours,
            )
        if self.label is not None:
            result["label"] = from_union(
                [lambda x: to_enum(Label, x), from_none], self.label
            )
        if self.latitude is not None:
            result["latitude"] = from_none(self.latitude)
        if self.longitude is not None:
            result["longitude"] = from_none(self.longitude)
        if self.mail_demandeur is not None:
            result["mail_demandeur"] = from_union(
                [from_none, from_str], self.mail_demandeur
            )
        if self.mail_structure is not None:
            result["mail_structure"] = from_union(
                [from_none, from_str], self.mail_structure
            )
        if self.nom_demandeur is not None:
            result["nom_demandeur"] = from_union(
                [from_none, from_str], self.nom_demandeur
            )
        if self.nom_salle is not None:
            result["nom_salle"] = from_union([from_str, from_none], self.nom_salle)
        if self.nom_structure is not None:
            result["nom_structure"] = from_union(
                [from_none, from_str], self.nom_structure
            )
        if self.nombre_personnes is not None:
            result["nombre_personnes"] = from_union(
                [from_none, from_str], self.nombre_personnes
            )
        if self.nombre_seances is not None:
            result["nombre_seances"] = from_union(
                [from_none, from_str], self.nombre_seances
            )
        if self.objectif is not None:
            result["objectif"] = from_union(
                [from_none, lambda x: to_enum(Objectif, x)], self.objectif
            )
        if self.prenom_demandeur is not None:
            result["prenom_demandeur"] = from_union(
                [from_none, from_str], self.prenom_demandeur
            )
        if self.public is not None:
            result["public"] = from_union([from_none, from_str], self.public)
        if self.telephone is not None:
            result["telephone"] = from_union([from_none, from_str], self.telephone)
        if self.ville_salle is not None:
            result["ville_salle"] = from_union([from_str, from_none], self.ville_salle)
        if self.cartographie is not None:
            result["cartographie"] = from_union(
                [lambda x: to_class(Cartographie, x), from_none], self.cartographie
            )
        if self.affiche is not None:
            result["affiche"] = from_union(
                [from_none, lambda x: to_class(Affiche, x)], self.affiche
            )
        if self.geo is not None:
            result["_geo"] = from_union(
                [lambda x: to_class(Geo, x), from_none], self.geo
            )
        if self.date_debut_timestamp is not None:
            result["date_debut_timestamp"] = from_union(
                [from_int, from_none], self.date_debut_timestamp
            )
        if self.date_fin_timestamp is not None:
            result["date_fin_timestamp"] = from_union(
                [from_int, from_none], self.date_fin_timestamp
            )
        if self.thumbnail is not None:
            result["thumbnail"] = from_union([from_none, from_str], self.thumbnail)
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return not query or (
            (self.lower_titre and query in self.lower_titre)
            or (self.lower_addresse and query in self.lower_addresse)
            or (self.lower_description and query in self.lower_description)
            or (self.lower_site_web and query in self.lower_site_web)
            or (self.lower_action and query in self.lower_action)
            or (self.lower_adresse_salle and query in self.lower_adresse_salle)
            or (self.lower_adresse_structure and query in self.lower_adresse_structure)
            or (self.lower_nom_salle and query in self.lower_nom_salle)
            or (self.lower_nom_structure and query in self.lower_nom_structure)
            or (self.lower_ville_salle and query in self.lower_ville_salle)
        )
