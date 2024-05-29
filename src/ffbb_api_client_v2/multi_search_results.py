from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from ffbb_api_client_v2.CompetitionIDSexe import CompetitionIDSexe
from ffbb_api_client_v2.converters import (
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


@dataclass
class CompetitionIDTypeCompetition:
    championnat: Optional[int] = None
    coupe: Optional[int] = None
    plateau: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionIDTypeCompetition":
        assert isinstance(obj, dict)
        championnat = from_union([from_int, from_none], obj.get("Championnat"))
        coupe = from_union([from_int, from_none], obj.get("Coupe"))
        plateau = from_union([from_int, from_none], obj.get("Plateau"))
        return CompetitionIDTypeCompetition(championnat, coupe, plateau)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.championnat is not None:
            result["Championnat"] = from_union([from_int, from_none], self.championnat)
        if self.coupe is not None:
            result["Coupe"] = from_union([from_int, from_none], self.coupe)
        if self.plateau is not None:
            result["Plateau"] = from_union([from_int, from_none], self.plateau)
        return result


@dataclass
class Label:
    basket_santé_découverte: Optional[int] = None
    basket_santé_résolutions: Optional[int] = None
    micro_basket: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Label":
        assert isinstance(obj, dict)
        basket_santé_découverte = from_union(
            [from_int, from_none], obj.get("Basket Santé Découverte")
        )
        basket_santé_résolutions = from_union(
            [from_int, from_none], obj.get("Basket Santé Résolutions")
        )
        micro_basket = from_union([from_int, from_none], obj.get("Micro Basket"))
        return Label(basket_santé_découverte, basket_santé_résolutions, micro_basket)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.basket_santé_découverte is not None:
            result["Basket Santé Découverte"] = from_union(
                [from_int, from_none], self.basket_santé_découverte
            )
        if self.basket_santé_résolutions is not None:
            result["Basket Santé Résolutions"] = from_union(
                [from_int, from_none], self.basket_santé_résolutions
            )
        if self.micro_basket is not None:
            result["Micro Basket"] = from_union(
                [from_int, from_none], self.micro_basket
            )
        return result


@dataclass
class Labellisation:
    basket_santé_résolutions: Optional[int] = None
    micro_basket: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Labellisation":
        assert isinstance(obj, dict)
        basket_santé_résolutions = from_union(
            [from_int, from_none], obj.get("Basket Santé / Résolutions")
        )
        micro_basket = from_union([from_int, from_none], obj.get("Micro Basket"))
        return Labellisation(basket_santé_résolutions, micro_basket)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.basket_santé_résolutions is not None:
            result["Basket Santé / Résolutions"] = from_union(
                [from_int, from_none], self.basket_santé_résolutions
            )
        if self.micro_basket is not None:
            result["Micro Basket"] = from_union(
                [from_int, from_none], self.micro_basket
            )
        return result


@dataclass
class NiveauClass:
    départemental: Optional[int] = None
    régional: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "NiveauClass":
        assert isinstance(obj, dict)
        départemental = from_union([from_int, from_none], obj.get("Départemental"))
        régional = from_union([from_int, from_none], obj.get("Régional"))
        return NiveauClass(départemental, régional)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.départemental is not None:
            result["Départemental"] = from_union(
                [from_int, from_none], self.départemental
            )
        if self.régional is not None:
            result["Régional"] = from_union([from_int, from_none], self.régional)
        return result


@dataclass
class FacetStats:
    pass

    @staticmethod
    def from_dict(obj: Any) -> "FacetStats":
        assert isinstance(obj, dict)
        return FacetStats()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class TypeClass:
    groupement: Optional[int] = None
    basket_santé: Optional[int] = None
    micro_basket: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "TypeClass":
        assert isinstance(obj, dict)
        groupement = from_union([from_int, from_none], obj.get("Groupement"))
        basket_santé = from_union([from_int, from_none], obj.get("Basket Santé"))
        micro_basket = from_union([from_int, from_none], obj.get("Micro Basket"))
        return TypeClass(groupement, basket_santé, micro_basket)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.groupement is not None:
            result["Groupement"] = from_union([from_int, from_none], self.groupement)
        if self.basket_santé is not None:
            result["Basket Santé"] = from_union(
                [from_int, from_none], self.basket_santé
            )
        if self.micro_basket is not None:
            result["Micro Basket"] = from_union(
                [from_int, from_none], self.micro_basket
            )
        return result


@dataclass
class TypeAssociationLibelle:
    club: Optional[int] = None
    coopération_territoriale_club: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "TypeAssociationLibelle":
        assert isinstance(obj, dict)
        club = from_union([from_int, from_none], obj.get("Club"))
        coopération_territoriale_club = from_union(
            [from_int, from_none], obj.get("Coopération Territoriale Club")
        )
        return TypeAssociationLibelle(club, coopération_territoriale_club)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.club is not None:
            result["Club"] = from_union([from_int, from_none], self.club)
        if self.coopération_territoriale_club is not None:
            result["Coopération Territoriale Club"] = from_union(
                [from_int, from_none], self.coopération_territoriale_club
            )
        return result


@dataclass
class FacetDistribution:
    labellisation: Optional[Labellisation] = None
    offres_pratiques: Optional[Dict[str, int]] = None
    type: Optional[TypeClass] = None
    type_association_libelle: Optional[TypeAssociationLibelle] = None
    competition_id_categorie_code: Optional[Dict[str, int]] = None
    competition_id_nom_extended: Optional[Dict[str, int]] = None
    competition_id_sexe: Optional[CompetitionIDSexe] = None
    competition_id_type_competition: Optional[CompetitionIDTypeCompetition] = None
    niveau: Optional[NiveauClass] = None
    organisateur_id: Optional[Dict[str, int]] = None
    organisateur_nom: Optional[Dict[str, int]] = None
    sexe: Optional[FacetStats] = None
    tournoi_type: Optional[FacetStats] = None
    tournoi_types3_x3_libelle: Optional[FacetStats] = None
    label: Optional[Label] = None

    @staticmethod
    def from_dict(obj: Any) -> "FacetDistribution":
        assert isinstance(obj, dict)
        labellisation = from_union(
            [Labellisation.from_dict, from_none], obj.get("labellisation")
        )
        offres_pratiques = from_union(
            [lambda x: from_dict(from_int, x), from_none], obj.get("offresPratiques")
        )
        type = from_union([TypeClass.from_dict, from_none], obj.get("type"))
        type_association_libelle = from_union(
            [TypeAssociationLibelle.from_dict, from_none],
            obj.get("type_association.libelle"),
        )
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
        niveau = from_union([NiveauClass.from_dict, from_none], obj.get("niveau"))
        organisateur_id = from_union(
            [lambda x: from_dict(from_int, x), from_none], obj.get("organisateur.id")
        )
        organisateur_nom = from_union(
            [lambda x: from_dict(from_int, x), from_none], obj.get("organisateur.nom")
        )
        sexe = from_union([FacetStats.from_dict, from_none], obj.get("sexe"))
        tournoi_type = from_union(
            [FacetStats.from_dict, from_none], obj.get("tournoiType")
        )
        tournoi_types3_x3_libelle = from_union(
            [FacetStats.from_dict, from_none], obj.get("tournoiTypes3x3.libelle")
        )
        label = from_union([Label.from_dict, from_none], obj.get("label"))
        return FacetDistribution(
            labellisation,
            offres_pratiques,
            type,
            type_association_libelle,
            competition_id_categorie_code,
            competition_id_nom_extended,
            competition_id_sexe,
            competition_id_type_competition,
            niveau,
            organisateur_id,
            organisateur_nom,
            sexe,
            tournoi_type,
            tournoi_types3_x3_libelle,
            label,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.labellisation is not None:
            result["labellisation"] = from_union(
                [lambda x: to_class(Labellisation, x), from_none], self.labellisation
            )
        if self.offres_pratiques is not None:
            result["offresPratiques"] = from_union(
                [lambda x: from_dict(from_int, x), from_none], self.offres_pratiques
            )
        if self.type is not None:
            result["type"] = from_union(
                [lambda x: to_class(TypeClass, x), from_none], self.type
            )
        if self.type_association_libelle is not None:
            result["type_association.libelle"] = from_union(
                [lambda x: to_class(TypeAssociationLibelle, x), from_none],
                self.type_association_libelle,
            )
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
        if self.niveau is not None:
            result["niveau"] = from_union(
                [lambda x: to_class(NiveauClass, x), from_none], self.niveau
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
                [lambda x: to_class(FacetStats, x), from_none], self.sexe
            )
        if self.tournoi_type is not None:
            result["tournoiType"] = from_union(
                [lambda x: to_class(FacetStats, x), from_none], self.tournoi_type
            )
        if self.tournoi_types3_x3_libelle is not None:
            result["tournoiTypes3x3.libelle"] = from_union(
                [lambda x: to_class(FacetStats, x), from_none],
                self.tournoi_types3_x3_libelle,
            )
        if self.label is not None:
            result["label"] = from_union(
                [lambda x: to_class(Label, x), from_none], self.label
            )
        return result


class HitAdresseComplement(Enum):
    CORBELIN = "CORBELIN"
    EMPTY = ""


@dataclass
class Affiche:
    id: Optional[UUID] = None
    gradient_color: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Affiche":
        assert isinstance(obj, dict)
        id = from_union([from_none, lambda x: UUID(x)], obj.get("id"))
        gradient_color = from_union([from_str, from_none], obj.get("gradient_color"))
        width = from_union([from_int, from_none], obj.get("width"))
        height = from_union([from_int, from_none], obj.get("height"))
        return Affiche(id, gradient_color, width, height)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_none, lambda x: str(x)], self.id)
        if self.gradient_color is not None:
            result["gradient_color"] = from_union(
                [from_str, from_none], self.gradient_color
            )
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        return result


