from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ...meilisearch.models.hit import Hit
from ...models.cartographie import Cartographie
from ...models.commune import Commune
from ...models.document_flyer import DocumentFlyer
from ...models.geo import Geo
from ...models.terrains_categorie_championnat_3x3_libelle import (
    CategorieChampionnat3X3Libelle,
)
from ...models.tournoi_type_enum import TournoiTypeEnum
from ...models.tournoi_types_3x3 import TournoiTypes3X3
from ...utils.converter_utils import (
    from_datetime,
    from_enum,
    from_int,
    from_list,
    from_obj,
    from_str,
)
from .terrains_sexe_enum import SexeEnum


@dataclass
class TournoisHit(Hit):
    nom: str | None = None
    sexe: SexeEnum | None = None
    adresse: str | None = None
    nom_organisateur: str | None = None
    description: str | None = None
    site_choisi: str | None = None
    id: int | None = None
    code: str | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    age_max: int | None = None
    age_min: int | None = None
    categorie_championnat3_x3_id: int | None = None
    categorie_championnat3_x3_libelle: CategorieChampionnat3X3Libelle | None = None
    debut: datetime | None = None
    fin: datetime | None = None
    mail_organisateur: str | None = None
    nb_participant_prevu: int | None = None
    tarif_organisateur: int | None = None
    telephone_organisateur: str | None = None
    url_organisateur: str | None = None
    adresse_complement: str | None = None
    tournoi_types3_x3: list[TournoiTypes3X3] | None = None
    cartographie: Cartographie | None = None
    commune: Commune | None = None
    document_flyer: DocumentFlyer | None = None
    tournoi_type: TournoiTypeEnum | None = None
    geo: Geo | None = None
    debut_timestamp: int | None = None
    fin_timestamp: int | None = None
    thumbnail: str | None = None
    lower_nom: str | None = field(init=False, default=None, repr=False)
    lower_addresse: str | None = field(init=False, default=None, repr=False)
    lower_nom_organisateur: str | None = field(init=False, default=None, repr=False)
    lower_description: str | None = field(init=False, default=None, repr=False)
    lower_site_choisi: str | None = field(init=False, default=None, repr=False)
    lower_code: str | None = field(init=False, default=None, repr=False)

    def __post_init__(self) -> None:
        self.lower_nom = self.nom.lower() if self.nom else None
        self.lower_addresse = self.adresse.lower() if self.adresse else None
        self.lower_nom_organisateur = (
            self.nom_organisateur.lower() if self.nom_organisateur else None
        )
        self.lower_description = self.description.lower() if self.description else None
        self.lower_site_choisi = self.site_choisi.lower() if self.site_choisi else None
        self.lower_code = self.code.lower() if self.code else None

    @staticmethod
    def from_dict(obj: Any) -> TournoisHit:
        assert isinstance(obj, dict)
        nom = from_str(obj, "nom")
        sexe = from_enum(SexeEnum, obj, "sexe")
        adresse = from_str(obj, "adresse")
        nom_organisateur = from_str(obj, "nomOrganisateur")
        description = from_str(obj, "description")
        site_choisi = from_str(obj, "siteChoisi")
        id = from_int(obj, "id")
        code = from_str(obj, "code")
        date_created = from_datetime(obj, "date_created")
        date_updated = from_datetime(obj, "date_updated")
        age_max = from_int(obj, "ageMax")
        age_min = from_int(obj, "ageMin")
        categorie_championnat3_x3_id = from_int(obj, "categorieChampionnat3x3Id")
        categorie_championnat3_x3_libelle = from_enum(
            CategorieChampionnat3X3Libelle, obj, "categorieChampionnat3x3Libelle"
        )
        debut = from_datetime(obj, "debut")
        fin = from_datetime(obj, "fin")
        mail_organisateur = from_str(obj, "mailOrganisateur")
        nb_participant_prevu = from_int(obj, "nbParticipantPrevu")
        tarif_organisateur = from_int(obj, "tarifOrganisateur")
        telephone_organisateur = from_str(obj, "telephoneOrganisateur")
        url_organisateur = from_str(obj, "urlOrganisateur")
        adresse_complement = from_str(obj, "adresseComplement")
        tournoi_types3_x3 = from_list(TournoiTypes3X3.from_dict, obj, "tournoiTypes3x3")
        cartographie = from_obj(Cartographie.from_dict, obj, "cartographie")
        commune = from_obj(Commune.from_dict, obj, "commune")
        document_flyer = from_obj(DocumentFlyer.from_dict, obj, "document_flyer")
        tournoi_type = from_enum(TournoiTypeEnum, obj, "tournoiType")
        geo = from_obj(Geo.from_dict, obj, "_geo")
        debut_timestamp = from_int(obj, "debut_timestamp")
        fin_timestamp = from_int(obj, "fin_timestamp")
        thumbnail = from_str(obj, "thumbnail")
        return TournoisHit(
            nom=nom,
            sexe=sexe,
            adresse=adresse,
            nom_organisateur=nom_organisateur,
            description=description,
            site_choisi=site_choisi,
            id=id,
            code=code,
            date_created=date_created,
            date_updated=date_updated,
            age_max=age_max,
            age_min=age_min,
            categorie_championnat3_x3_id=categorie_championnat3_x3_id,
            categorie_championnat3_x3_libelle=categorie_championnat3_x3_libelle,
            debut=debut,
            fin=fin,
            mail_organisateur=mail_organisateur,
            nb_participant_prevu=nb_participant_prevu,
            tarif_organisateur=tarif_organisateur,
            telephone_organisateur=telephone_organisateur,
            url_organisateur=url_organisateur,
            adresse_complement=adresse_complement,
            tournoi_types3_x3=tournoi_types3_x3,
            cartographie=cartographie,
            commune=commune,
            document_flyer=document_flyer,
            tournoi_type=tournoi_type,
            geo=geo,
            debut_timestamp=debut_timestamp,
            fin_timestamp=fin_timestamp,
            thumbnail=thumbnail,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom is not None:
            result["nom"] = self.nom
        if self.sexe is not None:
            result["sexe"] = self.sexe.value
        if self.adresse is not None:
            result["adresse"] = self.adresse
        if self.nom_organisateur is not None:
            result["nomOrganisateur"] = self.nom_organisateur
        if self.description is not None:
            result["description"] = self.description
        if self.site_choisi is not None:
            result["siteChoisi"] = self.site_choisi
        if self.id is not None:
            result["id"] = str(self.id)
        if self.code is not None:
            result["code"] = self.code
        if self.date_created is not None:
            result["date_created"] = self.date_created.isoformat()
        if self.date_updated is not None:
            result["date_updated"] = self.date_updated.isoformat()
        if self.age_max is not None:
            result["ageMax"] = self.age_max
        if self.age_min is not None:
            result["ageMin"] = self.age_min
        if self.categorie_championnat3_x3_id is not None:
            result["categorieChampionnat3x3Id"] = str(self.categorie_championnat3_x3_id)
        if self.categorie_championnat3_x3_libelle is not None:
            result["categorieChampionnat3x3Libelle"] = (
                self.categorie_championnat3_x3_libelle.value
            )
        if self.debut is not None:
            result["debut"] = self.debut.isoformat()
        if self.fin is not None:
            result["fin"] = self.fin.isoformat()
        if self.mail_organisateur is not None:
            result["mailOrganisateur"] = self.mail_organisateur
        if self.nb_participant_prevu is not None:
            result["nbParticipantPrevu"] = str(self.nb_participant_prevu)
        if self.tarif_organisateur is not None:
            result["tarifOrganisateur"] = str(self.tarif_organisateur)
        if self.telephone_organisateur is not None:
            result["telephoneOrganisateur"] = self.telephone_organisateur
        if self.url_organisateur is not None:
            result["urlOrganisateur"] = self.url_organisateur
        if self.adresse_complement is not None:
            result["adresseComplement"] = self.adresse_complement
        if self.tournoi_types3_x3 is not None:
            result["tournoiTypes3x3"] = [t.to_dict() for t in self.tournoi_types3_x3]
        if self.cartographie is not None:
            result["cartographie"] = self.cartographie.to_dict()
        if self.commune is not None:
            result["commune"] = self.commune.to_dict()
        if self.document_flyer is not None:
            result["document_flyer"] = self.document_flyer.to_dict()
        if self.tournoi_type is not None:
            result["tournoiType"] = self.tournoi_type.value
        if self.geo is not None:
            result["_geo"] = self.geo.to_dict()
        if self.debut_timestamp is not None:
            result["debut_timestamp"] = self.debut_timestamp
        if self.fin_timestamp is not None:
            result["fin_timestamp"] = self.fin_timestamp
        if self.thumbnail is not None:
            result["thumbnail"] = self.thumbnail
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return bool(
            not query
            or (self.lower_nom and query in self.lower_nom)
            or (self.lower_addresse and query in self.lower_addresse)
            or (self.lower_description and query in self.lower_description)
            or (self.lower_code and query in self.lower_code)
            or (self.lower_nom_organisateur and query in self.lower_nom_organisateur)
            or (self.lower_site_choisi and query in self.lower_site_choisi)
        )
