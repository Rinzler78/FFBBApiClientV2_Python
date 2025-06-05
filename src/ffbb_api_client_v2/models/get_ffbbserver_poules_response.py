from datetime import datetime
from enum import Enum
from typing import Any, Callable, List, Optional, Type, TypeVar, cast
from uuid import UUID

import dateutil.parser

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except Exception:
            pass
    assert False


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


class Nom(Enum):
    AIL_DE_ROUSSET = "AIL DE ROUSSET"
    BASKET_CLUB_PENNOIS = "BASKET CLUB PENNOIS"
    CAVIGAL_NICE_BASKET_06 = "CAVIGAL NICE BASKET 06"
    CJL_ST_CHAMAS_AIL_BASKET = "CJL ST CHAMAS AIL BASKET"
    CTC_DRACENIE83 = "CTC DRACENIE83"
    DRAGUIGNAN_UNION_CLUB = "DRAGUIGNAN UNION CLUB"
    HAUTE_PROVENCE_BASKET = "HAUTE PROVENCE BASKET"
    MONTFAVET_BASKET_CLUB = "MONTFAVET BASKET CLUB"
    SAINT_RAPHAEL_VAR_BASKET = "SAINT RAPHAEL VAR BASKET"
    SENAS_BASKET_BALL = "SENAS BASKET BALL"
    UNION_MARSEILLE_BASKET_BALL_UMBB = "UNION MARSEILLE BASKET BALL (UMBB)"


class IDEngagement:
    code_abrege: Optional[str]
    logo: None
    nom: Nom
    nom_officiel: Optional[str]
    nom_usuel: Optional[str]

    def __init__(
        self,
        code_abrege: Optional[str],
        logo: None,
        nom: Nom,
        nom_officiel: Optional[str],
        nom_usuel: Optional[str],
    ) -> None:
        self.code_abrege = code_abrege
        self.logo = logo
        self.nom = nom
        self.nom_officiel = nom_officiel
        self.nom_usuel = nom_usuel

    @staticmethod
    def from_dict(obj: Any) -> "IDEngagement":
        assert isinstance(obj, dict)
        code_abrege = from_union([from_none, from_str], obj.get("codeAbrege"))
        logo = from_none(obj.get("logo"))
        nom = Nom(obj.get("nom"))
        nom_officiel = from_union([from_none, from_str], obj.get("nomOfficiel"))
        nom_usuel = from_union([from_none, from_str], obj.get("nomUsuel"))
        return IDEngagement(code_abrege, logo, nom, nom_officiel, nom_usuel)

    def to_dict(self) -> dict:
        result: dict = {}
        result["codeAbrege"] = from_union([from_none, from_str], self.code_abrege)
        result["logo"] = from_none(self.logo)
        result["nom"] = to_enum(Nom, self.nom)
        if self.nom_officiel is not None:
            result["nomOfficiel"] = from_union([from_none, from_str], self.nom_officiel)
        result["nomUsuel"] = from_union([from_none, from_str], self.nom_usuel)
        return result


