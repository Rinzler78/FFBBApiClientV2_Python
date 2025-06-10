from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from ..utils.converters import (
    from_datetime,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    to_class,
    to_enum,
)
from .cartographie import Cartographie
from .commune import Commune
from .logo import Logo
from .salle import Salle


class Code(Enum):
    SE = "SE"
    U11 = "U11"
    U13 = "U13"
    U15 = "U15"
    U17 = "U17"


class Categorie:
    code: Code
    ordre: int

    def __init__(self, code: Code, ordre: int) -> None:
        self.code = code
        self.ordre = ordre

    @staticmethod
    def from_dict(obj: Any) -> "Categorie":
        assert isinstance(obj, dict)
        code = Code(obj.get("code"))
        ordre = from_int(obj.get("ordre"))
        return Categorie(code, ordre)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = to_enum(Code, self.code)
        result["ordre"] = from_int(self.ordre)
        return result


class IDCompetitionPere:
    id: str
    nom: str

    def __init__(self, id: str, nom: str) -> None:
        self.id = id
        self.nom = nom

    @staticmethod
    def from_dict(obj: Any) -> "IDCompetitionPere":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        nom = from_str(obj.get("nom"))
        return IDCompetitionPere(id, nom)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["nom"] = from_str(self.nom)
        return result


class TypeEnum(Enum):
    C = "C"
    L = "L"