class CoordonneesType(Enum):
    POINT = "Point"


@dataclass
class Coordonnees:
    type: Optional[CoordonneesType] = None
    coordinates: Optional[List[float]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Coordonnees":
        assert isinstance(obj, dict)
        type = from_union([CoordonneesType, from_none], obj.get("type"))
        coordinates = from_union(
            [lambda x: from_list(from_float, x), from_none], obj.get("coordinates")
        )
        return Coordonnees(type, coordinates)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["type"] = from_union(
                [lambda x: to_enum(CoordonneesType, x), from_none], self.type
            )
        if self.coordinates is not None:
            result["coordinates"] = from_union(
                [lambda x: from_list(to_float, x), from_none], self.coordinates
            )
        return result


class Status(Enum):
    DRAFT = "draft"


@dataclass
class Cartographie:
    adresse: Optional[str] = None
    code_postal: Optional[int] = None
    coordonnees: Optional[Coordonnees] = None
    date_created: None
    date_updated: None
    id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    title: Optional[str] = None
    ville: Optional[str] = None
    status: Optional[Status] = None

    @staticmethod
    def from_dict(obj: Any) -> "Cartographie":
        assert isinstance(obj, dict)
        adresse = from_union([from_none, from_str], obj.get("adresse"))
        code_postal = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("codePostal")
        )
        coordonnees = from_union(
            [Coordonnees.from_dict, from_none], obj.get("coordonnees")
        )
        date_created = from_none(obj.get("date_created"))
        date_updated = from_none(obj.get("date_updated"))
        id = from_union([from_str, from_none], obj.get("id"))
        latitude = from_union([from_float, from_none], obj.get("latitude"))
        longitude = from_union([from_float, from_none], obj.get("longitude"))
        title = from_union([from_none, from_str], obj.get("title"))
        ville = from_union([from_str, from_none], obj.get("ville"))
        status = from_union([Status, from_none], obj.get("status"))
        return Cartographie(
            adresse,
            code_postal,
            coordonnees,
            date_created,
            date_updated,
            id,
            latitude,
            longitude,
            title,
            ville,
            status,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.adresse is not None:
            result["adresse"] = from_union([from_none, from_str], self.adresse)
        if self.code_postal is not None:
            result["codePostal"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.code_postal,
            )
        if self.coordonnees is not None:
            result["coordonnees"] = from_union(
                [lambda x: to_class(Coordonnees, x), from_none], self.coordonnees
            )
        if self.date_created is not None:
            result["date_created"] = from_none(self.date_created)
        if self.date_updated is not None:
            result["date_updated"] = from_none(self.date_updated)
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.latitude is not None:
            result["latitude"] = from_union([to_float, from_none], self.latitude)
        if self.longitude is not None:
            result["longitude"] = from_union([to_float, from_none], self.longitude)
        if self.title is not None:
            result["title"] = from_union([from_none, from_str], self.title)
        if self.ville is not None:
            result["ville"] = from_union([from_str, from_none], self.ville)
        if self.status is not None:
            result["status"] = from_union(
                [lambda x: to_enum(Status, x), from_none], self.status
            )
        return result


@dataclass
class Commune:
    libelle: Optional[str] = None
    code_postal: Optional[int] = None
    departement: Optional[str] = None
    code_insee: None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None
    id: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Commune":
        assert isinstance(obj, dict)
        libelle = from_union([from_str, from_none], obj.get("libelle"))
        code_postal = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("codePostal")
        )
        departement = from_union([from_str, from_none], obj.get("departement"))
        code_insee = from_none(obj.get("codeInsee"))
        date_created = from_union([from_datetime, from_none], obj.get("date_created"))
        date_updated = from_union([from_datetime, from_none], obj.get("date_updated"))
        id = from_union([from_str, from_none], obj.get("id"))
        return Commune(
            libelle,
            code_postal,
            departement,
            code_insee,
            date_created,
            date_updated,
            id,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.libelle is not None:
            result["libelle"] = from_union([from_str, from_none], self.libelle)
        if self.code_postal is not None:
            result["codePostal"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.code_postal,
            )
        if self.departement is not None:
            result["departement"] = from_union([from_str, from_none], self.departement)
        if self.code_insee is not None:
            result["codeInsee"] = from_none(self.code_insee)
        if self.date_created is not None:
            result["date_created"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_created
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_updated
            )
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        return result


class LibelleEnum(Enum):
    SE = "SE"
    SENIORS = "Seniors"
    U11 = "U11"
    U13 = "U13"
    U15 = "U15"
    U17 = "U17"


@dataclass
class CompetitionIDCategorie:
    code: Optional[LibelleEnum] = None
    libelle: Optional[LibelleEnum] = None
    ordre: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionIDCategorie":
        assert isinstance(obj, dict)
        code = from_union([LibelleEnum, from_none], obj.get("code"))
        libelle = from_union([LibelleEnum, from_none], obj.get("libelle"))
        ordre = from_union([from_int, from_none], obj.get("ordre"))
        return CompetitionIDCategorie(code, libelle, ordre)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = from_union(
                [lambda x: to_enum(LibelleEnum, x), from_none], self.code
            )
        if self.libelle is not None:
            result["libelle"] = from_union(
                [lambda x: to_enum(LibelleEnum, x), from_none], self.libelle
            )
        if self.ordre is not None:
            result["ordre"] = from_union([from_int, from_none], self.ordre)
        return result


@dataclass
class CompetitionOrigineCategorie:
    ordre: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionOrigineCategorie":
        assert isinstance(obj, dict)
        ordre = from_union([from_int, from_none], obj.get("ordre"))
        return CompetitionOrigineCategorie(ordre)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.ordre is not None:
            result["ordre"] = from_union([from_int, from_none], self.ordre)
        return result


class CompetitionOrigineTypeCompetition(Enum):
    COUPE = "COUPE"
    DIV = "DIV"
    PLAT = "PLAT"


@dataclass
class PurpleLogo:
    id: Optional[UUID] = None

    @staticmethod
    def from_dict(obj: Any) -> "PurpleLogo":
        assert isinstance(obj, dict)
        id = from_union([from_none, lambda x: UUID(x)], obj.get("id"))
        return PurpleLogo(id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_none, lambda x: str(x)], self.id)
        return result