class Logo:
    id: UUID

    def __init__(self, id: UUID) -> None:
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> "Logo":
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        return Logo(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        return result


class Organisme:
    logo: Optional[Logo]
    nom: Nom

    def __init__(self, logo: Optional[Logo], nom: Nom) -> None:
        self.logo = logo
        self.nom = nom

    @staticmethod
    def from_dict(obj: Any) -> "Organisme":
        assert isinstance(obj, dict)
        logo = from_union([Logo.from_dict, from_none], obj.get("logo"))
        nom = Nom(obj.get("nom"))
        return Organisme(logo, nom)

    def to_dict(self) -> dict:
        result: dict = {}
        result["logo"] = from_union([lambda x: to_class(Logo, x), from_none], self.logo)
        result["nom"] = to_enum(Nom, self.nom)
        return result


class Classement:
    difference: int
    gagnes: int
    hors_classement: bool
    id: str
    id_competition: str
    id_engagement: IDEngagement
    id_poule: str
    match_joues: int
    nombre_defauts: int
    nombre_forfaits: int
    nuls: int
    organisme: Organisme
    paniers_encaisses: int
    paniers_marques: int
    penalites_arbitrage: int
    penalites_diverses: int
    penalites_entraineur: int
    perdus: int
    points: int
    position: int
    quotient: float

    def __init__(
        self,
        difference: int,
        gagnes: int,
        hors_classement: bool,
        id: str,
        id_competition: str,
        id_engagement: IDEngagement,
        id_poule: str,
        match_joues: int,
        nombre_defauts: int,
        nombre_forfaits: int,
        nuls: int,
        organisme: Organisme,
        paniers_encaisses: int,
        paniers_marques: int,
        penalites_arbitrage: int,
        penalites_diverses: int,
        penalites_entraineur: int,
        perdus: int,
        points: int,
        position: int,
        quotient: float,
    ) -> None:
        self.difference = difference
        self.gagnes = gagnes
        self.hors_classement = hors_classement
        self.id = id
        self.id_competition = id_competition
        self.id_engagement = id_engagement
        self.id_poule = id_poule
        self.match_joues = match_joues
        self.nombre_defauts = nombre_defauts
        self.nombre_forfaits = nombre_forfaits
        self.nuls = nuls
        self.organisme = organisme
        self.paniers_encaisses = paniers_encaisses
        self.paniers_marques = paniers_marques
        self.penalites_arbitrage = penalites_arbitrage
        self.penalites_diverses = penalites_diverses
        self.penalites_entraineur = penalites_entraineur
        self.perdus = perdus
        self.points = points
        self.position = position
        self.quotient = quotient

    @staticmethod
    def from_dict(obj: Any) -> "Classement":
        assert isinstance(obj, dict)
        difference = int(from_str(obj.get("difference")))
        gagnes = int(from_str(obj.get("gagnes")))
        hors_classement = from_bool(obj.get("horsClassement"))
        id = from_str(obj.get("id"))
        id_competition = from_str(obj.get("idCompetition"))
        id_engagement = IDEngagement.from_dict(obj.get("idEngagement"))
        id_poule = from_str(obj.get("idPoule"))
        match_joues = int(from_str(obj.get("matchJoues")))
        nombre_defauts = int(from_str(obj.get("nombreDefauts")))
        nombre_forfaits = int(from_str(obj.get("nombreForfaits")))
        nuls = int(from_str(obj.get("nuls")))
        organisme = Organisme.from_dict(obj.get("organisme"))
        paniers_encaisses = int(from_str(obj.get("paniersEncaisses")))
        paniers_marques = int(from_str(obj.get("paniersMarques")))
        penalites_arbitrage = int(from_str(obj.get("penalitesArbitrage")))
        penalites_diverses = int(from_str(obj.get("penalitesDiverses")))
        penalites_entraineur = int(from_str(obj.get("penalitesEntraineur")))
        perdus = int(from_str(obj.get("perdus")))
        points = int(from_str(obj.get("points")))
        position = int(from_str(obj.get("position")))
        quotient = from_float(obj.get("quotient"))
        return Classement(
            difference,
            gagnes,
            hors_classement,
            id,
            id_competition,
            id_engagement,
            id_poule,
            match_joues,
            nombre_defauts,
            nombre_forfaits,
            nuls,
            organisme,
            paniers_encaisses,
            paniers_marques,
            penalites_arbitrage,
            penalites_diverses,
            penalites_entraineur,
            perdus,
            points,
            position,
            quotient,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["difference"] = from_str(str(self.difference))
        result["gagnes"] = from_str(str(self.gagnes))
        result["horsClassement"] = from_bool(self.hors_classement)
        result["id"] = from_str(self.id)
        result["idCompetition"] = from_str(self.id_competition)
        result["idEngagement"] = to_class(IDEngagement, self.id_engagement)
        result["idPoule"] = from_str(self.id_poule)
        result["matchJoues"] = from_str(str(self.match_joues))
        result["nombreDefauts"] = from_str(str(self.nombre_defauts))
        result["nombreForfaits"] = from_str(str(self.nombre_forfaits))
        result["nuls"] = from_str(str(self.nuls))
        result["organisme"] = to_class(Organisme, self.organisme)
        result["paniersEncaisses"] = from_str(str(self.paniers_encaisses))
        result["paniersMarques"] = from_str(str(self.paniers_marques))
        result["penalitesArbitrage"] = from_str(str(self.penalites_arbitrage))
        result["penalitesDiverses"] = from_str(str(self.penalites_diverses))
        result["penalitesEntraineur"] = from_str(str(self.penalites_entraineur))
        result["perdus"] = from_str(str(self.perdus))
        result["points"] = from_str(str(self.points))
        result["position"] = from_str(str(self.position))
        result["quotient"] = to_float(self.quotient)
        return result


class IDOrganismeEquipe:
    logo: Optional[Logo]

    def __init__(self, logo: Optional[Logo]) -> None:
        self.logo = logo

    @staticmethod
    def from_dict(obj: Any) -> "IDOrganismeEquipe":
        assert isinstance(obj, dict)
        logo = from_union([Logo.from_dict, from_none], obj.get("logo"))
        return IDOrganismeEquipe(logo)

    def to_dict(self) -> dict:
        result: dict = {}
        result["logo"] = from_union([lambda x: to_class(Logo, x), from_none], self.logo)
        return result


class Libelle(Enum):
    AIDE_MARQUEUR = "Aide marqueur"
    ARBITRE = "Arbitre"
    CHRONOMETREUR = "Chronometreur"
    CHRONOMÉTREUR_DES_TIRS = "Chronométreur des tirs"
    DÉLÉGUÉ_DE_CLUB = "Délégué de club"
    DÉLÉGUÉ_FAIR_PLAY = "Délégué Fair Play"
    MARQUEUR = "Marqueur"
    OFFICIEL_DE_TABLE_DE_MARQUE = "Officiel de Table de Marque"
    STATISTICIEN_ABOYEUR = "Statisticien (Aboyeur)"


class Fonction:
    libelle: Libelle

    def __init__(self, libelle: Libelle) -> None:
        self.libelle = libelle

    @staticmethod
    def from_dict(obj: Any) -> "Fonction":
        assert isinstance(obj, dict)
        libelle = Libelle(obj.get("libelle"))
        return Fonction(libelle)

    def to_dict(self) -> dict:
        result: dict = {}
        result["libelle"] = to_enum(Libelle, self.libelle)
        return result


class OfficielOfficiel:
    nom: str
    prenom: str

    def __init__(self, nom: str, prenom: str) -> None:
        self.nom = nom
        self.prenom = prenom

    @staticmethod
    def from_dict(obj: Any) -> "OfficielOfficiel":
        assert isinstance(obj, dict)
        nom = from_str(obj.get("nom"))
        prenom = from_str(obj.get("prenom"))
        return OfficielOfficiel(nom, prenom)

    def to_dict(self) -> dict:
        result: dict = {}
        result["nom"] = from_str(self.nom)
        result["prenom"] = from_str(self.prenom)
        return result


class OfficielElement:
    fonction: Fonction
    officiel: OfficielOfficiel
    ordre: int

    def __init__(
        self, fonction: Fonction, officiel: OfficielOfficiel, ordre: int
    ) -> None:
        self.fonction = fonction
        self.officiel = officiel
        self.ordre = ordre

    @staticmethod
    def from_dict(obj: Any) -> "OfficielElement":
        assert isinstance(obj, dict)
        fonction = Fonction.from_dict(obj.get("fonction"))
        officiel = OfficielOfficiel.from_dict(obj.get("officiel"))
        ordre = from_int(obj.get("ordre"))
        return OfficielElement(fonction, officiel, ordre)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fonction"] = to_class(Fonction, self.fonction)
        result["officiel"] = to_class(OfficielOfficiel, self.officiel)
        result["ordre"] = from_int(self.ordre)
        return result


class AdresseComplement(Enum):
    EMPTY = ""
    MONTFAVET = "MONTFAVET"


class Cartographie:
    latitude: float
    longitude: float

    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def from_dict(obj: Any) -> "Cartographie":
        assert isinstance(obj, dict)
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        return Cartographie(latitude, longitude)

    def to_dict(self) -> dict:
        result: dict = {}
        result["latitude"] = to_float(self.latitude)
        result["longitude"] = to_float(self.longitude)
        return result


class Commune:
    code_postal: str
    libelle: str

    def __init__(self, code_postal: str, libelle: str) -> None:
        self.code_postal = code_postal
        self.libelle = libelle

    @staticmethod
    def from_dict(obj: Any) -> "Commune":
        assert isinstance(obj, dict)
        code_postal = from_str(obj.get("codePostal"))
        libelle = from_str(obj.get("libelle"))
        return Commune(code_postal, libelle)

    def to_dict(self) -> dict:
        result: dict = {}
        result["codePostal"] = from_str(self.code_postal)
        result["libelle"] = from_str(self.libelle)
        return result


class Libelle2(Enum):
    EMPTY = ""
    PARC_DES_SPORTS_POUDRERIE = "PARC DES SPORTS POUDRERIE"
    SALLE_NASARRE = "SALLE NASARRE"


class Salle:
    adresse: str
    adresse_complement: AdresseComplement
    cartographie: Cartographie
    commune: Commune
    id: str
    libelle: str
    libelle2: Libelle2
    numero: int

    def __init__(
        self,
        adresse: str,
        adresse_complement: AdresseComplement,
        cartographie: Cartographie,
        commune: Commune,
        id: str,
        libelle: str,
        libelle2: Libelle2,
        numero: int,
    ) -> None:
        self.adresse = adresse
        self.adresse_complement = adresse_complement
        self.cartographie = cartographie
        self.commune = commune
        self.id = id
        self.libelle = libelle
        self.libelle2 = libelle2
        self.numero = numero

    @staticmethod
    def from_dict(obj: Any) -> "Salle":
        assert isinstance(obj, dict)
        adresse = from_str(obj.get("adresse"))
        adresse_complement = AdresseComplement(obj.get("adresseComplement"))
        cartographie = Cartographie.from_dict(obj.get("cartographie"))
        commune = Commune.from_dict(obj.get("commune"))
        id = from_str(obj.get("id"))
        libelle = from_str(obj.get("libelle"))
        libelle2 = Libelle2(obj.get("libelle2"))
        numero = int(from_str(obj.get("numero")))
        return Salle(
            adresse,
            adresse_complement,
            cartographie,
            commune,
            id,
            libelle,
            libelle2,
            numero,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["adresse"] = from_str(self.adresse)
        result["adresseComplement"] = to_enum(
            AdresseComplement, self.adresse_complement
        )
        result["cartographie"] = to_class(Cartographie, self.cartographie)
        result["commune"] = to_class(Commune, self.commune)
        result["id"] = from_str(self.id)
        result["libelle"] = from_str(self.libelle)
        result["libelle2"] = to_enum(Libelle2, self.libelle2)
        result["numero"] = from_str(str(self.numero))
        return result


class Rencontre:
    competition_id: str
    date_rencontre: datetime
    gs_id: None
    id: str
    id_engagement_equipe1: IDEngagement
    id_engagement_equipe2: IDEngagement
    id_organisme_equipe1: IDOrganismeEquipe
    id_organisme_equipe2: IDOrganismeEquipe
    id_poule: str
    joue: bool
    nom_equipe1: str
    nom_equipe2: str
    numero: int
    numero_journee: int
    officiels: List[OfficielElement]
    resultat_equipe1: Optional[int]
    resultat_equipe2: Optional[int]
    salle: Optional[Salle]

    def __init__(
        self,
        competition_id: str,
        date_rencontre: datetime,
        gs_id: None,
        id: str,
        id_engagement_equipe1: IDEngagement,
        id_engagement_equipe2: IDEngagement,
        id_organisme_equipe1: IDOrganismeEquipe,
        id_organisme_equipe2: IDOrganismeEquipe,
        id_poule: str,
        joue: bool,
        nom_equipe1: str,
        nom_equipe2: str,
        numero: int,
        numero_journee: int,
        officiels: List[OfficielElement],
        resultat_equipe1: Optional[int],
        resultat_equipe2: Optional[int],
        salle: Optional[Salle],
    ) -> None:
        self.competition_id = competition_id
        self.date_rencontre = date_rencontre
        self.gs_id = gs_id
        self.id = id
        self.id_engagement_equipe1 = id_engagement_equipe1
        self.id_engagement_equipe2 = id_engagement_equipe2
        self.id_organisme_equipe1 = id_organisme_equipe1
        self.id_organisme_equipe2 = id_organisme_equipe2
        self.id_poule = id_poule
        self.joue = joue
        self.nom_equipe1 = nom_equipe1
        self.nom_equipe2 = nom_equipe2
        self.numero = numero
        self.numero_journee = numero_journee
        self.officiels = officiels
        self.resultat_equipe1 = resultat_equipe1
        self.resultat_equipe2 = resultat_equipe2
        self.salle = salle

    @staticmethod
    def from_dict(obj: Any) -> "Rencontre":
        assert isinstance(obj, dict)
        competition_id = from_str(obj.get("competitionId"))
        date_rencontre = from_datetime(obj.get("date_rencontre"))
        gs_id = from_none(obj.get("gsId"))
        id = from_str(obj.get("id"))
        id_engagement_equipe1 = IDEngagement.from_dict(obj.get("idEngagementEquipe1"))
        id_engagement_equipe2 = IDEngagement.from_dict(obj.get("idEngagementEquipe2"))
        id_organisme_equipe1 = IDOrganismeEquipe.from_dict(
            obj.get("idOrganismeEquipe1")
        )
        id_organisme_equipe2 = IDOrganismeEquipe.from_dict(
            obj.get("idOrganismeEquipe2")
        )
        id_poule = from_str(obj.get("idPoule"))
        joue = from_bool(obj.get("joue"))
        nom_equipe1 = from_str(obj.get("nomEquipe1"))
        nom_equipe2 = from_str(obj.get("nomEquipe2"))
        numero = int(from_str(obj.get("numero")))
        numero_journee = int(from_str(obj.get("numeroJournee")))
        officiels = from_list(OfficielElement.from_dict, obj.get("officiels"))
        resultat_equipe1 = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("resultatEquipe1")
        )
        resultat_equipe2 = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("resultatEquipe2")
        )
        salle = from_union([Salle.from_dict, from_none], obj.get("salle"))
        return Rencontre(
            competition_id,
            date_rencontre,
            gs_id,
            id,
            id_engagement_equipe1,
            id_engagement_equipe2,
            id_organisme_equipe1,
            id_organisme_equipe2,
            id_poule,
            joue,
            nom_equipe1,
            nom_equipe2,
            numero,
            numero_journee,
            officiels,
            resultat_equipe1,
            resultat_equipe2,
            salle,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["competitionId"] = from_str(self.competition_id)
        result["date_rencontre"] = self.date_rencontre.isoformat()
        result["gsId"] = from_none(self.gs_id)
        result["id"] = from_str(self.id)
        result["idEngagementEquipe1"] = to_class(
            IDEngagement, self.id_engagement_equipe1
        )
        result["idEngagementEquipe2"] = to_class(
            IDEngagement, self.id_engagement_equipe2
        )
        result["idOrganismeEquipe1"] = to_class(
            IDOrganismeEquipe, self.id_organisme_equipe1
        )
        result["idOrganismeEquipe2"] = to_class(
            IDOrganismeEquipe, self.id_organisme_equipe2
        )
        result["idPoule"] = from_str(self.id_poule)
        result["joue"] = from_bool(self.joue)
        result["nomEquipe1"] = from_str(self.nom_equipe1)
        result["nomEquipe2"] = from_str(self.nom_equipe2)
        result["numero"] = from_str(str(self.numero))
        result["numeroJournee"] = from_str(str(self.numero_journee))
        result["officiels"] = from_list(
            lambda x: to_class(OfficielElement, x), self.officiels
        )
        result["resultatEquipe1"] = from_union(
            [
                lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
            ],
            self.resultat_equipe1,
        )
        result["resultatEquipe2"] = from_union(
            [
                lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
            ],
            self.resultat_equipe2,
        )
        result["salle"] = from_union(
            [lambda x: to_class(Salle, x), from_none], self.salle
        )
        return result


class Data:
    classements: List[Classement]
    id: str
    rencontres: List[Rencontre]

    def __init__(
        self, classements: List[Classement], id: str, rencontres: List[Rencontre]
    ) -> None:
        self.classements = classements
        self.id = id
        self.rencontres = rencontres

    @staticmethod
    def from_dict(obj: Any) -> "Data":
        assert isinstance(obj, dict)
        classements = from_list(Classement.from_dict, obj.get("classements"))
        id = from_str(obj.get("id"))
        rencontres = from_list(Rencontre.from_dict, obj.get("rencontres"))
        return Data(classements, id, rencontres)

    def to_dict(self) -> dict:
        result: dict = {}
        result["classements"] = from_list(
            lambda x: to_class(Classement, x), self.classements
        )
        result["id"] = from_str(self.id)
        result["rencontres"] = from_list(
            lambda x: to_class(Rencontre, x), self.rencontres
        )
        return result


class GetFfbbserverPoulesResponse:
    data: Data

    def __init__(self, data: Data) -> None:
        self.data = data

    @staticmethod
    def from_dict(obj: Any) -> "GetFfbbserverPoulesResponse":
        assert isinstance(obj, dict)
        data = Data.from_dict(obj.get("data"))
        return GetFfbbserverPoulesResponse(data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = to_class(Data, self.data)
        return result


def get_ffbbserver_poules_response_from_dict(s: Any) -> GetFfbbserverPoulesResponse:
    return GetFfbbserverPoulesResponse.from_dict(s)


def get_ffbbserver_poules_response_to_dict(x: GetFfbbserverPoulesResponse) -> Any:
    return to_class(GetFfbbserverPoulesResponse, x)
