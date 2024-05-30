from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional
from uuid import UUID

from ffbb_api_client_v2.Cartographie import Cartographie
from ffbb_api_client_v2.Commune import Commune
from ffbb_api_client_v2.converters import (
    from_datetime,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
    to_enum,
)
from ffbb_api_client_v2.DocumentFlyer import DocumentFlyer
from ffbb_api_client_v2.FacetStats import FacetStats
from ffbb_api_client_v2.Geo import Geo
from ffbb_api_client_v2.TournoiTypeClass import TournoiTypeClass
from ffbb_api_client_v2.TypeLeague import TypeLeague


@dataclass
class SexeClass:
    féminin: Optional[int] = None
    masculin: Optional[int] = None
    mixte: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "SexeClass":
        assert isinstance(obj, dict)
        féminin = from_union([from_int, from_none], obj.get("Féminin"))
        masculin = from_union([from_int, from_none], obj.get("Masculin"))
        mixte = from_union([from_int, from_none], obj.get("Mixte"))
        return SexeClass(féminin, masculin, mixte)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.féminin is not None:
            result["Féminin"] = from_union([from_int, from_none], self.féminin)
        if self.masculin is not None:
            result["Masculin"] = from_union([from_int, from_none], self.masculin)
        if self.mixte is not None:
            result["Mixte"] = from_union([from_int, from_none], self.mixte)
        return result


