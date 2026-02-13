from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ...meilisearch.models.hit import Hit
from ...models.affiche import Affiche
from ...models.cartographie import Cartographie
from ...models.geo import Geo
from ...models.jour import Jour
from ...models.label import Label
from ...models.objectif import Objectif
from ...models.pratiques_hit_type import HitType
from ...utils.converter_utils import (
    from_datetime,
    from_enum,
    from_float,
    from_int,
    from_list,
    from_obj,
    from_str,
)


@dataclass
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
    facebook: str | None = None
    site_web: str | None = None
    twitter: str | None = None
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
    latitude: float | None = None
    longitude: float | None = None
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
    lower_titre: str | None = field(init=False, default=None, repr=False)
    lower_addresse: str | None = field(init=False, default=None, repr=False)
    lower_description: str | None = field(init=False, default=None, repr=False)
    lower_site_web: str | None = field(init=False, default=None, repr=False)
    lower_action: str | None = field(init=False, default=None, repr=False)
    lower_adresse_salle: str | None = field(init=False, default=None, repr=False)
    lower_adresse_structure: str | None = field(init=False, default=None, repr=False)
    lower_nom_salle: str | None = field(init=False, default=None, repr=False)
    lower_nom_structure: str | None = field(init=False, default=None, repr=False)
    lower_ville_salle: str | None = field(init=False, default=None, repr=False)

    def __post_init__(self) -> None:
        self.lower_titre = self.titre.lower() if self.titre else None
        self.lower_addresse = self.adresse.lower() if self.adresse else None
        self.lower_description = self.description.lower() if self.description else None
        self.lower_site_web = self.site_web.lower() if self.site_web else None
        self.lower_action = self.action.lower() if self.action else None
        self.lower_adresse_salle = (
            self.adresse_salle.lower() if self.adresse_salle else None
        )
        self.lower_adresse_structure = (
            self.adresse_structure.lower() if self.adresse_structure else None
        )
        self.lower_nom_salle = self.nom_salle.lower() if self.nom_salle else None
        self.lower_nom_structure = (
            self.nom_structure.lower() if self.nom_structure else None
        )
        self.lower_ville_salle = self.ville_salle.lower() if self.ville_salle else None

    @staticmethod
    def from_dict(obj: Any) -> PratiquesHit:
        assert isinstance(obj, dict)
        titre = from_str(obj, "titre")
        type = from_enum(HitType, obj, "type")
        adresse = from_str(obj, "adresse")
        description = from_str(obj, "description")
        id = from_int(obj, "id")
        date_created = from_datetime(obj, "date_created")
        date_debut = from_datetime(obj, "date_debut")
        date_demande = from_int(obj, "date_demande")
        date_fin = from_datetime(obj, "date_fin")
        date_updated = from_datetime(obj, "date_updated")
        facebook = from_str(obj, "facebook")
        site_web = from_str(obj, "site_web")
        twitter = from_str(obj, "twitter")
        action = from_str(obj, "action")
        adresse_salle = from_str(obj, "adresse_salle")
        adresse_structure = from_str(obj, "adresse_structure")
        assurance = from_str(obj, "assurance")
        code = from_str(obj, "code")
        cp_salle = from_str(obj, "cp_salle")
        date_inscription = from_int(obj, "date_inscription")
        email = from_str(obj, "email")
        engagement = from_str(obj, "engagement")
        horaires_seances = from_str(obj, "horaires_seances")
        inscriptions = from_str(obj, "inscriptions")
        jours = from_list(Jour, obj, "jours")
        label = from_enum(Label, obj, "label")
        latitude = from_float(obj, "latitude")
        longitude = from_float(obj, "longitude")
        mail_demandeur = from_str(obj, "mail_demandeur")
        mail_structure = from_str(obj, "mail_structure")
        nom_demandeur = from_str(obj, "nom_demandeur")
        nom_salle = from_str(obj, "nom_salle")
        nom_structure = from_str(obj, "nom_structure")
        nombre_personnes = from_str(obj, "nombre_personnes")
        nombre_seances = from_str(obj, "nombre_seances")
        objectif = from_enum(Objectif, obj, "objectif")
        prenom_demandeur = from_str(obj, "prenom_demandeur")
        public = from_str(obj, "public")
        telephone = from_str(obj, "telephone")
        ville_salle = from_str(obj, "ville_salle")
        cartographie = from_obj(Cartographie.from_dict, obj, "cartographie")
        affiche = from_obj(Affiche.from_dict, obj, "affiche")
        geo = from_obj(Geo.from_dict, obj, "_geo")
        date_debut_timestamp = from_int(obj, "date_debut_timestamp")
        date_fin_timestamp = from_int(obj, "date_fin_timestamp")
        thumbnail = from_str(obj, "thumbnail")
        return PratiquesHit(
            titre=titre,
            type=type,
            adresse=adresse,
            description=description,
            id=id,
            date_created=date_created,
            date_debut=date_debut,
            date_demande=date_demande,
            date_fin=date_fin,
            date_updated=date_updated,
            facebook=facebook,
            site_web=site_web,
            twitter=twitter,
            action=action,
            adresse_salle=adresse_salle,
            adresse_structure=adresse_structure,
            assurance=assurance,
            code=code,
            cp_salle=cp_salle,
            date_inscription=date_inscription,
            email=email,
            engagement=engagement,
            horaires_seances=horaires_seances,
            inscriptions=inscriptions,
            jours=jours,
            label=label,
            latitude=latitude,
            longitude=longitude,
            mail_demandeur=mail_demandeur,
            mail_structure=mail_structure,
            nom_demandeur=nom_demandeur,
            nom_salle=nom_salle,
            nom_structure=nom_structure,
            nombre_personnes=nombre_personnes,
            nombre_seances=nombre_seances,
            objectif=objectif,
            prenom_demandeur=prenom_demandeur,
            public=public,
            telephone=telephone,
            ville_salle=ville_salle,
            cartographie=cartographie,
            affiche=affiche,
            geo=geo,
            date_debut_timestamp=date_debut_timestamp,
            date_fin_timestamp=date_fin_timestamp,
            thumbnail=thumbnail,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.titre is not None:
            result["titre"] = self.titre
        if self.type is not None:
            result["type"] = self.type.value
        if self.adresse is not None:
            result["adresse"] = self.adresse
        if self.description is not None:
            result["description"] = self.description
        if self.id is not None:
            result["id"] = str(self.id)
        if self.date_created is not None:
            result["date_created"] = self.date_created.isoformat()
        if self.date_debut is not None:
            result["date_debut"] = self.date_debut.isoformat()
        if self.date_demande is not None:
            result["date_demande"] = str(self.date_demande)
        if self.date_fin is not None:
            result["date_fin"] = self.date_fin.isoformat()
        if self.date_updated is not None:
            result["date_updated"] = self.date_updated.isoformat()
        if self.facebook is not None:
            result["facebook"] = self.facebook
        if self.site_web is not None:
            result["site_web"] = self.site_web
        if self.twitter is not None:
            result["twitter"] = self.twitter
        if self.action is not None:
            result["action"] = self.action
        if self.adresse_salle is not None:
            result["adresse_salle"] = self.adresse_salle
        if self.adresse_structure is not None:
            result["adresse_structure"] = self.adresse_structure
        if self.assurance is not None:
            result["assurance"] = self.assurance
        if self.code is not None:
            result["code"] = self.code
        if self.cp_salle is not None:
            result["cp_salle"] = self.cp_salle
        if self.date_inscription is not None:
            result["date_inscription"] = str(self.date_inscription)
        if self.email is not None:
            result["email"] = self.email
        if self.engagement is not None:
            result["engagement"] = self.engagement
        if self.horaires_seances is not None:
            result["horaires_seances"] = self.horaires_seances
        if self.inscriptions is not None:
            result["inscriptions"] = self.inscriptions
        if self.jours is not None:
            result["jours"] = [j.value for j in self.jours]
        if self.label is not None:
            result["label"] = self.label.value
        if self.latitude is not None:
            result["latitude"] = self.latitude
        if self.longitude is not None:
            result["longitude"] = self.longitude
        if self.mail_demandeur is not None:
            result["mail_demandeur"] = self.mail_demandeur
        if self.mail_structure is not None:
            result["mail_structure"] = self.mail_structure
        if self.nom_demandeur is not None:
            result["nom_demandeur"] = self.nom_demandeur
        if self.nom_salle is not None:
            result["nom_salle"] = self.nom_salle
        if self.nom_structure is not None:
            result["nom_structure"] = self.nom_structure
        if self.nombre_personnes is not None:
            result["nombre_personnes"] = self.nombre_personnes
        if self.nombre_seances is not None:
            result["nombre_seances"] = self.nombre_seances
        if self.objectif is not None:
            result["objectif"] = self.objectif.value
        if self.prenom_demandeur is not None:
            result["prenom_demandeur"] = self.prenom_demandeur
        if self.public is not None:
            result["public"] = self.public
        if self.telephone is not None:
            result["telephone"] = self.telephone
        if self.ville_salle is not None:
            result["ville_salle"] = self.ville_salle
        if self.cartographie is not None:
            result["cartographie"] = self.cartographie.to_dict()
        if self.affiche is not None:
            result["affiche"] = self.affiche.to_dict()
        if self.geo is not None:
            result["_geo"] = self.geo.to_dict()
        if self.date_debut_timestamp is not None:
            result["date_debut_timestamp"] = self.date_debut_timestamp
        if self.date_fin_timestamp is not None:
            result["date_fin_timestamp"] = self.date_fin_timestamp
        if self.thumbnail is not None:
            result["thumbnail"] = self.thumbnail
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return bool(
            not query
            or (self.lower_titre and query in self.lower_titre)
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