@dataclass
class CompetitionOrigineTypeCompetitionGenerique:
    logo: Optional[PurpleLogo] = None

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionOrigineTypeCompetitionGenerique":
        assert isinstance(obj, dict)
        logo = from_union([PurpleLogo.from_dict, from_none], obj.get("logo"))
        return CompetitionOrigineTypeCompetitionGenerique(logo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.logo is not None:
            result["logo"] = from_union(
                [lambda x: to_class(PurpleLogo, x), from_none], self.logo
            )
        return result


@dataclass
class CompetitionOrigine:
    id: Optional[str] = None
    code: Optional[str] = None
    nom: Optional[str] = None
    type_competition: Optional[CompetitionOrigineTypeCompetition] = None
    categorie: Optional[CompetitionOrigineCategorie] = None
    type_competition_generique: Optional[CompetitionOrigineTypeCompetitionGenerique] = (
        None
    )

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionOrigine":
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        code = from_union([from_str, from_none], obj.get("code"))
        nom = from_union([from_str, from_none], obj.get("nom"))
        type_competition = from_union(
            [CompetitionOrigineTypeCompetition, from_none], obj.get("typeCompetition")
        )
        categorie = from_union(
            [CompetitionOrigineCategorie.from_dict, from_none], obj.get("categorie")
        )
        type_competition_generique = from_union(
            [CompetitionOrigineTypeCompetitionGenerique.from_dict, from_none],
            obj.get("typeCompetitionGenerique"),
        )
        return CompetitionOrigine(
            id, code, nom, type_competition, categorie, type_competition_generique
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.type_competition is not None:
            result["typeCompetition"] = from_union(
                [lambda x: to_enum(CompetitionOrigineTypeCompetition, x), from_none],
                self.type_competition,
            )
        if self.categorie is not None:
            result["categorie"] = from_union(
                [lambda x: to_class(CompetitionOrigineCategorie, x), from_none],
                self.categorie,
            )
        if self.type_competition_generique is not None:
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


class Sexe(Enum):
    FÉMININ = "Féminin"
    MASCULIN = "Masculin"
    MIXTE = "Mixte"


class CompetitionIDTypeCompetitionEnum(Enum):
    CHAMPIONNAT = "Championnat"
    COUPE = "Coupe"
    PLATEAU = "Plateau"


@dataclass
class IDOrganismeEquipe1Logo:
    id: Optional[UUID] = None
    gradient_color: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "IDOrganismeEquipe1Logo":
        assert isinstance(obj, dict)
        id = from_union([from_none, lambda x: UUID(x)], obj.get("id"))
        gradient_color = from_union([from_str, from_none], obj.get("gradient_color"))
        return IDOrganismeEquipe1Logo(id, gradient_color)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_none, lambda x: str(x)], self.id)
        if self.gradient_color is not None:
            result["gradient_color"] = from_union(
                [from_str, from_none], self.gradient_color
            )
        return result