class Organisateur:
    type: TypeEnum

    def __init__(self, type: TypeEnum) -> None:
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> "Organisateur":
        assert isinstance(obj, dict)
        type = TypeEnum(obj.get("type"))
        return Organisateur(type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = to_enum(TypeEnum, self.type)
        return result


class IDPoule:
    id: str

    def __init__(self, id: str) -> None:
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> "IDPoule":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        return IDPoule(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        return result


class Sexe(Enum):
    F = "F"
    M = "M"
    X = "X"


class TypeCompetition(Enum):
    COUPE = "COUPE"
    DIV = "DIV"
    PLAT = "PLAT"


class GradientColor(Enum):
    EB6_D88 = "#EB6D88"
    ED3833 = "#ed3833"
    THE_00_B5_EA = "#00B5EA"
    THE_04378_B = "#04378B"


class TypeCompetitionGenerique:
    logo: Logo

    def __init__(self, logo: Logo) -> None:
        self.logo = logo

    @staticmethod
    def from_dict(obj: Any) -> "TypeCompetitionGenerique":
        assert isinstance(obj, dict)
        logo = Logo.from_dict(obj.get("logo"))
        return TypeCompetitionGenerique(logo)

    def to_dict(self) -> dict:
        result: dict = {}
        result["logo"] = to_class(Logo, self.logo)
        return result


class IDCompetition:
    categorie: Categorie
    code: str
    competition_origine: str
    competition_origine_niveau: int
    competition_origine_nom: str
    id: str
    id_competition_pere: Optional[IDCompetitionPere]
    logo: None
    nom: str
    organisateur: Organisateur
    saison: IDPoule
    sexe: Sexe
    type_competition: TypeCompetition
    type_competition_generique: Optional[TypeCompetitionGenerique]

    def __init__(
        self,
        categorie: Categorie,
        code: str,
        competition_origine: str,
        competition_origine_niveau: int,
        competition_origine_nom: str,
        id: str,
        id_competition_pere: Optional[IDCompetitionPere],
        logo: None,
        nom: str,
        organisateur: Organisateur,
        saison: IDPoule,
        sexe: Sexe,
        type_competition: TypeCompetition,
        type_competition_generique: Optional[TypeCompetitionGenerique],
    ) -> None:
        self.categorie = categorie
        self.code = code
        self.competition_origine = competition_origine
        self.competition_origine_niveau = competition_origine_niveau
        self.competition_origine_nom = competition_origine_nom
        self.id = id
        self.id_competition_pere = id_competition_pere
        self.logo = logo
        self.nom = nom
        self.organisateur = organisateur
        self.saison = saison
        self.sexe = sexe
        self.type_competition = type_competition
        self.type_competition_generique = type_competition_generique

    @staticmethod
    def from_dict(obj: Any) -> "IDCompetition":
        assert isinstance(obj, dict)
        categorie = Categorie.from_dict(obj.get("categorie"))
        code = from_str(obj.get("code"))
        competition_origine = from_str(obj.get("competition_origine"))
        competition_origine_niveau = from_int(obj.get("competition_origine_niveau"))
        competition_origine_nom = from_str(obj.get("competition_origine_nom"))
        id = from_str(obj.get("id"))
        id_competition_pere = from_union(
            [IDCompetitionPere.from_dict, from_none], obj.get("idCompetitionPere")
        )
        logo = from_none(obj.get("logo"))
        nom = from_str(obj.get("nom"))
        organisateur = Organisateur.from_dict(obj.get("organisateur"))
        saison = IDPoule.from_dict(obj.get("saison"))
        sexe = Sexe(obj.get("sexe"))
        type_competition = TypeCompetition(obj.get("typeCompetition"))
        type_competition_generique = from_union(
            [TypeCompetitionGenerique.from_dict, from_none],
            obj.get("typeCompetitionGenerique"),
        )
        return IDCompetition(
            categorie,
            code,
            competition_origine,
            competition_origine_niveau,
            competition_origine_nom,
            id,
            id_competition_pere,
            logo,
            nom,
            organisateur,
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
        result["competition_origine_niveau"] = from_int(self.competition_origine_niveau)
        result["competition_origine_nom"] = from_str(self.competition_origine_nom)
        result["id"] = from_str(self.id)
        result["idCompetitionPere"] = from_union(
            [lambda x: to_class(IDCompetitionPere, x), from_none],
            self.id_competition_pere,
        )
        result["logo"] = from_none(self.logo)
        result["nom"] = from_str(self.nom)
        result["organisateur"] = to_class(Organisateur, self.organisateur)
        result["saison"] = to_class(IDPoule, self.saison)
        result["sexe"] = to_enum(Sexe, self.sexe)
        result["typeCompetition"] = to_enum(TypeCompetition, self.type_competition)
        result["typeCompetitionGenerique"] = from_union(
            [lambda x: to_class(TypeCompetitionGenerique, x), from_none],
            self.type_competition_generique,
        )
        return result


class Engagement:
    id: str
    id_competition: IDCompetition
    id_poule: IDPoule

    def __init__(
        self, id: str, id_competition: IDCompetition, id_poule: IDPoule
    ) -> None:
        self.id = id
        self.id_competition = id_competition
        self.id_poule = id_poule

    @staticmethod
    def from_dict(obj: Any) -> "Engagement":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        id_competition = IDCompetition.from_dict(obj.get("idCompetition"))
        id_poule = IDPoule.from_dict(obj.get("idPoule"))
        return Engagement(id, id_competition, id_poule)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["idCompetition"] = to_class(IDCompetition, self.id_competition)
        result["idPoule"] = to_class(IDPoule, self.id_poule)
        return result


class IDLabellisationProgramme:
    id: int
    labellisation_label: int
    libelle: str
    logo_vertical: Optional[IDPoule]

    def __init__(
        self,
        id: int,
        labellisation_label: int,
        libelle: str,
        logo_vertical: Optional[IDPoule],
    ) -> None:
        self.id = id
        self.labellisation_label = labellisation_label
        self.libelle = libelle
        self.logo_vertical = logo_vertical

    @staticmethod
    def from_dict(obj: Any) -> "IDLabellisationProgramme":
        assert isinstance(obj, dict)
        id = int(from_str(obj.get("id")))
        labellisation_label = int(from_str(obj.get("labellisationLabel")))
        libelle = from_str(obj.get("libelle"))
        logo_vertical = from_union(
            [IDPoule.from_dict, from_none], obj.get("logo_vertical")
        )
        return IDLabellisationProgramme(id, labellisation_label, libelle, logo_vertical)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(str(self.id))
        result["labellisationLabel"] = from_str(str(self.labellisation_label))
        result["libelle"] = from_str(self.libelle)
        result["logo_vertical"] = from_union(
            [lambda x: to_class(IDPoule, x), from_none], self.logo_vertical
        )
        return result


class Labellisation:
    debut: datetime
    fin: datetime
    id: str
    id_labellisation_programme: IDLabellisationProgramme

    def __init__(
        self,
        debut: datetime,
        fin: datetime,
        id: str,
        id_labellisation_programme: IDLabellisationProgramme,
    ) -> None:
        self.debut = debut
        self.fin = fin
        self.id = id
        self.id_labellisation_programme = id_labellisation_programme

    @staticmethod
    def from_dict(obj: Any) -> "Labellisation":
        assert isinstance(obj, dict)
        debut = from_datetime(obj.get("debut"))
        fin = from_datetime(obj.get("fin"))
        id = from_str(obj.get("id"))
        id_labellisation_programme = IDLabellisationProgramme.from_dict(
            obj.get("idLabellisationProgramme")
        )
        return Labellisation(debut, fin, id, id_labellisation_programme)

    def to_dict(self) -> dict:
        result: dict = {}
        result["debut"] = self.debut.isoformat()
        result["fin"] = self.fin.isoformat()
        result["id"] = from_str(self.id)
        result["idLabellisationProgramme"] = to_class(
            IDLabellisationProgramme, self.id_labellisation_programme
        )
        return result


class Membre:
    adresse1: str
    adresse2: None
    code_fonction: str
    code_postal: int
    id: int
    mail: str
    nom: str
    prenom: str
    telephone_fixe: None
    telephone_portable: str
    ville: str

    def __init__(
        self,
        adresse1: str,
        adresse2: None,
        code_fonction: str,
        code_postal: int,
        id: int,
        mail: str,
        nom: str,
        prenom: str,
        telephone_fixe: None,
        telephone_portable: str,
        ville: str,
    ) -> None:
        self.adresse1 = adresse1
        self.adresse2 = adresse2
        self.code_fonction = code_fonction
        self.code_postal = code_postal
        self.id = id
        self.mail = mail
        self.nom = nom
        self.prenom = prenom
        self.telephone_fixe = telephone_fixe
        self.telephone_portable = telephone_portable
        self.ville = ville

    @staticmethod
    def from_dict(obj: Any) -> "Membre":
        assert isinstance(obj, dict)
        adresse1 = from_str(obj.get("adresse1"))
        adresse2 = from_none(obj.get("adresse2"))
        code_fonction = from_str(obj.get("codeFonction"))
        code_postal = int(from_str(obj.get("codePostal")))
        id = int(from_str(obj.get("id")))
        mail = from_str(obj.get("mail"))
        nom = from_str(obj.get("nom"))
        prenom = from_str(obj.get("prenom"))
        telephone_fixe = from_none(obj.get("telephoneFixe"))
        telephone_portable = from_str(obj.get("telephonePortable"))
        ville = from_str(obj.get("ville"))
        return Membre(
            adresse1,
            adresse2,
            code_fonction,
            code_postal,
            id,
            mail,
            nom,
            prenom,
            telephone_fixe,
            telephone_portable,
            ville,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["adresse1"] = from_str(self.adresse1)
        result["adresse2"] = from_none(self.adresse2)
        result["codeFonction"] = from_str(self.code_fonction)
        result["codePostal"] = from_str(str(self.code_postal))
        result["id"] = from_str(str(self.id))
        result["mail"] = from_str(self.mail)
        result["nom"] = from_str(self.nom)
        result["prenom"] = from_str(self.prenom)
        result["telephoneFixe"] = from_none(self.telephone_fixe)
        result["telephonePortable"] = from_str(self.telephone_portable)
        result["ville"] = from_str(self.ville)
        return result


class FfbbserverOffresPratiquesID:
    categorie_pratique: str
    id: str
    title: str
    type_pratique: str

    def __init__(
        self, categorie_pratique: str, id: str, title: str, type_pratique: str
    ) -> None:
        self.categorie_pratique = categorie_pratique
        self.id = id
        self.title = title
        self.type_pratique = type_pratique

    @staticmethod
    def from_dict(obj: Any) -> "FfbbserverOffresPratiquesID":
        assert isinstance(obj, dict)
        categorie_pratique = from_str(obj.get("categoriePratique"))
        id = from_str(obj.get("id"))
        title = from_str(obj.get("title"))
        type_pratique = from_str(obj.get("typePratique"))
        return FfbbserverOffresPratiquesID(categorie_pratique, id, title, type_pratique)

    def to_dict(self) -> dict:
        result: dict = {}
        result["categoriePratique"] = from_str(self.categorie_pratique)
        result["id"] = from_str(self.id)
        result["title"] = from_str(self.title)
        result["typePratique"] = from_str(self.type_pratique)
        return result


class OffresPratique:
    ffbbserver_offres_pratiques_id: FfbbserverOffresPratiquesID

    def __init__(
        self, ffbbserver_offres_pratiques_id: FfbbserverOffresPratiquesID
    ) -> None:
        self.ffbbserver_offres_pratiques_id = ffbbserver_offres_pratiques_id

    @staticmethod
    def from_dict(obj: Any) -> "OffresPratique":
        assert isinstance(obj, dict)
        ffbbserver_offres_pratiques_id = FfbbserverOffresPratiquesID.from_dict(
            obj.get("ffbbserver_offres_pratiques_id")
        )
        return OffresPratique(ffbbserver_offres_pratiques_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ffbbserver_offres_pratiques_id"] = to_class(
            FfbbserverOffresPratiquesID, self.ffbbserver_offres_pratiques_id
        )
        return result


class Data:
    adresse: str
    adresse_club_pro: None
    cartographie: Cartographie
    code: str
    commune: Commune
    commune_club_pro: None
    competitions: List[Any]
    engagements: List[Engagement]
    id: int
    labellisation: List[Labellisation]
    logo: Logo
    mail: str
    membres: List[Membre]
    nom: str
    nom_simple: None
    nom_club_pro: str
    offres_pratiques: List[OffresPratique]
    organismes_fils: List[Any]
    salle: Salle
    telephone: str
    type: str
    url_site_web: str

    def __init__(
        self,
        adresse: str,
        adresse_club_pro: None,
        cartographie: Cartographie,
        code: str,
        commune: Commune,
        commune_club_pro: None,
        competitions: List[Any],
        engagements: List[Engagement],
        id: int,
        labellisation: List[Labellisation],
        logo: Logo,
        mail: str,
        membres: List[Membre],
        nom: str,
        nom_simple: None,
        nom_club_pro: str,
        offres_pratiques: List[OffresPratique],
        organismes_fils: List[Any],
        salle: Salle,
        telephone: str,
        type: str,
        url_site_web: str,
    ) -> None:
        self.adresse = adresse
        self.adresse_club_pro = adresse_club_pro
        self.cartographie = cartographie
        self.code = code
        self.commune = commune
        self.commune_club_pro = commune_club_pro
        self.competitions = competitions
        self.engagements = engagements
        self.id = id
        self.labellisation = labellisation
        self.logo = logo
        self.mail = mail
        self.membres = membres
        self.nom = nom
        self.nom_simple = nom_simple
        self.nom_club_pro = nom_club_pro
        self.offres_pratiques = offres_pratiques
        self.organismes_fils = organismes_fils
        self.salle = salle
        self.telephone = telephone
        self.type = type
        self.url_site_web = url_site_web

    @staticmethod
    def from_dict(obj: Any) -> "Data":
        assert isinstance(obj, dict)
        adresse = from_str(obj.get("adresse"))
        adresse_club_pro = from_none(obj.get("adresseClubPro"))
        cartographie = Cartographie.from_dict(obj.get("cartographie"))
        code = from_str(obj.get("code"))
        commune = Commune.from_dict(obj.get("commune"))
        commune_club_pro = from_none(obj.get("communeClubPro"))
        competitions = from_list(lambda x: x, obj.get("competitions"))
        engagements = from_list(Engagement.from_dict, obj.get("engagements"))
        id = int(from_str(obj.get("id")))
        labellisation = from_list(Labellisation.from_dict, obj.get("labellisation"))
        logo = Logo.from_dict(obj.get("logo"))
        mail = from_str(obj.get("mail"))
        membres = from_list(Membre.from_dict, obj.get("membres"))
        nom = from_str(obj.get("nom"))
        nom_simple = from_none(obj.get("nom_simple"))
        nom_club_pro = from_str(obj.get("nomClubPro"))
        offres_pratiques = from_list(
            OffresPratique.from_dict, obj.get("offresPratiques")
        )
        organismes_fils = from_list(lambda x: x, obj.get("organismes_fils"))
        salle = Salle.from_dict(obj.get("salle"))
        telephone = from_str(obj.get("telephone"))
        type = from_str(obj.get("type"))
        url_site_web = from_str(obj.get("urlSiteWeb"))
        return Data(
            adresse,
            adresse_club_pro,
            cartographie,
            code,
            commune,
            commune_club_pro,
            competitions,
            engagements,
            id,
            labellisation,
            logo,
            mail,
            membres,
            nom,
            nom_simple,
            nom_club_pro,
            offres_pratiques,
            organismes_fils,
            salle,
            telephone,
            type,
            url_site_web,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["adresse"] = from_str(self.adresse)
        result["adresseClubPro"] = from_none(self.adresse_club_pro)
        result["cartographie"] = to_class(Cartographie, self.cartographie)
        result["code"] = from_str(self.code)
        result["commune"] = to_class(Commune, self.commune)
        result["communeClubPro"] = from_none(self.commune_club_pro)
        result["competitions"] = from_list(lambda x: x, self.competitions)
        result["engagements"] = from_list(
            lambda x: to_class(Engagement, x), self.engagements
        )
        result["id"] = from_str(str(self.id))
        result["labellisation"] = from_list(
            lambda x: to_class(Labellisation, x), self.labellisation
        )
        result["logo"] = to_class(Logo, self.logo)
        result["mail"] = from_str(self.mail)
        result["membres"] = from_list(lambda x: to_class(Membre, x), self.membres)
        result["nom"] = from_str(self.nom)
        result["nom_simple"] = from_none(self.nom_simple)
        result["nomClubPro"] = from_str(self.nom_club_pro)
        result["offresPratiques"] = from_list(
            lambda x: to_class(OffresPratique, x), self.offres_pratiques
        )
        result["organismes_fils"] = from_list(lambda x: x, self.organismes_fils)
        result["salle"] = to_class(Salle, self.salle)
        result["telephone"] = from_str(self.telephone)
        result["type"] = from_str(self.type)
        result["urlSiteWeb"] = from_str(self.url_site_web)
        return result


class GetFfbbserverOrganismesResponse:
    data: Data

    def __init__(self, data: Data) -> None:
        self.data = data

    @staticmethod
    def from_dict(obj: Any) -> "GetFfbbserverOrganismesResponse":
        assert isinstance(obj, dict)
        data = Data.from_dict(obj.get("data"))
        return GetFfbbserverOrganismesResponse(data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = to_class(Data, self.data)
        return result


def get_ffbbserver_organismes_response_from_dict(
    s: Any,
) -> GetFfbbserverOrganismesResponse:
    return GetFfbbserverOrganismesResponse.from_dict(s)


def get_ffbbserver_organismes_response_to_dict(
    x: GetFfbbserverOrganismesResponse,
) -> Any:
    return to_class(GetFfbbserverOrganismesResponse, x)
