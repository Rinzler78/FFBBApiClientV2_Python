from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from ..utils.converters import (
    from_bool,
    from_datetime,
    from_dict,
    from_float,
    from_int,
    from_list,
    from_none,
    from_str,
    from_stringified_bool,
    from_union,
    is_type,
    to_class,
    to_enum,
    to_float,
)

from .cartographie import Cartographie
from .commune import Commune
from .id_organisme_equipe import IDOrganismeEquipe
from .id_poule import IDPoule
from .logo import Logo

from .salle import Salle


class CompetitionIDSexe:
    féminin: int
    masculin: int
    mixte: int

    def __init__(self, féminin: int, masculin: int, mixte: int) -> None:
        self.féminin = féminin
        self.masculin = masculin
        self.mixte = mixte

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionIDSexe":
        assert isinstance(obj, dict)
        féminin = from_int(obj.get("Féminin"))
        masculin = from_int(obj.get("Masculin"))
        mixte = from_int(obj.get("Mixte"))
        return CompetitionIDSexe(féminin, masculin, mixte)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Féminin"] = from_int(self.féminin)
        result["Masculin"] = from_int(self.masculin)
        result["Mixte"] = from_int(self.mixte)
        return result


class CompetitionIDTypeCompetition:
    championnat: int
    championnat_3_x3: int
    coupe: int
    plateau: int

    def __init__(
        self, championnat: int, championnat_3_x3: int, coupe: int, plateau: int
    ) -> None:
        self.championnat = championnat
        self.championnat_3_x3 = championnat_3_x3
        self.coupe = coupe
        self.plateau = plateau

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionIDTypeCompetition":
        assert isinstance(obj, dict)
        championnat = from_int(obj.get("Championnat"))
        championnat_3_x3 = from_int(obj.get("Championnat 3x3"))
        coupe = from_int(obj.get("Coupe"))
        plateau = from_int(obj.get("Plateau"))
        return CompetitionIDTypeCompetition(
            championnat, championnat_3_x3, coupe, plateau
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["Championnat"] = from_int(self.championnat)
        result["Championnat 3x3"] = from_int(self.championnat_3_x3)
        result["Coupe"] = from_int(self.coupe)
        result["Plateau"] = from_int(self.plateau)
        return result


class Niveau:
    départemental: int
    handibasket: int
    international: int
    national: int
    pro: int
    régional: int

    def __init__(
        self,
        départemental: int,
        handibasket: int,
        international: int,
        national: int,
        pro: int,
        régional: int,
    ) -> None:
        self.départemental = départemental
        self.handibasket = handibasket
        self.international = international
        self.national = national
        self.pro = pro
        self.régional = régional

    @staticmethod
    def from_dict(obj: Any) -> "Niveau":
        assert isinstance(obj, dict)
        départemental = from_int(obj.get("Départemental"))
        handibasket = from_int(obj.get("Handibasket"))
        international = from_int(obj.get("International"))
        national = from_int(obj.get("National"))
        pro = from_int(obj.get("Pro"))
        régional = from_int(obj.get("Régional"))
        return Niveau(
            départemental, handibasket, international, national, pro, régional
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["Départemental"] = from_int(self.départemental)
        result["Handibasket"] = from_int(self.handibasket)
        result["International"] = from_int(self.international)
        result["National"] = from_int(self.national)
        result["Pro"] = from_int(self.pro)
        result["Régional"] = from_int(self.régional)
        return result


class TournoiType:
    open_plus: int
    open_plus_access: int
    open_start: int

    def __init__(self, open_plus: int, open_plus_access: int, open_start: int) -> None:
        self.open_plus = open_plus
        self.open_plus_access = open_plus_access
        self.open_start = open_start

    @staticmethod
    def from_dict(obj: Any) -> "TournoiType":
        assert isinstance(obj, dict)
        open_plus = from_int(obj.get("Open Plus"))
        open_plus_access = from_int(obj.get("Open Plus Access"))
        open_start = from_int(obj.get("Open Start"))
        return TournoiType(open_plus, open_plus_access, open_start)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Open Plus"] = from_int(self.open_plus)
        result["Open Plus Access"] = from_int(self.open_plus_access)
        result["Open Start"] = from_int(self.open_start)
        return result


class TournoiTypes3X3Libelle:
    open_plus_junior_league_3_x3: int
    open_plus_super_league_3_x3: int
    open_plus_access_junior_league_3_x3: int
    open_plus_access_super_league_3_x3: int
    open_start_junior_league_3_x3: int
    open_start_super_league_3_x3: int

    def __init__(
        self,
        open_plus_junior_league_3_x3: int,
        open_plus_super_league_3_x3: int,
        open_plus_access_junior_league_3_x3: int,
        open_plus_access_super_league_3_x3: int,
        open_start_junior_league_3_x3: int,
        open_start_super_league_3_x3: int,
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
        open_plus_junior_league_3_x3 = from_int(
            obj.get("Open Plus - Junior league 3x3")
        )
        open_plus_super_league_3_x3 = from_int(obj.get("Open Plus - Super league 3x3"))
        open_plus_access_junior_league_3_x3 = from_int(
            obj.get("Open Plus Access - Junior league 3x3")
        )
        open_plus_access_super_league_3_x3 = from_int(
            obj.get("Open Plus Access - Super league 3x3")
        )
        open_start_junior_league_3_x3 = from_int(
            obj.get("Open Start - Junior league 3x3")
        )
        open_start_super_league_3_x3 = from_int(
            obj.get("Open Start - Super league 3x3")
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
        result["Open Plus - Junior league 3x3"] = from_int(
            self.open_plus_junior_league_3_x3
        )
        result["Open Plus - Super league 3x3"] = from_int(
            self.open_plus_super_league_3_x3
        )
        result["Open Plus Access - Junior league 3x3"] = from_int(
            self.open_plus_access_junior_league_3_x3
        )
        result["Open Plus Access - Super league 3x3"] = from_int(
            self.open_plus_access_super_league_3_x3
        )
        result["Open Start - Junior league 3x3"] = from_int(
            self.open_start_junior_league_3_x3
        )
        result["Open Start - Super league 3x3"] = from_int(
            self.open_start_super_league_3_x3
        )
        return result


class TypeAssociationLibelle:
    association_club_professionnel: int
    club: int
    entente: int
    union: int

    def __init__(
        self, association_club_professionnel: int, club: int, entente: int, union: int
    ) -> None:
        self.association_club_professionnel = association_club_professionnel
        self.club = club
        self.entente = entente
        self.union = union

    @staticmethod
    def from_dict(obj: Any) -> "TypeAssociationLibelle":
        assert isinstance(obj, dict)
        association_club_professionnel = from_int(
            obj.get("Association club professionnel")
        )
        club = from_int(obj.get("Club"))
        entente = from_int(obj.get("Entente"))
        union = from_int(obj.get("Union"))
        return TypeAssociationLibelle(
            association_club_professionnel, club, entente, union
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["Association club professionnel"] = from_int(
            self.association_club_professionnel
        )
        result["Club"] = from_int(self.club)
        result["Entente"] = from_int(self.entente)
        result["Union"] = from_int(self.union)
        return result


class FacetDistribution:
    competition_id_categorie_code: Optional[Dict[str, int]]
    competition_id_nom_extended: Optional[Dict[str, int]]
    competition_id_sexe: Optional[CompetitionIDSexe]
    competition_id_type_competition: Optional[CompetitionIDTypeCompetition]
    label: Optional[Dict[str, int]]
    labellisation: Optional[Dict[str, int]]
    niveau: Optional[Niveau]
    offres_pratiques: Optional[Dict[str, int]]
    organisateur_id: Optional[Dict[str, int]]
    organisateur_nom: Optional[Dict[str, int]]
    sexe: Optional[CompetitionIDSexe]
    tournoi_type: Optional[TournoiType]
    tournoi_types3_x3_libelle: Optional[TournoiTypes3X3Libelle]
    type: Optional[Dict[str, int]]
    type_association_libelle: Optional[TypeAssociationLibelle]

    def __init__(
        self,
        competition_id_categorie_code: Optional[Dict[str, int]],
        competition_id_nom_extended: Optional[Dict[str, int]],
        competition_id_sexe: Optional[CompetitionIDSexe],
        competition_id_type_competition: Optional[CompetitionIDTypeCompetition],
        label: Optional[Dict[str, int]],
        labellisation: Optional[Dict[str, int]],
        niveau: Optional[Niveau],
        offres_pratiques: Optional[Dict[str, int]],
        organisateur_id: Optional[Dict[str, int]],
        organisateur_nom: Optional[Dict[str, int]],
        sexe: Optional[CompetitionIDSexe],
        tournoi_type: Optional[TournoiType],
        tournoi_types3_x3_libelle: Optional[TournoiTypes3X3Libelle],
        type: Optional[Dict[str, int]],
        type_association_libelle: Optional[TypeAssociationLibelle],
    ) -> None:
        self.competition_id_categorie_code = competition_id_categorie_code
        self.competition_id_nom_extended = competition_id_nom_extended
        self.competition_id_sexe = competition_id_sexe
        self.competition_id_type_competition = competition_id_type_competition
        self.label = label
        self.labellisation = labellisation
        self.niveau = niveau
        self.offres_pratiques = offres_pratiques
        self.organisateur_id = organisateur_id
        self.organisateur_nom = organisateur_nom
        self.sexe = sexe
        self.tournoi_type = tournoi_type
        self.tournoi_types3_x3_libelle = tournoi_types3_x3_libelle
        self.type = type
        self.type_association_libelle = type_association_libelle

    @staticmethod
    def from_dict(obj: Any) -> "FacetDistribution":
        assert isinstance(obj, dict)
        competition_id_categorie_code = from_union(
            [lambda x: from_dict(from_int, x), from_none],
            obj.get("competitionId.categorie.code"),
        )
        competition_id_nom_extended = from_union(
            [lambda x: from_dict(from_int, x), from_none],
            obj.get("competitionId.nomExtended"),
        )
        competition_id_sexe = from_union(
            [CompetitionIDSexe.from_dict, from_none], obj.get("competitionId.sexe")
        )
        competition_id_type_competition = from_union(
            [CompetitionIDTypeCompetition.from_dict, from_none],
            obj.get("competitionId.typeCompetition"),
        )
        label = from_union(
            [lambda x: from_dict(from_int, x), from_none], obj.get("label")
        )
        labellisation = from_union(
            [lambda x: from_dict(from_int, x), from_none], obj.get("labellisation")
        )
        niveau = from_union([Niveau.from_dict, from_none], obj.get("niveau"))
        offres_pratiques = from_union(
            [lambda x: from_dict(from_int, x), from_none], obj.get("offresPratiques")
        )
        organisateur_id = from_union(
            [lambda x: from_dict(from_int, x), from_none], obj.get("organisateur.id")
        )
        organisateur_nom = from_union(
            [lambda x: from_dict(from_int, x), from_none], obj.get("organisateur.nom")
        )
        sexe = from_union([CompetitionIDSexe.from_dict, from_none], obj.get("sexe"))
        tournoi_type = from_union(
            [TournoiType.from_dict, from_none], obj.get("tournoiType")
        )
        tournoi_types3_x3_libelle = from_union(
            [TournoiTypes3X3Libelle.from_dict, from_none],
            obj.get("tournoiTypes3x3.libelle"),
        )
        type = from_union(
            [lambda x: from_dict(from_int, x), from_none], obj.get("type")
        )
        type_association_libelle = from_union(
            [TypeAssociationLibelle.from_dict, from_none],
            obj.get("type_association.libelle"),
        )
        return FacetDistribution(
            competition_id_categorie_code,
            competition_id_nom_extended,
            competition_id_sexe,
            competition_id_type_competition,
            label,
            labellisation,
            niveau,
            offres_pratiques,
            organisateur_id,
            organisateur_nom,
            sexe,
            tournoi_type,
            tournoi_types3_x3_libelle,
            type,
            type_association_libelle,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.competition_id_categorie_code is not None:
            result["competitionId.categorie.code"] = from_union(
                [lambda x: from_dict(from_int, x), from_none],
                self.competition_id_categorie_code,
            )
        if self.competition_id_nom_extended is not None:
            result["competitionId.nomExtended"] = from_union(
                [lambda x: from_dict(from_int, x), from_none],
                self.competition_id_nom_extended,
            )
        if self.competition_id_sexe is not None:
            result["competitionId.sexe"] = from_union(
                [lambda x: to_class(CompetitionIDSexe, x), from_none],
                self.competition_id_sexe,
            )
        if self.competition_id_type_competition is not None:
            result["competitionId.typeCompetition"] = from_union(
                [lambda x: to_class(CompetitionIDTypeCompetition, x), from_none],
                self.competition_id_type_competition,
            )
        if self.label is not None:
            result["label"] = from_union(
                [lambda x: from_dict(from_int, x), from_none], self.label
            )
        if self.labellisation is not None:
            result["labellisation"] = from_union(
                [lambda x: from_dict(from_int, x), from_none], self.labellisation
            )
        if self.niveau is not None:
            result["niveau"] = from_union(
                [lambda x: to_class(Niveau, x), from_none], self.niveau
            )
        if self.offres_pratiques is not None:
            result["offresPratiques"] = from_union(
                [lambda x: from_dict(from_int, x), from_none], self.offres_pratiques
            )
        if self.organisateur_id is not None:
            result["organisateur.id"] = from_union(
                [lambda x: from_dict(from_int, x), from_none], self.organisateur_id
            )
        if self.organisateur_nom is not None:
            result["organisateur.nom"] = from_union(
                [lambda x: from_dict(from_int, x), from_none], self.organisateur_nom
            )
        if self.sexe is not None:
            result["sexe"] = from_union(
                [lambda x: to_class(CompetitionIDSexe, x), from_none], self.sexe
            )
        if self.tournoi_type is not None:
            result["tournoiType"] = from_union(
                [lambda x: to_class(TournoiType, x), from_none], self.tournoi_type
            )
        if self.tournoi_types3_x3_libelle is not None:
            result["tournoiTypes3x3.libelle"] = from_union(
                [lambda x: to_class(TournoiTypes3X3Libelle, x), from_none],
                self.tournoi_types3_x3_libelle,
            )
        if self.type is not None:
            result["type"] = from_union(
                [lambda x: from_dict(from_int, x), from_none], self.type
            )
        if self.type_association_libelle is not None:
            result["type_association.libelle"] = from_union(
                [lambda x: to_class(TypeAssociationLibelle, x), from_none],
                self.type_association_libelle,
            )
        return result


class FacetStats:
    pass

    def __init__(
        self,
    ) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> "FacetStats":
        assert isinstance(obj, dict)
        return FacetStats()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


class AfficheType(Enum):
    APPLICATION_PDF = "application/pdf"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"


class Affiche:
    gradient_color: Optional[str]
    height: Optional[int]
    id: UUID
    type: AfficheType
    width: Optional[int]

    def __init__(
        self,
        gradient_color: Optional[str],
        height: Optional[int],
        id: UUID,
        type: AfficheType,
        width: Optional[int],
    ) -> None:
        self.gradient_color = gradient_color
        self.height = height
        self.id = id
        self.type = type
        self.width = width

    @staticmethod
    def from_dict(obj: Any) -> "Affiche":
        assert isinstance(obj, dict)
        gradient_color = from_union([from_none, from_str], obj.get("gradient_color"))
        height = from_union([from_int, from_none], obj.get("height"))
        id = UUID(obj.get("id"))
        type = AfficheType(obj.get("type"))
        width = from_union([from_int, from_none], obj.get("width"))
        return Affiche(gradient_color, height, id, type, width)

    def to_dict(self) -> dict:
        result: dict = {}
        result["gradient_color"] = from_union(
            [from_none, from_str], self.gradient_color
        )
        result["height"] = from_union([from_int, from_none], self.height)
        result["id"] = str(self.id)
        result["type"] = to_enum(AfficheType, self.type)
        result["width"] = from_union([from_int, from_none], self.width)
        return result


class CoordonneesType(Enum):
    POINT = "Point"


class Coordonnees:
    coordinates: List[float]
    type: CoordonneesType

    def __init__(self, coordinates: List[float], type: CoordonneesType) -> None:
        self.coordinates = coordinates
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> "Coordonnees":
        assert isinstance(obj, dict)
        coordinates = from_list(from_float, obj.get("coordinates"))
        type = CoordonneesType(obj.get("type"))
        return Coordonnees(coordinates, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["coordinates"] = from_list(to_float, self.coordinates)
        result["type"] = to_enum(CoordonneesType, self.type)
        return result


class CartographieStatus(Enum):
    DRAFT = "draft"


class CategorieCode(Enum):
    BIT = "BIT"
    BT = "BT"
    EBT = "EBT"
    EBTP = "EBTP"
    PB = "PB"
    SE = "SE"
    SS = "SS"
    U11 = "U11"
    U13 = "U13"
    U15 = "U15"
    U17 = "U17"
    U18 = "U18"
    U20 = "U20"
    U21 = "U21"
    U7 = "U7"
    U9 = "U9"
    VE = "VE"


class CategorieLibelle(Enum):
    BITUME = "BITUME"
    BÉTON = "Béton"
    ENROBÉ_BITUME = "Enrobé / Bitume"
    ENROBÉ_BITUME_PEINT = "Enrobé / Bitume peint"
    PARQUET_BOIS_SOL_INTÉRIEUR = "Parquet bois (sol intérieur)"
    SENIOR = "Senior"
    SENIORS = "Seniors"
    SOL_SYNTHÉTIQUE = "Sol synthétique"
    U11 = "U11"
    U13 = "U13"
    U15 = "U15"
    U17 = "U17"
    U18 = "U18"
    U20 = "U20"
    U21 = "U21"
    U7 = "U7"
    U9 = "U9"
    VÉTÉRANS = "Vétérans"


class NatureSolClass:
    code: CategorieCode
    date_created: datetime
    date_updated: datetime
    id: str
    libelle: CategorieLibelle
    ordre: Optional[int]
    terrain: Optional[bool]

    def __init__(
        self,
        code: CategorieCode,
        date_created: datetime,
        date_updated: datetime,
        id: str,
        libelle: CategorieLibelle,
        ordre: Optional[int],
        terrain: Optional[bool],
    ) -> None:
        self.code = code
        self.date_created = date_created
        self.date_updated = date_updated
        self.id = id
        self.libelle = libelle
        self.ordre = ordre
        self.terrain = terrain

    @staticmethod
    def from_dict(obj: Any) -> "NatureSolClass":
        assert isinstance(obj, dict)
        code = CategorieCode(obj.get("code"))
        date_created = from_datetime(obj.get("date_created"))
        date_updated = from_datetime(obj.get("date_updated"))
        id = from_str(obj.get("id"))
        libelle = CategorieLibelle(obj.get("libelle"))
        ordre = from_union([from_int, from_none], obj.get("ordre"))
        terrain = from_union(
            [from_none, lambda x: from_stringified_bool(from_str(x))],
            obj.get("terrain"),
        )
        return NatureSolClass(
            code, date_created, date_updated, id, libelle, ordre, terrain
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = to_enum(CategorieCode, self.code)
        result["date_created"] = self.date_created.isoformat()
        result["date_updated"] = self.date_updated.isoformat()
        result["id"] = from_str(self.id)
        result["libelle"] = to_enum(CategorieLibelle, self.libelle)
        if self.ordre is not None:
            result["ordre"] = from_union([from_int, from_none], self.ordre)
        if self.terrain is not None:
            result["terrain"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x)
                    ),
                ],
                self.terrain,
            )
        return result


class CodeLigueEnum(Enum):
    ARA = "ARA"
    BFC = "BFC"
    BRE = "BRE"
    COR = "COR"
    CVL = "CVL"
    EMPTY = ""
    GES = "GES"
    GUA = "GUA"
    GUY = "GUY"
    HAN = "HAN"
    HDF = "HDF"
    IDF = "IDF"
    LNB = "LNB"
    MAR = "MAR"
    MAY = "MAY"
    NAQ = "NAQ"
    NCA = "NCA"
    NOR = "NOR"
    OCC = "OCC"
    PDL = "PDL"
    PFR = "PFR"
    REU = "REU"
    SUD = "SUD"
    WEF = "WEF"


class Departement(Enum):
    AIN = "Ain"
    AISNE = "Aisne"
    ALLIER = "Allier"
    ALPES_DE_HAUTE_PROVENCE = "Alpes-de-Haute-Provence"
    ALPES_MARITIMES = "Alpes-maritimes"
    ARDENNES = "Ardennes"
    ARDÈCHE = "Ardèche"
    ARIÈGE = "Ariège"
    AUBE = "Aube"
    AUDE = "Aude"
    AVEYRON = "Aveyron"
    BAS_RHIN = "Bas-rhin"
    BOUCHES_DU_RHÔNE = "Bouches-du-Rhône"
    CALVADOS = "Calvados"
    CANTAL = "Cantal"
    CHARENTE = "Charente"
    CHARENTE_MARITIME = "Charente-maritime"
    CHER = "Cher"
    CORRÈZE = "Corrèze"
    CORSE = "Corse"
    CREUSE = "Creuse"
    CÔTES_D_ARMOR = "Côtes-d'Armor"
    CÔTE_D_OR = "Côte-d'Or"
    DEUX_SÈVRES = "Deux-sèvres"
    DORDOGNE = "Dordogne"
    DOUBS = "Doubs"
    DRÔME = "Drôme"
    ESSONNE = "Essonne"
    EURE = "Eure"
    EURE_ET_LOIR = "Eure-et-loir"
    FINISTÈRE = "Finistère"
    GARD = "Gard"
    GERS = "Gers"
    GIRONDE = "Gironde"
    GUADELOUPE = "Guadeloupe"
    GUYANE = "Guyane"
    HAUTES_ALPES = "Hautes-Alpes"
    HAUTES_PYRÉNÉES = "Hautes-Pyrénées"
    HAUTE_GARONNE = "Haute-garonne"
    HAUTE_LOIRE = "Haute-loire"
    HAUTE_MARNE = "Haute-marne"
    HAUTE_SAVOIE = "Haute-savoie"
    HAUTE_SAÔNE = "Haute-saône"
    HAUTE_VIENNE = "Haute-vienne"
    HAUTS_DE_SEINE = "Hauts-de-Seine"
    HAUT_RHIN = "Haut-rhin"
    HÉRAULT = "Hérault"
    ILLE_ET_VILAINE = "Ille-et-vilaine"
    INDRE = "Indre"
    INDRE_ET_LOIRE = "Indre-et-loire"
    ISÈRE = "Isère"
    JURA = "Jura"
    LANDES = "Landes"
    LA_RÉUNION = "La Réunion"
    LOIRE = "Loire"
    LOIRET = "Loiret"
    LOIRE_ATLANTIQUE = "Loire-atlantique"
    LOIR_ET_CHER = "Loir-et-cher"
    LOT = "Lot"
    LOT_ET_GARONNE = "Lot-et-garonne"
    LOZÈRE = "Lozère"
    MAINE_ET_LOIRE = "Maine-et-loire "
    MANCHE = "Manche"
    MARNE = "Marne"
    MARTINIQUE = "Martinique"
    MAYENNE = "Mayenne"
    MAYOTTE = "Mayotte"
    MEURTHE_ET_MOSELLE = "Meurthe-et-moselle"
    MEUSE = "Meuse"
    MONACO = "Monaco"
    MORBIHAN = "Morbihan"
    MOSELLE = "Moselle"
    NIÈVRE = "Nièvre"
    NORD = "Nord"
    NOUVELLE_CALÉDONIE = "Nouvelle-Calédonie"
    OISE = "Oise"
    ORNE = "Orne"
    PARIS = "Paris"
    PAS_DE_CALAIS = "Pas-de-calais"
    POLYNÉSIE_FRANÇAISE = "Polynésie française"
    PUY_DE_DÔME = "Puy-de-dôme"
    PYRÉNÉES_ATLANTIQUES = "Pyrénées-atlantiques"
    PYRÉNÉES_ORIENTALES = "Pyrénées-orientales"
    RHÔNE = "Rhône"
    SAINT_PIERRE_ET_MIQUELON = "Saint-Pierre-et-Miquelon."
    SARTHE = "Sarthe"
    SAVOIE = "Savoie"
    SAÔNE_ET_LOIRE = "Saône-et-loire"
    SEINE_ET_MARNE = "Seine-et-marne"
    SEINE_MARITIME = "Seine-maritime"
    SEINE_SAINT_DENIS = "Seine-Saint-Denis"
    SOMME = "Somme"
    TARN = "Tarn"
    TARN_ET_GARONNE = "Tarn-et-Garonne"
    TERRITOIRE_DE_BELFORT = "Territoire de Belfort"
    VAL_DE_MARNE = "Val-de-Marne"
    VAL_D_OISE = "Val-d'Oise"
    VAR = "Var"
    VAUCLUSE = "Vaucluse"
    VENDÉE = "Vendée"
    VIENNE = "Vienne"
    VOSGES = "Vosges"
    WALLIS_ET_FUTUNA = "Wallis-et-Futuna"
    YONNE = "Yonne"
    YVELINES = "Yvelines"


class CommuneClubPro:
    code_postal: str
    departement: Departement
    libelle: str

    def __init__(
        self, code_postal: str, departement: Departement, libelle: str
    ) -> None:
        self.code_postal = code_postal
        self.departement = departement
        self.libelle = libelle

    @staticmethod
    def from_dict(obj: Any) -> "CommuneClubPro":
        assert isinstance(obj, dict)
        code_postal = from_str(obj.get("codePostal"))
        departement = Departement(obj.get("departement"))
        libelle = from_str(obj.get("libelle"))
        return CommuneClubPro(code_postal, departement, libelle)

    def to_dict(self) -> dict:
        result: dict = {}
        result["codePostal"] = from_str(self.code_postal)
        result["departement"] = to_enum(Departement, self.departement)
        result["libelle"] = from_str(self.libelle)
        return result


class CompetitionIDCategorie:
    code: CategorieCode
    libelle: CategorieLibelle
    ordre: int

    def __init__(
        self, code: CategorieCode, libelle: CategorieLibelle, ordre: int
    ) -> None:
        self.code = code
        self.libelle = libelle
        self.ordre = ordre

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionIDCategorie":
        assert isinstance(obj, dict)
        code = CategorieCode(obj.get("code"))
        libelle = CategorieLibelle(obj.get("libelle"))
        ordre = from_int(obj.get("ordre"))
        return CompetitionIDCategorie(code, libelle, ordre)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = to_enum(CategorieCode, self.code)
        result["libelle"] = to_enum(CategorieLibelle, self.libelle)
        result["ordre"] = from_int(self.ordre)
        return result


class CompetitionOrigineCategorie:
    ordre: int

    def __init__(self, ordre: int) -> None:
        self.ordre = ordre

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionOrigineCategorie":
        assert isinstance(obj, dict)
        ordre = from_int(obj.get("ordre"))
        return CompetitionOrigineCategorie(ordre)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ordre"] = from_int(self.ordre)
        return result


class CompetitionOrigineTypeCompetition(Enum):
    DIV = "DIV"
    DIV_3_X3 = "DIV_3x3"
    PLAT = "PLAT"


class Engagement:
    id: str

    def __init__(self, id: str) -> None:
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> "Engagement":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        return Engagement(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        return result


class CompetitionOrigineTypeCompetitionGenerique:
    logo: Engagement

    def __init__(self, logo: Engagement) -> None:
        self.logo = logo

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionOrigineTypeCompetitionGenerique":
        assert isinstance(obj, dict)
        logo = Engagement.from_dict(obj.get("logo"))
        return CompetitionOrigineTypeCompetitionGenerique(logo)

    def to_dict(self) -> dict:
        result: dict = {}
        result["logo"] = to_class(Engagement, self.logo)
        return result


class CompetitionOrigine:
    categorie: CompetitionOrigineCategorie
    code: str
    id: str
    nom: str
    slug: str
    type_competition: CompetitionOrigineTypeCompetition
    type_competition_generique: Optional[CompetitionOrigineTypeCompetitionGenerique]

    def __init__(
        self,
        categorie: CompetitionOrigineCategorie,
        code: str,
        id: str,
        nom: str,
        slug: str,
        type_competition: CompetitionOrigineTypeCompetition,
        type_competition_generique: Optional[
            CompetitionOrigineTypeCompetitionGenerique
        ],
    ) -> None:
        self.categorie = categorie
        self.code = code
        self.id = id
        self.nom = nom
        self.slug = slug
        self.type_competition = type_competition
        self.type_competition_generique = type_competition_generique

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionOrigine":
        assert isinstance(obj, dict)
        categorie = CompetitionOrigineCategorie.from_dict(obj.get("categorie"))
        code = from_str(obj.get("code"))
        id = from_str(obj.get("id"))
        nom = from_str(obj.get("nom"))
        slug = from_str(obj.get("slug"))
        type_competition = CompetitionOrigineTypeCompetition(obj.get("typeCompetition"))
        type_competition_generique = from_union(
            [CompetitionOrigineTypeCompetitionGenerique.from_dict, from_none],
            obj.get("typeCompetitionGenerique"),
        )
        return CompetitionOrigine(
            categorie, code, id, nom, slug, type_competition, type_competition_generique
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["categorie"] = to_class(CompetitionOrigineCategorie, self.categorie)
        result["code"] = from_str(self.code)
        result["id"] = from_str(self.id)
        result["nom"] = from_str(self.nom)
        result["slug"] = from_str(self.slug)
        result["typeCompetition"] = to_enum(
            CompetitionOrigineTypeCompetition, self.type_competition
        )
        result["typeCompetitionGenerique"] = from_union(
            [
                lambda x: to_class(CompetitionOrigineTypeCompetitionGenerique, x),
                from_none,
            ],
            self.type_competition_generique,
        )
        return result


class PublicationInternet(Enum):
    AFFICHÉE = "Affichée"
    ASC = "ASC"
    NE_PAS_AFFICHER = "Ne pas afficher"


class SexeEnum(Enum):
    FÉMININ = "Féminin"
    MASCULIN = "Masculin"
    MIXTE = "Mixte"


class CompetitionIDTypeCompetitionEnum(Enum):
    CHAMPIONNAT = "Championnat"
    CHAMPIONNAT_3_X3 = "Championnat 3x3"
    COUPE = "Coupe"
    PLATEAU = "Plateau"


class CompetitionIDTypeCompetitionGenerique:
    logo: Logo

    def __init__(self, logo: Logo) -> None:
        self.logo = logo

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionIDTypeCompetitionGenerique":
        assert isinstance(obj, dict)
        logo = Logo.from_dict(obj.get("logo"))
        return CompetitionIDTypeCompetitionGenerique(logo)

    def to_dict(self) -> dict:
        result: dict = {}
        result["logo"] = to_class(Logo, self.logo)
        return result


class CompetitionID:
    categorie: CompetitionIDCategorie
    code: str
    competition_origine: Optional[CompetitionOrigine]
    competition_origine_nom: str
    creation_en_cours: bool
    id: str
    live_stat: bool
    logo: None
    nom: str
    nom_extended: Optional[str]
    pro: Optional[bool]
    publication_internet: PublicationInternet
    sexe: SexeEnum
    slug: Optional[str]
    type_competition: CompetitionIDTypeCompetitionEnum
    type_competition_generique: Optional[CompetitionIDTypeCompetitionGenerique]

    def __init__(
        self,
        categorie: CompetitionIDCategorie,
        code: str,
        competition_origine: Optional[CompetitionOrigine],
        competition_origine_nom: str,
        creation_en_cours: bool,
        id: str,
        live_stat: bool,
        logo: None,
        nom: str,
        nom_extended: Optional[str],
        pro: Optional[bool],
        publication_internet: PublicationInternet,
        sexe: SexeEnum,
        slug: Optional[str],
        type_competition: CompetitionIDTypeCompetitionEnum,
        type_competition_generique: Optional[CompetitionIDTypeCompetitionGenerique],
    ) -> None:
        self.categorie = categorie
        self.code = code
        self.competition_origine = competition_origine
        self.competition_origine_nom = competition_origine_nom
        self.creation_en_cours = creation_en_cours
        self.id = id
        self.live_stat = live_stat
        self.logo = logo
        self.nom = nom
        self.nom_extended = nom_extended
        self.pro = pro
        self.publication_internet = publication_internet
        self.sexe = sexe
        self.slug = slug
        self.type_competition = type_competition
        self.type_competition_generique = type_competition_generique

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionID":
        assert isinstance(obj, dict)
        categorie = CompetitionIDCategorie.from_dict(obj.get("categorie"))
        code = from_str(obj.get("code"))
        competition_origine = from_union(
            [CompetitionOrigine.from_dict, from_none], obj.get("competition_origine")
        )
        competition_origine_nom = from_str(obj.get("competition_origine_nom"))
        creation_en_cours = from_bool(obj.get("creationEnCours"))
        id = from_str(obj.get("id"))
        live_stat = from_bool(obj.get("liveStat"))
        logo = from_none(obj.get("logo"))
        nom = from_str(obj.get("nom"))
        nom_extended = from_union([from_str, from_none], obj.get("nomExtended"))
        pro = from_union([from_bool, from_none], obj.get("pro"))
        publication_internet = PublicationInternet(obj.get("publicationInternet"))
        sexe = SexeEnum(obj.get("sexe"))
        slug = from_union([from_str, from_none], obj.get("slug"))
        type_competition = CompetitionIDTypeCompetitionEnum(obj.get("typeCompetition"))
        type_competition_generique = from_union(
            [CompetitionIDTypeCompetitionGenerique.from_dict, from_none],
            obj.get("typeCompetitionGenerique"),
        )
        return CompetitionID(
            categorie,
            code,
            competition_origine,
            competition_origine_nom,
            creation_en_cours,
            id,
            live_stat,
            logo,
            nom,
            nom_extended,
            pro,
            publication_internet,
            sexe,
            slug,
            type_competition,
            type_competition_generique,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["categorie"] = to_class(CompetitionIDCategorie, self.categorie)
        result["code"] = from_str(self.code)
        if self.competition_origine is not None:
            result["competition_origine"] = from_union(
                [lambda x: to_class(CompetitionOrigine, x), from_none],
                self.competition_origine,
            )
        result["competition_origine_nom"] = from_str(self.competition_origine_nom)
        result["creationEnCours"] = from_bool(self.creation_en_cours)
        result["id"] = from_str(self.id)
        result["liveStat"] = from_bool(self.live_stat)
        if self.logo is not None:
            result["logo"] = from_none(self.logo)
        result["nom"] = from_str(self.nom)
        if self.nom_extended is not None:
            result["nomExtended"] = from_union([from_str, from_none], self.nom_extended)
        if self.pro is not None:
            result["pro"] = from_union([from_bool, from_none], self.pro)
        result["publicationInternet"] = to_enum(
            PublicationInternet, self.publication_internet
        )
        result["sexe"] = to_enum(SexeEnum, self.sexe)
        if self.slug is not None:
            result["slug"] = from_union([from_str, from_none], self.slug)
        result["typeCompetition"] = to_enum(
            CompetitionIDTypeCompetitionEnum, self.type_competition
        )
        if self.type_competition_generique is not None:
            result["typeCompetitionGenerique"] = from_union(
                [
                    lambda x: to_class(CompetitionIDTypeCompetitionGenerique, x),
                    from_none,
                ],
                self.type_competition_generique,
            )
        return result


class Name(Enum):
    TOURNOIS = "Tournois"


class Folder:
    id: UUID
    name: Name
    parent: None

    def __init__(self, id: UUID, name: Name, parent: None) -> None:
        self.id = id
        self.name = name
        self.parent = parent

    @staticmethod
    def from_dict(obj: Any) -> "Folder":
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        name = Name(obj.get("name"))
        parent = from_none(obj.get("parent"))
        return Folder(id, name, parent)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        result["name"] = to_enum(Name, self.name)
        result["parent"] = from_none(self.parent)
        return result


class Source(Enum):
    FFBB_SERVEUR = "FFBB Serveur"


class Storage(Enum):
    MINIO = "minio"


class DocumentFlyer:
    blurhash: Optional[str]
    category: List[Any]
    charset: None
    created_on: datetime
    credits: None
    date_published: None
    description: None
    duration: None
    embed: None
    ffbbsite_asset_type: None
    ffbbsite_assets_tags: List[Any]
    filename_disk: str
    filename_download: str
    filesize: int
    focal_point_x: None
    focal_point_y: None
    folder: Folder
    gradient_color: str
    gradient_color_bis: None
    height: int
    id: UUID
    is_asset_hidden: bool
    location: None
    md5: str
    metadata: FacetStats
    modified_by: None
    modified_on: datetime
    newsbridge_labels: List[Any]
    newsbridge_media_id: None
    newsbridge_metadatas: None
    newsbridge_mission: None
    newsbridge_name: None
    newsbridge_persons: List[Any]
    newsbridge_recorded_at: None
    order: None
    source: Source
    storage: Storage
    tags: None
    title: str
    tus_data: None
    tus_id: None
    type: AfficheType
    uploaded_by: None
    uploaded_on: datetime
    width: int

    def __init__(
        self,
        blurhash: Optional[str],
        category: List[Any],
        charset: None,
        created_on: datetime,
        credits: None,
        date_published: None,
        description: None,
        duration: None,
        embed: None,
        ffbbsite_asset_type: None,
        ffbbsite_assets_tags: List[Any],
        filename_disk: str,
        filename_download: str,
        filesize: int,
        focal_point_x: None,
        focal_point_y: None,
        folder: Folder,
        gradient_color: str,
        gradient_color_bis: None,
        height: int,
        id: UUID,
        is_asset_hidden: bool,
        location: None,
        md5: str,
        metadata: FacetStats,
        modified_by: None,
        modified_on: datetime,
        newsbridge_labels: List[Any],
        newsbridge_media_id: None,
        newsbridge_metadatas: None,
        newsbridge_mission: None,
        newsbridge_name: None,
        newsbridge_persons: List[Any],
        newsbridge_recorded_at: None,
        order: None,
        source: Source,
        storage: Storage,
        tags: None,
        title: str,
        tus_data: None,
        tus_id: None,
        type: AfficheType,
        uploaded_by: None,
        uploaded_on: datetime,
        width: int,
    ) -> None:
        self.blurhash = blurhash
        self.category = category
        self.charset = charset
        self.created_on = created_on
        self.credits = credits
        self.date_published = date_published
        self.description = description
        self.duration = duration
        self.embed = embed
        self.ffbbsite_asset_type = ffbbsite_asset_type
        self.ffbbsite_assets_tags = ffbbsite_assets_tags
        self.filename_disk = filename_disk
        self.filename_download = filename_download
        self.filesize = filesize
        self.focal_point_x = focal_point_x
        self.focal_point_y = focal_point_y
        self.folder = folder
        self.gradient_color = gradient_color
        self.gradient_color_bis = gradient_color_bis
        self.height = height
        self.id = id
        self.is_asset_hidden = is_asset_hidden
        self.location = location
        self.md5 = md5
        self.metadata = metadata
        self.modified_by = modified_by
        self.modified_on = modified_on
        self.newsbridge_labels = newsbridge_labels
        self.newsbridge_media_id = newsbridge_media_id
        self.newsbridge_metadatas = newsbridge_metadatas
        self.newsbridge_mission = newsbridge_mission
        self.newsbridge_name = newsbridge_name
        self.newsbridge_persons = newsbridge_persons
        self.newsbridge_recorded_at = newsbridge_recorded_at
        self.order = order
        self.source = source
        self.storage = storage
        self.tags = tags
        self.title = title
        self.tus_data = tus_data
        self.tus_id = tus_id
        self.type = type
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.width = width

    @staticmethod
    def from_dict(obj: Any) -> "DocumentFlyer":
        assert isinstance(obj, dict)
        blurhash = from_union([from_none, from_str], obj.get("blurhash"))
        category = from_list(lambda x: x, obj.get("category"))
        charset = from_none(obj.get("charset"))
        created_on = from_datetime(obj.get("created_on"))
        credits = from_none(obj.get("credits"))
        date_published = from_none(obj.get("date_published"))
        description = from_none(obj.get("description"))
        duration = from_none(obj.get("duration"))
        embed = from_none(obj.get("embed"))
        ffbbsite_asset_type = from_none(obj.get("ffbbsite_asset_type"))
        ffbbsite_assets_tags = from_list(lambda x: x, obj.get("ffbbsite_assets_tags"))
        filename_disk = from_str(obj.get("filename_disk"))
        filename_download = from_str(obj.get("filename_download"))
        filesize = int(from_str(obj.get("filesize")))
        focal_point_x = from_none(obj.get("focal_point_x"))
        focal_point_y = from_none(obj.get("focal_point_y"))
        folder = Folder.from_dict(obj.get("folder"))
        gradient_color = from_str(obj.get("gradient_color"))
        gradient_color_bis = from_none(obj.get("gradient_color_bis"))
        height = from_int(obj.get("height"))
        id = UUID(obj.get("id"))
        is_asset_hidden = from_bool(obj.get("is_asset_hidden"))
        location = from_none(obj.get("location"))
        md5 = from_str(obj.get("md5"))
        metadata = FacetStats.from_dict(obj.get("metadata"))
        modified_by = from_none(obj.get("modified_by"))
        modified_on = from_datetime(obj.get("modified_on"))
        newsbridge_labels = from_list(lambda x: x, obj.get("newsbridge_labels"))
        newsbridge_media_id = from_none(obj.get("newsbridge_media_id"))
        newsbridge_metadatas = from_none(obj.get("newsbridge_metadatas"))
        newsbridge_mission = from_none(obj.get("newsbridge_mission"))
        newsbridge_name = from_none(obj.get("newsbridge_name"))
        newsbridge_persons = from_list(lambda x: x, obj.get("newsbridge_persons"))
        newsbridge_recorded_at = from_none(obj.get("newsbridge_recorded_at"))
        order = from_none(obj.get("order"))
        source = Source(obj.get("source"))
        storage = Storage(obj.get("storage"))
        tags = from_none(obj.get("tags"))
        title = from_str(obj.get("title"))
        tus_data = from_none(obj.get("tus_data"))
        tus_id = from_none(obj.get("tus_id"))
        type = AfficheType(obj.get("type"))
        uploaded_by = from_none(obj.get("uploaded_by"))
        uploaded_on = from_datetime(obj.get("uploaded_on"))
        width = from_int(obj.get("width"))
        return DocumentFlyer(
            blurhash,
            category,
            charset,
            created_on,
            credits,
            date_published,
            description,
            duration,
            embed,
            ffbbsite_asset_type,
            ffbbsite_assets_tags,
            filename_disk,
            filename_download,
            filesize,
            focal_point_x,
            focal_point_y,
            folder,
            gradient_color,
            gradient_color_bis,
            height,
            id,
            is_asset_hidden,
            location,
            md5,
            metadata,
            modified_by,
            modified_on,
            newsbridge_labels,
            newsbridge_media_id,
            newsbridge_metadatas,
            newsbridge_mission,
            newsbridge_name,
            newsbridge_persons,
            newsbridge_recorded_at,
            order,
            source,
            storage,
            tags,
            title,
            tus_data,
            tus_id,
            type,
            uploaded_by,
            uploaded_on,
            width,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["blurhash"] = from_union([from_none, from_str], self.blurhash)
        result["category"] = from_list(lambda x: x, self.category)
        result["charset"] = from_none(self.charset)
        result["created_on"] = self.created_on.isoformat()
        result["credits"] = from_none(self.credits)
        result["date_published"] = from_none(self.date_published)
        result["description"] = from_none(self.description)
        result["duration"] = from_none(self.duration)
        result["embed"] = from_none(self.embed)
        result["ffbbsite_asset_type"] = from_none(self.ffbbsite_asset_type)
        result["ffbbsite_assets_tags"] = from_list(
            lambda x: x, self.ffbbsite_assets_tags
        )
        result["filename_disk"] = from_str(self.filename_disk)
        result["filename_download"] = from_str(self.filename_download)
        result["filesize"] = from_str(str(self.filesize))
        result["focal_point_x"] = from_none(self.focal_point_x)
        result["focal_point_y"] = from_none(self.focal_point_y)
        result["folder"] = to_class(Folder, self.folder)
        result["gradient_color"] = from_str(self.gradient_color)
        result["gradient_color_bis"] = from_none(self.gradient_color_bis)
        result["height"] = from_int(self.height)
        result["id"] = str(self.id)
        result["is_asset_hidden"] = from_bool(self.is_asset_hidden)
        result["location"] = from_none(self.location)
        result["md5"] = from_str(self.md5)
        result["metadata"] = to_class(FacetStats, self.metadata)
        result["modified_by"] = from_none(self.modified_by)
        result["modified_on"] = self.modified_on.isoformat()
        result["newsbridge_labels"] = from_list(lambda x: x, self.newsbridge_labels)
        result["newsbridge_media_id"] = from_none(self.newsbridge_media_id)
        result["newsbridge_metadatas"] = from_none(self.newsbridge_metadatas)
        result["newsbridge_mission"] = from_none(self.newsbridge_mission)
        result["newsbridge_name"] = from_none(self.newsbridge_name)
        result["newsbridge_persons"] = from_list(lambda x: x, self.newsbridge_persons)
        result["newsbridge_recorded_at"] = from_none(self.newsbridge_recorded_at)
        result["order"] = from_none(self.order)
        result["source"] = to_enum(Source, self.source)
        result["storage"] = to_enum(Storage, self.storage)
        result["tags"] = from_none(self.tags)
        result["title"] = from_str(self.title)
        result["tus_data"] = from_none(self.tus_data)
        result["tus_id"] = from_none(self.tus_id)
        result["type"] = to_enum(AfficheType, self.type)
        result["uploaded_by"] = from_none(self.uploaded_by)
        result["uploaded_on"] = self.uploaded_on.isoformat()
        result["width"] = from_int(self.width)
        return result


class Etat(Enum):
    A = "A"


class Geo:
    lat: float
    lng: float

    def __init__(self, lat: float, lng: float) -> None:
        self.lat = lat
        self.lng = lng

    @staticmethod
    def from_dict(obj: Any) -> "Geo":
        assert isinstance(obj, dict)
        lat = from_float(obj.get("lat"))
        lng = from_float(obj.get("lng"))
        return Geo(lat, lng)

    def to_dict(self) -> dict:
        result: dict = {}
        result["lat"] = to_float(self.lat)
        result["lng"] = to_float(self.lng)
        return result


class IDEngagementEquipe:
    id: str
    logo: None
    nom_usuel: Optional[str]

    def __init__(self, id: str, logo: None, nom_usuel: Optional[str]) -> None:
        self.id = id
        self.logo = logo
        self.nom_usuel = nom_usuel

    @staticmethod
    def from_dict(obj: Any) -> "IDEngagementEquipe":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        logo = from_none(obj.get("logo"))
        nom_usuel = from_union([from_none, from_str], obj.get("nomUsuel"))
        return IDEngagementEquipe(id, logo, nom_usuel)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["logo"] = from_none(self.logo)
        result["nomUsuel"] = from_union([from_none, from_str], self.nom_usuel)
        return result


class NomClubPro(Enum):
    AIX_MAURIENNE_SAVOIE_BASKET = "AIX MAURIENNE SAVOIE BASKET"
    ALLIANCE_SPORT_ALSACE = "ALLIANCE SPORT ALSACE"
    ALM_EVREUX_BASKET = "ALM EVREUX BASKET"
    AMBITIONS_GIRONDINES = "AMBITIONS GIRONDINES"
    ASVEL_BASKET_SASP = "ASVEL BASKET (SASP)"
    AS_MONACO_BASKET_BALL_S_A = "AS MONACO BASKET-BALL S.A."
    AURORE_VITRE_BASKET_BRETAGNE = "AURORE VITRE BASKET BRETAGNE"
    BASKET_CLUB_MARITIME_GRAVELINES_GRAND_FORT_PHILIPPE = (
        "BASKET CLUB MARITIME GRAVELINES - GRAND FORT PHILIPPE"
    )
    BASKET_LANDES_SASP = "BASKET LANDES SASP"
    BLMA = "BLMA"
    BOULAZAC_BASKET_DORDOGNE_PRO = "BOULAZAC BASKET DORDOGNE PRO"
    BOULOGNE_LEVALLOIS_METROPOLITANS_92 = "BOULOGNE LEVALLOIS METROPOLITANS 92"
    BOURGES_BASKET = "BOURGES BASKET"
    CAEN_BASKET_CALVADOS = "CAEN BASKET CALVADOS"
    CEP_LORIENT_BREIZH_BASKET = "CEP LORIENT BREIZH BASKET"
    CHOLET_BASKET = "CHOLET BASKET"
    C_CHARTRES_METROPOLE_BASKET = "C'CHARTRES METROPOLE BASKET"
    ELAN_BEARNAIS_PAU_LACQ_ORTHEZ = "ELAN BEARNAIS PAU LACQ ORTHEZ"
    EMPTY = ""
    ESB_VILLENEUVE_D_ASCQ_LILLE_METROPOLE = "ESB VILLENEUVE D'ASCQ LILLE METROPOLE"
    JEANNE_D_ARC_DE_VICHY = "JEANNE D'ARC DE VICHY"
    JSA_BORDEAUX_METROPOLE_BASKET = "JSA BORDEAUX METROPOLE BASKET"
    J_L_BOURG_BASKET = "J.L. BOURG BASKET "
    LANDERNEAU_BRETAGNE_BASKET_HN = "LANDERNEAU BRETAGNE BASKET HN"
    LA_CHARITE_BASKET_58 = "LA CHARITE BASKET 58"
    LEVALLOIS_BASKETBALL = "LEVALLOIS BASKETBALL"
    LE_MANS_SARTHE_BASKET = "LE MANS SARTHE BASKET"
    LILLE_METROPOLE_BASKET_SASP = "LILLE METROPOLE BASKET SASP"
    LIMOGES_CSP_SASP = "LIMOGES CSP (SASP)"
    LYONSO_BASKET = "LYONSO BASKET"
    LYON_ASVEL_FEMININ = "LYON ASVEL FEMININ"
    MULHOUSE_BASKET_AGGLOMERATION = "MULHOUSE BASKET AGGLOMERATION"
    NANTERRE_92 = "NANTERRE 92"
    NANTES_BASKET_HERMINE = "NANTES BASKET HERMINE"
    ORLEANS_LOIRET_BASKET = "ORLEANS LOIRET BASKET"
    PARIS_BASKETBALL = "PARIS BASKETBALL"
    POITIERS_BASKET_86 = "POITIERS BASKET 86"
    RAC_BASKET_PREMIERE = "RAC BASKET PREMIERE"
    ROUEN_METROPOLE_BASKET = "ROUEN METROPOLE BASKET"
    SAINT_AMAND_HAINAUT_BASKET = "SAINT-AMAND HAINAUT BASKET"
    SAINT_VALLIER_BASKET_DRÔME = "SAINT-VALLIER BASKET DRÔME"
    SAOS_CHORALE_DE_ROANNE_BASKET = "SAOS CHORALE DE ROANNE BASKET"
    SASP_ADA_BLOIS_BASKET = "SASP ADA BLOIS BASKET"
    SASP_BC_ORCHIES = "SASP BC ORCHIES"
    SASP_ESSM_LE_PORTEL_BASKET_BALL_COTE_D_OPALE = (
        "SASP ESSM LE PORTEL BASKET BALL COTE D'OPALE"
    )
    SASP_JDA_DIJON_BASKET = "SASP JDA DIJON BASKET"
    SASP_SAINT_QUENTIN_BASKET_BALL = "SASP - SAINT QUENTIN BASKET BALL"
    SASP_SAINT_THOMAS_BASKET_LE_HAVRE = "SASP SAINT THOMAS BASKET LE HAVRE"
    SASP_SLUC_NANCY_BASKET = "SASP SLUC NANCY BASKET"
    SAS_CCRB_PRO = "SAS CCRB PRO"
    SAS_FOS_PROVENCE_BASKET = "SAS FOS PROVENCE BASKET"
    SAS_SAINT_CHAMOND_BASKET_VALLÉE_DU_GIER = "SAS Saint Chamond Basket Vallée du Gier"
    SAS_STADE_ROCHELAIS_RUPELLA = "SAS STADE ROCHELAIS RUPELLA"
    SA_OLYMPIQUE_ANTIBES_JUAN_LES_PINS_COTE_D_AZUR = (
        "SA OLYMPIQUE ANTIBES JUAN LES PINS COTE D'AZUR"
    )
    SEM_ELAN_CHALON = "SEM ELAN CHALON"
    SIG_STRASBOURG = "SIG STRASBOURG"
    TARBES_GESPE_BIGORRE = "TARBES GESPE BIGORRE"
    TOULOUSE_METROPOLE_BASKET_SAS = "TOULOUSE METROPOLE BASKET SAS"
    TOURS_METROPOLE_BASKET = "TOURS METROPOLE BASKET"
    UJAP_QUIMPER_29 = "UJAP QUIMPER 29"
    VANVES_GPSO_BASKET = "VANVES GPSO BASKET"


class Jour(Enum):
    DIMANCHE = "dimanche"
    JEUDI = "jeudi"
    LUNDI = "lundi"
    MARDI = "mardi"
    MERCREDI = "mercredi"
    SAMEDI = "samedi"
    VENDREDI = "vendredi"


class Label(Enum):
    BASKET_INCLUSIF = "Basket Inclusif"
    BASKET_SANTÉ_CONFORT = "Basket Santé Confort"
    BASKET_SANTÉ_DÉCOUVERTE = "Basket Santé Découverte"
    BASKET_SANTÉ_RÉSOLUTIONS = "Basket Santé Résolutions"
    BASKE_TONIK = "BaskeTonik"
    BASKE_TONIK_FORME = "BaskeTonik forme"
    DÉCOUVERTE_BASKET_INCLUSIF = "Découverte Basket Inclusif"
    DÉCOUVERTE_MICRO_BASKET = "Découverte Micro Basket"
    EMPTY = ""
    MICRO_BASKET = "Micro Basket"


class Labellisation(Enum):
    BASKET_INCLUSIF = "Basket Inclusif"
    BASKET_INCLUSIF_DÉCOUVERTE = "Basket Inclusif / Découverte"
    BASKET_SANTÉ_CONFORT = "Basket Santé / Confort"
    BASKET_SANTÉ_DÉCOUVERTE = "Basket Santé / Découverte"
    BASKET_SANTÉ_RÉSOLUTIONS = "Basket Santé / Résolutions"
    BASKE_TONIK_DÉCOUVERTE = "BaskeTonik / Découverte"
    BASKE_TONIK_FORME = "BaskeTonik / Forme"
    BASKE_TONIK_NIVEAU_1 = "BaskeTonik / Niveau 1"
    EFMB2 = "EFMB2"
    EFMB3 = "EFMB3"
    LABEL_FFBB_CITOYEN_MAIF_1_ÉTOILE = "Label FFBB Citoyen MAIF 1 étoile"
    LABEL_FFBB_CITOYEN_MAIF_2_ÉTOILES = "Label FFBB Citoyen MAIF 2 étoiles"
    LABEL_FFBB_CITOYEN_MAIF_3_ÉTOILES = "Label FFBB Citoyen MAIF 3 étoiles"
    MICRO_BASKET = "Micro Basket"
    MICRO_BASKET_DÉCOUVERTE = "Micro Basket / Découverte"


class NiveauEnum(Enum):
    DÉPARTEMENTAL = "Départemental"
    HANDIBASKET = "Handibasket"
    INTERNATIONAL = "International"
    NATIONAL = "National"
    PRO = "Pro"
    RÉGIONAL = "Régional"


class Objectif(Enum):
    ACCOMPAGNEMENT = "Accompagnement"
    CURATIF = "Curatif"
    PRÉVENTIF = "Préventif"


class OffresPratique(Enum):
    BASKET_INCLUSIF = "Basket Inclusif"
    BASKET_SANTÉ = "Basket Santé"
    BASKE_TONIK = "BaskeTonik"
    COMPÉTITION_3_X3 = "Compétition 3x3"
    COMPÉTITION_5_X5 = "Compétition 5x5"
    COMPÉTITION_MINI_BASKET = "Compétition MiniBasket"
    ENTREPRISE_3_X3 = "Entreprise 3x3"
    ENTREPRISE_5_X5 = "Entreprise 5x5"
    LOISIR_3_X3 = "Loisir 3x3"
    LOISIR_5_X5 = "Loisir 5x5"
    MICRO_BASKET = "Micro Basket"


class Nom(Enum):
    LIGUE_NATIONALE_DE_BASKET_BALL = "LIGUE NATIONALE DE BASKET-BALL"
    LIGUE_REGIONALE_DES_HAUTS_DE_FRANCE_DE_BASKET_BALL = (
        "LIGUE REGIONALE DES HAUTS-DE-FRANCE DE BASKET-BALL"
    )
    LIGUE_REGIONALE_DES_PAYS_DE_LA_LOIRE_DE_BASKET_BALL = (
        "LIGUE REGIONALE DES PAYS-DE-LA-LOIRE DE BASKET-BALL"
    )
    LIGUE_REGIONALE_DE_BOURGOGNE_FRANCHE_COMTE_DE_BASKET_BALL = (
        "LIGUE REGIONALE DE BOURGOGNE-FRANCHE-COMTE DE BASKET-BALL"
    )
    LIGUE_REGIONALE_DE_BRETAGNE_DE_BASKET_BALL = (
        "LIGUE REGIONALE DE BRETAGNE DE BASKET-BALL"
    )
    LIGUE_REGIONALE_DE_CORSE_DE_BASKET_BALL = "LIGUE REGIONALE DE CORSE DE BASKET-BALL"
    LIGUE_REGIONALE_DE_GUADELOUPE_DE_BASKET_BALL = (
        "LIGUE REGIONALE DE GUADELOUPE DE BASKET-BALL"
    )
    LIGUE_REGIONALE_DE_GUYANE_DE_BASKET_BALL = (
        "LIGUE REGIONALE DE GUYANE DE BASKET-BALL"
    )
    LIGUE_REGIONALE_DE_HANDI_DE_BASKET_BALL = "LIGUE REGIONALE DE HANDI DE BASKET-BALL"
    LIGUE_REGIONALE_DE_LA_REUNION_DE_BASKET_BALL = (
        "LIGUE REGIONALE DE LA REUNION DE BASKET-BALL"
    )
    LIGUE_REGIONALE_DE_MARTINIQUE_DE_BASKET_BALL = (
        "LIGUE REGIONALE DE MARTINIQUE DE BASKET-BALL"
    )
    LIGUE_REGIONALE_DE_MAYOTTE_DE_BASKET_BALL = (
        "LIGUE REGIONALE DE MAYOTTE DE BASKET-BALL"
    )
    LIGUE_REGIONALE_DE_NORMANDIE_DE_BASKET_BALL = (
        "LIGUE REGIONALE DE NORMANDIE DE BASKET-BALL"
    )
    LIGUE_REGIONALE_DE_NOUVELLE_AQUITAINE_DE_BASKET_BALL = (
        "LIGUE REGIONALE DE NOUVELLE-AQUITAINE DE BASKET-BALL"
    )
    LIGUE_REGIONALE_DE_NOUVELLE_CALEDONIE_DE_BASKET_BALL = (
        "LIGUE REGIONALE DE NOUVELLE-CALEDONIE DE BASKET-BALL"
    )
    LIGUE_REGIONALE_DE_POLYNESIE_FRANCAISE_DE_BASKET_BALL = (
        "LIGUE REGIONALE DE POLYNESIE-FRANCAISE DE BASKET-BALL"
    )
    LIGUE_REGIONALE_DE_WALLIS_ET_FUTUNA_DE_BASKET_BALL = (
        "LIGUE REGIONALE DE WALLIS-ET-FUTUNA DE BASKET-BALL"
    )
    LIGUE_REGIONALE_DU_CENTRE_VAL_DE_LOIRE_DE_BASKET_BALL = (
        "LIGUE REGIONALE DU CENTRE-VAL-DE-LOIRE DE BASKET-BALL"
    )
    LIGUE_REGIONALE_DU_SUD_DE_BASKET_BALL = "LIGUE REGIONALE DU SUD DE BASKET-BALL"
    LIGUE_REGIONALE_D_AUVERGNE_RHÔNE_ALPES_DE_BASKET_BALL = (
        "LIGUE REGIONALE D'AUVERGNE-RHÔNE-ALPES DE BASKET-BALL"
    )
    LIGUE_REGIONALE_D_ILE_DE_FRANCE_DE_BASKET_BALL = (
        "LIGUE REGIONALE D'ILE-DE-FRANCE DE BASKET-BALL"
    )
    LIGUE_REGIONALE_D_OCCITANIE_DE_BASKET_BALL = (
        "LIGUE REGIONALE D'OCCITANIE DE BASKET-BALL"
    )
    LIGUE_REGIONALE_GRAND_EST_DE_BASKET_BALL = (
        "LIGUE REGIONALE GRAND EST DE BASKET-BALL"
    )


class OrganismeIDPereType(Enum):
    C = "C"
    COMITÉ = "Comité"
    F = "F"
    FÉDÉRATION = "Fédération"
    L = "L"
    LIGUE = "Ligue"


class OrganisateurOrganismeIDPere:
    code: CodeLigueEnum
    id: Optional[str]
    nom: Optional[Nom]
    type: Optional[OrganismeIDPereType]

    def __init__(
        self,
        code: CodeLigueEnum,
        id: Optional[str],
        nom: Optional[Nom],
        type: Optional[OrganismeIDPereType],
    ) -> None:
        self.code = code
        self.id = id
        self.nom = nom
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> "OrganisateurOrganismeIDPere":
        assert isinstance(obj, dict)
        code = CodeLigueEnum(obj.get("code"))
        id = from_union([from_str, from_none], obj.get("id"))
        nom = from_union([Nom, from_none], obj.get("nom"))
        type = from_union([OrganismeIDPereType, from_none], obj.get("type"))
        return OrganisateurOrganismeIDPere(code, id, nom, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = to_enum(CodeLigueEnum, self.code)
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.nom is not None:
            result["nom"] = from_union([lambda x: to_enum(Nom, x), from_none], self.nom)
        if self.type is not None:
            result["type"] = from_union(
                [lambda x: to_enum(OrganismeIDPereType, x), from_none], self.type
            )
        return result


class Organisateur:
    adresse: Optional[str]
    adresse_club_pro: None
    cartographie: Optional[str]
    code: str
    commune: Optional[str]
    commune_club_pro: None
    competitions: Optional[List[str]]
    date_created: Optional[datetime]
    date_updated: Optional[datetime]
    date_affiliation: None
    engagements: Optional[List[Any]]
    entreprise: Optional[bool]
    handibasket: Optional[bool]
    hors_association: Optional[bool]
    id: str
    labellisation: Optional[List[Any]]
    logo: Optional[UUID]
    logo_base64: None
    mail: Optional[str]
    membres: Optional[List[int]]
    nom: str
    nom_simple: Optional[str]
    nom_club_pro: Optional[str]
    offres_pratiques: Optional[List[Any]]
    omnisport: Optional[bool]
    organisme_id_pere: Optional[OrganisateurOrganismeIDPere]
    organismes_fils: Optional[List[int]]
    saison_en_cours: Optional[bool]
    salle: None
    telephone: Optional[str]
    type: OrganismeIDPereType
    type_association: None
    url_competition: Optional[str]
    url_site_web: Optional[str]

    def __init__(
        self,
        adresse: Optional[str],
        adresse_club_pro: None,
        cartographie: Optional[str],
        code: str,
        commune: Optional[str],
        commune_club_pro: None,
        competitions: Optional[List[str]],
        date_created: Optional[datetime],
        date_updated: Optional[datetime],
        date_affiliation: None,
        engagements: Optional[List[Any]],
        entreprise: Optional[bool],
        handibasket: Optional[bool],
        hors_association: Optional[bool],
        id: str,
        labellisation: Optional[List[Any]],
        logo: Optional[UUID],
        logo_base64: None,
        mail: Optional[str],
        membres: Optional[List[int]],
        nom: str,
        nom_simple: Optional[str],
        nom_club_pro: Optional[str],
        offres_pratiques: Optional[List[Any]],
        omnisport: Optional[bool],
        organisme_id_pere: Optional[OrganisateurOrganismeIDPere],
        organismes_fils: Optional[List[int]],
        saison_en_cours: Optional[bool],
        salle: None,
        telephone: Optional[str],
        type: OrganismeIDPereType,
        type_association: None,
        url_competition: Optional[str],
        url_site_web: Optional[str],
    ) -> None:
        self.adresse = adresse
        self.adresse_club_pro = adresse_club_pro
        self.cartographie = cartographie
        self.code = code
        self.commune = commune
        self.commune_club_pro = commune_club_pro
        self.competitions = competitions
        self.date_created = date_created
        self.date_updated = date_updated
        self.date_affiliation = date_affiliation
        self.engagements = engagements
        self.entreprise = entreprise
        self.handibasket = handibasket
        self.hors_association = hors_association
        self.id = id
        self.labellisation = labellisation
        self.logo = logo
        self.logo_base64 = logo_base64
        self.mail = mail
        self.membres = membres
        self.nom = nom
        self.nom_simple = nom_simple
        self.nom_club_pro = nom_club_pro
        self.offres_pratiques = offres_pratiques
        self.omnisport = omnisport
        self.organisme_id_pere = organisme_id_pere
        self.organismes_fils = organismes_fils
        self.saison_en_cours = saison_en_cours
        self.salle = salle
        self.telephone = telephone
        self.type = type
        self.type_association = type_association
        self.url_competition = url_competition
        self.url_site_web = url_site_web

    @staticmethod
    def from_dict(obj: Any) -> "Organisateur":
        assert isinstance(obj, dict)
        adresse = from_union([from_str, from_none], obj.get("adresse"))
        adresse_club_pro = from_none(obj.get("adresseClubPro"))
        cartographie = from_union([from_str, from_none], obj.get("cartographie"))
        code = from_str(obj.get("code"))
        commune = from_union([from_str, from_none], obj.get("commune"))
        commune_club_pro = from_none(obj.get("communeClubPro"))
        competitions = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("competitions")
        )
        date_created = from_union([from_datetime, from_none], obj.get("date_created"))
        date_updated = from_union([from_datetime, from_none], obj.get("date_updated"))
        date_affiliation = from_none(obj.get("dateAffiliation"))
        engagements = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], obj.get("engagements")
        )
        entreprise = from_union([from_bool, from_none], obj.get("entreprise"))
        handibasket = from_union([from_bool, from_none], obj.get("handibasket"))
        hors_association = from_union(
            [from_bool, from_none], obj.get("horsAssociation")
        )
        id = from_str(obj.get("id"))
        labellisation = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], obj.get("labellisation")
        )
        logo = from_union([from_none, lambda x: UUID(x)], obj.get("logo"))
        logo_base64 = from_none(obj.get("logo_base64"))
        mail = from_union([from_str, from_none], obj.get("mail"))
        membres = from_union(
            [lambda x: from_list(lambda x: int(from_str(x)), x), from_none],
            obj.get("membres"),
        )
        nom = from_str(obj.get("nom"))
        nom_simple = from_union([from_none, from_str], obj.get("nom_simple"))
        nom_club_pro = from_union([from_str, from_none], obj.get("nomClubPro"))
        offres_pratiques = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], obj.get("offresPratiques")
        )
        omnisport = from_union([from_bool, from_none], obj.get("omnisport"))
        organisme_id_pere = from_union(
            [OrganisateurOrganismeIDPere.from_dict, from_none],
            obj.get("organisme_id_pere"),
        )
        organismes_fils = from_union(
            [lambda x: from_list(lambda x: int(from_str(x)), x), from_none],
            obj.get("organismes_fils"),
        )
        saison_en_cours = from_union([from_bool, from_none], obj.get("saison_en_cours"))
        salle = from_none(obj.get("salle"))
        telephone = from_union([from_str, from_none], obj.get("telephone"))
        type = OrganismeIDPereType(obj.get("type"))
        type_association = from_none(obj.get("type_association"))
        url_competition = from_union([from_none, from_str], obj.get("url_competition"))
        url_site_web = from_union([from_str, from_none], obj.get("urlSiteWeb"))
        return Organisateur(
            adresse,
            adresse_club_pro,
            cartographie,
            code,
            commune,
            commune_club_pro,
            competitions,
            date_created,
            date_updated,
            date_affiliation,
            engagements,
            entreprise,
            handibasket,
            hors_association,
            id,
            labellisation,
            logo,
            logo_base64,
            mail,
            membres,
            nom,
            nom_simple,
            nom_club_pro,
            offres_pratiques,
            omnisport,
            organisme_id_pere,
            organismes_fils,
            saison_en_cours,
            salle,
            telephone,
            type,
            type_association,
            url_competition,
            url_site_web,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.adresse is not None:
            result["adresse"] = from_union([from_str, from_none], self.adresse)
        if self.adresse_club_pro is not None:
            result["adresseClubPro"] = from_none(self.adresse_club_pro)
        if self.cartographie is not None:
            result["cartographie"] = from_union(
                [from_str, from_none], self.cartographie
            )
        result["code"] = from_str(self.code)
        if self.commune is not None:
            result["commune"] = from_union([from_str, from_none], self.commune)
        if self.commune_club_pro is not None:
            result["communeClubPro"] = from_none(self.commune_club_pro)
        if self.competitions is not None:
            result["competitions"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.competitions
            )
        if self.date_created is not None:
            result["date_created"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_created
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_updated
            )
        if self.date_affiliation is not None:
            result["dateAffiliation"] = from_none(self.date_affiliation)
        if self.engagements is not None:
            result["engagements"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.engagements
            )
        if self.entreprise is not None:
            result["entreprise"] = from_union([from_bool, from_none], self.entreprise)
        if self.handibasket is not None:
            result["handibasket"] = from_union([from_bool, from_none], self.handibasket)
        if self.hors_association is not None:
            result["horsAssociation"] = from_union(
                [from_bool, from_none], self.hors_association
            )
        result["id"] = from_str(self.id)
        if self.labellisation is not None:
            result["labellisation"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.labellisation
            )
        if self.logo is not None:
            result["logo"] = from_union([from_none, lambda x: str(x)], self.logo)
        if self.logo_base64 is not None:
            result["logo_base64"] = from_none(self.logo_base64)
        if self.mail is not None:
            result["mail"] = from_union([from_str, from_none], self.mail)
        if self.membres is not None:
            result["membres"] = from_union(
                [
                    lambda x: from_list(lambda x: from_str((lambda x: str(x))(x)), x),
                    from_none,
                ],
                self.membres,
            )
        result["nom"] = from_str(self.nom)
        if self.nom_simple is not None:
            result["nom_simple"] = from_union([from_none, from_str], self.nom_simple)
        if self.nom_club_pro is not None:
            result["nomClubPro"] = from_union([from_str, from_none], self.nom_club_pro)
        if self.offres_pratiques is not None:
            result["offresPratiques"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.offres_pratiques
            )
        if self.omnisport is not None:
            result["omnisport"] = from_union([from_bool, from_none], self.omnisport)
        if self.organisme_id_pere is not None:
            result["organisme_id_pere"] = from_union(
                [lambda x: to_class(OrganisateurOrganismeIDPere, x), from_none],
                self.organisme_id_pere,
            )
        if self.organismes_fils is not None:
            result["organismes_fils"] = from_union(
                [
                    lambda x: from_list(lambda x: from_str((lambda x: str(x))(x)), x),
                    from_none,
                ],
                self.organismes_fils,
            )
        if self.saison_en_cours is not None:
            result["saison_en_cours"] = from_union(
                [from_bool, from_none], self.saison_en_cours
            )
        if self.salle is not None:
            result["salle"] = from_none(self.salle)
        if self.telephone is not None:
            result["telephone"] = from_union([from_str, from_none], self.telephone)
        result["type"] = to_enum(OrganismeIDPereType, self.type)
        if self.type_association is not None:
            result["type_association"] = from_none(self.type_association)
        if self.url_competition is not None:
            result["url_competition"] = from_union(
                [from_none, from_str], self.url_competition
            )
        if self.url_site_web is not None:
            result["urlSiteWeb"] = from_union([from_str, from_none], self.url_site_web)
        return result


class HitOrganismeIDPere:
    adresse: Optional[str]
    code: str
    commune: str
    id: str
    ligue_code: Optional[str]
    nom: str
    nom_simple: Optional[str]
    organisme_id_pere: Optional[OrganisateurOrganismeIDPere]
    type: OrganismeIDPereType

    def __init__(
        self,
        adresse: Optional[str],
        code: str,
        commune: str,
        id: str,
        ligue_code: Optional[str],
        nom: str,
        nom_simple: Optional[str],
        organisme_id_pere: Optional[OrganisateurOrganismeIDPere],
        type: OrganismeIDPereType,
    ) -> None:
        self.adresse = adresse
        self.code = code
        self.commune = commune
        self.id = id
        self.ligue_code = ligue_code
        self.nom = nom
        self.nom_simple = nom_simple
        self.organisme_id_pere = organisme_id_pere
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> "HitOrganismeIDPere":
        assert isinstance(obj, dict)
        adresse = from_union([from_none, from_str], obj.get("adresse"))
        code = from_str(obj.get("code"))
        commune = from_str(obj.get("commune"))
        id = from_str(obj.get("id"))
        ligue_code = from_union([from_str, from_none], obj.get("ligueCode"))
        nom = from_str(obj.get("nom"))
        nom_simple = from_union([from_none, from_str], obj.get("nom_simple"))
        organisme_id_pere = from_union(
            [OrganisateurOrganismeIDPere.from_dict, from_none],
            obj.get("organisme_id_pere"),
        )
        type = OrganismeIDPereType(obj.get("type"))
        return HitOrganismeIDPere(
            adresse,
            code,
            commune,
            id,
            ligue_code,
            nom,
            nom_simple,
            organisme_id_pere,
            type,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["adresse"] = from_union([from_none, from_str], self.adresse)
        result["code"] = from_str(self.code)
        result["commune"] = from_str(self.commune)
        result["id"] = from_str(self.id)
        if self.ligue_code is not None:
            result["ligueCode"] = from_union([from_str, from_none], self.ligue_code)
        result["nom"] = from_str(self.nom)
        result["nom_simple"] = from_union([from_none, from_str], self.nom_simple)
        result["organisme_id_pere"] = from_union(
            [lambda x: to_class(OrganisateurOrganismeIDPere, x), from_none],
            self.organisme_id_pere,
        )
        result["type"] = to_enum(OrganismeIDPereType, self.type)
        return result


class PhaseCode(Enum):
    B1 = "B1"
    B2 = "B2"
    F = "F"
    J2 = "J2"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"
    P6 = "P6"
    P7 = "P7"
    T1 = "T1"
    T2 = "T2"
    T3 = "T3"
    THE_116 = "1/16"
    THE_12 = "1/2"
    THE_132 = "1/32"
    THE_14 = "1/4"
    THE_164 = "1/64"
    THE_18 = "1/8"
    TP = "TP"


class Poule:
    engagements: List[Engagement]
    id: str
    nom: str

    def __init__(self, engagements: List[Engagement], id: str, nom: str) -> None:
        self.engagements = engagements
        self.id = id
        self.nom = nom

    @staticmethod
    def from_dict(obj: Any) -> "Poule":
        assert isinstance(obj, dict)
        engagements = from_list(Engagement.from_dict, obj.get("engagements"))
        id = from_str(obj.get("id"))
        nom = from_str(obj.get("nom"))
        return Poule(engagements, id, nom)

    def to_dict(self) -> dict:
        result: dict = {}
        result["engagements"] = from_list(
            lambda x: to_class(Engagement, x), self.engagements
        )
        result["id"] = from_str(self.id)
        result["nom"] = from_str(self.nom)
        return result


class Pratique(Enum):
    HANDISPORT = "Handisport"
    THE_3_X3 = "3x3"
    THE_5_X5 = "5x5"


class SaisonCode(Enum):
    THE_2425 = "24-25"


class Saison:
    code: SaisonCode

    def __init__(self, code: SaisonCode) -> None:
        self.code = code

    @staticmethod
    def from_dict(obj: Any) -> "Saison":
        assert isinstance(obj, dict)
        code = SaisonCode(obj.get("code"))
        return Saison(code)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = to_enum(SaisonCode, self.code)
        return result


class HitStatus(Enum):
    PUBLISHED = "published"


class TournoiTypeEnum(Enum):
    OPEN_PLUS = "Open Plus"
    OPEN_PLUS_ACCESS = "Open Plus Access"
    OPEN_START = "Open Start"


class TournoiTypes3X3LibelleEnum(Enum):
    OPEN_PLUS_ACCESS_JUNIOR_LEAGUE_3_X3 = "Open Plus Access - Junior league 3x3"
    OPEN_PLUS_ACCESS_SUPER_LEAGUE_3_X3 = "Open Plus Access - Super league 3x3"
    OPEN_PLUS_JUNIOR_LEAGUE_3_X3 = "Open Plus - Junior league 3x3"
    OPEN_PLUS_SUPER_LEAGUE_3_X3 = "Open Plus - Super league 3x3"
    OPEN_START_JUNIOR_LEAGUE_3_X3 = "Open Start - Junior league 3x3"
    OPEN_START_SUPER_LEAGUE_3_X3 = "Open Start - Super league 3x3"


class TypeLeague(Enum):
    JUNIOR = "junior"
    SENIOR = "senior"


class TournoiTypes3X3:
    libelle: TournoiTypes3X3LibelleEnum
    logo: UUID
    type_league: TypeLeague
    type_tournois: int

    def __init__(
        self,
        libelle: TournoiTypes3X3LibelleEnum,
        logo: UUID,
        type_league: TypeLeague,
        type_tournois: int,
    ) -> None:
        self.libelle = libelle
        self.logo = logo
        self.type_league = type_league
        self.type_tournois = type_tournois

    @staticmethod
    def from_dict(obj: Any) -> "TournoiTypes3X3":
        assert isinstance(obj, dict)
        libelle = TournoiTypes3X3LibelleEnum(obj.get("libelle"))
        logo = UUID(obj.get("logo"))
        type_league = TypeLeague(obj.get("type_league"))
        type_tournois = int(from_str(obj.get("type_tournois")))
        return TournoiTypes3X3(libelle, logo, type_league, type_tournois)

    def to_dict(self) -> dict:
        result: dict = {}
        result["libelle"] = to_enum(TournoiTypes3X3LibelleEnum, self.libelle)
        result["logo"] = str(self.logo)
        result["type_league"] = to_enum(TypeLeague, self.type_league)
        result["type_tournois"] = from_str(str(self.type_tournois))
        return result


class HitType(Enum):
    BASKET_INCLUSIF = "Basket Inclusif"
    BASKET_SANTÉ = "Basket Santé"
    BASKE_TONIK = "BaskeTonik"
    CENTRE_GÉNÉRATION_BASKET = "Centre Génération Basket"
    COMITÉ = "Comité"
    FÉDÉRATION = "Fédération"
    GROUPEMENT = "Groupement"
    LIGUE = "Ligue"
    MICRO_BASKET = "Micro Basket"
    SALLE = "Salle"
    TERRAIN = "Terrain"


class TypeAssociationCode(Enum):
    C = "C"
    K = "K"
    P = "P"
    U = "U"


class TypeAssociationLibelleEnum(Enum):
    ASSOCIATION_CLUB_PROFESSIONNEL = "Association club professionnel"
    CLUB = "Club"
    ENTENTE = "Entente"
    SALLE = "Salle"
    UNION = "Union"


class TypeAssociation:
    code: Optional[TypeAssociationCode]
    libelle: TypeAssociationLibelleEnum

    def __init__(
        self, code: Optional[TypeAssociationCode], libelle: TypeAssociationLibelleEnum
    ) -> None:
        self.code = code
        self.libelle = libelle

    @staticmethod
    def from_dict(obj: Any) -> "TypeAssociation":
        assert isinstance(obj, dict)
        code = from_union([TypeAssociationCode, from_none], obj.get("code"))
        libelle = TypeAssociationLibelleEnum(obj.get("libelle"))
        return TypeAssociation(code, libelle)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = from_union(
                [lambda x: to_enum(TypeAssociationCode, x), from_none], self.code
            )
        result["libelle"] = to_enum(TypeAssociationLibelleEnum, self.libelle)
        return result


class HitTypeCompetitionGenerique:
    id: str
    logo: Logo

    def __init__(self, id: str, logo: Logo) -> None:
        self.id = id
        self.logo = logo

    @staticmethod
    def from_dict(obj: Any) -> "HitTypeCompetitionGenerique":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        logo = Logo.from_dict(obj.get("logo"))
        return HitTypeCompetitionGenerique(id, logo)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["logo"] = to_class(Logo, self.logo)
        return result


class Hit:
    geo: Optional[Geo]
    acces_libre: Optional[bool]
    action: Optional[str]
    adresse: Optional[str]
    adresse_salle: Optional[str]
    adresse_structure: Optional[str]
    adresse_club_pro: None
    adresse_complement: Optional[str]
    affiche: Optional[Affiche]
    age_max: Optional[int]
    age_min: Optional[int]
    assurance: Optional[str]
    capacite_spectateur: Optional[str]
    cartographie: Optional[Cartographie]
    categorie: Optional[NatureSolClass]
    categorie_championnat3_x3_id: None
    categorie_championnat3_x3_libelle: None
    code: Optional[str]
    code_comite: Optional[str]
    code_ligue: Optional[CodeLigueEnum]
    commune: Optional[Commune]
    commune_club_pro: Optional[CommuneClubPro]
    compare_old_site: Optional[bool]
    competition_orgine: Optional[str]
    competition_origine: Optional[str]
    competition_origine_niveau: Optional[int]
    competition_origine_nom: Optional[str]
    competition_id: Optional[CompetitionID]
    cp_salle: Optional[str]
    creation_timestamp: Optional[int]
    creation_en_cours: Optional[bool]
    date: Optional[datetime]
    date_created: Optional[datetime]
    date_debut: Optional[datetime]
    date_debut_timestamp: Optional[int]
    date_demande: Optional[int]
    date_fin: Optional[datetime]
    date_fin_timestamp: Optional[int]
    date_inscription: Optional[int]
    date_rencontre: Optional[datetime]
    date_rencontre_timestamp: Optional[int]
    date_timestamp: Optional[int]
    date_updated: Optional[datetime]
    date_affiliation: None
    date_saisie_resultat_timestamp: Optional[int]
    debut: Optional[datetime]
    debut_timestamp: Optional[int]
    defaut_equipe1: Optional[bool]
    defaut_equipe2: Optional[bool]
    description: Optional[str]
    document_flyer: Optional[DocumentFlyer]
    email: Optional[str]
    emarque_v2: Optional[bool]
    engagement: Optional[str]
    engagements_codes: Optional[str]
    engagements_noms: Optional[str]
    etat: Optional[Etat]
    facebook: None
    fin: Optional[datetime]
    fin_timestamp: Optional[int]
    forfait_equipe1: Optional[bool]
    forfait_equipe2: Optional[bool]
    gs_id: None
    horaire: Optional[Union[int, datetime]]
    horaires_seances: Optional[str]
    id: str
    id_competition_pere: None
    id_engagement_equipe1: Optional[IDEngagementEquipe]
    id_engagement_equipe2: Optional[IDEngagementEquipe]
    id_organisme_equipe1: Optional[IDOrganismeEquipe]
    id_organisme_equipe2: Optional[IDOrganismeEquipe]
    id_poule: Optional[IDPoule]
    inscriptions: Optional[str]
    joue: Optional[bool]
    jours: Optional[List[Jour]]
    label: Optional[Label]
    labellisation: Optional[List[Labellisation]]
    largeur: Optional[int]
    latitude: None
    libelle: Optional[str]
    libelle2: Optional[str]
    live_stat: Optional[bool]
    logo: Optional[Logo]
    longitude: None
    longueur: Optional[int]
    mail: Optional[str]
    mail_demandeur: Optional[str]
    mail_structure: Optional[str]
    mail_organisateur: Optional[str]
    modification_timestamp: Optional[int]
    nature_sol: Optional[NatureSolClass]
    nb_participant_prevu: None
    niveau: Optional[NiveauEnum]
    niveau_nb: Optional[int]
    nom: Optional[str]
    nom_demandeur: Optional[str]
    nom_salle: Optional[str]
    nom_simple: Optional[str]
    nom_structure: Optional[str]
    nombre_personnes: Optional[str]
    nombre_seances: Optional[str]
    nom_club_pro: Optional[NomClubPro]
    nom_equipe1: Optional[str]
    nom_equipe2: Optional[str]
    nom_extended: Optional[str]
    nom_organisateur: Optional[str]
    numero: Optional[Union[int, str]]
    numero_journee: Optional[str]
    objectif: Optional[Objectif]
    officiels: Optional[Union[List[Any], str]]
    offres_pratiques: Optional[List[OffresPratique]]
    ordre: Optional[int]
    organisateur: Optional[Organisateur]
    organisme_id_pere: Optional[HitOrganismeIDPere]
    penalite_equipe1: Optional[bool]
    penalite_equipe2: Optional[bool]
    phase_code: Optional[PhaseCode]
    phases: Optional[List[str]]
    poules: Optional[List[Poule]]
    pratique: Optional[Pratique]
    prenom_demandeur: Optional[str]
    pro: Optional[bool]
    public: Optional[str]
    publication_internet: Optional[PublicationInternet]
    resultat_equipe1: Optional[int]
    resultat_equipe2: Optional[int]
    rue: Optional[str]
    saison: Optional[Saison]
    saison_en_cours: Optional[bool]
    salle: Optional[Salle]
    sexe: Optional[SexeEnum]
    site_web: Optional[str]
    site_choisi: Optional[str]
    slug: Optional[str]
    status: Optional[HitStatus]
    tarif_organisateur: Optional[int]
    telephone: Optional[str]
    telephone_organisateur: Optional[str]
    thumbnail: Optional[str]
    titre: Optional[str]
    to_update: Optional[bool]
    tournoi_type: Optional[TournoiTypeEnum]
    tournoi_types3_x3: Optional[List[TournoiTypes3X3]]
    twitter: None
    type: Optional[HitType]
    type_association: Optional[TypeAssociation]
    type_competition: Optional[CompetitionIDTypeCompetitionEnum]
    type_competition_generique: Optional[HitTypeCompetitionGenerique]
    unique_key: Optional[str]
    url_competition: Optional[str]
    url_organisateur: Optional[str]
    url_site_web: Optional[str]
    ville_salle: Optional[str]

    def __init__(
        self,
        geo: Optional[Geo],
        acces_libre: Optional[bool],
        action: Optional[str],
        adresse: Optional[str],
        adresse_salle: Optional[str],
        adresse_structure: Optional[str],
        adresse_club_pro: None,
        adresse_complement: Optional[str],
        affiche: Optional[Affiche],
        age_max: Optional[int],
        age_min: Optional[int],
        assurance: Optional[str],
        capacite_spectateur: Optional[str],
        cartographie: Optional[Cartographie],
        categorie: Optional[NatureSolClass],
        categorie_championnat3_x3_id: None,
        categorie_championnat3_x3_libelle: None,
        code: Optional[str],
        code_comite: Optional[str],
        code_ligue: Optional[CodeLigueEnum],
        commune: Optional[Commune],
        commune_club_pro: Optional[CommuneClubPro],
        compare_old_site: Optional[bool],
        competition_orgine: Optional[str],
        competition_origine: Optional[str],
        competition_origine_niveau: Optional[int],
        competition_origine_nom: Optional[str],
        competition_id: Optional[CompetitionID],
        cp_salle: Optional[str],
        creation_timestamp: Optional[int],
        creation_en_cours: Optional[bool],
        date: Optional[datetime],
        date_created: Optional[datetime],
        date_debut: Optional[datetime],
        date_debut_timestamp: Optional[int],
        date_demande: Optional[int],
        date_fin: Optional[datetime],
        date_fin_timestamp: Optional[int],
        date_inscription: Optional[int],
        date_rencontre: Optional[datetime],
        date_rencontre_timestamp: Optional[int],
        date_timestamp: Optional[int],
        date_updated: Optional[datetime],
        date_affiliation: None,
        date_saisie_resultat_timestamp: Optional[int],
        debut: Optional[datetime],
        debut_timestamp: Optional[int],
        defaut_equipe1: Optional[bool],
        defaut_equipe2: Optional[bool],
        description: Optional[str],
        document_flyer: Optional[DocumentFlyer],
        email: Optional[str],
        emarque_v2: Optional[bool],
        engagement: Optional[str],
        engagements_codes: Optional[str],
        engagements_noms: Optional[str],
        etat: Optional[Etat],
        facebook: None,
        fin: Optional[datetime],
        fin_timestamp: Optional[int],
        forfait_equipe1: Optional[bool],
        forfait_equipe2: Optional[bool],
        gs_id: None,
        horaire: Optional[Union[int, datetime]],
        horaires_seances: Optional[str],
        id: str,
        id_competition_pere: None,
        id_engagement_equipe1: Optional[IDEngagementEquipe],
        id_engagement_equipe2: Optional[IDEngagementEquipe],
        id_organisme_equipe1: Optional[IDOrganismeEquipe],
        id_organisme_equipe2: Optional[IDOrganismeEquipe],
        id_poule: Optional[IDPoule],
        inscriptions: Optional[str],
        joue: Optional[bool],
        jours: Optional[List[Jour]],
        label: Optional[Label],
        labellisation: Optional[List[Labellisation]],
        largeur: Optional[int],
        latitude: None,
        libelle: Optional[str],
        libelle2: Optional[str],
        live_stat: Optional[bool],
        logo: Optional[Logo],
        longitude: None,
        longueur: Optional[int],
        mail: Optional[str],
        mail_demandeur: Optional[str],
        mail_structure: Optional[str],
        mail_organisateur: Optional[str],
        modification_timestamp: Optional[int],
        nature_sol: Optional[NatureSolClass],
        nb_participant_prevu: None,
        niveau: Optional[NiveauEnum],
        niveau_nb: Optional[int],
        nom: Optional[str],
        nom_demandeur: Optional[str],
        nom_salle: Optional[str],
        nom_simple: Optional[str],
        nom_structure: Optional[str],
        nombre_personnes: Optional[str],
        nombre_seances: Optional[str],
        nom_club_pro: Optional[NomClubPro],
        nom_equipe1: Optional[str],
        nom_equipe2: Optional[str],
        nom_extended: Optional[str],
        nom_organisateur: Optional[str],
        numero: Optional[Union[int, str]],
        numero_journee: Optional[str],
        objectif: Optional[Objectif],
        officiels: Optional[Union[List[Any], str]],
        offres_pratiques: Optional[List[OffresPratique]],
        ordre: Optional[int],
        organisateur: Optional[Organisateur],
        organisme_id_pere: Optional[HitOrganismeIDPere],
        penalite_equipe1: Optional[bool],
        penalite_equipe2: Optional[bool],
        phase_code: Optional[PhaseCode],
        phases: Optional[List[str]],
        poules: Optional[List[Poule]],
        pratique: Optional[Pratique],
        prenom_demandeur: Optional[str],
        pro: Optional[bool],
        public: Optional[str],
        publication_internet: Optional[PublicationInternet],
        resultat_equipe1: Optional[int],
        resultat_equipe2: Optional[int],
        rue: Optional[str],
        saison: Optional[Saison],
        saison_en_cours: Optional[bool],
        salle: Optional[Salle],
        sexe: Optional[SexeEnum],
        site_web: Optional[str],
        site_choisi: Optional[str],
        slug: Optional[str],
        status: Optional[HitStatus],
        tarif_organisateur: Optional[int],
        telephone: Optional[str],
        telephone_organisateur: Optional[str],
        thumbnail: Optional[str],
        titre: Optional[str],
        to_update: Optional[bool],
        tournoi_type: Optional[TournoiTypeEnum],
        tournoi_types3_x3: Optional[List[TournoiTypes3X3]],
        twitter: None,
        type: Optional[HitType],
        type_association: Optional[TypeAssociation],
        type_competition: Optional[CompetitionIDTypeCompetitionEnum],
        type_competition_generique: Optional[HitTypeCompetitionGenerique],
        unique_key: Optional[str],
        url_competition: Optional[str],
        url_organisateur: Optional[str],
        url_site_web: Optional[str],
        ville_salle: Optional[str],
    ) -> None:
        self.geo = geo
        self.acces_libre = acces_libre
        self.action = action
        self.adresse = adresse
        self.adresse_salle = adresse_salle
        self.adresse_structure = adresse_structure
        self.adresse_club_pro = adresse_club_pro
        self.adresse_complement = adresse_complement
        self.affiche = affiche
        self.age_max = age_max
        self.age_min = age_min
        self.assurance = assurance
        self.capacite_spectateur = capacite_spectateur
        self.cartographie = cartographie
        self.categorie = categorie
        self.categorie_championnat3_x3_id = categorie_championnat3_x3_id
        self.categorie_championnat3_x3_libelle = categorie_championnat3_x3_libelle
        self.code = code
        self.code_comite = code_comite
        self.code_ligue = code_ligue
        self.commune = commune
        self.commune_club_pro = commune_club_pro
        self.compare_old_site = compare_old_site
        self.competition_orgine = competition_orgine
        self.competition_origine = competition_origine
        self.competition_origine_niveau = competition_origine_niveau
        self.competition_origine_nom = competition_origine_nom
        self.competition_id = competition_id
        self.cp_salle = cp_salle
        self.creation_timestamp = creation_timestamp
        self.creation_en_cours = creation_en_cours
        self.date = date
        self.date_created = date_created
        self.date_debut = date_debut
        self.date_debut_timestamp = date_debut_timestamp
        self.date_demande = date_demande
        self.date_fin = date_fin
        self.date_fin_timestamp = date_fin_timestamp
        self.date_inscription = date_inscription
        self.date_rencontre = date_rencontre
        self.date_rencontre_timestamp = date_rencontre_timestamp
        self.date_timestamp = date_timestamp
        self.date_updated = date_updated
        self.date_affiliation = date_affiliation
        self.date_saisie_resultat_timestamp = date_saisie_resultat_timestamp
        self.debut = debut
        self.debut_timestamp = debut_timestamp
        self.defaut_equipe1 = defaut_equipe1
        self.defaut_equipe2 = defaut_equipe2
        self.description = description
        self.document_flyer = document_flyer
        self.email = email
        self.emarque_v2 = emarque_v2
        self.engagement = engagement
        self.engagements_codes = engagements_codes
        self.engagements_noms = engagements_noms
        self.etat = etat
        self.facebook = facebook
        self.fin = fin
        self.fin_timestamp = fin_timestamp
        self.forfait_equipe1 = forfait_equipe1
        self.forfait_equipe2 = forfait_equipe2
        self.gs_id = gs_id
        self.horaire = horaire
        self.horaires_seances = horaires_seances
        self.id = id
        self.id_competition_pere = id_competition_pere
        self.id_engagement_equipe1 = id_engagement_equipe1
        self.id_engagement_equipe2 = id_engagement_equipe2
        self.id_organisme_equipe1 = id_organisme_equipe1
        self.id_organisme_equipe2 = id_organisme_equipe2
        self.id_poule = id_poule
        self.inscriptions = inscriptions
        self.joue = joue
        self.jours = jours
        self.label = label
        self.labellisation = labellisation
        self.largeur = largeur
        self.latitude = latitude
        self.libelle = libelle
        self.libelle2 = libelle2
        self.live_stat = live_stat
        self.logo = logo
        self.longitude = longitude
        self.longueur = longueur
        self.mail = mail
        self.mail_demandeur = mail_demandeur
        self.mail_structure = mail_structure
        self.mail_organisateur = mail_organisateur
        self.modification_timestamp = modification_timestamp
        self.nature_sol = nature_sol
        self.nb_participant_prevu = nb_participant_prevu
        self.niveau = niveau
        self.niveau_nb = niveau_nb
        self.nom = nom
        self.nom_demandeur = nom_demandeur
        self.nom_salle = nom_salle
        self.nom_simple = nom_simple
        self.nom_structure = nom_structure
        self.nombre_personnes = nombre_personnes
        self.nombre_seances = nombre_seances
        self.nom_club_pro = nom_club_pro
        self.nom_equipe1 = nom_equipe1
        self.nom_equipe2 = nom_equipe2
        self.nom_extended = nom_extended
        self.nom_organisateur = nom_organisateur
        self.numero = numero
        self.numero_journee = numero_journee
        self.objectif = objectif
        self.officiels = officiels
        self.offres_pratiques = offres_pratiques
        self.ordre = ordre
        self.organisateur = organisateur
        self.organisme_id_pere = organisme_id_pere
        self.penalite_equipe1 = penalite_equipe1
        self.penalite_equipe2 = penalite_equipe2
        self.phase_code = phase_code
        self.phases = phases
        self.poules = poules
        self.pratique = pratique
        self.prenom_demandeur = prenom_demandeur
        self.pro = pro
        self.public = public
        self.publication_internet = publication_internet
        self.resultat_equipe1 = resultat_equipe1
        self.resultat_equipe2 = resultat_equipe2
        self.rue = rue
        self.saison = saison
        self.saison_en_cours = saison_en_cours
        self.salle = salle
        self.sexe = sexe
        self.site_web = site_web
        self.site_choisi = site_choisi
        self.slug = slug
        self.status = status
        self.tarif_organisateur = tarif_organisateur
        self.telephone = telephone
        self.telephone_organisateur = telephone_organisateur
        self.thumbnail = thumbnail
        self.titre = titre
        self.to_update = to_update
        self.tournoi_type = tournoi_type
        self.tournoi_types3_x3 = tournoi_types3_x3
        self.twitter = twitter
        self.type = type
        self.type_association = type_association
        self.type_competition = type_competition
        self.type_competition_generique = type_competition_generique
        self.unique_key = unique_key
        self.url_competition = url_competition
        self.url_organisateur = url_organisateur
        self.url_site_web = url_site_web
        self.ville_salle = ville_salle

    @staticmethod
    def from_dict(obj: Any) -> "Hit":
        assert isinstance(obj, dict)
        geo = from_union([Geo.from_dict, from_none], obj.get("_geo"))
        acces_libre = from_union([from_bool, from_none], obj.get("accesLibre"))
        action = from_union([from_str, from_none], obj.get("action"))
        adresse = from_union([from_none, from_str], obj.get("adresse"))
        adresse_salle = from_union([from_str, from_none], obj.get("adresse_salle"))
        adresse_structure = from_union(
            [from_none, from_str], obj.get("adresse_structure")
        )
        adresse_club_pro = from_none(obj.get("adresseClubPro"))
        adresse_complement = from_union(
            [from_none, from_str], obj.get("adresseComplement")
        )
        affiche = from_union([Affiche.from_dict, from_none], obj.get("affiche"))
        age_max = from_union([from_int, from_none], obj.get("ageMax"))
        age_min = from_union([from_int, from_none], obj.get("ageMin"))
        assurance = from_union([from_none, from_str], obj.get("assurance"))
        capacite_spectateur = from_union(
            [from_none, from_str], obj.get("capaciteSpectateur")
        )
        cartographie = from_union(
            [Cartographie.from_dict, from_none], obj.get("cartographie")
        )
        categorie = from_union(
            [NatureSolClass.from_dict, from_none], obj.get("categorie")
        )
        categorie_championnat3_x3_id = from_none(obj.get("categorieChampionnat3x3Id"))
        categorie_championnat3_x3_libelle = from_none(
            obj.get("categorieChampionnat3x3Libelle")
        )
        code = from_union([from_none, from_str], obj.get("code"))
        code_comite = from_union([from_str, from_none], obj.get("codeComite"))
        code_ligue = from_union([CodeLigueEnum, from_none], obj.get("codeLigue"))
        commune = from_union([Commune.from_dict, from_none], obj.get("commune"))
        commune_club_pro = from_union(
            [CommuneClubPro.from_dict, from_none], obj.get("communeClubPro")
        )
        compare_old_site = from_union(
            [from_bool, from_none], obj.get("compare_old_site")
        )
        competition_orgine = from_union(
            [from_str, from_none], obj.get("competition_orgine")
        )
        competition_origine = from_union(
            [from_none, from_str], obj.get("competition_origine")
        )
        competition_origine_niveau = from_union(
            [from_int, from_none], obj.get("competition_origine_niveau")
        )
        competition_origine_nom = from_union(
            [from_str, from_none], obj.get("competition_origine_nom")
        )
        competition_id = from_union(
            [CompetitionID.from_dict, from_none], obj.get("competitionId")
        )
        cp_salle = from_union([from_str, from_none], obj.get("cp_salle"))
        creation_timestamp = from_union(
            [from_int, from_none], obj.get("creation_timestamp")
        )
        creation_en_cours = from_union(
            [from_bool, from_none], obj.get("creationEnCours")
        )
        date = from_union([from_datetime, from_none], obj.get("date"))
        date_created = from_union([from_datetime, from_none], obj.get("date_created"))
        date_debut = from_union([from_datetime, from_none], obj.get("date_debut"))
        date_debut_timestamp = from_union(
            [from_int, from_none], obj.get("date_debut_timestamp")
        )
        date_demande = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("date_demande")
        )
        date_fin = from_union([from_datetime, from_none], obj.get("date_fin"))
        date_fin_timestamp = from_union(
            [from_int, from_none], obj.get("date_fin_timestamp")
        )
        date_inscription = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("date_inscription")
        )
        date_rencontre = from_union(
            [from_datetime, from_none], obj.get("date_rencontre")
        )
        date_rencontre_timestamp = from_union(
            [from_none, from_int, lambda x: int(from_str(x))],
            obj.get("date_rencontre_timestamp"),
        )
        date_timestamp = from_union(
            [from_none, from_int, lambda x: int(from_str(x))], obj.get("date_timestamp")
        )
        date_updated = from_union([from_datetime, from_none], obj.get("date_updated"))
        date_affiliation = from_none(obj.get("dateAffiliation"))
        date_saisie_resultat_timestamp = from_union(
            [from_int, from_none], obj.get("dateSaisieResultat_timestamp")
        )
        debut = from_union([from_datetime, from_none], obj.get("debut"))
        debut_timestamp = from_union([from_int, from_none], obj.get("debut_timestamp"))
        defaut_equipe1 = from_union([from_bool, from_none], obj.get("defautEquipe1"))
        defaut_equipe2 = from_union([from_bool, from_none], obj.get("defautEquipe2"))
        description = from_union([from_none, from_str], obj.get("description"))
        document_flyer = from_union(
            [DocumentFlyer.from_dict, from_none], obj.get("document_flyer")
        )
        email = from_union([from_none, from_str], obj.get("email"))
        emarque_v2 = from_union([from_bool, from_none], obj.get("emarqueV2"))
        engagement = from_union([from_none, from_str], obj.get("engagement"))
        engagements_codes = from_union(
            [from_str, from_none], obj.get("engagements_codes")
        )
        engagements_noms = from_union(
            [from_str, from_none], obj.get("engagements_noms")
        )
        etat = from_union([Etat, from_none], obj.get("etat"))
        facebook = from_none(obj.get("facebook"))
        fin = from_union([from_datetime, from_none], obj.get("fin"))
        fin_timestamp = from_union([from_int, from_none], obj.get("fin_timestamp"))
        forfait_equipe1 = from_union([from_bool, from_none], obj.get("forfaitEquipe1"))
        forfait_equipe2 = from_union([from_bool, from_none], obj.get("forfaitEquipe2"))
        gs_id = from_none(obj.get("gsId"))
        horaire = from_union(
            [
                from_none,
                lambda x: from_union([from_datetime, lambda x: int(x)], from_str(x)),
            ],
            obj.get("horaire"),
        )
        horaires_seances = from_union(
            [from_none, from_str], obj.get("horaires_seances")
        )
        id = from_str(obj.get("id"))
        id_competition_pere = from_none(obj.get("idCompetitionPere"))
        id_engagement_equipe1 = from_union(
            [IDEngagementEquipe.from_dict, from_none], obj.get("idEngagementEquipe1")
        )
        id_engagement_equipe2 = from_union(
            [IDEngagementEquipe.from_dict, from_none], obj.get("idEngagementEquipe2")
        )
        id_organisme_equipe1 = from_union(
            [IDOrganismeEquipe.from_dict, from_none], obj.get("idOrganismeEquipe1")
        )
        id_organisme_equipe2 = from_union(
            [IDOrganismeEquipe.from_dict, from_none], obj.get("idOrganismeEquipe2")
        )
        id_poule = from_union([IDPoule.from_dict, from_none], obj.get("idPoule"))
        inscriptions = from_union([from_none, from_str], obj.get("inscriptions"))
        joue = from_union([from_bool, from_none], obj.get("joue"))
        jours = from_union([lambda x: from_list(Jour, x), from_none], obj.get("jours"))
        label = from_union([Label, from_none], obj.get("label"))
        labellisation = from_union(
            [lambda x: from_list(Labellisation, x), from_none], obj.get("labellisation")
        )
        largeur = from_union([from_int, from_none], obj.get("largeur"))
        latitude = from_none(obj.get("latitude"))
        libelle = from_union([from_str, from_none], obj.get("libelle"))
        libelle2 = from_union([from_none, from_str], obj.get("libelle2"))
        live_stat = from_union([from_bool, from_none], obj.get("liveStat"))
        logo = from_union([Logo.from_dict, from_none], obj.get("logo"))
        longitude = from_none(obj.get("longitude"))
        longueur = from_union([from_int, from_none], obj.get("longueur"))
        mail = from_union([from_none, from_str], obj.get("mail"))
        mail_demandeur = from_union([from_none, from_str], obj.get("mail_demandeur"))
        mail_structure = from_union([from_none, from_str], obj.get("mail_structure"))
        mail_organisateur = from_union(
            [from_none, from_str], obj.get("mailOrganisateur")
        )
        modification_timestamp = from_union(
            [from_int, from_none], obj.get("modification_timestamp")
        )
        nature_sol = from_union(
            [NatureSolClass.from_dict, from_none], obj.get("natureSol")
        )
        nb_participant_prevu = from_none(obj.get("nbParticipantPrevu"))
        niveau = from_union([NiveauEnum, from_none], obj.get("niveau"))
        niveau_nb = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("niveau_nb")
        )
        nom = from_union([from_str, from_none], obj.get("nom"))
        nom_demandeur = from_union([from_none, from_str], obj.get("nom_demandeur"))
        nom_salle = from_union([from_str, from_none], obj.get("nom_salle"))
        nom_simple = from_union([from_none, from_str], obj.get("nom_simple"))
        nom_structure = from_union([from_none, from_str], obj.get("nom_structure"))
        nombre_personnes = from_union(
            [from_none, from_str], obj.get("nombre_personnes")
        )
        nombre_seances = from_union([from_none, from_str], obj.get("nombre_seances"))
        nom_club_pro = from_union([from_none, NomClubPro], obj.get("nomClubPro"))
        nom_equipe1 = from_union([from_str, from_none], obj.get("nomEquipe1"))
        nom_equipe2 = from_union([from_str, from_none], obj.get("nomEquipe2"))
        nom_extended = from_union([from_str, from_none], obj.get("nomExtended"))
        nom_organisateur = from_union([from_none, from_str], obj.get("nomOrganisateur"))
        numero = from_union([from_int, from_str, from_none], obj.get("numero"))
        numero_journee = from_union([from_str, from_none], obj.get("numeroJournee"))
        objectif = from_union([from_none, Objectif], obj.get("objectif"))
        officiels = from_union(
            [lambda x: from_list(lambda x: x, x), from_str, from_none],
            obj.get("officiels"),
        )
        offres_pratiques = from_union(
            [lambda x: from_list(OffresPratique, x), from_none],
            obj.get("offresPratiques"),
        )
        ordre = from_union([from_int, from_none], obj.get("ordre"))
        organisateur = from_union(
            [Organisateur.from_dict, from_none], obj.get("organisateur")
        )
        organisme_id_pere = from_union(
            [HitOrganismeIDPere.from_dict, from_none], obj.get("organisme_id_pere")
        )
        penalite_equipe1 = from_union(
            [from_bool, from_none], obj.get("penaliteEquipe1")
        )
        penalite_equipe2 = from_union(
            [from_bool, from_none], obj.get("penaliteEquipe2")
        )
        phase_code = from_union([PhaseCode, from_none], obj.get("phase_code"))
        phases = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("phases")
        )
        poules = from_union(
            [lambda x: from_list(Poule.from_dict, x), from_none], obj.get("poules")
        )
        pratique = from_union([Pratique, from_none], obj.get("pratique"))
        prenom_demandeur = from_union(
            [from_none, from_str], obj.get("prenom_demandeur")
        )
        pro = from_union([from_bool, from_none], obj.get("pro"))
        public = from_union([from_none, from_str], obj.get("public"))
        publication_internet = from_union(
            [PublicationInternet, from_none], obj.get("publicationInternet")
        )
        resultat_equipe1 = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("resultatEquipe1")
        )
        resultat_equipe2 = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("resultatEquipe2")
        )
        rue = from_union([from_none, from_str], obj.get("rue"))
        saison = from_union([Saison.from_dict, from_none], obj.get("saison"))
        saison_en_cours = from_union([from_bool, from_none], obj.get("saison_en_cours"))
        salle = from_union([Salle.from_dict, from_none], obj.get("salle"))
        sexe = from_union([SexeEnum, from_none], obj.get("sexe"))
        site_web = from_union([from_none, from_str], obj.get("site_web"))
        site_choisi = from_union([from_str, from_none], obj.get("siteChoisi"))
        slug = from_union([from_str, from_none], obj.get("slug"))
        status = from_union([HitStatus, from_none], obj.get("status"))
        tarif_organisateur = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("tarifOrganisateur")
        )
        telephone = from_union([from_none, from_str], obj.get("telephone"))
        telephone_organisateur = from_union(
            [from_str, from_none], obj.get("telephoneOrganisateur")
        )
        thumbnail = from_union([from_none, from_str], obj.get("thumbnail"))
        titre = from_union([from_str, from_none], obj.get("titre"))
        to_update = from_union([from_bool, from_none], obj.get("toUpdate"))
        tournoi_type = from_union([TournoiTypeEnum, from_none], obj.get("tournoiType"))
        tournoi_types3_x3 = from_union(
            [lambda x: from_list(TournoiTypes3X3.from_dict, x), from_none],
            obj.get("tournoiTypes3x3"),
        )
        twitter = from_none(obj.get("twitter"))
        type = from_union([HitType, from_none], obj.get("type"))
        type_association = from_union(
            [TypeAssociation.from_dict, from_none], obj.get("type_association")
        )
        type_competition = from_union(
            [CompetitionIDTypeCompetitionEnum, from_none], obj.get("typeCompetition")
        )
        type_competition_generique = from_union(
            [HitTypeCompetitionGenerique.from_dict, from_none],
            obj.get("typeCompetitionGenerique"),
        )
        unique_key = from_union([from_str, from_none], obj.get("uniqueKey"))
        url_competition = from_union([from_none, from_str], obj.get("url_competition"))
        url_organisateur = from_union([from_none, from_str], obj.get("urlOrganisateur"))
        url_site_web = from_union([from_none, from_str], obj.get("urlSiteWeb"))
        ville_salle = from_union([from_str, from_none], obj.get("ville_salle"))
        return Hit(
            geo,
            acces_libre,
            action,
            adresse,
            adresse_salle,
            adresse_structure,
            adresse_club_pro,
            adresse_complement,
            affiche,
            age_max,
            age_min,
            assurance,
            capacite_spectateur,
            cartographie,
            categorie,
            categorie_championnat3_x3_id,
            categorie_championnat3_x3_libelle,
            code,
            code_comite,
            code_ligue,
            commune,
            commune_club_pro,
            compare_old_site,
            competition_orgine,
            competition_origine,
            competition_origine_niveau,
            competition_origine_nom,
            competition_id,
            cp_salle,
            creation_timestamp,
            creation_en_cours,
            date,
            date_created,
            date_debut,
            date_debut_timestamp,
            date_demande,
            date_fin,
            date_fin_timestamp,
            date_inscription,
            date_rencontre,
            date_rencontre_timestamp,
            date_timestamp,
            date_updated,
            date_affiliation,
            date_saisie_resultat_timestamp,
            debut,
            debut_timestamp,
            defaut_equipe1,
            defaut_equipe2,
            description,
            document_flyer,
            email,
            emarque_v2,
            engagement,
            engagements_codes,
            engagements_noms,
            etat,
            facebook,
            fin,
            fin_timestamp,
            forfait_equipe1,
            forfait_equipe2,
            gs_id,
            horaire,
            horaires_seances,
            id,
            id_competition_pere,
            id_engagement_equipe1,
            id_engagement_equipe2,
            id_organisme_equipe1,
            id_organisme_equipe2,
            id_poule,
            inscriptions,
            joue,
            jours,
            label,
            labellisation,
            largeur,
            latitude,
            libelle,
            libelle2,
            live_stat,
            logo,
            longitude,
            longueur,
            mail,
            mail_demandeur,
            mail_structure,
            mail_organisateur,
            modification_timestamp,
            nature_sol,
            nb_participant_prevu,
            niveau,
            niveau_nb,
            nom,
            nom_demandeur,
            nom_salle,
            nom_simple,
            nom_structure,
            nombre_personnes,
            nombre_seances,
            nom_club_pro,
            nom_equipe1,
            nom_equipe2,
            nom_extended,
            nom_organisateur,
            numero,
            numero_journee,
            objectif,
            officiels,
            offres_pratiques,
            ordre,
            organisateur,
            organisme_id_pere,
            penalite_equipe1,
            penalite_equipe2,
            phase_code,
            phases,
            poules,
            pratique,
            prenom_demandeur,
            pro,
            public,
            publication_internet,
            resultat_equipe1,
            resultat_equipe2,
            rue,
            saison,
            saison_en_cours,
            salle,
            sexe,
            site_web,
            site_choisi,
            slug,
            status,
            tarif_organisateur,
            telephone,
            telephone_organisateur,
            thumbnail,
            titre,
            to_update,
            tournoi_type,
            tournoi_types3_x3,
            twitter,
            type,
            type_association,
            type_competition,
            type_competition_generique,
            unique_key,
            url_competition,
            url_organisateur,
            url_site_web,
            ville_salle,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.geo is not None:
            result["_geo"] = from_union(
                [lambda x: to_class(Geo, x), from_none], self.geo
            )
        if self.acces_libre is not None:
            result["accesLibre"] = from_union([from_bool, from_none], self.acces_libre)
        if self.action is not None:
            result["action"] = from_union([from_str, from_none], self.action)
        if self.adresse is not None:
            result["adresse"] = from_union([from_none, from_str], self.adresse)
        if self.adresse_salle is not None:
            result["adresse_salle"] = from_union(
                [from_str, from_none], self.adresse_salle
            )
        if self.adresse_structure is not None:
            result["adresse_structure"] = from_union(
                [from_none, from_str], self.adresse_structure
            )
        if self.adresse_club_pro is not None:
            result["adresseClubPro"] = from_none(self.adresse_club_pro)
        if self.adresse_complement is not None:
            result["adresseComplement"] = from_union(
                [from_none, from_str], self.adresse_complement
            )
        if self.affiche is not None:
            result["affiche"] = from_union(
                [lambda x: to_class(Affiche, x), from_none], self.affiche
            )
        if self.age_max is not None:
            result["ageMax"] = from_union([from_int, from_none], self.age_max)
        if self.age_min is not None:
            result["ageMin"] = from_union([from_int, from_none], self.age_min)
        if self.assurance is not None:
            result["assurance"] = from_union([from_none, from_str], self.assurance)
        if self.capacite_spectateur is not None:
            result["capaciteSpectateur"] = from_union(
                [from_none, from_str], self.capacite_spectateur
            )
        if self.cartographie is not None:
            result["cartographie"] = from_union(
                [lambda x: to_class(Cartographie, x), from_none], self.cartographie
            )
        if self.categorie is not None:
            result["categorie"] = from_union(
                [lambda x: to_class(NatureSolClass, x), from_none], self.categorie
            )
        if self.categorie_championnat3_x3_id is not None:
            result["categorieChampionnat3x3Id"] = from_none(
                self.categorie_championnat3_x3_id
            )
        if self.categorie_championnat3_x3_libelle is not None:
            result["categorieChampionnat3x3Libelle"] = from_none(
                self.categorie_championnat3_x3_libelle
            )
        if self.code is not None:
            result["code"] = from_union([from_none, from_str], self.code)
        if self.code_comite is not None:
            result["codeComite"] = from_union([from_str, from_none], self.code_comite)
        if self.code_ligue is not None:
            result["codeLigue"] = from_union(
                [lambda x: to_enum(CodeLigueEnum, x), from_none], self.code_ligue
            )
        if self.commune is not None:
            result["commune"] = from_union(
                [lambda x: to_class(Commune, x), from_none], self.commune
            )
        if self.commune_club_pro is not None:
            result["communeClubPro"] = from_union(
                [lambda x: to_class(CommuneClubPro, x), from_none],
                self.commune_club_pro,
            )
        if self.compare_old_site is not None:
            result["compare_old_site"] = from_union(
                [from_bool, from_none], self.compare_old_site
            )
        if self.competition_orgine is not None:
            result["competition_orgine"] = from_union(
                [from_str, from_none], self.competition_orgine
            )
        if self.competition_origine is not None:
            result["competition_origine"] = from_union(
                [from_none, from_str], self.competition_origine
            )
        if self.competition_origine_niveau is not None:
            result["competition_origine_niveau"] = from_union(
                [from_int, from_none], self.competition_origine_niveau
            )
        if self.competition_origine_nom is not None:
            result["competition_origine_nom"] = from_union(
                [from_str, from_none], self.competition_origine_nom
            )
        if self.competition_id is not None:
            result["competitionId"] = from_union(
                [lambda x: to_class(CompetitionID, x), from_none], self.competition_id
            )
        if self.cp_salle is not None:
            result["cp_salle"] = from_union([from_str, from_none], self.cp_salle)
        if self.creation_timestamp is not None:
            result["creation_timestamp"] = from_union(
                [from_int, from_none], self.creation_timestamp
            )
        if self.creation_en_cours is not None:
            result["creationEnCours"] = from_union(
                [from_bool, from_none], self.creation_en_cours
            )
        if self.date is not None:
            result["date"] = from_union([lambda x: x.isoformat(), from_none], self.date)
        if self.date_created is not None:
            result["date_created"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_created
            )
        if self.date_debut is not None:
            result["date_debut"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_debut
            )
        if self.date_debut_timestamp is not None:
            result["date_debut_timestamp"] = from_union(
                [from_int, from_none], self.date_debut_timestamp
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
        if self.date_fin_timestamp is not None:
            result["date_fin_timestamp"] = from_union(
                [from_int, from_none], self.date_fin_timestamp
            )
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
        if self.date_rencontre is not None:
            result["date_rencontre"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_rencontre
            )
        if self.date_rencontre_timestamp is not None:
            result["date_rencontre_timestamp"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_int((lambda x: is_type(int, x))(x)),
                ],
                self.date_rencontre_timestamp,
            )
        if self.date_timestamp is not None:
            result["date_timestamp"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_int((lambda x: is_type(int, x))(x)),
                ],
                self.date_timestamp,
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_updated
            )
        if self.date_affiliation is not None:
            result["dateAffiliation"] = from_none(self.date_affiliation)
        if self.date_saisie_resultat_timestamp is not None:
            result["dateSaisieResultat_timestamp"] = from_union(
                [from_int, from_none], self.date_saisie_resultat_timestamp
            )
        if self.debut is not None:
            result["debut"] = from_union(
                [lambda x: x.isoformat(), from_none], self.debut
            )
        if self.debut_timestamp is not None:
            result["debut_timestamp"] = from_union(
                [from_int, from_none], self.debut_timestamp
            )
        if self.defaut_equipe1 is not None:
            result["defautEquipe1"] = from_union(
                [from_bool, from_none], self.defaut_equipe1
            )
        if self.defaut_equipe2 is not None:
            result["defautEquipe2"] = from_union(
                [from_bool, from_none], self.defaut_equipe2
            )
        if self.description is not None:
            result["description"] = from_union([from_none, from_str], self.description)
        if self.document_flyer is not None:
            result["document_flyer"] = from_union(
                [lambda x: to_class(DocumentFlyer, x), from_none], self.document_flyer
            )
        if self.email is not None:
            result["email"] = from_union([from_none, from_str], self.email)
        if self.emarque_v2 is not None:
            result["emarqueV2"] = from_union([from_bool, from_none], self.emarque_v2)
        if self.engagement is not None:
            result["engagement"] = from_union([from_none, from_str], self.engagement)
        if self.engagements_codes is not None:
            result["engagements_codes"] = from_union(
                [from_str, from_none], self.engagements_codes
            )
        if self.engagements_noms is not None:
            result["engagements_noms"] = from_union(
                [from_str, from_none], self.engagements_noms
            )
        if self.etat is not None:
            result["etat"] = from_union(
                [lambda x: to_enum(Etat, x), from_none], self.etat
            )
        if self.facebook is not None:
            result["facebook"] = from_none(self.facebook)
        if self.fin is not None:
            result["fin"] = from_union([lambda x: x.isoformat(), from_none], self.fin)
        if self.fin_timestamp is not None:
            result["fin_timestamp"] = from_union(
                [from_int, from_none], self.fin_timestamp
            )
        if self.forfait_equipe1 is not None:
            result["forfaitEquipe1"] = from_union(
                [from_bool, from_none], self.forfait_equipe1
            )
        if self.forfait_equipe2 is not None:
            result["forfaitEquipe2"] = from_union(
                [from_bool, from_none], self.forfait_equipe2
            )
        if self.gs_id is not None:
            result["gsId"] = from_none(self.gs_id)
        if self.horaire is not None:
            result["horaire"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: (lambda x: is_type(datetime, x))(x).isoformat())(x)
                    ),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.horaire,
            )
        if self.horaires_seances is not None:
            result["horaires_seances"] = from_union(
                [from_none, from_str], self.horaires_seances
            )
        result["id"] = from_str(self.id)
        if self.id_competition_pere is not None:
            result["idCompetitionPere"] = from_none(self.id_competition_pere)
        if self.id_engagement_equipe1 is not None:
            result["idEngagementEquipe1"] = from_union(
                [lambda x: to_class(IDEngagementEquipe, x), from_none],
                self.id_engagement_equipe1,
            )
        if self.id_engagement_equipe2 is not None:
            result["idEngagementEquipe2"] = from_union(
                [lambda x: to_class(IDEngagementEquipe, x), from_none],
                self.id_engagement_equipe2,
            )
        if self.id_organisme_equipe1 is not None:
            result["idOrganismeEquipe1"] = from_union(
                [lambda x: to_class(IDOrganismeEquipe, x), from_none],
                self.id_organisme_equipe1,
            )
        if self.id_organisme_equipe2 is not None:
            result["idOrganismeEquipe2"] = from_union(
                [lambda x: to_class(IDOrganismeEquipe, x), from_none],
                self.id_organisme_equipe2,
            )
        if self.id_poule is not None:
            result["idPoule"] = from_union(
                [lambda x: to_class(IDPoule, x), from_none], self.id_poule
            )
        if self.inscriptions is not None:
            result["inscriptions"] = from_union(
                [from_none, from_str], self.inscriptions
            )
        if self.joue is not None:
            result["joue"] = from_union([from_bool, from_none], self.joue)
        if self.jours is not None:
            result["jours"] = from_union(
                [lambda x: from_list(lambda x: to_enum(Jour, x), x), from_none],
                self.jours,
            )
        if self.label is not None:
            result["label"] = from_union(
                [lambda x: to_enum(Label, x), from_none], self.label
            )
        if self.labellisation is not None:
            result["labellisation"] = from_union(
                [
                    lambda x: from_list(lambda x: to_enum(Labellisation, x), x),
                    from_none,
                ],
                self.labellisation,
            )
        if self.largeur is not None:
            result["largeur"] = from_union([from_int, from_none], self.largeur)
        if self.latitude is not None:
            result["latitude"] = from_none(self.latitude)
        if self.libelle is not None:
            result["libelle"] = from_union([from_str, from_none], self.libelle)
        if self.libelle2 is not None:
            result["libelle2"] = from_union([from_none, from_str], self.libelle2)
        if self.live_stat is not None:
            result["liveStat"] = from_union([from_bool, from_none], self.live_stat)
        if self.logo is not None:
            result["logo"] = from_union(
                [lambda x: to_class(Logo, x), from_none], self.logo
            )
        if self.longitude is not None:
            result["longitude"] = from_none(self.longitude)
        if self.longueur is not None:
            result["longueur"] = from_union([from_int, from_none], self.longueur)
        if self.mail is not None:
            result["mail"] = from_union([from_none, from_str], self.mail)
        if self.mail_demandeur is not None:
            result["mail_demandeur"] = from_union(
                [from_none, from_str], self.mail_demandeur
            )
        if self.mail_structure is not None:
            result["mail_structure"] = from_union(
                [from_none, from_str], self.mail_structure
            )
        if self.mail_organisateur is not None:
            result["mailOrganisateur"] = from_union(
                [from_none, from_str], self.mail_organisateur
            )
        if self.modification_timestamp is not None:
            result["modification_timestamp"] = from_union(
                [from_int, from_none], self.modification_timestamp
            )
        if self.nature_sol is not None:
            result["natureSol"] = from_union(
                [lambda x: to_class(NatureSolClass, x), from_none], self.nature_sol
            )
        if self.nb_participant_prevu is not None:
            result["nbParticipantPrevu"] = from_none(self.nb_participant_prevu)
        if self.niveau is not None:
            result["niveau"] = from_union(
                [lambda x: to_enum(NiveauEnum, x), from_none], self.niveau
            )
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
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.nom_demandeur is not None:
            result["nom_demandeur"] = from_union(
                [from_none, from_str], self.nom_demandeur
            )
        if self.nom_salle is not None:
            result["nom_salle"] = from_union([from_str, from_none], self.nom_salle)
        if self.nom_simple is not None:
            result["nom_simple"] = from_union([from_none, from_str], self.nom_simple)
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
        if self.nom_club_pro is not None:
            result["nomClubPro"] = from_union(
                [from_none, lambda x: to_enum(NomClubPro, x)], self.nom_club_pro
            )
        if self.nom_equipe1 is not None:
            result["nomEquipe1"] = from_union([from_str, from_none], self.nom_equipe1)
        if self.nom_equipe2 is not None:
            result["nomEquipe2"] = from_union([from_str, from_none], self.nom_equipe2)
        if self.nom_extended is not None:
            result["nomExtended"] = from_union([from_str, from_none], self.nom_extended)
        if self.nom_organisateur is not None:
            result["nomOrganisateur"] = from_union(
                [from_none, from_str], self.nom_organisateur
            )
        if self.numero is not None:
            result["numero"] = from_union([from_int, from_str, from_none], self.numero)
        if self.numero_journee is not None:
            result["numeroJournee"] = from_union(
                [from_str, from_none], self.numero_journee
            )
        if self.objectif is not None:
            result["objectif"] = from_union(
                [from_none, lambda x: to_enum(Objectif, x)], self.objectif
            )
        if self.officiels is not None:
            result["officiels"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_str, from_none],
                self.officiels,
            )
        if self.offres_pratiques is not None:
            result["offresPratiques"] = from_union(
                [
                    lambda x: from_list(lambda x: to_enum(OffresPratique, x), x),
                    from_none,
                ],
                self.offres_pratiques,
            )
        if self.ordre is not None:
            result["ordre"] = from_union([from_int, from_none], self.ordre)
        if self.organisateur is not None:
            result["organisateur"] = from_union(
                [lambda x: to_class(Organisateur, x), from_none], self.organisateur
            )
        if self.organisme_id_pere is not None:
            result["organisme_id_pere"] = from_union(
                [lambda x: to_class(HitOrganismeIDPere, x), from_none],
                self.organisme_id_pere,
            )
        if self.penalite_equipe1 is not None:
            result["penaliteEquipe1"] = from_union(
                [from_bool, from_none], self.penalite_equipe1
            )
        if self.penalite_equipe2 is not None:
            result["penaliteEquipe2"] = from_union(
                [from_bool, from_none], self.penalite_equipe2
            )
        if self.phase_code is not None:
            result["phase_code"] = from_union(
                [lambda x: to_enum(PhaseCode, x), from_none], self.phase_code
            )
        if self.phases is not None:
            result["phases"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.phases
            )
        if self.poules is not None:
            result["poules"] = from_union(
                [lambda x: from_list(lambda x: to_class(Poule, x), x), from_none],
                self.poules,
            )
        if self.pratique is not None:
            result["pratique"] = from_union(
                [lambda x: to_enum(Pratique, x), from_none], self.pratique
            )
        if self.prenom_demandeur is not None:
            result["prenom_demandeur"] = from_union(
                [from_none, from_str], self.prenom_demandeur
            )
        if self.pro is not None:
            result["pro"] = from_union([from_bool, from_none], self.pro)
        if self.public is not None:
            result["public"] = from_union([from_none, from_str], self.public)
        if self.publication_internet is not None:
            result["publicationInternet"] = from_union(
                [lambda x: to_enum(PublicationInternet, x), from_none],
                self.publication_internet,
            )
        if self.resultat_equipe1 is not None:
            result["resultatEquipe1"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.resultat_equipe1,
            )
        if self.resultat_equipe2 is not None:
            result["resultatEquipe2"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.resultat_equipe2,
            )
        if self.rue is not None:
            result["rue"] = from_union([from_none, from_str], self.rue)
        if self.saison is not None:
            result["saison"] = from_union(
                [lambda x: to_class(Saison, x), from_none], self.saison
            )
        if self.saison_en_cours is not None:
            result["saison_en_cours"] = from_union(
                [from_bool, from_none], self.saison_en_cours
            )
        if self.salle is not None:
            result["salle"] = from_union(
                [lambda x: to_class(Salle, x), from_none], self.salle
            )
        if self.sexe is not None:
            result["sexe"] = from_union(
                [lambda x: to_enum(SexeEnum, x), from_none], self.sexe
            )
        if self.site_web is not None:
            result["site_web"] = from_union([from_none, from_str], self.site_web)
        if self.site_choisi is not None:
            result["siteChoisi"] = from_union([from_str, from_none], self.site_choisi)
        if self.slug is not None:
            result["slug"] = from_union([from_str, from_none], self.slug)
        if self.status is not None:
            result["status"] = from_union(
                [lambda x: to_enum(HitStatus, x), from_none], self.status
            )
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
        if self.telephone is not None:
            result["telephone"] = from_union([from_none, from_str], self.telephone)
        if self.telephone_organisateur is not None:
            result["telephoneOrganisateur"] = from_union(
                [from_str, from_none], self.telephone_organisateur
            )
        result["thumbnail"] = from_union([from_none, from_str], self.thumbnail)
        if self.titre is not None:
            result["titre"] = from_union([from_str, from_none], self.titre)
        if self.to_update is not None:
            result["toUpdate"] = from_union([from_bool, from_none], self.to_update)
        if self.tournoi_type is not None:
            result["tournoiType"] = from_union(
                [lambda x: to_enum(TournoiTypeEnum, x), from_none], self.tournoi_type
            )
        if self.tournoi_types3_x3 is not None:
            result["tournoiTypes3x3"] = from_union(
                [
                    lambda x: from_list(lambda x: to_class(TournoiTypes3X3, x), x),
                    from_none,
                ],
                self.tournoi_types3_x3,
            )
        if self.twitter is not None:
            result["twitter"] = from_none(self.twitter)
        if self.type is not None:
            result["type"] = from_union(
                [lambda x: to_enum(HitType, x), from_none], self.type
            )
        if self.type_association is not None:
            result["type_association"] = from_union(
                [lambda x: to_class(TypeAssociation, x), from_none],
                self.type_association,
            )
        if self.type_competition is not None:
            result["typeCompetition"] = from_union(
                [lambda x: to_enum(CompetitionIDTypeCompetitionEnum, x), from_none],
                self.type_competition,
            )
        if self.type_competition_generique is not None:
            result["typeCompetitionGenerique"] = from_union(
                [lambda x: to_class(HitTypeCompetitionGenerique, x), from_none],
                self.type_competition_generique,
            )
        if self.unique_key is not None:
            result["uniqueKey"] = from_union([from_str, from_none], self.unique_key)
        if self.url_competition is not None:
            result["url_competition"] = from_union(
                [from_none, from_str], self.url_competition
            )
        if self.url_organisateur is not None:
            result["urlOrganisateur"] = from_union(
                [from_none, from_str], self.url_organisateur
            )
        if self.url_site_web is not None:
            result["urlSiteWeb"] = from_union([from_none, from_str], self.url_site_web)
        if self.ville_salle is not None:
            result["ville_salle"] = from_union([from_str, from_none], self.ville_salle)
        return result