@dataclass
class TournoiTypes3X3Libelle:
    open_plus_junior_league_3_x3: Optional[int] = None
    open_plus_super_league_3_x3: Optional[int] = None
    open_plus_access_junior_league_3_x3: Optional[int] = None
    open_plus_access_super_league_3_x3: Optional[int] = None
    open_start_junior_league_3_x3: Optional[int] = None
    open_start_super_league_3_x3: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "TournoiTypes3X3Libelle":
        assert isinstance(obj, dict)
        open_plus_junior_league_3_x3 = from_union(
            [from_int, from_none], obj.get("Open Plus - Junior league 3x3")
        )
        open_plus_super_league_3_x3 = from_union(
            [from_int, from_none], obj.get("Open Plus - Super league 3x3")
        )
        open_plus_access_junior_league_3_x3 = from_union(
            [from_int, from_none], obj.get("Open Plus Access - Junior league 3x3")
        )
        open_plus_access_super_league_3_x3 = from_union(
            [from_int, from_none], obj.get("Open Plus Access - Super league 3x3")
        )
        open_start_junior_league_3_x3 = from_union(
            [from_int, from_none], obj.get("Open Start - Junior league 3x3")
        )
        open_start_super_league_3_x3 = from_union(
            [from_int, from_none], obj.get("Open Start - Super league 3x3")
        )
        return TournoiTypes3X3Libelle(
            open_plus_junior_league_3_x3,
            open_plus_super_league_3_x3,
            open_plus_access_junior_league_3_x3,
            open_plus_access_super_league_3_x3,
            open_start_junior_league_3_x3,
            open_start_super_league_3_x3,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.open_plus_junior_league_3_x3 is not None:
            result["Open Plus - Junior league 3x3"] = from_union(
                [from_int, from_none], self.open_plus_junior_league_3_x3
            )
        if self.open_plus_super_league_3_x3 is not None:
            result["Open Plus - Super league 3x3"] = from_union(
                [from_int, from_none], self.open_plus_super_league_3_x3
            )
        if self.open_plus_access_junior_league_3_x3 is not None:
            result["Open Plus Access - Junior league 3x3"] = from_union(
                [from_int, from_none], self.open_plus_access_junior_league_3_x3
            )
        if self.open_plus_access_super_league_3_x3 is not None:
            result["Open Plus Access - Super league 3x3"] = from_union(
                [from_int, from_none], self.open_plus_access_super_league_3_x3
            )
        if self.open_start_junior_league_3_x3 is not None:
            result["Open Start - Junior league 3x3"] = from_union(
                [from_int, from_none], self.open_start_junior_league_3_x3
            )
        if self.open_start_super_league_3_x3 is not None:
            result["Open Start - Super league 3x3"] = from_union(
                [from_int, from_none], self.open_start_super_league_3_x3
            )
        return result


@dataclass
class FacetDistribution:
    sexe: Optional[SexeClass] = None
    tournoi_type: Optional[TournoiTypeClass] = None
    tournoi_types3_x3_libelle: Optional[TournoiTypes3X3Libelle] = None

    @staticmethod
    def from_dict(obj: Any) -> "FacetDistribution":
        assert isinstance(obj, dict)
        sexe = from_union([SexeClass.from_dict, from_none], obj.get("sexe"))
        tournoi_type = from_union(
            [TournoiTypeClass.from_dict, from_none], obj.get("tournoiType")
        )
        tournoi_types3_x3_libelle = from_union(
            [TournoiTypes3X3Libelle.from_dict, from_none],
            obj.get("tournoiTypes3x3.libelle"),
        )
        return FacetDistribution(sexe, tournoi_type, tournoi_types3_x3_libelle)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.sexe is not None:
            result["sexe"] = from_union(
                [lambda x: to_class(SexeClass, x), from_none], self.sexe
            )
        if self.tournoi_type is not None:
            result["tournoiType"] = from_union(
                [lambda x: to_class(TournoiTypeClass, x), from_none], self.tournoi_type
            )
        if self.tournoi_types3_x3_libelle is not None:
            result["tournoiTypes3x3.libelle"] = from_union(
                [lambda x: to_class(TournoiTypes3X3Libelle, x), from_none],
                self.tournoi_types3_x3_libelle,
            )
        return result


class CategorieChampionnat3X3Libelle(Enum):
    U18 = "U18"


class Name(Enum):
    TOURNOIS = "Tournois"


class Source(Enum):
    FFBB_SERVEUR = "FFBB Serveur"


class Storage(Enum):
    MINIO = "minio"


class DocumentFlyerType(Enum):
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"


class SexeEnum(Enum):
    FÉMININ = "Féminin"
    MASCULIN = "Masculin"
    MIXTE = "Mixte"


class TournoiTypeEnum(Enum):
    OPEN_PLUS = "Open Plus"
    OPEN_PLUS_ACCESS = "Open Plus Access"
    OPEN_START = "Open Start"


class Libelle(Enum):
    OPEN_PLUS_ACCESS_JUNIOR_LEAGUE_3_X3 = "Open Plus Access - Junior league 3x3"
    OPEN_PLUS_ACCESS_SUPER_LEAGUE_3_X3 = "Open Plus Access - Super league 3x3"
    OPEN_PLUS_JUNIOR_LEAGUE_3_X3 = "Open Plus - Junior league 3x3"
    OPEN_PLUS_SUPER_LEAGUE_3_X3 = "Open Plus - Super league 3x3"
    OPEN_START_JUNIOR_LEAGUE_3_X3 = "Open Start - Junior league 3x3"
    OPEN_START_SUPER_LEAGUE_3_X3 = "Open Start - Super league 3x3"


@dataclass
class TournoiTypes3X3:
    libelle: Optional[Libelle] = None
    logo: Optional[UUID] = None
    type_league: Optional[TypeLeague] = None
    type_tournois: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "TournoiTypes3X3":
        assert isinstance(obj, dict)
        libelle = from_union([Libelle, from_none], obj.get("libelle"))
        logo = from_union([lambda x: UUID(x), from_none], obj.get("logo"))
        type_league = from_union([TypeLeague, from_none], obj.get("type_league"))
        type_tournois = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("type_tournois")
        )
        return TournoiTypes3X3(libelle, logo, type_league, type_tournois)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.libelle is not None:
            result["libelle"] = from_union(
                [lambda x: to_enum(Libelle, x), from_none], self.libelle
            )
        if self.logo is not None:
            result["logo"] = from_union([lambda x: str(x), from_none], self.logo)
        if self.type_league is not None:
            result["type_league"] = from_union(
                [lambda x: to_enum(TypeLeague, x), from_none], self.type_league
            )
        if self.type_tournois is not None:
            result["type_tournois"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.type_tournois,
            )
        return result