@dataclass
class CompetitionIDTypeCompetitionGenerique:
    logo: Optional[IDOrganismeEquipe1Logo] = None

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionIDTypeCompetitionGenerique":
        assert isinstance(obj, dict)
        logo = from_union(
            [IDOrganismeEquipe1Logo.from_dict, from_none], obj.get("logo")
        )
        return CompetitionIDTypeCompetitionGenerique(logo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.logo is not None:
            result["logo"] = from_union(
                [lambda x: to_class(IDOrganismeEquipe1Logo, x), from_none], self.logo
            )
        return result


@dataclass
class CompetitionID:
    id: Optional[str] = None
    nom: Optional[str] = None
    competition_origine_nom: Optional[str] = None
    code: Optional[str] = None
    creation_en_cours: Optional[bool] = None
    live_stat: Optional[bool] = None
    publication_internet: Optional[PublicationInternet] = None
    sexe: Optional[Sexe] = None
    type_competition: Optional[CompetitionIDTypeCompetitionEnum] = None
    pro: Optional[bool] = None
    logo: None
    categorie: Optional[CompetitionIDCategorie] = None
    type_competition_generique: Optional[CompetitionIDTypeCompetitionGenerique] = None
    competition_origine: Optional[CompetitionOrigine] = None
    nom_extended: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionID":
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        nom = from_union([from_str, from_none], obj.get("nom"))
        competition_origine_nom = from_union(
            [from_str, from_none], obj.get("competition_origine_nom")
        )
        code = from_union([from_str, from_none], obj.get("code"))
        creation_en_cours = from_union(
            [from_bool, from_none], obj.get("creationEnCours")
        )
        live_stat = from_union([from_bool, from_none], obj.get("liveStat"))
        publication_internet = from_union(
            [PublicationInternet, from_none], obj.get("publicationInternet")
        )
        sexe = from_union([Sexe, from_none], obj.get("sexe"))
        type_competition = from_union(
            [CompetitionIDTypeCompetitionEnum, from_none], obj.get("typeCompetition")
        )
        pro = from_union([from_bool, from_none], obj.get("pro"))
        logo = from_none(obj.get("logo"))
        categorie = from_union(
            [CompetitionIDCategorie.from_dict, from_none], obj.get("categorie")
        )
        type_competition_generique = from_union(
            [CompetitionIDTypeCompetitionGenerique.from_dict, from_none],
            obj.get("typeCompetitionGenerique"),
        )
        competition_origine = from_union(
            [CompetitionOrigine.from_dict, from_none], obj.get("competition_origine")
        )
        nom_extended = from_union([from_str, from_none], obj.get("nomExtended"))
        return CompetitionID(
            id,
            nom,
            competition_origine_nom,
            code,
            creation_en_cours,
            live_stat,
            publication_internet,
            sexe,
            type_competition,
            pro,
            logo,
            categorie,
            type_competition_generique,
            competition_origine,
            nom_extended,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.competition_origine_nom is not None:
            result["competition_origine_nom"] = from_union(
                [from_str, from_none], self.competition_origine_nom
            )
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.creation_en_cours is not None:
            result["creationEnCours"] = from_union(
                [from_bool, from_none], self.creation_en_cours
            )
        if self.live_stat is not None:
            result["liveStat"] = from_union([from_bool, from_none], self.live_stat)
        if self.publication_internet is not None:
            result["publicationInternet"] = from_union(
                [lambda x: to_enum(PublicationInternet, x), from_none],
                self.publication_internet,
            )
        if self.sexe is not None:
            result["sexe"] = from_union(
                [lambda x: to_enum(Sexe, x), from_none], self.sexe
            )
        if self.type_competition is not None:
            result["typeCompetition"] = from_union(
                [lambda x: to_enum(CompetitionIDTypeCompetitionEnum, x), from_none],
                self.type_competition,
            )
        if self.pro is not None:
            result["pro"] = from_union([from_bool, from_none], self.pro)
        if self.logo is not None:
            result["logo"] = from_none(self.logo)
        if self.categorie is not None:
            result["categorie"] = from_union(
                [lambda x: to_class(CompetitionIDCategorie, x), from_none],
                self.categorie,
            )
        if self.type_competition_generique is not None:
            result["typeCompetitionGenerique"] = from_union(
                [
                    lambda x: to_class(CompetitionIDTypeCompetitionGenerique, x),
                    from_none,
                ],
                self.type_competition_generique,
            )
        if self.competition_origine is not None:
            result["competition_origine"] = from_union(
                [lambda x: to_class(CompetitionOrigine, x), from_none],
                self.competition_origine,
            )
        if self.nom_extended is not None:
            result["nomExtended"] = from_union([from_str, from_none], self.nom_extended)
        return result


@dataclass
class Geo:
    lat: Optional[float] = None
    lng: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> "Geo":
        assert isinstance(obj, dict)
        lat = from_union([from_float, from_none], obj.get("lat"))
        lng = from_union([from_float, from_none], obj.get("lng"))
        return Geo(lat, lng)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.lat is not None:
            result["lat"] = from_union([to_float, from_none], self.lat)
        if self.lng is not None:
            result["lng"] = from_union([to_float, from_none], self.lng)
        return result


@dataclass
class IDEngagementEquipe:
    id: Optional[str] = None
    nom_usuel: Optional[str] = None
    logo: None

    @staticmethod
    def from_dict(obj: Any) -> "IDEngagementEquipe":
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        nom_usuel = from_union([from_none, from_str], obj.get("nomUsuel"))
        logo = from_none(obj.get("logo"))
        return IDEngagementEquipe(id, nom_usuel, logo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.nom_usuel is not None:
            result["nomUsuel"] = from_union([from_none, from_str], self.nom_usuel)
        if self.logo is not None:
            result["logo"] = from_none(self.logo)
        return result


class NomClubPro(Enum):
    EMPTY = ""
    SAS_FOS_PROVENCE_BASKET = "SAS FOS PROVENCE BASKET"


@dataclass
class IDOrganismeEquipe:
    id: Optional[str] = None
    nom: Optional[str] = None
    nom_simple: None
    code: Optional[str] = None
    nom_club_pro: Optional[NomClubPro] = None
    logo: Optional[IDOrganismeEquipe1Logo] = None

    @staticmethod
    def from_dict(obj: Any) -> "IDOrganismeEquipe":
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        nom = from_union([from_str, from_none], obj.get("nom"))
        nom_simple = from_none(obj.get("nom_simple"))
        code = from_union([from_str, from_none], obj.get("code"))
        nom_club_pro = from_union([NomClubPro, from_none], obj.get("nomClubPro"))
        logo = from_union(
            [IDOrganismeEquipe1Logo.from_dict, from_none], obj.get("logo")
        )
        return IDOrganismeEquipe(id, nom, nom_simple, code, nom_club_pro, logo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.nom_simple is not None:
            result["nom_simple"] = from_none(self.nom_simple)
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.nom_club_pro is not None:
            result["nomClubPro"] = from_union(
                [lambda x: to_enum(NomClubPro, x), from_none], self.nom_club_pro
            )
        if self.logo is not None:
            result["logo"] = from_union(
                [lambda x: to_class(IDOrganismeEquipe1Logo, x), from_none], self.logo
            )
        return result


class Nom(Enum):
    POULE_A = "Poule A"
    POULE_B = "Poule B"
    POULE_C = "Poule C"
    POULE_D = "Poule D"
    POULE_E = "Poule E"


@dataclass
class IDPoule:
    id: Optional[str] = None
    nom: Optional[Nom] = None

    @staticmethod
    def from_dict(obj: Any) -> "IDPoule":
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        nom = from_union([Nom, from_none], obj.get("nom"))
        return IDPoule(id, nom)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.nom is not None:
            result["nom"] = from_union([lambda x: to_enum(Nom, x), from_none], self.nom)
        return result


class Libelle2(Enum):
    BON_PASTEUR = "BON PASTEUR"
    EMPTY = ""
    GYMNASE_SYLVAIN_DUPECHEZ = "GYMNASE SYLVAIN DUPECHEZ"
    PIERRE_DE_COUBERTIN = "Pierre de Coubertin"


class NatureSolCode(Enum):
    BIT = "BIT"
    BT = "BT"
    SS = "SS"


class NatureSolLibelle(Enum):
    BITUME = "BITUME"
    BÉTON = "Béton"
    SOL_SYNTHÉTIQUE = "Sol synthétique"


@dataclass
class NatureSol:
    code: Optional[NatureSolCode] = None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None
    id: Optional[str] = None
    libelle: Optional[NatureSolLibelle] = None
    terrain: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> "NatureSol":
        assert isinstance(obj, dict)
        code = from_union([NatureSolCode, from_none], obj.get("code"))
        date_created = from_union([from_datetime, from_none], obj.get("date_created"))
        date_updated = from_union([from_datetime, from_none], obj.get("date_updated"))
        id = from_union([from_str, from_none], obj.get("id"))
        libelle = from_union([NatureSolLibelle, from_none], obj.get("libelle"))
        terrain = from_union(
            [from_none, lambda x: from_stringified_bool(from_str(x))],
            obj.get("terrain"),
        )
        return NatureSol(code, date_created, date_updated, id, libelle, terrain)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = from_union(
                [lambda x: to_enum(NatureSolCode, x), from_none], self.code
            )
        if self.date_created is not None:
            result["date_created"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_created
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_updated
            )
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.libelle is not None:
            result["libelle"] = from_union(
                [lambda x: to_enum(NatureSolLibelle, x), from_none], self.libelle
            )
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


class NiveauEnum(Enum):
    DÉPARTEMENTAL = "Départemental"
    RÉGIONAL = "Régional"


class OrganisateurType(Enum):
    C = "C"
    L = "L"


@dataclass
class Organisateur:
    id: Optional[str] = None
    code: Optional[str] = None
    nom: Optional[str] = None
    type: Optional[OrganisateurType] = None

    @staticmethod
    def from_dict(obj: Any) -> "Organisateur":
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        code = from_union([from_str, from_none], obj.get("code"))
        nom = from_union([from_str, from_none], obj.get("nom"))
        type = from_union([OrganisateurType, from_none], obj.get("type"))
        return Organisateur(id, code, nom, type)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.type is not None:
            result["type"] = from_union(
                [lambda x: to_enum(OrganisateurType, x), from_none], self.type
            )
        return result


@dataclass
class OrganismeIDPere:
    adresse: Optional[str] = None
    adresse_club_pro: None
    cartographie: Optional[str] = None
    code: Optional[str] = None
    commune: Optional[int] = None
    commune_club_pro: None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None
    id: Optional[int] = None
    mail: Optional[str] = None
    nom: Optional[str] = None
    nom_club_pro: Optional[str] = None
    organisme_id_pere: Optional[str] = None
    salle: None
    telephone: Optional[str] = None
    type: Optional[str] = None
    type_association: None
    url_site_web: Optional[str] = None
    logo: Optional[UUID] = None
    nom_simple: Optional[str] = None
    date_affiliation: None
    saison_en_cours: Optional[bool] = None
    entreprise: Optional[bool] = None
    handibasket: Optional[bool] = None
    omnisport: Optional[bool] = None
    hors_association: Optional[bool] = None
    offres_pratiques: Optional[List[Any]] = None
    engagements: Optional[List[Any]] = None
    labellisation: Optional[List[Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> "OrganismeIDPere":
        assert isinstance(obj, dict)
        adresse = from_union([from_str, from_none], obj.get("adresse"))
        adresse_club_pro = from_none(obj.get("adresseClubPro"))
        cartographie = from_union([from_str, from_none], obj.get("cartographie"))
        code = from_union([from_str, from_none], obj.get("code"))
        commune = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("commune")
        )
        commune_club_pro = from_none(obj.get("communeClubPro"))
        date_created = from_union([from_datetime, from_none], obj.get("date_created"))
        date_updated = from_union([from_datetime, from_none], obj.get("date_updated"))
        id = from_union([from_none, lambda x: int(from_str(x))], obj.get("id"))
        mail = from_union([from_str, from_none], obj.get("mail"))
        nom = from_union([from_str, from_none], obj.get("nom"))
        nom_club_pro = from_union([from_str, from_none], obj.get("nomClubPro"))
        organisme_id_pere = from_union(
            [from_str, from_none], obj.get("organisme_id_pere")
        )
        salle = from_none(obj.get("salle"))
        telephone = from_union([from_str, from_none], obj.get("telephone"))
        type = from_union([from_str, from_none], obj.get("type"))
        type_association = from_none(obj.get("type_association"))
        url_site_web = from_union([from_str, from_none], obj.get("urlSiteWeb"))
        logo = from_union([from_none, lambda x: UUID(x)], obj.get("logo"))
        nom_simple = from_union([from_str, from_none], obj.get("nom_simple"))
        date_affiliation = from_none(obj.get("dateAffiliation"))
        saison_en_cours = from_union([from_bool, from_none], obj.get("saison_en_cours"))
        entreprise = from_union([from_bool, from_none], obj.get("entreprise"))
        handibasket = from_union([from_bool, from_none], obj.get("handibasket"))
        omnisport = from_union([from_bool, from_none], obj.get("omnisport"))
        hors_association = from_union(
            [from_bool, from_none], obj.get("horsAssociation")
        )
        offres_pratiques = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], obj.get("offresPratiques")
        )
        engagements = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], obj.get("engagements")
        )
        labellisation = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], obj.get("labellisation")
        )
        return OrganismeIDPere(
            adresse,
            adresse_club_pro,
            cartographie,
            code,
            commune,
            commune_club_pro,
            date_created,
            date_updated,
            id,
            mail,
            nom,
            nom_club_pro,
            organisme_id_pere,
            salle,
            telephone,
            type,
            type_association,
            url_site_web,
            logo,
            nom_simple,
            date_affiliation,
            saison_en_cours,
            entreprise,
            handibasket,
            omnisport,
            hors_association,
            offres_pratiques,
            engagements,
            labellisation,
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
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.commune is not None:
            result["commune"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.commune,
            )
        if self.commune_club_pro is not None:
            result["communeClubPro"] = from_none(self.commune_club_pro)
        if self.date_created is not None:
            result["date_created"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_created
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_updated
            )
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
        if self.mail is not None:
            result["mail"] = from_union([from_str, from_none], self.mail)
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.nom_club_pro is not None:
            result["nomClubPro"] = from_union([from_str, from_none], self.nom_club_pro)
        if self.organisme_id_pere is not None:
            result["organisme_id_pere"] = from_union(
                [from_str, from_none], self.organisme_id_pere
            )
        if self.salle is not None:
            result["salle"] = from_none(self.salle)
        if self.telephone is not None:
            result["telephone"] = from_union([from_str, from_none], self.telephone)
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        if self.type_association is not None:
            result["type_association"] = from_none(self.type_association)
        if self.url_site_web is not None:
            result["urlSiteWeb"] = from_union([from_str, from_none], self.url_site_web)
        if self.logo is not None:
            result["logo"] = from_union([from_none, lambda x: str(x)], self.logo)
        if self.nom_simple is not None:
            result["nom_simple"] = from_union([from_str, from_none], self.nom_simple)
        if self.date_affiliation is not None:
            result["dateAffiliation"] = from_none(self.date_affiliation)
        if self.saison_en_cours is not None:
            result["saison_en_cours"] = from_union(
                [from_bool, from_none], self.saison_en_cours
            )
        if self.entreprise is not None:
            result["entreprise"] = from_union([from_bool, from_none], self.entreprise)
        if self.handibasket is not None:
            result["handibasket"] = from_union([from_bool, from_none], self.handibasket)
        if self.omnisport is not None:
            result["omnisport"] = from_union([from_bool, from_none], self.omnisport)
        if self.hors_association is not None:
            result["horsAssociation"] = from_union(
                [from_bool, from_none], self.hors_association
            )
        if self.offres_pratiques is not None:
            result["offresPratiques"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.offres_pratiques
            )
        if self.engagements is not None:
            result["engagements"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.engagements
            )
        if self.labellisation is not None:
            result["labellisation"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.labellisation
            )
        return result


class Pratique(Enum):
    THE_5_X5 = "5x5"


class SaisonCode(Enum):
    THE_2324 = "23-24"


@dataclass
class Saison:
    code: Optional[SaisonCode] = None

    @staticmethod
    def from_dict(obj: Any) -> "Saison":
        assert isinstance(obj, dict)
        code = from_union([SaisonCode, from_none], obj.get("code"))
        return Saison(code)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = from_union(
                [lambda x: to_enum(SaisonCode, x), from_none], self.code
            )
        return result


class SalleAdresseComplement(Enum):
    ANC_RUE_DU_LYCÉE = "Anc. rue du Lycée"
    EMPTY = ""


@dataclass
class Salle:
    id: Optional[str] = None
    libelle: Optional[str] = None
    adresse: Optional[str] = None
    adresse_complement: Optional[SalleAdresseComplement] = None
    cartographie: Optional[Cartographie] = None

    @staticmethod
    def from_dict(obj: Any) -> "Salle":
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        libelle = from_union([from_str, from_none], obj.get("libelle"))
        adresse = from_union([from_str, from_none], obj.get("adresse"))
        adresse_complement = from_union(
            [SalleAdresseComplement, from_none], obj.get("adresseComplement")
        )
        cartographie = from_union(
            [Cartographie.from_dict, from_none], obj.get("cartographie")
        )
        return Salle(id, libelle, adresse, adresse_complement, cartographie)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.libelle is not None:
            result["libelle"] = from_union([from_str, from_none], self.libelle)
        if self.adresse is not None:
            result["adresse"] = from_union([from_str, from_none], self.adresse)
        if self.adresse_complement is not None:
            result["adresseComplement"] = from_union(
                [lambda x: to_enum(SalleAdresseComplement, x), from_none],
                self.adresse_complement,
            )
        if self.cartographie is not None:
            result["cartographie"] = from_union(
                [lambda x: to_class(Cartographie, x), from_none], self.cartographie
            )
        return result


class HitType(Enum):
    BASKET_SANTÉ = "Basket Santé"
    GROUPEMENT = "Groupement"
    MICRO_BASKET = "Micro Basket"
    SALLE = "Salle"
    TERRAIN = "Terrain"


class TypeAssociationLibelleEnum(Enum):
    CLUB = "Club"
    COOPÉRATION_TERRITORIALE_CLUB = "Coopération Territoriale Club"
    SALLE = "Salle"


@dataclass
class TypeAssociation:
    libelle: Optional[TypeAssociationLibelleEnum] = None

    @staticmethod
    def from_dict(obj: Any) -> "TypeAssociation":
        assert isinstance(obj, dict)
        libelle = from_union(
            [TypeAssociationLibelleEnum, from_none], obj.get("libelle")
        )
        return TypeAssociation(libelle)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.libelle is not None:
            result["libelle"] = from_union(
                [lambda x: to_enum(TypeAssociationLibelleEnum, x), from_none],
                self.libelle,
            )
        return result


@dataclass
class Hit:
    nom_club_pro: Optional[str] = None
    nom: Optional[str] = None
    adresse: Optional[str] = None
    adresse_club_pro: None
    code: Optional[str] = None
    id: Optional[str] = None
    engagements_noms: Optional[str] = None
    mail: Optional[str] = None
    telephone: Optional[str] = None
    type: Optional[HitType] = None
    url_site_web: Optional[str] = None
    nom_simple: None
    date_affiliation: None
    saison_en_cours: Optional[bool] = None
    offres_pratiques: Optional[List[str]] = None
    labellisation: Optional[List[str]] = None
    cartographie: Optional[Cartographie] = None
    organisme_id_pere: Optional[OrganismeIDPere] = None
    commune: Optional[Commune] = None
    commune_club_pro: None
    type_association: Optional[TypeAssociation] = None
    logo: Optional[IDOrganismeEquipe1Logo] = None
    geo: Optional[Geo] = None
    thumbnail: Optional[str] = None
    niveau: Optional[NiveauEnum] = None
    date: Optional[datetime] = None
    date_rencontre: Optional[datetime] = None
    horaire: Optional[int] = None
    nom_equipe1: Optional[str] = None
    nom_equipe2: Optional[str] = None
    numero_journee: Optional[int] = None
    pratique: Optional[Pratique] = None
    gs_id: None
    officiels: Optional[List[str]] = None
    competition_id: Optional[CompetitionID] = None
    id_organisme_equipe1: Optional[IDOrganismeEquipe] = None
    id_organisme_equipe2: Optional[IDOrganismeEquipe] = None
    id_poule: Optional[IDPoule] = None
    saison: Optional[Saison] = None
    salle: Optional[Salle] = None
    id_engagement_equipe1: Optional[IDEngagementEquipe] = None
    id_engagement_equipe2: Optional[IDEngagementEquipe] = None
    date_timestamp: Optional[int] = None
    date_rencontre_timestamp: Optional[int] = None
    creation_timestamp: Optional[int] = None
    date_saisie_resultat_timestamp: Optional[int] = None
    modification_timestamp: Optional[int] = None
    organisateur: Optional[Organisateur] = None
    niveau_nb: Optional[int] = None
    rue: Optional[str] = None
    acces_libre: Optional[bool] = None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None
    largeur: Optional[int] = None
    longueur: Optional[int] = None
    numero: Optional[Union[int, str]] = None
    nature_sol: Optional[NatureSol] = None
    libelle: Optional[str] = None
    adresse_complement: Optional[HitAdresseComplement] = None
    capacite_spectateur: Optional[str] = None
    libelle2: Optional[Libelle2] = None
    titre: Optional[str] = None
    description: None
    date_debut: Optional[datetime] = None
    date_demande: Optional[int] = None
    date_fin: Optional[datetime] = None
    facebook: None
    site_web: Optional[str] = None
    twitter: None
    action: Optional[str] = None
    adresse_salle: Optional[str] = None
    adresse_structure: Optional[str] = None
    assurance: Optional[str] = None
    cp_salle: Optional[int] = None
    date_inscription: Optional[int] = None
    email: Optional[str] = None
    engagement: Optional[str] = None
    horaires_seances: Optional[str] = None
    inscriptions: Optional[str] = None
    jours: Optional[List[str]] = None
    label: Optional[str] = None
    latitude: None
    longitude: None
    mail_demandeur: Optional[str] = None
    mail_structure: Optional[str] = None
    nom_demandeur: Optional[str] = None
    nom_salle: Optional[str] = None
    nom_structure: Optional[str] = None
    nombre_personnes: Optional[str] = None
    nombre_seances: Optional[int] = None
    objectif: Optional[str] = None
    prenom_demandeur: Optional[str] = None
    public: Optional[str] = None
    ville_salle: Optional[str] = None
    affiche: Optional[Affiche] = None
    date_debut_timestamp: Optional[int] = None
    date_fin_timestamp: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Hit":
        assert isinstance(obj, dict)
        nom_club_pro = from_union([from_str, from_none], obj.get("nomClubPro"))
        nom = from_union([from_str, from_none], obj.get("nom"))
        adresse = from_union([from_str, from_none], obj.get("adresse"))
        adresse_club_pro = from_none(obj.get("adresseClubPro"))
        code = from_union([from_str, from_none], obj.get("code"))
        id = from_union([from_str, from_none], obj.get("id"))
        engagements_noms = from_union(
            [from_str, from_none], obj.get("engagements_noms")
        )
        mail = from_union([from_none, from_str], obj.get("mail"))
        telephone = from_union([from_none, from_str], obj.get("telephone"))
        type = from_union([HitType, from_none], obj.get("type"))
        url_site_web = from_union([from_str, from_none], obj.get("urlSiteWeb"))
        nom_simple = from_none(obj.get("nom_simple"))
        date_affiliation = from_none(obj.get("dateAffiliation"))
        saison_en_cours = from_union([from_bool, from_none], obj.get("saison_en_cours"))
        offres_pratiques = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("offresPratiques")
        )
        labellisation = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("labellisation")
        )
        cartographie = from_union(
            [Cartographie.from_dict, from_none], obj.get("cartographie")
        )
        organisme_id_pere = from_union(
            [OrganismeIDPere.from_dict, from_none], obj.get("organisme_id_pere")
        )
        commune = from_union([Commune.from_dict, from_none], obj.get("commune"))
        commune_club_pro = from_none(obj.get("communeClubPro"))
        type_association = from_union(
            [TypeAssociation.from_dict, from_none], obj.get("type_association")
        )
        logo = from_union(
            [IDOrganismeEquipe1Logo.from_dict, from_none], obj.get("logo")
        )
        geo = from_union([Geo.from_dict, from_none], obj.get("_geo"))
        thumbnail = from_union([from_none, from_str], obj.get("thumbnail"))
        niveau = from_union([NiveauEnum, from_none], obj.get("niveau"))
        date = from_union([from_datetime, from_none], obj.get("date"))
        date_rencontre = from_union(
            [from_datetime, from_none], obj.get("date_rencontre")
        )
        horaire = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("horaire")
        )
        nom_equipe1 = from_union([from_str, from_none], obj.get("nomEquipe1"))
        nom_equipe2 = from_union([from_str, from_none], obj.get("nomEquipe2"))
        numero_journee = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("numeroJournee")
        )
        pratique = from_union([from_none, Pratique], obj.get("pratique"))
        gs_id = from_none(obj.get("gsId"))
        officiels = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("officiels")
        )
        competition_id = from_union(
            [CompetitionID.from_dict, from_none], obj.get("competitionId")
        )
        id_organisme_equipe1 = from_union(
            [IDOrganismeEquipe.from_dict, from_none], obj.get("idOrganismeEquipe1")
        )
        id_organisme_equipe2 = from_union(
            [IDOrganismeEquipe.from_dict, from_none], obj.get("idOrganismeEquipe2")
        )
        id_poule = from_union([IDPoule.from_dict, from_none], obj.get("idPoule"))
        saison = from_union([Saison.from_dict, from_none], obj.get("saison"))
        salle = from_union([Salle.from_dict, from_none], obj.get("salle"))
        id_engagement_equipe1 = from_union(
            [IDEngagementEquipe.from_dict, from_none], obj.get("idEngagementEquipe1")
        )
        id_engagement_equipe2 = from_union(
            [IDEngagementEquipe.from_dict, from_none], obj.get("idEngagementEquipe2")
        )
        date_timestamp = from_union([from_int, from_none], obj.get("date_timestamp"))
        date_rencontre_timestamp = from_union(
            [from_int, from_none], obj.get("date_rencontre_timestamp")
        )
        creation_timestamp = from_union(
            [from_int, from_none], obj.get("creation_timestamp")
        )
        date_saisie_resultat_timestamp = from_union(
            [from_int, from_none], obj.get("dateSaisieResultat_timestamp")
        )
        modification_timestamp = from_union(
            [from_int, from_none], obj.get("modification_timestamp")
        )
        organisateur = from_union(
            [Organisateur.from_dict, from_none], obj.get("organisateur")
        )
        niveau_nb = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("niveau_nb")
        )
        rue = from_union([from_str, from_none], obj.get("rue"))
        acces_libre = from_union([from_bool, from_none], obj.get("accesLibre"))
        date_created = from_union([from_datetime, from_none], obj.get("date_created"))
        date_updated = from_union([from_datetime, from_none], obj.get("date_updated"))
        largeur = from_union([from_int, from_none], obj.get("largeur"))
        longueur = from_union([from_int, from_none], obj.get("longueur"))
        numero = from_union([from_int, from_str, from_none], obj.get("numero"))
        nature_sol = from_union([NatureSol.from_dict, from_none], obj.get("natureSol"))
        libelle = from_union([from_str, from_none], obj.get("libelle"))
        adresse_complement = from_union(
            [HitAdresseComplement, from_none], obj.get("adresseComplement")
        )
        capacite_spectateur = from_union(
            [from_str, from_none], obj.get("capaciteSpectateur")
        )
        libelle2 = from_union([Libelle2, from_none], obj.get("libelle2"))
        titre = from_union([from_str, from_none], obj.get("titre"))
        description = from_none(obj.get("description"))
        date_debut = from_union([from_datetime, from_none], obj.get("date_debut"))
        date_demande = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("date_demande")
        )
        date_fin = from_union([from_datetime, from_none], obj.get("date_fin"))
        facebook = from_none(obj.get("facebook"))
        site_web = from_union([from_none, from_str], obj.get("site_web"))
        twitter = from_none(obj.get("twitter"))
        action = from_union([from_str, from_none], obj.get("action"))
        adresse_salle = from_union([from_str, from_none], obj.get("adresse_salle"))
        adresse_structure = from_union(
            [from_none, from_str], obj.get("adresse_structure")
        )
        assurance = from_union([from_str, from_none], obj.get("assurance"))
        cp_salle = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("cp_salle")
        )
        date_inscription = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("date_inscription")
        )
        email = from_union([from_str, from_none], obj.get("email"))
        engagement = from_union([from_str, from_none], obj.get("engagement"))
        horaires_seances = from_union(
            [from_str, from_none], obj.get("horaires_seances")
        )
        inscriptions = from_union([from_none, from_str], obj.get("inscriptions"))
        jours = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("jours")
        )
        label = from_union([from_str, from_none], obj.get("label"))
        latitude = from_none(obj.get("latitude"))
        longitude = from_none(obj.get("longitude"))
        mail_demandeur = from_union([from_str, from_none], obj.get("mail_demandeur"))
        mail_structure = from_union([from_str, from_none], obj.get("mail_structure"))
        nom_demandeur = from_union([from_str, from_none], obj.get("nom_demandeur"))
        nom_salle = from_union([from_str, from_none], obj.get("nom_salle"))
        nom_structure = from_union([from_str, from_none], obj.get("nom_structure"))
        nombre_personnes = from_union(
            [from_none, from_str], obj.get("nombre_personnes")
        )
        nombre_seances = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("nombre_seances")
        )
        objectif = from_union([from_none, from_str], obj.get("objectif"))
        prenom_demandeur = from_union(
            [from_str, from_none], obj.get("prenom_demandeur")
        )
        public = from_union([from_none, from_str], obj.get("public"))
        ville_salle = from_union([from_str, from_none], obj.get("ville_salle"))
        affiche = from_union([Affiche.from_dict, from_none], obj.get("affiche"))
        date_debut_timestamp = from_union(
            [from_int, from_none], obj.get("date_debut_timestamp")
        )
        date_fin_timestamp = from_union(
            [from_int, from_none], obj.get("date_fin_timestamp")
        )
        return Hit(
            nom_club_pro,
            nom,
            adresse,
            adresse_club_pro,
            code,
            id,
            engagements_noms,
            mail,
            telephone,
            type,
            url_site_web,
            nom_simple,
            date_affiliation,
            saison_en_cours,
            offres_pratiques,
            labellisation,
            cartographie,
            organisme_id_pere,
            commune,
            commune_club_pro,
            type_association,
            logo,
            geo,
            thumbnail,
            niveau,
            date,
            date_rencontre,
            horaire,
            nom_equipe1,
            nom_equipe2,
            numero_journee,
            pratique,
            gs_id,
            officiels,
            competition_id,
            id_organisme_equipe1,
            id_organisme_equipe2,
            id_poule,
            saison,
            salle,
            id_engagement_equipe1,
            id_engagement_equipe2,
            date_timestamp,
            date_rencontre_timestamp,
            creation_timestamp,
            date_saisie_resultat_timestamp,
            modification_timestamp,
            organisateur,
            niveau_nb,
            rue,
            acces_libre,
            date_created,
            date_updated,
            largeur,
            longueur,
            numero,
            nature_sol,
            libelle,
            adresse_complement,
            capacite_spectateur,
            libelle2,
            titre,
            description,
            date_debut,
            date_demande,
            date_fin,
            facebook,
            site_web,
            twitter,
            action,
            adresse_salle,
            adresse_structure,
            assurance,
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
            ville_salle,
            affiche,
            date_debut_timestamp,
            date_fin_timestamp,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom_club_pro is not None:
            result["nomClubPro"] = from_union([from_str, from_none], self.nom_club_pro)
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.adresse is not None:
            result["adresse"] = from_union([from_str, from_none], self.adresse)
        if self.adresse_club_pro is not None:
            result["adresseClubPro"] = from_none(self.adresse_club_pro)
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.engagements_noms is not None:
            result["engagements_noms"] = from_union(
                [from_str, from_none], self.engagements_noms
            )
        if self.mail is not None:
            result["mail"] = from_union([from_none, from_str], self.mail)
        if self.telephone is not None:
            result["telephone"] = from_union([from_none, from_str], self.telephone)
        if self.type is not None:
            result["type"] = from_union(
                [lambda x: to_enum(HitType, x), from_none], self.type
            )
        if self.url_site_web is not None:
            result["urlSiteWeb"] = from_union([from_str, from_none], self.url_site_web)
        if self.nom_simple is not None:
            result["nom_simple"] = from_none(self.nom_simple)
        if self.date_affiliation is not None:
            result["dateAffiliation"] = from_none(self.date_affiliation)
        if self.saison_en_cours is not None:
            result["saison_en_cours"] = from_union(
                [from_bool, from_none], self.saison_en_cours
            )
        if self.offres_pratiques is not None:
            result["offresPratiques"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.offres_pratiques
            )
        if self.labellisation is not None:
            result["labellisation"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.labellisation
            )
        if self.cartographie is not None:
            result["cartographie"] = from_union(
                [lambda x: to_class(Cartographie, x), from_none], self.cartographie
            )
        if self.organisme_id_pere is not None:
            result["organisme_id_pere"] = from_union(
                [lambda x: to_class(OrganismeIDPere, x), from_none],
                self.organisme_id_pere,
            )
        if self.commune is not None:
            result["commune"] = from_union(
                [lambda x: to_class(Commune, x), from_none], self.commune
            )
        if self.commune_club_pro is not None:
            result["communeClubPro"] = from_none(self.commune_club_pro)
        if self.type_association is not None:
            result["type_association"] = from_union(
                [lambda x: to_class(TypeAssociation, x), from_none],
                self.type_association,
            )
        if self.logo is not None:
            result["logo"] = from_union(
                [lambda x: to_class(IDOrganismeEquipe1Logo, x), from_none], self.logo
            )
        if self.geo is not None:
            result["_geo"] = from_union(
                [lambda x: to_class(Geo, x), from_none], self.geo
            )
        if self.thumbnail is not None:
            result["thumbnail"] = from_union([from_none, from_str], self.thumbnail)
        if self.niveau is not None:
            result["niveau"] = from_union(
                [lambda x: to_enum(NiveauEnum, x), from_none], self.niveau
            )
        if self.date is not None:
            result["date"] = from_union([lambda x: x.isoformat(), from_none], self.date)
        if self.date_rencontre is not None:
            result["date_rencontre"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_rencontre
            )
        if self.horaire is not None:
            result["horaire"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.horaire,
            )
        if self.nom_equipe1 is not None:
            result["nomEquipe1"] = from_union([from_str, from_none], self.nom_equipe1)
        if self.nom_equipe2 is not None:
            result["nomEquipe2"] = from_union([from_str, from_none], self.nom_equipe2)
        if self.numero_journee is not None:
            result["numeroJournee"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.numero_journee,
            )
        if self.pratique is not None:
            result["pratique"] = from_union(
                [from_none, lambda x: to_enum(Pratique, x)], self.pratique
            )
        if self.gs_id is not None:
            result["gsId"] = from_none(self.gs_id)
        if self.officiels is not None:
            result["officiels"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.officiels
            )
        if self.competition_id is not None:
            result["competitionId"] = from_union(
                [lambda x: to_class(CompetitionID, x), from_none], self.competition_id
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
        if self.saison is not None:
            result["saison"] = from_union(
                [lambda x: to_class(Saison, x), from_none], self.saison
            )
        if self.salle is not None:
            result["salle"] = from_union(
                [lambda x: to_class(Salle, x), from_none], self.salle
            )
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
        if self.date_timestamp is not None:
            result["date_timestamp"] = from_union(
                [from_int, from_none], self.date_timestamp
            )
        if self.date_rencontre_timestamp is not None:
            result["date_rencontre_timestamp"] = from_union(
                [from_int, from_none], self.date_rencontre_timestamp
            )
        if self.creation_timestamp is not None:
            result["creation_timestamp"] = from_union(
                [from_int, from_none], self.creation_timestamp
            )
        if self.date_saisie_resultat_timestamp is not None:
            result["dateSaisieResultat_timestamp"] = from_union(
                [from_int, from_none], self.date_saisie_resultat_timestamp
            )
        if self.modification_timestamp is not None:
            result["modification_timestamp"] = from_union(
                [from_int, from_none], self.modification_timestamp
            )
        if self.organisateur is not None:
            result["organisateur"] = from_union(
                [lambda x: to_class(Organisateur, x), from_none], self.organisateur
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
        if self.rue is not None:
            result["rue"] = from_union([from_str, from_none], self.rue)
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
            result["numero"] = from_union([from_int, from_str, from_none], self.numero)
        if self.nature_sol is not None:
            result["natureSol"] = from_union(
                [lambda x: to_class(NatureSol, x), from_none], self.nature_sol
            )
        if self.libelle is not None:
            result["libelle"] = from_union([from_str, from_none], self.libelle)
        if self.adresse_complement is not None:
            result["adresseComplement"] = from_union(
                [lambda x: to_enum(HitAdresseComplement, x), from_none],
                self.adresse_complement,
            )
        if self.capacite_spectateur is not None:
            result["capaciteSpectateur"] = from_union(
                [from_str, from_none], self.capacite_spectateur
            )
        if self.libelle2 is not None:
            result["libelle2"] = from_union(
                [lambda x: to_enum(Libelle2, x), from_none], self.libelle2
            )
        if self.titre is not None:
            result["titre"] = from_union([from_str, from_none], self.titre)
        if self.description is not None:
            result["description"] = from_none(self.description)
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
            result["assurance"] = from_union([from_str, from_none], self.assurance)
        if self.cp_salle is not None:
            result["cp_salle"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.cp_salle,
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
        if self.email is not None:
            result["email"] = from_union([from_str, from_none], self.email)
        if self.engagement is not None:
            result["engagement"] = from_union([from_str, from_none], self.engagement)
        if self.horaires_seances is not None:
            result["horaires_seances"] = from_union(
                [from_str, from_none], self.horaires_seances
            )
        if self.inscriptions is not None:
            result["inscriptions"] = from_union(
                [from_none, from_str], self.inscriptions
            )
        if self.jours is not None:
            result["jours"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.jours
            )
        if self.label is not None:
            result["label"] = from_union([from_str, from_none], self.label)
        if self.latitude is not None:
            result["latitude"] = from_none(self.latitude)
        if self.longitude is not None:
            result["longitude"] = from_none(self.longitude)
        if self.mail_demandeur is not None:
            result["mail_demandeur"] = from_union(
                [from_str, from_none], self.mail_demandeur
            )
        if self.mail_structure is not None:
            result["mail_structure"] = from_union(
                [from_str, from_none], self.mail_structure
            )
        if self.nom_demandeur is not None:
            result["nom_demandeur"] = from_union(
                [from_str, from_none], self.nom_demandeur
            )
        if self.nom_salle is not None:
            result["nom_salle"] = from_union([from_str, from_none], self.nom_salle)
        if self.nom_structure is not None:
            result["nom_structure"] = from_union(
                [from_str, from_none], self.nom_structure
            )
        if self.nombre_personnes is not None:
            result["nombre_personnes"] = from_union(
                [from_none, from_str], self.nombre_personnes
            )
        if self.nombre_seances is not None:
            result["nombre_seances"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.nombre_seances,
            )
        if self.objectif is not None:
            result["objectif"] = from_union([from_none, from_str], self.objectif)
        if self.prenom_demandeur is not None:
            result["prenom_demandeur"] = from_union(
                [from_str, from_none], self.prenom_demandeur
            )
        if self.public is not None:
            result["public"] = from_union([from_none, from_str], self.public)
        if self.ville_salle is not None:
            result["ville_salle"] = from_union([from_str, from_none], self.ville_salle)
        if self.affiche is not None:
            result["affiche"] = from_union(
                [lambda x: to_class(Affiche, x), from_none], self.affiche
            )
        if self.date_debut_timestamp is not None:
            result["date_debut_timestamp"] = from_union(
                [from_int, from_none], self.date_debut_timestamp
            )
        if self.date_fin_timestamp is not None:
            result["date_fin_timestamp"] = from_union(
                [from_int, from_none], self.date_fin_timestamp
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
