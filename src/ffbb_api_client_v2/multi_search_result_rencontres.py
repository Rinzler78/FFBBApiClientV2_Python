from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from ffbb_api_client_v2.Categorie import Categorie
from ffbb_api_client_v2.converters import (
    from_bool,
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
from ffbb_api_client_v2.Etat import Etat
from ffbb_api_client_v2.Logo import Logo
from ffbb_api_client_v2.Niveau import Niveau
from ffbb_api_client_v2.Organisateur import Organisateur
from ffbb_api_client_v2.PublicationInternet import PublicationInternet
from ffbb_api_client_v2.Saison import Saison
from ffbb_api_client_v2.Sexe import Sexe
from ffbb_api_client_v2.TypeCompetition import TypeCompetition
from ffbb_api_client_v2.TypeCompetitionGenerique import TypeCompetitionGenerique


class LibelleEnum(Enum):
    SE = "SE"
    SENIORS = "Seniors"
    U11 = "U11"
    U13 = "U13"
    U15 = "U15"
    U17 = "U17"
    U18 = "U18"
    U20 = "U20"
    U7 = "U7"
    U9 = "U9"
    VE = "VE"
    VÉTÉRANS = "Vétérans"


class PhaseCode(Enum):
    B1 = "B1"
    B2 = "B2"
    F = "F"
    J1 = "J1"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    T1 = "T1"
    T2 = "T2"
    THE_116 = "1/16"
    THE_12 = "1/2"
    THE_132 = "1/32"
    THE_14 = "1/4"
    THE_164 = "1/64"
    THE_18 = "1/8"
    TP = "TP"


@dataclass
class Engagement:
    id: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Engagement":
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        return Engagement(id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        return result


@dataclass
class Poule:
    nom: Optional[str] = None
    id: Optional[str] = None
    engagements: Optional[List[Engagement]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Poule":
        assert isinstance(obj, dict)
        nom = from_union([from_str, from_none], obj.get("nom"))
        id = from_union([from_str, from_none], obj.get("id"))
        engagements = from_union(
            [lambda x: from_list(Engagement.from_dict, x), from_none],
            obj.get("engagements"),
        )
        return Poule(nom, id, engagements)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.engagements is not None:
            result["engagements"] = from_union(
                [lambda x: from_list(lambda x: to_class(Engagement, x), x), from_none],
                self.engagements,
            )
        return result


@dataclass
class Hit:
    nom: Optional[str] = None
    code: Optional[str] = None
    niveau: Optional[Niveau] = None
    type_competition: Optional[TypeCompetition] = None
    sexe: Optional[Sexe] = None
    id: Optional[str] = None
    creation_en_cours: Optional[bool] = None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None
    emarque_v2: Optional[bool] = None
    live_stat: Optional[bool] = None
    publication_internet: Optional[PublicationInternet] = None
    pro: Optional[bool] = None
    competition_origine: Optional[str] = None
    competition_origine_niveau: Optional[int] = None
    phase_code: Optional[PhaseCode] = None
    competition_origine_nom: Optional[str] = None
    etat: Optional[Etat] = None
    poules: Optional[List[Poule]] = None
    phases: Optional[List[str]] = None
    categorie: Optional[Categorie] = None
    id_competition_pere: None
    organisateur: Optional[Organisateur] = None
    saison: Optional[Saison] = None
    logo: Optional[Logo] = None
    type_competition_generique: Optional[TypeCompetitionGenerique] = None
    thumbnail: Optional[str] = None
    niveau_nb: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Hit":
        assert isinstance(obj, dict)
        nom = from_union([from_str, from_none], obj.get("nom"))
        code = from_union([from_str, from_none], obj.get("code"))
        niveau = from_union([Niveau, from_none], obj.get("niveau"))
        type_competition = from_union(
            [TypeCompetition, from_none], obj.get("typeCompetition")
        )
        sexe = from_union([Sexe, from_none], obj.get("sexe"))
        id = from_union([from_str, from_none], obj.get("id"))
        creation_en_cours = from_union(
            [from_bool, from_none], obj.get("creationEnCours")
        )
        date_created = from_union([from_datetime, from_none], obj.get("date_created"))
        date_updated = from_union([from_datetime, from_none], obj.get("date_updated"))
        emarque_v2 = from_union([from_bool, from_none], obj.get("emarqueV2"))
        live_stat = from_union([from_bool, from_none], obj.get("liveStat"))
        publication_internet = from_union(
            [PublicationInternet, from_none], obj.get("publicationInternet")
        )
        pro = from_union([from_bool, from_none], obj.get("pro"))
        competition_origine = from_union(
            [from_str, from_none], obj.get("competition_origine")
        )
        competition_origine_niveau = from_union(
            [from_int, from_none], obj.get("competition_origine_niveau")
        )
        phase_code = from_union([PhaseCode, from_none], obj.get("phase_code"))
        competition_origine_nom = from_union(
            [from_str, from_none], obj.get("competition_origine_nom")
        )
        etat = from_union([Etat, from_none], obj.get("etat"))
        poules = from_union(
            [lambda x: from_list(Poule.from_dict, x), from_none], obj.get("poules")
        )
        phases = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("phases")
        )
        categorie = from_union([Categorie.from_dict, from_none], obj.get("categorie"))
        id_competition_pere = from_none(obj.get("idCompetitionPere"))
        organisateur = from_union(
            [Organisateur.from_dict, from_none], obj.get("organisateur")
        )
        saison = from_union([Saison.from_dict, from_none], obj.get("saison"))
        logo = from_union([Logo.from_dict, from_none], obj.get("logo"))
        type_competition_generique = from_union(
            [TypeCompetitionGenerique.from_dict, from_none],
            obj.get("typeCompetitionGenerique"),
        )
        thumbnail = from_union([from_none, from_str], obj.get("thumbnail"))
        niveau_nb = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("niveau_nb")
        )
        return Hit(
            nom,
            code,
            niveau,
            type_competition,
            sexe,
            id,
            creation_en_cours,
            date_created,
            date_updated,
            emarque_v2,
            live_stat,
            publication_internet,
            pro,
            competition_origine,
            competition_origine_niveau,
            phase_code,
            competition_origine_nom,
            etat,
            poules,
            phases,
            categorie,
            id_competition_pere,
            organisateur,
            saison,
            logo,
            type_competition_generique,
            thumbnail,
            niveau_nb,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.niveau is not None:
            result["niveau"] = from_union(
                [lambda x: to_enum(Niveau, x), from_none], self.niveau
            )
        if self.type_competition is not None:
            result["typeCompetition"] = from_union(
                [lambda x: to_enum(TypeCompetition, x), from_none],
                self.type_competition,
            )
        if self.sexe is not None:
            result["sexe"] = from_union(
                [lambda x: to_enum(Sexe, x), from_none], self.sexe
            )
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.creation_en_cours is not None:
            result["creationEnCours"] = from_union(
                [from_bool, from_none], self.creation_en_cours
            )
        if self.date_created is not None:
            result["date_created"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_created
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_updated
            )
        if self.emarque_v2 is not None:
            result["emarqueV2"] = from_union([from_bool, from_none], self.emarque_v2)
        if self.live_stat is not None:
            result["liveStat"] = from_union([from_bool, from_none], self.live_stat)
        if self.publication_internet is not None:
            result["publicationInternet"] = from_union(
                [lambda x: to_enum(PublicationInternet, x), from_none],
                self.publication_internet,
            )
        if self.pro is not None:
            result["pro"] = from_union([from_bool, from_none], self.pro)
        if self.competition_origine is not None:
            result["competition_origine"] = from_union(
                [from_str, from_none], self.competition_origine
            )
        if self.competition_origine_niveau is not None:
            result["competition_origine_niveau"] = from_union(
                [from_int, from_none], self.competition_origine_niveau
            )
        if self.phase_code is not None:
            result["phase_code"] = from_union(
                [lambda x: to_enum(PhaseCode, x), from_none], self.phase_code
            )
        if self.competition_origine_nom is not None:
            result["competition_origine_nom"] = from_union(
                [from_str, from_none], self.competition_origine_nom
            )
        if self.etat is not None:
            result["etat"] = from_union(
                [lambda x: to_enum(Etat, x), from_none], self.etat
            )
        if self.poules is not None:
            result["poules"] = from_union(
                [lambda x: from_list(lambda x: to_class(Poule, x), x), from_none],
                self.poules,
            )
        if self.phases is not None:
            result["phases"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.phases
            )
        if self.categorie is not None:
            result["categorie"] = from_union(
                [lambda x: to_class(Categorie, x), from_none], self.categorie
            )
        if self.id_competition_pere is not None:
            result["idCompetitionPere"] = from_none(self.id_competition_pere)
        if self.organisateur is not None:
            result["organisateur"] = from_union(
                [lambda x: to_class(Organisateur, x), from_none], self.organisateur
            )
        if self.saison is not None:
            result["saison"] = from_union(
                [lambda x: to_class(Saison, x), from_none], self.saison
            )
        if self.logo is not None:
            result["logo"] = from_union(
                [lambda x: to_class(Logo, x), from_none], self.logo
            )
        if self.type_competition_generique is not None:
            result["typeCompetitionGenerique"] = from_union(
                [lambda x: to_class(TypeCompetitionGenerique, x), from_none],
                self.type_competition_generique,
            )
        if self.thumbnail is not None:
            result["thumbnail"] = from_union([from_none, from_str], self.thumbnail)
        if self.niveau_nb is not None:
            result["niveau_nb"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.niveau_nb,
            )
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
        return Result(
            index_uid,
            hits,
            query,
            processing_time_ms,
            limit,
            offset,
            estimated_total_hits,
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