@dataclass
class Hit:
    nom: Optional[str] = None
    sexe: Optional[SexeEnum] = None
    adresse: Optional[str] = None
    nom_organisateur: Optional[str] = None
    description: Optional[str] = None
    site_choisi: Optional[str] = None
    id: Optional[int] = None
    code: Optional[str] = None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None
    age_max: Optional[int] = None
    age_min: Optional[int] = None
    categorie_championnat3_x3_id: Optional[int] = None
    categorie_championnat3_x3_libelle: Optional[CategorieChampionnat3X3Libelle] = None
    debut: Optional[datetime] = None
    fin: Optional[datetime] = None
    mail_organisateur: Optional[str] = None
    nb_participant_prevu: None
    tarif_organisateur: Optional[int] = None
    telephone_organisateur: Optional[str] = None
    url_organisateur: Optional[str] = None
    adresse_complement: None
    tournoi_types3_x3: Optional[List[TournoiTypes3X3]] = None
    cartographie: Optional[Cartographie] = None
    commune: Optional[Commune] = None
    document_flyer: Optional[DocumentFlyer] = None
    tournoi_type: Optional[TournoiTypeEnum] = None
    geo: Optional[Geo] = None
    debut_timestamp: Optional[int] = None
    fin_timestamp: Optional[int] = None
    thumbnail: None

    @staticmethod
    def from_dict(obj: Any) -> "Hit":
        assert isinstance(obj, dict)
        nom = from_union([from_str, from_none], obj.get("nom"))
        sexe = from_union([SexeEnum, from_none], obj.get("sexe"))
        adresse = from_union([from_str, from_none], obj.get("adresse"))
        nom_organisateur = from_union([from_none, from_str], obj.get("nomOrganisateur"))
        description = from_union([from_str, from_none], obj.get("description"))
        site_choisi = from_union([from_str, from_none], obj.get("siteChoisi"))
        id = from_union([from_none, lambda x: int(from_str(x))], obj.get("id"))
        code = from_union([from_str, from_none], obj.get("code"))
        date_created = from_union([from_datetime, from_none], obj.get("date_created"))
        date_updated = from_union([from_datetime, from_none], obj.get("date_updated"))
        age_max = from_union([from_int, from_none], obj.get("ageMax"))
        age_min = from_union([from_int, from_none], obj.get("ageMin"))
        categorie_championnat3_x3_id = from_union(
            [from_none, lambda x: int(from_str(x))],
            obj.get("categorieChampionnat3x3Id"),
        )
        categorie_championnat3_x3_libelle = from_union(
            [from_none, CategorieChampionnat3X3Libelle],
            obj.get("categorieChampionnat3x3Libelle"),
        )
        debut = from_union([from_datetime, from_none], obj.get("debut"))
        fin = from_union([from_datetime, from_none], obj.get("fin"))
        mail_organisateur = from_union(
            [from_none, from_str], obj.get("mailOrganisateur")
        )
        nb_participant_prevu = from_none(obj.get("nbParticipantPrevu"))
        tarif_organisateur = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("tarifOrganisateur")
        )
        telephone_organisateur = from_union(
            [from_str, from_none], obj.get("telephoneOrganisateur")
        )
        url_organisateur = from_union([from_none, from_str], obj.get("urlOrganisateur"))
        adresse_complement = from_none(obj.get("adresseComplement"))
        tournoi_types3_x3 = from_union(
            [lambda x: from_list(TournoiTypes3X3.from_dict, x), from_none],
            obj.get("tournoiTypes3x3"),
        )
        cartographie = from_union(
            [Cartographie.from_dict, from_none], obj.get("cartographie")
        )
        commune = from_union([Commune.from_dict, from_none], obj.get("commune"))
        document_flyer = from_union(
            [DocumentFlyer.from_dict, from_none], obj.get("document_flyer")
        )
        tournoi_type = from_union([TournoiTypeEnum, from_none], obj.get("tournoiType"))
        geo = from_union([Geo.from_dict, from_none], obj.get("_geo"))
        debut_timestamp = from_union([from_int, from_none], obj.get("debut_timestamp"))
        fin_timestamp = from_union([from_int, from_none], obj.get("fin_timestamp"))
        thumbnail = from_none(obj.get("thumbnail"))
        return Hit(
            nom,
            sexe,
            adresse,
            nom_organisateur,
            description,
            site_choisi,
            id,
            code,
            date_created,
            date_updated,
            age_max,
            age_min,
            categorie_championnat3_x3_id,
            categorie_championnat3_x3_libelle,
            debut,
            fin,
            mail_organisateur,
            nb_participant_prevu,
            tarif_organisateur,
            telephone_organisateur,
            url_organisateur,
            adresse_complement,
            tournoi_types3_x3,
            cartographie,
            commune,
            document_flyer,
            tournoi_type,
            geo,
            debut_timestamp,
            fin_timestamp,
            thumbnail,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.sexe is not None:
            result["sexe"] = from_union(
                [lambda x: to_enum(SexeEnum, x), from_none], self.sexe
            )
        if self.adresse is not None:
            result["adresse"] = from_union([from_str, from_none], self.adresse)
        if self.nom_organisateur is not None:
            result["nomOrganisateur"] = from_union(
                [from_none, from_str], self.nom_organisateur
            )
        if self.description is not None:
            result["description"] = from_union([from_str, from_none], self.description)
        if self.site_choisi is not None:
            result["siteChoisi"] = from_union([from_str, from_none], self.site_choisi)
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
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.date_created is not None:
            result["date_created"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_created
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_updated
            )
        if self.age_max is not None:
            result["ageMax"] = from_union([from_int, from_none], self.age_max)
        if self.age_min is not None:
            result["ageMin"] = from_union([from_int, from_none], self.age_min)
        if self.categorie_championnat3_x3_id is not None:
            result["categorieChampionnat3x3Id"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.categorie_championnat3_x3_id,
            )
        if self.categorie_championnat3_x3_libelle is not None:
            result["categorieChampionnat3x3Libelle"] = from_union(
                [from_none, lambda x: to_enum(CategorieChampionnat3X3Libelle, x)],
                self.categorie_championnat3_x3_libelle,
            )
        if self.debut is not None:
            result["debut"] = from_union(
                [lambda x: x.isoformat(), from_none], self.debut
            )
        if self.fin is not None:
            result["fin"] = from_union([lambda x: x.isoformat(), from_none], self.fin)
        if self.mail_organisateur is not None:
            result["mailOrganisateur"] = from_union(
                [from_none, from_str], self.mail_organisateur
            )
        if self.nb_participant_prevu is not None:
            result["nbParticipantPrevu"] = from_none(self.nb_participant_prevu)
        if self.tarif_organisateur is not None:
            result["tarifOrganisateur"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.tarif_organisateur,
            )
        if self.telephone_organisateur is not None:
            result["telephoneOrganisateur"] = from_union(
                [from_str, from_none], self.telephone_organisateur
            )
        if self.url_organisateur is not None:
            result["urlOrganisateur"] = from_union(
                [from_none, from_str], self.url_organisateur
            )
        if self.adresse_complement is not None:
            result["adresseComplement"] = from_none(self.adresse_complement)
        if self.tournoi_types3_x3 is not None:
            result["tournoiTypes3x3"] = from_union(
                [
                    lambda x: from_list(lambda x: to_class(TournoiTypes3X3, x), x),
                    from_none,
                ],
                self.tournoi_types3_x3,
            )
        if self.cartographie is not None:
            result["cartographie"] = from_union(
                [lambda x: to_class(Cartographie, x), from_none], self.cartographie
            )
        if self.commune is not None:
            result["commune"] = from_union(
                [lambda x: to_class(Commune, x), from_none], self.commune
            )
        if self.document_flyer is not None:
            result["document_flyer"] = from_union(
                [lambda x: to_class(DocumentFlyer, x), from_none], self.document_flyer
            )
        if self.tournoi_type is not None:
            result["tournoiType"] = from_union(
                [lambda x: to_enum(TournoiTypeEnum, x), from_none], self.tournoi_type
            )
        if self.geo is not None:
            result["_geo"] = from_union(
                [lambda x: to_class(Geo, x), from_none], self.geo
            )
        if self.debut_timestamp is not None:
            result["debut_timestamp"] = from_union(
                [from_int, from_none], self.debut_timestamp
            )
        if self.fin_timestamp is not None:
            result["fin_timestamp"] = from_union(
                [from_int, from_none], self.fin_timestamp
            )
        if self.thumbnail is not None:
            result["thumbnail"] = from_none(self.thumbnail)
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
