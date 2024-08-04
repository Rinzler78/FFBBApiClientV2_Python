from datetime import datetime
from enum import Enum
from typing import Any, Optional

from .Cartographie import Cartographie
from .Commune import Commune
from .converters import (
    from_bool,
    from_datetime,
    from_int,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
    to_enum,
)
from .FacetDistribution import FacetDistribution
from .FacetStats import FacetStats
from .Geo import Geo
from .Hit import Hit
from .multi_search_result_terrains import TournoiTypes3X3Libelle
from .NatureSol import NatureSol
from .TournoiTypeClass import TournoiTypeClass


class SexeClass:
    féminin: Optional[int] = None
    masculin: Optional[int] = None
    mixte: Optional[int] = None

    def __init__(
        self, féminin: Optional[int], masculin: Optional[int], mixte: Optional[int]
    ) -> None:
        self.féminin = féminin
        self.masculin = masculin
        self.mixte = mixte

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


class TournoisFacetDistribution(FacetDistribution):
    sexe: Optional[SexeClass] = None
    tournoi_type: Optional[TournoiTypeClass] = None
    tournoi_types3_x3_libelle: Optional[TournoiTypes3X3Libelle] = None

    def __init__(
        self,
        sexe: Optional[SexeClass],
        tournoi_type: Optional[TournoiTypeClass],
        tournoi_types3_x3_libelle: Optional[TournoiTypes3X3Libelle],
    ) -> None:
        self.sexe = sexe
        self.tournoi_type = tournoi_type
        self.tournoi_types3_x3_libelle = tournoi_types3_x3_libelle

    @staticmethod
    def from_dict(obj: Any) -> "TournoisFacetDistribution":
        assert isinstance(obj, dict)
        sexe = from_union([SexeClass.from_dict, from_none], obj.get("sexe"))
        tournoi_type = from_union(
            [TournoiTypeClass.from_dict, from_none], obj.get("tournoiType")
        )
        tournoi_types3_x3_libelle = from_union(
            [TournoiTypes3X3Libelle.from_dict, from_none],
            obj.get("tournoiTypes3x3.libelle"),
        )
        return TournoisFacetDistribution(sexe, tournoi_type, tournoi_types3_x3_libelle)

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


class Libelle(Enum):
    BITUME = "BITUME"
    BÉTON = "Béton"
    SOL_SYNTHÉTIQUE = "Sol synthétique"


class HitType(Enum):
    TERRAIN = "Terrain"


class TournoisHit(Hit):
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

    def __init__(
        self,
        nom: Optional[str],
        rue: Optional[str],
        id: Optional[int],
        acces_libre: Optional[bool],
        date_created: Optional[datetime],
        date_updated: Optional[datetime],
        largeur: Optional[int],
        longueur: Optional[int],
        numero: Optional[int],
        cartographie: Optional[Cartographie],
        commune: Optional[Commune],
        nature_sol: Optional[NatureSol],
        geo: Optional[Geo],
        thumbnail: None,
        type: Optional[HitType],
    ) -> None:
        self.nom = nom
        self.rue = rue
        self.lower_nom = nom.lower() if nom else None
        self.lower_rue = rue.lower() if rue else None
        self.id = id
        self.acces_libre = acces_libre
        self.date_created = date_created
        self.date_updated = date_updated
        self.largeur = largeur
        self.longueur = longueur
        self.numero = numero
        self.cartographie = cartographie
        self.commune = commune
        self.nature_sol = nature_sol
        self.geo = geo
        self.thumbnail = thumbnail
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> "TournoisHit":
        assert isinstance(obj, dict)
        nom = from_union([from_str, from_none], obj.get("nom"))
        rue = from_union([from_str, from_none], obj.get("rue"))
        id = from_union([lambda x: int(from_str(x)), from_none], obj.get("id"))
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
        return TournoisHit(
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

    def is_valid_for_query(self, query: str) -> bool:
        return (
            not query
            or (self.lower_nom and query in self.lower_nom)
            or (self.lower_rue and query in self.lower_rue)
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


class TournoisFacetStats(FacetStats):
    @staticmethod
    def from_dict(obj: Any) -> "TournoisFacetStats":
        return TournoisFacetStats()

    def to_dict(self) -> dict:
        super().to_dict()
