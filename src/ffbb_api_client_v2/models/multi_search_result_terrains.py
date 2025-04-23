from datetime import datetime
from enum import Enum
from typing import Any, List, Optional
from uuid import UUID

from .Cartographie import Cartographie
from .Commune import Commune
from .converters import (
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
from .DocumentFlyer import DocumentFlyer
from .FacetDistribution import FacetDistribution
from .FacetStats import FacetStats
from .Geo import Geo
from .Hit import Hit
from .TournoiTypeClass import TournoiTypeClass
from .TournoiTypeEnum import TournoiTypeEnum
from .TypeLeague import TypeLeague


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


class TournoiTypes3X3Libelle:
    open_plus_junior_league_3_x3: Optional[int] = None
    open_plus_super_league_3_x3: Optional[int] = None
    open_plus_access_junior_league_3_x3: Optional[int] = None
    open_plus_access_super_league_3_x3: Optional[int] = None
    open_start_junior_league_3_x3: Optional[int] = None
    open_start_super_league_3_x3: Optional[int] = None

    def __init__(
        self,
        open_plus_junior_league_3_x3: Optional[int],
        open_plus_super_league_3_x3: Optional[int],
        open_plus_access_junior_league_3_x3: Optional[int],
        open_plus_access_super_league_3_x3: Optional[int],
        open_start_junior_league_3_x3: Optional[int],
        open_start_super_league_3_x3: Optional[int],
    ) -> None:
        self.open_plus_junior_league_3_x3 = open_plus_junior_league_3_x3
        self.open_plus_super_league_3_x3 = open_plus_super_league_3_x3
        self.open_plus_access_junior_league_3_x3 = open_plus_access_junior_league_3_x3
        self.open_plus_access_super_league_3_x3 = open_plus_access_super_league_3_x3
        self.open_start_junior_league_3_x3 = open_start_junior_league_3_x3
        self.open_start_super_league_3_x3 = open_start_super_league_3_x3

    @staticmethod
    def from_dict(obj: Any) -> "TournoiTypes3X3Libelle":
        assert isinstance(obj, dict)
        open_plus_junior_league_3_x3 = from_union(
            [from_none, from_int], obj.get("Open Plus - Junior league 3x3")
        )
        open_plus_super_league_3_x3 = from_union(
            [from_none, from_int], obj.get("Open Plus - Super league 3x3")
        )
        open_plus_access_junior_league_3_x3 = from_union(
            [from_none, from_int], obj.get("Open Plus Access - Junior league 3x3")
        )
        open_plus_access_super_league_3_x3 = from_union(
            [from_none, from_int], obj.get("Open Plus Access - Super league 3x3")
        )
        open_start_junior_league_3_x3 = from_union(
            [from_none, from_int], obj.get("Open Start - Junior league 3x3")
        )
        open_start_super_league_3_x3 = from_union(
            [from_none, from_int], obj.get("Open Start - Super league 3x3")
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
                [from_none, from_int], self.open_plus_junior_league_3_x3
            )
        if self.open_plus_super_league_3_x3 is not None:
            result["Open Plus - Super league 3x3"] = from_union(
                [from_none, from_int], self.open_plus_super_league_3_x3
            )
        if self.open_plus_access_junior_league_3_x3 is not None:
            result["Open Plus Access - Junior league 3x3"] = from_union(
                [from_none, from_int], self.open_plus_access_junior_league_3_x3
            )
        if self.open_plus_access_super_league_3_x3 is not None:
            result["Open Plus Access - Super league 3x3"] = from_union(
                [from_none, from_int], self.open_plus_access_super_league_3_x3
            )
        if self.open_start_junior_league_3_x3 is not None:
            result["Open Start - Junior league 3x3"] = from_union(
                [from_none, from_int], self.open_start_junior_league_3_x3
            )
        if self.open_start_super_league_3_x3 is not None:
            result["Open Start - Super league 3x3"] = from_union(
                [from_none, from_int], self.open_start_super_league_3_x3
            )
        return result


class TerrainsFacetDistribution(FacetDistribution):
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
    def from_dict(obj: Any) -> "TerrainsFacetDistribution":
        assert isinstance(obj, dict)
        sexe = from_union([from_none, SexeClass.from_dict], obj.get("sexe"))
        tournoi_type = from_union(
            [from_none, TournoiTypeClass.from_dict], obj.get("tournoiType")
        )
        tournoi_types3_x3_libelle = from_union(
            [from_none, TournoiTypes3X3Libelle.from_dict],
            obj.get("tournoiTypes3x3.libelle"),
        )
        return TerrainsFacetDistribution(sexe, tournoi_type, tournoi_types3_x3_libelle)

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


class CategorieChampionnat3X3Libelle(Enum):
    U18 = "U18"


class Name(Enum):
    TOURNOIS = "Tournois"


class Storage(Enum):
    MINIO = "minio"


class SexeEnum(Enum):
    FÉMININ = "Féminin"
    MASCULIN = "Masculin"
    MIXTE = "Mixte"


class Libelle(Enum):
    OPEN_PLUS_ACCESS_JUNIOR_LEAGUE_3_X3 = "Open Plus Access - Junior league 3x3"
    OPEN_PLUS_ACCESS_SUPER_LEAGUE_3_X3 = "Open Plus Access - Super league 3x3"
    OPEN_PLUS_JUNIOR_LEAGUE_3_X3 = "Open Plus - Junior league 3x3"
    OPEN_PLUS_SUPER_LEAGUE_3_X3 = "Open Plus - Super league 3x3"
    OPEN_START_JUNIOR_LEAGUE_3_X3 = "Open Start - Junior league 3x3"
    OPEN_START_SUPER_LEAGUE_3_X3 = "Open Start - Super league 3x3"


class TournoiTypes3X3:
    libelle: Optional[Libelle] = None
    logo: Optional[UUID] = None
    type_league: Optional[TypeLeague] = None
    type_tournois: Optional[int] = None

    def __init__(
        self,
        libelle: Optional[Libelle],
        logo: Optional[UUID],
        type_league: Optional[TypeLeague],
        type_tournois: Optional[int],
    ) -> None:
        self.libelle = libelle
        self.logo = logo
        self.type_league = type_league
        self.type_tournois = type_tournois

    @staticmethod
    def from_dict(obj: Any) -> "TournoiTypes3X3":
        assert isinstance(obj, dict)
        libelle = from_union([from_none, Libelle], obj.get("libelle"))
        logo = from_union([from_none, lambda x: UUID(x)], obj.get("logo"))
        type_league = from_union([from_none, TypeLeague], obj.get("type_league"))
        type_tournois = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("type_tournois")
        )
        return TournoiTypes3X3(libelle, logo, type_league, type_tournois)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.libelle is not None:
            result["libelle"] = from_union(
                [from_none, lambda x: to_enum(Libelle, x)], self.libelle
            )
        if self.logo is not None:
            result["logo"] = from_union([from_none, lambda x: str(x)], self.logo)
        if self.type_league is not None:
            result["type_league"] = from_union(
                [from_none, lambda x: to_enum(TypeLeague, x)], self.type_league
            )
        if self.type_tournois is not None:
            result["type_tournois"] = from_union(
                [
                    from_none,
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.type_tournois,
            )
        return result


class TerrainsHit(Hit):
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

    def __init__(
        self,
        nom: Optional[str],
        sexe: Optional[SexeEnum],
        adresse: Optional[str],
        nom_organisateur: Optional[str],
        description: Optional[str],
        site_choisi: Optional[str],
        id: Optional[int],
        code: Optional[str],
        date_created: Optional[datetime],
        date_updated: Optional[datetime],
        age_max: Optional[int],
        age_min: Optional[int],
        categorie_championnat3_x3_id: Optional[int],
        categorie_championnat3_x3_libelle: Optional[CategorieChampionnat3X3Libelle],
        debut: Optional[datetime],
        fin: Optional[datetime],
        mail_organisateur: Optional[str],
        nb_participant_prevu: None,
        tarif_organisateur: Optional[int],
        telephone_organisateur: Optional[str],
        url_organisateur: Optional[str],
        adresse_complement: None,
        tournoi_types3_x3: Optional[List[TournoiTypes3X3]],
        cartographie: Optional[Cartographie],
        commune: Optional[Commune],
        document_flyer: Optional[DocumentFlyer],
        tournoi_type: Optional[TournoiTypeEnum],
        geo: Optional[Geo],
        debut_timestamp: Optional[int],
        fin_timestamp: Optional[int],
        thumbnail: None,
    ) -> None:
        self.nom = nom
        self.lower_nom = nom.lower() if nom else None

        self.sexe = sexe
        self.adresse = adresse
        self.lower_addresse = adresse.lower() if adresse else None

        self.nom_organisateur = nom_organisateur
        self.lower_nom_organisateur = (
            nom_organisateur.lower() if nom_organisateur else None
        )

        self.description = description
        self.lower_description = description.lower() if description else None

        self.site_choisi = site_choisi
        self.lower_site_choisi = site_choisi.lower() if site_choisi else None

        self.id = id
        self.code = code
        self.lower_code = code.lower() if code else None

        self.date_created = date_created
        self.date_updated = date_updated
        self.age_max = age_max
        self.age_min = age_min
        self.categorie_championnat3_x3_id = categorie_championnat3_x3_id
        self.categorie_championnat3_x3_libelle = categorie_championnat3_x3_libelle
        self.debut = debut
        self.fin = fin
        self.mail_organisateur = mail_organisateur
        self.nb_participant_prevu = nb_participant_prevu
        self.tarif_organisateur = tarif_organisateur
        self.telephone_organisateur = telephone_organisateur
        self.url_organisateur = url_organisateur
        self.adresse_complement = adresse_complement
        self.tournoi_types3_x3 = tournoi_types3_x3
        self.cartographie = cartographie
        self.commune = commune
        self.document_flyer = document_flyer
        self.tournoi_type = tournoi_type
        self.geo = geo
        self.debut_timestamp = debut_timestamp
        self.fin_timestamp = fin_timestamp
        self.thumbnail = thumbnail

    @staticmethod
    def from_dict(obj: Any) -> "TerrainsHit":
        assert isinstance(obj, dict)
        nom = from_union([from_none, from_str], obj.get("nom"))
        sexe = from_union([from_none, SexeEnum], obj.get("sexe"))
        adresse = from_union([from_none, from_str], obj.get("adresse"))
        nom_organisateur = from_union([from_none, from_str], obj.get("nomOrganisateur"))
        description = from_union([from_none, from_str], obj.get("description"))
        site_choisi = from_union([from_none, from_str], obj.get("siteChoisi"))
        id = from_union([from_none, lambda x: int(from_str(x))], obj.get("id"))
        code = from_union([from_none, from_str], obj.get("code"))
        date_created = from_union([from_none, from_datetime], obj.get("date_created"))
        date_updated = from_union([from_none, from_datetime], obj.get("date_updated"))
        age_max = from_union([from_none, from_int], obj.get("ageMax"))
        age_min = from_union([from_none, from_int], obj.get("ageMin"))
        categorie_championnat3_x3_id = from_union(
            [from_none, lambda x: int(from_str(x))],
            obj.get("categorieChampionnat3x3Id"),
        )
        categorie_championnat3_x3_libelle = from_union(
            [from_none, CategorieChampionnat3X3Libelle],
            obj.get("categorieChampionnat3x3Libelle"),
        )
        debut = from_union([from_none, from_datetime], obj.get("debut"))
        fin = from_union([from_none, from_datetime], obj.get("fin"))
        mail_organisateur = from_union(
            [from_none, from_str], obj.get("mailOrganisateur")
        )
        nb_participant_prevu = from_none(obj.get("nbParticipantPrevu"))
        tarif_organisateur = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("tarifOrganisateur")
        )
        telephone_organisateur = from_union(
            [from_none, from_str], obj.get("telephoneOrganisateur")
        )
        url_organisateur = from_union([from_none, from_str], obj.get("urlOrganisateur"))
        adresse_complement = from_none(obj.get("adresseComplement"))
        tournoi_types3_x3 = from_union(
            [from_none, lambda x: from_list(TournoiTypes3X3.from_dict, x)],
            obj.get("tournoiTypes3x3"),
        )
        cartographie = from_union(
            [from_none, Cartographie.from_dict], obj.get("cartographie")
        )
        commune = from_union([from_none, Commune.from_dict], obj.get("commune"))
        document_flyer = from_union(
            [from_none, DocumentFlyer.from_dict], obj.get("document_flyer")
        )
        tournoi_type = from_union([from_none, TournoiTypeEnum], obj.get("tournoiType"))
        geo = from_union([from_none, Geo.from_dict], obj.get("_geo"))
        debut_timestamp = from_union([from_none, from_int], obj.get("debut_timestamp"))
        fin_timestamp = from_union([from_none, from_int], obj.get("fin_timestamp"))
        thumbnail = from_none(obj.get("thumbnail"))
        return TerrainsHit(
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
            result["nom"] = from_union([from_none, from_str], self.nom)
        if self.sexe is not None:
            result["sexe"] = from_union(
                [from_none, lambda x: to_enum(SexeEnum, x)], self.sexe
            )
        if self.adresse is not None:
            result["adresse"] = from_union([from_none, from_str], self.adresse)
        if self.nom_organisateur is not None:
            result["nomOrganisateur"] = from_union(
                [from_none, from_str], self.nom_organisateur
            )
        if self.description is not None:
            result["description"] = from_union([from_none, from_str], self.description)
        if self.site_choisi is not None:
            result["siteChoisi"] = from_union([from_none, from_str], self.site_choisi)
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
        if self.code is not None:
            result["code"] = from_union([from_none, from_str], self.code)
        if self.date_created is not None:
            result["date_created"] = from_union(
                [from_none, lambda x: x.isoformat()], self.date_created
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [from_none, lambda x: x.isoformat()], self.date_updated
            )
        if self.age_max is not None:
            result["ageMax"] = from_union([from_none, from_int], self.age_max)
        if self.age_min is not None:
            result["ageMin"] = from_union([from_none, from_int], self.age_min)
        if self.categorie_championnat3_x3_id is not None:
            result["categorieChampionnat3x3Id"] = from_union(
                [
                    from_none,
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
                [from_none, lambda x: x.isoformat()], self.debut
            )
        if self.fin is not None:
            result["fin"] = from_union([from_none, lambda x: x.isoformat()], self.fin)
        if self.mail_organisateur is not None:
            result["mailOrganisateur"] = from_union(
                [from_none, from_str], self.mail_organisateur
            )
        if self.nb_participant_prevu is not None:
            result["nbParticipantPrevu"] = from_none(self.nb_participant_prevu)
        if self.tarif_organisateur is not None:
            result["tarifOrganisateur"] = from_union(
                [
                    from_none,
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.tarif_organisateur,
            )
        if self.telephone_organisateur is not None:
            result["telephoneOrganisateur"] = from_union(
                [from_none, from_str], self.telephone_organisateur
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
                    from_none,
                    lambda x: from_list(lambda x: to_class(TournoiTypes3X3, x), x),
                ],
                self.tournoi_types3_x3,
            )
        if self.cartographie is not None:
            result["cartographie"] = from_union(
                [from_none, lambda x: to_class(Cartographie, x)], self.cartographie
            )
        if self.commune is not None:
            result["commune"] = from_union(
                [from_none, lambda x: to_class(Commune, x)], self.commune
            )
        if self.document_flyer is not None:
            result["document_flyer"] = from_union(
                [from_none, lambda x: to_class(DocumentFlyer, x)], self.document_flyer
            )
        if self.tournoi_type is not None:
            result["tournoiType"] = from_union(
                [from_none, lambda x: to_enum(TournoiTypeEnum, x)], self.tournoi_type
            )
        if self.geo is not None:
            result["_geo"] = from_union(
                [from_none, lambda x: to_class(Geo, x)], self.geo
            )
        if self.debut_timestamp is not None:
            result["debut_timestamp"] = from_union(
                [from_none, from_int], self.debut_timestamp
            )
        if self.fin_timestamp is not None:
            result["fin_timestamp"] = from_union(
                [from_none, from_int], self.fin_timestamp
            )
        if self.thumbnail is not None:
            result["thumbnail"] = from_none(self.thumbnail)
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return (
            not query
            or (self.lower_nom and query in self.lower_nom)
            or (self.lower_addresse and query in self.lower_addresse)
            or (self.lower_description and query in self.lower_description)
            or (self.lower_code and query in self.lower_code)
            or (self.lower_nom_organisateur and query in self)
            or (self.lower_nom_organisateur and query in self.lower_nom_organisateur)
            or (self.lower_site_choisi and query in self.lower_site_choisi)
        )


class TerrainsFacetStats(FacetStats):
    @staticmethod
    def from_dict(obj: Any) -> "TerrainsFacetStats":
        return TerrainsFacetStats()

    def to_dict(self) -> dict:
        super().to_dict()