class Result:
    estimated_total_hits: int
    facet_distribution: Optional[FacetDistribution]
    facet_stats: Optional[FacetStats]
    hits: List[Hit]
    index_uid: str
    limit: int
    offset: int
    processing_time_ms: int
    query: str

    def __init__(
        self,
        estimated_total_hits: int,
        facet_distribution: Optional[FacetDistribution],
        facet_stats: Optional[FacetStats],
        hits: List[Hit],
        index_uid: str,
        limit: int,
        offset: int,
        processing_time_ms: int,
        query: str,
    ) -> None:
        self.estimated_total_hits = estimated_total_hits
        self.facet_distribution = facet_distribution
        self.facet_stats = facet_stats
        self.hits = hits
        self.index_uid = index_uid
        self.limit = limit
        self.offset = offset
        self.processing_time_ms = processing_time_ms
        self.query = query

    @staticmethod
    def from_dict(obj: Any) -> "Result":
        assert isinstance(obj, dict)
        estimated_total_hits = from_int(obj.get("estimatedTotalHits"))
        facet_distribution = from_union(
            [FacetDistribution.from_dict, from_none], obj.get("facetDistribution")
        )
        facet_stats = from_union(
            [FacetStats.from_dict, from_none], obj.get("facetStats")
        )
        hits = from_list(Hit.from_dict, obj.get("hits"))
        index_uid = from_str(obj.get("indexUid"))
        limit = from_int(obj.get("limit"))
        offset = from_int(obj.get("offset"))
        processing_time_ms = from_int(obj.get("processingTimeMs"))
        query = from_str(obj.get("query"))
        return Result(
            estimated_total_hits,
            facet_distribution,
            facet_stats,
            hits,
            index_uid,
            limit,
            offset,
            processing_time_ms,
            query,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["estimatedTotalHits"] = from_int(self.estimated_total_hits)
        if self.facet_distribution is not None:
            result["facetDistribution"] = from_union(
                [lambda x: to_class(FacetDistribution, x), from_none],
                self.facet_distribution,
            )
        if self.facet_stats is not None:
            result["facetStats"] = from_union(
                [lambda x: to_class(FacetStats, x), from_none], self.facet_stats
            )
        result["hits"] = from_list(lambda x: to_class(Hit, x), self.hits)
        result["indexUid"] = from_str(self.index_uid)
        result["limit"] = from_int(self.limit)
        result["offset"] = from_int(self.offset)
        result["processingTimeMs"] = from_int(self.processing_time_ms)
        result["query"] = from_str(self.query)
        return result


class PostMultiSearchResponse:
    results: List[Result]

    def __init__(self, results: List[Result]) -> None:
        self.results = results

    @staticmethod
    def from_dict(obj: Any) -> "PostMultiSearchResponse":
        assert isinstance(obj, dict)
        results = from_list(Result.from_dict, obj.get("results"))
        return PostMultiSearchResponse(results)

    def to_dict(self) -> dict:
        result: dict = {}
        result["results"] = from_list(lambda x: to_class(Result, x), self.results)
        return result


def post_multi_search_response_from_dict(s: Any) -> PostMultiSearchResponse:
    return PostMultiSearchResponse.from_dict(s)


def post_multi_search_response_to_dict(x: PostMultiSearchResponse) -> Any:
    return to_class(PostMultiSearchResponse, x)
