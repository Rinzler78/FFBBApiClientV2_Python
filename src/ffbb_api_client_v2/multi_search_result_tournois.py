from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from ffbb_api_client_v2.Cartographie import Cartographie
from ffbb_api_client_v2.Commune import Commune
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
from ffbb_api_client_v2.Geo import Geo
from ffbb_api_client_v2.NatureSol import NatureSol


class Code(Enum):
    BIT = "BIT"
    BT = "BT"
    SS = "SS"


class Libelle(Enum):
    BITUME = "BITUME"
    BÉTON = "Béton"
    SOL_SYNTHÉTIQUE = "Sol synthétique"


class HitType(Enum):
    TERRAIN = "Terrain"


@dataclass
class Hit:
    nom: Optional[str] = None
    rue: Optional[str] = None
    id: Optional[int] = None
    acces_libre: Optional[bool] = None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None
    largeur: Optional[int] = None
    longueur: Optional[int] = None
    numero: Optional[int] = None
    cartographie: Optional[Cartographie] = None
    commune: Optional[Commune] = None
    nature_sol: Optional[NatureSol] = None
    geo: Optional[Geo] = None
    thumbnail: None
    type: Optional[HitType] = None

    @staticmethod
    def from_dict(obj: Any) -> "Hit":
        assert isinstance(obj, dict)
        nom = from_union([from_str, from_none], obj.get("nom"))
        rue = from_union([from_str, from_none], obj.get("rue"))
        id = from_union([from_none, lambda x: int(from_str(x))], obj.get("id"))
        acces_libre = from_union([from_bool, from_none], obj.get("accesLibre"))
        date_created = from_union([from_datetime, from_none], obj.get("date_created"))
        date_updated = from_union([from_datetime, from_none], obj.get("date_updated"))
        largeur = from_union([from_int, from_none], obj.get("largeur"))
        longueur = from_union([from_int, from_none], obj.get("longueur"))
        numero = from_union([from_int, from_none], obj.get("numero"))
        cartographie = from_union(
            [Cartographie.from_dict, from_none], obj.get("cartographie")
        )
        commune = from_union([Commune.from_dict, from_none], obj.get("commune"))
        nature_sol = from_union([NatureSol.from_dict, from_none], obj.get("natureSol"))
        geo = from_union([Geo.from_dict, from_none], obj.get("_geo"))
        thumbnail = from_none(obj.get("thumbnail"))
        type = from_union([HitType, from_none], obj.get("type"))
        return Hit(
            nom,
            rue,
            id,
            acces_libre,
            date_created,
            date_updated,
            largeur,
            longueur,
            numero,
            cartographie,
            commune,
            nature_sol,
            geo,
            thumbnail,
            type,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.rue is not None:
            result["rue"] = from_union([from_str, from_none], self.rue)
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
        if self.acces_libre is not None:
            result["accesLibre"] = from_union([from_bool, from_none], self.acces_libre)
        if self.date_created is not None:
            result["date_created"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_created
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_updated
            )
        if self.largeur is not None:
            result["largeur"] = from_union([from_int, from_none], self.largeur)
        if self.longueur is not None:
            result["longueur"] = from_union([from_int, from_none], self.longueur)
        if self.numero is not None:
            result["numero"] = from_union([from_int, from_none], self.numero)
        if self.cartographie is not None:
            result["cartographie"] = from_union(
                [lambda x: to_class(Cartographie, x), from_none], self.cartographie
            )
        if self.commune is not None:
            result["commune"] = from_union(
                [lambda x: to_class(Commune, x), from_none], self.commune
            )
        if self.nature_sol is not None:
            result["natureSol"] = from_union(
                [lambda x: to_class(NatureSol, x), from_none], self.nature_sol
            )
        if self.geo is not None:
            result["_geo"] = from_union(
                [lambda x: to_class(Geo, x), from_none], self.geo
            )
        if self.thumbnail is not None:
            result["thumbnail"] = from_none(self.thumbnail)
        if self.type is not None:
            result["type"] = from_union(
                [lambda x: to_enum(HitType, x), from_none], self.type
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
