from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


# Query Parameters Model
@dataclass
class OrganismesQuery:
    fields_: list[str] = None  # Original: fields[]


# Response Model
@dataclass
class OrganismesModel:
    id: str
    nom: str
    code: str
    telephone: str
    adresse: str
    mail: str
    type: str
    nom_simple: Optional[Any]
    urlSiteWeb: str
    nomClubPro: str
    adresseClubPro: Optional[Any]

    @dataclass
    class CommuneModel:
        codePostal: str
        libelle: str

    commune: CommuneModel

    @dataclass
    class CartographieModel:
        latitude: float
        longitude: float

    cartographie: CartographieModel
    communeClubPro: Optional[Any]

    @dataclass
    class MembresitemModel:
        id: str
        nom: str
        prenom: str
        adresse1: str
        adresse2: Optional[Any]
        codePostal: str
        ville: str
        mail: str
        telephoneFixe: Optional[Any]
        telephonePortable: str
        codeFonction: str

    membres: list[MembresitemModel]
    competitions: list[Any]

    @dataclass
    class EngagementsitemModel:
        id: str

        @dataclass
        class IdpouleModel:
            id: str

        idPoule: IdpouleModel

        @dataclass
        class IdcompetitionModel:
            id: str
            nom: str
            code: str
            sexe: str
            competition_origine: str
            competition_origine_nom: str
            competition_origine_niveau: int
            typeCompetition: str
            logo: Optional[Any]

            @dataclass
            class SaisonModel:
                id: str

            saison: SaisonModel
            idCompetitionPere: Optional[Any]

            @dataclass
            class OrganisateurModel:
                type: str

            organisateur: OrganisateurModel

            @dataclass
            class TypecompetitiongeneriqueModel:

                @dataclass
                class LogoModel:
                    id: str
                    gradient_color: str

                logo: LogoModel

            typeCompetitionGenerique: TypecompetitiongeneriqueModel

            @dataclass
            class CategorieModel:
                code: str
                ordre: int

            categorie: CategorieModel

        idCompetition: IdcompetitionModel

    engagements: list[EngagementsitemModel]
    organismes_fils: list[Any]

    @dataclass
    class OffrespratiquesitemModel:

        @dataclass
        class Ffbbserver_Offres_Pratiques_IdModel:
            id: str
            title: str
            categoriePratique: str
            typePratique: str

        ffbbserver_offres_pratiques_id: Ffbbserver_Offres_Pratiques_IdModel

    offresPratiques: list[OffrespratiquesitemModel]

    @dataclass
    class LabellisationitemModel:
        id: str
        debut: datetime
        fin: datetime

        @dataclass
        class IdlabellisationprogrammeModel:
            id: str
            libelle: str
            labellisationLabel: str
            logo_vertical: Optional[Any]

        idLabellisationProgramme: IdlabellisationprogrammeModel

    labellisation: list[LabellisationitemModel]

    @dataclass
    class SalleModel:
        id: str
        numero: str
        libelle: str
        libelle2: str
        adresse: str
        adresseComplement: str

        @dataclass
        class CommuneModel:
            codePostal: str
            libelle: str

        commune: CommuneModel

        @dataclass
        class CartographieModel:
            latitude: float
            longitude: float

        cartographie: CartographieModel

    salle: SalleModel

    @dataclass
    class LogoModel:
        id: str
        gradient_color: str

    logo: LogoModel
