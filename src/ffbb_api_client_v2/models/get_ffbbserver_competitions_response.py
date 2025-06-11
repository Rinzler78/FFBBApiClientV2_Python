from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from ..utils.converters import (
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
from .categorie import Categorie
from .id_engagement_equipe import IDEngagementEquipe
from .id_organisme_equipe import IDOrganismeEquipe
from .salle import Salle
from .type_competition_generique import TypeCompetitionGenerique


class IDOrganisme:
    id: str

    def __init__(self, id: str) -> None:
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> "IDOrganisme":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        return IDOrganisme(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        return result


class Engagement:
    id: str
    id_organisme: IDOrganisme

    def __init__(self, id: str, id_organisme: IDOrganisme) -> None:
        self.id = id
        self.id_organisme = id_organisme

    @staticmethod
    def from_dict(obj: Any) -> "Engagement":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        id_organisme = IDOrganisme.from_dict(obj.get("idOrganisme"))
        return Engagement(id, id_organisme)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["idOrganisme"] = to_class(IDOrganisme, self.id_organisme)
        return result


class Libelle(Enum):
    AIDE_MARQUEUR = "Aide marqueur"
    ARBITRE = "Arbitre"
    CHRONOMETREUR = "Chronometreur"
    CHRONOMÉTREUR_DES_TIRS = "Chronométreur des tirs"
    DELEGUE = "Delegue"
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
    ordre: Optional[int]

    def __init__(
        self, fonction: Fonction, officiel: OfficielOfficiel, ordre: Optional[int]
    ) -> None:
        self.fonction = fonction
        self.officiel = officiel
        self.ordre = ordre

    @staticmethod
    def from_dict(obj: Any) -> "OfficielElement":
        assert isinstance(obj, dict)
        fonction = Fonction.from_dict(obj.get("fonction"))
        officiel = OfficielOfficiel.from_dict(obj.get("officiel"))
        ordre = from_union([from_int, from_none], obj.get("ordre"))
        return OfficielElement(fonction, officiel, ordre)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fonction"] = to_class(Fonction, self.fonction)
        result["officiel"] = to_class(OfficielOfficiel, self.officiel)
        result["ordre"] = from_union([from_int, from_none], self.ordre)
        return result


class AdresseComplement(Enum):
    ADRESSE_COMPLEMENT = ""
    AVENUE_DE_VERDUN = "AVENUE DE VERDUN"
    EMPTY = " "
    MONTFAVET = "MONTFAVET"


class Rencontre:
    competition_id: str
    date_rencontre: datetime
    gs_id: None
    id: str
    id_engagement_equipe1: IDEngagementEquipe
    id_engagement_equipe2: IDEngagementEquipe
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
        id_engagement_equipe1: IDEngagementEquipe,
        id_engagement_equipe2: IDEngagementEquipe,
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
        id_engagement_equipe1 = IDEngagementEquipe.from_dict(
            obj.get("idEngagementEquipe1")
        )
        id_engagement_equipe2 = IDEngagementEquipe.from_dict(
            obj.get("idEngagementEquipe2")
        )
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
            IDEngagementEquipe, self.id_engagement_equipe1
        )
        result["idEngagementEquipe2"] = to_class(
            IDEngagementEquipe, self.id_engagement_equipe2
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


class PhasePoule:
    engagements: List[Engagement]
    id: str
    nom: str
    rencontres: List[Rencontre]

    def __init__(
        self,
        engagements: List[Engagement],
        id: str,
        nom: str,
        rencontres: List[Rencontre],
    ) -> None:
        self.engagements = engagements
        self.id = id
        self.nom = nom
        self.rencontres = rencontres

    @staticmethod
    def from_dict(obj: Any) -> "PhasePoule":
        assert isinstance(obj, dict)
        engagements = from_list(Engagement.from_dict, obj.get("engagements"))
        id = from_str(obj.get("id"))
        nom = from_str(obj.get("nom"))
        rencontres = from_list(Rencontre.from_dict, obj.get("rencontres"))
        return PhasePoule(engagements, id, nom, rencontres)

    def to_dict(self) -> dict:
        result: dict = {}
        result["engagements"] = from_list(
            lambda x: to_class(Engagement, x), self.engagements
        )
        result["id"] = from_str(self.id)
        result["nom"] = from_str(self.nom)
        result["rencontres"] = from_list(
            lambda x: to_class(Rencontre, x), self.rencontres
        )
        return result


class Phase:
    id: str
    live_stat: bool
    nom: str
    phase_code: str
    poules: List[PhasePoule]

    def __init__(
        self,
        id: str,
        live_stat: bool,
        nom: str,
        phase_code: str,
        poules: List[PhasePoule],
    ) -> None:
        self.id = id
        self.live_stat = live_stat
        self.nom = nom
        self.phase_code = phase_code
        self.poules = poules

    @staticmethod
    def from_dict(obj: Any) -> "Phase":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        live_stat = from_bool(obj.get("liveStat"))
        nom = from_str(obj.get("nom"))
        phase_code = from_str(obj.get("phase_code"))
        poules = from_list(PhasePoule.from_dict, obj.get("poules"))
        return Phase(id, live_stat, nom, phase_code, poules)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["liveStat"] = from_bool(self.live_stat)
        result["nom"] = from_str(self.nom)
        result["phase_code"] = from_str(self.phase_code)
        result["poules"] = from_list(lambda x: to_class(PhasePoule, x), self.poules)
        return result


class DataPoule:
    id: str
    nom: str

    def __init__(self, id: str, nom: str) -> None:
        self.id = id
        self.nom = nom

    @staticmethod
    def from_dict(obj: Any) -> "DataPoule":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        nom = from_str(obj.get("nom"))
        return DataPoule(id, nom)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["nom"] = from_str(self.nom)
        return result


class Data:
    categorie: Categorie
    code: str
    competition_origine: str
    competition_origine_nom: str
    id: str
    live_stat: bool
    logo: None
    nom: str
    phases: List[Phase]
    poules: List[DataPoule]
    publication_internet: str
    saison: int
    sexe: str
    type_competition: str
    type_competition_generique: TypeCompetitionGenerique

    def __init__(
        self,
        categorie: Categorie,
        code: str,
        competition_origine: str,
        competition_origine_nom: str,
        id: str,
        live_stat: bool,
        logo: None,
        nom: str,
        phases: List[Phase],
        poules: List[DataPoule],
        publication_internet: str,
        saison: int,
        sexe: str,
        type_competition: str,
        type_competition_generique: TypeCompetitionGenerique,
    ) -> None:
        self.categorie = categorie
        self.code = code
        self.competition_origine = competition_origine
        self.competition_origine_nom = competition_origine_nom
        self.id = id
        self.live_stat = live_stat
        self.logo = logo
        self.nom = nom
        self.phases = phases
        self.poules = poules
        self.publication_internet = publication_internet
        self.saison = saison
        self.sexe = sexe
        self.type_competition = type_competition
        self.type_competition_generique = type_competition_generique

    @staticmethod
    def from_dict(obj: Any) -> "Data":
        assert isinstance(obj, dict)
        categorie = Categorie.from_dict(obj.get("categorie"))
        code = from_str(obj.get("code"))
        competition_origine = from_str(obj.get("competition_origine"))
        competition_origine_nom = from_str(obj.get("competition_origine_nom"))
        id = from_str(obj.get("id"))
        live_stat = from_bool(obj.get("liveStat"))
        logo = from_none(obj.get("logo"))
        nom = from_str(obj.get("nom"))
        phases = from_list(Phase.from_dict, obj.get("phases"))
        poules = from_list(DataPoule.from_dict, obj.get("poules"))
        publication_internet = from_str(obj.get("publicationInternet"))
        saison = int(from_str(obj.get("saison")))
        sexe = from_str(obj.get("sexe"))
        type_competition = from_str(obj.get("typeCompetition"))
        type_competition_generique = TypeCompetitionGenerique.from_dict(
            obj.get("typeCompetitionGenerique")
        )
        return Data(
            categorie,
            code,
            competition_origine,
            competition_origine_nom,
            id,
            live_stat,
            logo,
            nom,
            phases,
            poules,
            publication_internet,
            saison,
            sexe,
            type_competition,
            type_competition_generique,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["categorie"] = to_class(Categorie, self.categorie)
        result["code"] = from_str(self.code)
        result["competition_origine"] = from_str(self.competition_origine)
        result["competition_origine_nom"] = from_str(self.competition_origine_nom)
        result["id"] = from_str(self.id)
        result["liveStat"] = from_bool(self.live_stat)
        result["logo"] = from_none(self.logo)
        result["nom"] = from_str(self.nom)
        result["phases"] = from_list(lambda x: to_class(Phase, x), self.phases)
        result["poules"] = from_list(lambda x: to_class(DataPoule, x), self.poules)
        result["publicationInternet"] = from_str(self.publication_internet)
        result["saison"] = from_str(str(self.saison))
        result["sexe"] = from_str(self.sexe)
        result["typeCompetition"] = from_str(self.type_competition)
        result["typeCompetitionGenerique"] = to_class(
            TypeCompetitionGenerique, self.type_competition_generique
        )
        return result


class GetFfbbserverCompetitionsResponse:
    data: Data

    def __init__(self, data: Data) -> None:
        self.data = data

    @staticmethod
    def from_dict(obj: Any) -> "GetFfbbserverCompetitionsResponse":
        assert isinstance(obj, dict)
        data = Data.from_dict(obj.get("data"))
        return GetFfbbserverCompetitionsResponse(data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = to_class(Data, self.data)
        return result


def get_ffbbserver_competitions_response_from_dict(
    s: Any,
) -> GetFfbbserverCompetitionsResponse:
    return GetFfbbserverCompetitionsResponse.from_dict(s)


def get_ffbbserver_competitions_response_to_dict(
    x: GetFfbbserverCompetitionsResponse,
) -> Any:
    return to_class(GetFfbbserverCompetitionsResponse, x)
