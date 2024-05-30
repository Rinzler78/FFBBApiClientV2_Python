from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from ffbb_api_client_v2.Affiche import Affiche
from ffbb_api_client_v2.Cartographie import Cartographie
from ffbb_api_client_v2.converters import (
    from_datetime,
    from_dict,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
    to_enum,
)
from ffbb_api_client_v2.FacetStats import FacetStats
from ffbb_api_client_v2.Geo import Geo
from ffbb_api_client_v2.Jour import Jour
from ffbb_api_client_v2.Label import Label
from ffbb_api_client_v2.Objectif import Objectif
from ffbb_api_client_v2.TypeClass import TypeClass


@dataclass
class FacetDistribution:
    label: Optional[Dict[str, int]] = None
    type: Optional[TypeClass] = None

    @staticmethod
    def from_dict(obj: Any) -> "FacetDistribution":
        assert isinstance(obj, dict)
        label = from_union(
            [lambda x: from_dict(from_int, x), from_none], obj.get("label")
        )
        type = from_union([TypeClass.from_dict, from_none], obj.get("type"))
        return FacetDistribution(label, type)

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


class HitType(Enum):
    BASKET_INCLUSIF = "Basket Inclusif"
    BASKET_SANTÉ = "Basket Santé"
    BASKET_TONIK = "Basket Tonik"
    CENTRE_GÉNÉRATION_BASKET = "Centre Génération Basket"
    MICRO_BASKET = "Micro Basket"


@dataclass
class Hit:
    titre: Optional[str] = None
    type: Optional[HitType] = None
    adresse: Optional[str] = None
    description: Optional[str] = None
    id: Optional[int] = None
    date_created: Optional[datetime] = None
    date_debut: Optional[datetime] = None
    date_demande: Optional[int] = None
    date_fin: Optional[datetime] = None
    date_updated: Optional[datetime] = None
    facebook: None
    site_web: Optional[str] = None
    twitter: None
    action: Optional[str] = None
    adresse_salle: Optional[str] = None
    adresse_structure: Optional[str] = None
    assurance: Optional[str] = None
    code: Optional[str] = None
    cp_salle: Optional[str] = None
    date_inscription: Optional[int] = None
    email: Optional[str] = None
    engagement: Optional[str] = None
    horaires_seances: Optional[str] = None
    inscriptions: Optional[str] = None
    jours: Optional[List[Jour]] = None
    label: Optional[Label] = None
    latitude: None
    longitude: None
    mail_demandeur: Optional[str] = None
    mail_structure: Optional[str] = None
    nom_demandeur: Optional[str] = None
    nom_salle: Optional[str] = None
    nom_structure: Optional[str] = None
    nombre_personnes: Optional[str] = None
    nombre_seances: Optional[str] = None
    objectif: Optional[Objectif] = None
    prenom_demandeur: Optional[str] = None
    public: Optional[str] = None
    telephone: Optional[str] = None
    ville_salle: Optional[str] = None
    cartographie: Optional[Cartographie] = None
    affiche: Optional[Affiche] = None
    geo: Optional[Geo] = None
    date_debut_timestamp: Optional[int] = None
    date_fin_timestamp: Optional[int] = None
    thumbnail: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Hit":
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
        return Hit(
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


@dataclass
class Result:
    index_uid: Optional[str] = None
    hits: Optional[List[Hit]] = None
    query: Optional[str] = None
    processing_time_ms: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    estimated_total_hits: Optional[int] = None
    facet_distribution: Optional[FacetDistribution] = None
    facet_stats: Optional[FacetStats] = None

    @staticmethod
    def from_dict(obj: Any) -> "Result":
        assert isinstance(obj, dict)
        index_uid = from_union([from_str, from_none], obj.get("indexUid"))
        hits = from_union(
            [lambda x: from_list(Hit.from_dict, x), from_none], obj.get("hits")
        )
        query = from_union([from_str, from_none], obj.get("query"))
        processing_time_ms = from_union(
            [from_int, from_none], obj.get("processingTimeMs")
        )
        limit = from_union([from_int, from_none], obj.get("limit"))
        offset = from_union([from_int, from_none], obj.get("offset"))
        estimated_total_hits = from_union(
            [from_int, from_none], obj.get("estimatedTotalHits")
        )
        facet_distribution = from_union(
            [FacetDistribution.from_dict, from_none], obj.get("facetDistribution")
        )
        facet_stats = from_union(
            [FacetStats.from_dict, from_none], obj.get("facetStats")
        )
        return Result(
            index_uid,
            hits,
            query,
            processing_time_ms,
            limit,
            offset,
            estimated_total_hits,
            facet_distribution,
            facet_stats,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.index_uid is not None:
            result["indexUid"] = from_union([from_str, from_none], self.index_uid)
        if self.hits is not None:
            result["hits"] = from_union(
                [lambda x: from_list(lambda x: to_class(Hit, x), x), from_none],
                self.hits,
            )
        if self.query is not None:
            result["query"] = from_union([from_str, from_none], self.query)
        if self.processing_time_ms is not None:
            result["processingTimeMs"] = from_union(
                [from_int, from_none], self.processing_time_ms
            )
        if self.limit is not None:
            result["limit"] = from_union([from_int, from_none], self.limit)
        if self.offset is not None:
            result["offset"] = from_union([from_int, from_none], self.offset)
        if self.estimated_total_hits is not None:
            result["estimatedTotalHits"] = from_union(
                [from_int, from_none], self.estimated_total_hits
            )
        if self.facet_distribution is not None:
            result["facetDistribution"] = from_union(
                [lambda x: to_class(FacetDistribution, x), from_none],
                self.facet_distribution,
            )
        if self.facet_stats is not None:
            result["facetStats"] = from_union(
                [lambda x: to_class(FacetStats, x), from_none], self.facet_stats
            )
        return result


@dataclass
class MultiSearchResults:
    results: Optional[List[Result]] = None

    @staticmethod
    def from_dict(obj: Any) -> "MultiSearchResults":
        assert isinstance(obj, dict)
        results = from_union(
            [lambda x: from_list(Result.from_dict, x), from_none], obj.get("results")
        )
        return MultiSearchResults(results)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.results is not None:
            result["results"] = from_union(
                [lambda x: from_list(lambda x: to_class(Result, x), x), from_none],
                self.results,
            )
        return result


def multi_search_results_from_dict(s: Any) -> MultiSearchResults:
    return MultiSearchResults.from_dict(s)


def multi_search_results_to_dict(x: MultiSearchResults) -> Any:
    return to_class(MultiSearchResults, x)
