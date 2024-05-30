from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from ffbb_api_client_v2.Cartographie import Cartographie
from ffbb_api_client_v2.Commune import Commune
from ffbb_api_client_v2.converters import (
    from_datetime,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    to_class,
    to_enum,
)
from ffbb_api_client_v2.Geo import Geo
from ffbb_api_client_v2.TypeAssociation import TypeAssociation


class LibelleEnum(Enum):
    SALLE = "Salle"


@dataclass
class Hit:
    libelle: Optional[str] = None
    adresse: Optional[str] = None
    id: Optional[str] = None
    adresse_complement: Optional[str] = None
    capacite_spectateur: Optional[str] = None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None
    libelle2: Optional[str] = None
    mail: Optional[str] = None
    numero: Optional[str] = None
    telephone: Optional[str] = None
    cartographie: Optional[Cartographie] = None
    commune: Optional[Commune] = None
    geo: Optional[Geo] = None
    thumbnail: None
    type: Optional[LibelleEnum] = None
    type_association: Optional[TypeAssociation] = None

    @staticmethod
    def from_dict(obj: Any) -> "Hit":
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
        type = from_union([LibelleEnum, from_none], obj.get("type"))
        type_association = from_union(
            [TypeAssociation.from_dict, from_none], obj.get("type_association")
        )
        return Hit(
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
            result["type"] = from_union(
                [lambda x: to_enum(LibelleEnum, x), from_none], self.type
            )
        if self.type_association is not None:
            result["type_association"] = from_union(
                [lambda x: to_class(TypeAssociation, x), from_none],
                self.type_association,
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
