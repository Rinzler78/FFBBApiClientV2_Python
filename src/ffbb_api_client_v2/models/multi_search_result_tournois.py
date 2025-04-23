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
        féminin = from_union([from_none, from_int], obj.get("Féminin"))
        masculin = from_union([from_none, from_int], obj.get("Masculin"))
        mixte = from_union([from_none, from_int], obj.get("Mixte"))
        return SexeClass(féminin, masculin, mixte)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.féminin is not None:
            result["Féminin"] = from_union([from_none, from_int], self.féminin)
        if self.masculin is not None:
            result["Masculin"] = from_union([from_none, from_int], self.masculin)
        if self.mixte is not None:
            result["Mixte"] = from_union([from_none, from_int], self.mixte)
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
        sexe = from_union([from_none, SexeClass.from_dict], obj.get("sexe"))
        tournoi_type = from_union(
            [from_none, TournoiTypeClass.from_dict], obj.get("tournoiType")
        )
        tournoi_types3_x3_libelle = from_union(
            [from_none, TournoiTypes3X3Libelle.from_dict],
            obj.get("tournoiTypes3x3.libelle"),
        )
        return TournoisFacetDistribution(sexe, tournoi_type, tournoi_types3_x3_libelle)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.sexe is not None:
            result["sexe"] = from_union(
                [from_none, lambda x: to_class(SexeClass, x)], self.sexe
            )
        if self.tournoi_type is not None:
            result["tournoiType"] = from_union(
                [from_none, lambda x: to_class(TournoiTypeClass, x)], self.tournoi_type
            )
        if self.tournoi_types3_x3_libelle is not None:
            result["tournoiTypes3x3.libelle"] = from_union(
                [from_none, lambda x: to_class(TournoiTypes3X3Libelle, x)],
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
        nom = from_union([from_none, from_str], obj.get("nom"))
        rue = from_union([from_none, from_str], obj.get("rue"))
        id = from_union([from_none, lambda x: int(from_str(x))], obj.get("id"))
        acces_libre = from_union([from_none, from_bool], obj.get("accesLibre"))
        date_created = from_union([from_none, from_datetime], obj.get("date_created"))
        date_updated = from_union([from_none, from_datetime], obj.get("date_updated"))
        largeur = from_union([from_none, from_int], obj.get("largeur"))
        longueur = from_union([from_none, from_int], obj.get("longueur"))
        numero = from_union([from_none, from_int], obj.get("numero"))
        cartographie = from_union(
            [from_none, Cartographie.from_dict], obj.get("cartographie")
        )
        commune = from_union([from_none, Commune.from_dict], obj.get("commune"))
        nature_sol = from_union([from_none, NatureSol.from_dict], obj.get("natureSol"))
        geo = from_union([from_none, Geo.from_dict], obj.get("_geo"))
        thumbnail = from_none(obj.get("thumbnail"))
        type = from_union([from_none, HitType], obj.get("type"))
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
            result["nom"] = from_union([from_none, from_str], self.nom)
        if self.rue is not None:
            result["rue"] = from_union([from_none, from_str], self.rue)
        if self.id is not None:
            result["id"] = from_union(
                [
                    from_none,
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.id,
            )
        if self.acces_libre is not None:
            result["accesLibre"] = from_union([from_none, from_bool], self.acces_libre)
        if self.date_created is not None:
            result["date_created"] = from_union(
                [from_none, lambda x: x.isoformat()], self.date_created
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [from_none, lambda x: x.isoformat()], self.date_updated
            )
        if self.largeur is not None:
            result["largeur"] = from_union([from_none, from_int], self.largeur)
        if self.longueur is not None:
            result["longueur"] = from_union([from_none, from_int], self.longueur)
        if self.numero is not None:
            result["numero"] = from_union([from_none, from_int], self.numero)
        if self.cartographie is not None:
            result["cartographie"] = from_union(
                [from_none, lambda x: to_class(Cartographie, x)], self.cartographie
            )
        if self.commune is not None:
            result["commune"] = from_union(
                [from_none, lambda x: to_class(Commune, x)], self.commune
            )
        if self.nature_sol is not None:
            result["natureSol"] = from_union(
                [from_none, lambda x: to_class(NatureSol, x)], self.nature_sol
            )
        if self.geo is not None:
            result["_geo"] = from_union(
                [from_none, lambda x: to_class(Geo, x)], self.geo
            )
        if self.thumbnail is not None:
            result["thumbnail"] = from_none(self.thumbnail)
        if self.type is not None:
            result["type"] = from_union(
                [from_none, lambda x: to_enum(HitType, x)], self.type
            )
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return bool(
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
        return super().to_dict()
