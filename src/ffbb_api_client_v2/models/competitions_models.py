from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


# Query Parameters Model
@dataclass
class CompetitionsQuery:
    deep_phases_poules_rencontres__limit: Optional[str] = (
        "1000"  # Original: deep[phases][poules][rencontres][_limit]
    )
    fields_: list[str] = None  # Original: fields[]


# Response Model
@dataclass
class CompetitionsModel:
    id: str
    nom: str
    sexe: str
    saison: str
    code: str
    typeCompetition: str
    liveStat: int
    competition_origine: str
    competition_origine_nom: str
    publicationInternet: str

    @dataclass
    class CategorieModel:
        code: str
        ordre: int

    categorie: CategorieModel

    @dataclass
    class TypecompetitiongeneriqueModel:

        @dataclass
        class LogoModel:
            id: str
            gradient_color: str

        logo: LogoModel

    typeCompetitionGenerique: TypecompetitiongeneriqueModel
    logo: Optional[Any]

    @dataclass
    class PoulesitemModel:
        id: str
        nom: str

    poules: list[PoulesitemModel]

    @dataclass
    class PhasesitemModel:
        id: str
        nom: str
        liveStat: int
        phase_code: str

        @dataclass
        class PoulesitemModel:
            id: str
            nom: str

            @dataclass
            class RencontresitemModel:
                id: str
                numero: str
                numeroJournee: str
                idPoule: str
                competitionId: str
                resultatEquipe1: str
                resultatEquipe2: str
                joue: int
                nomEquipe1: str
                nomEquipe2: str
                date_rencontre: datetime

                @dataclass
                class Idorganismeequipe1Model:
                    logo: Optional[Any]

                idOrganismeEquipe1: Idorganismeequipe1Model

                @dataclass
                class Idorganismeequipe2Model:
                    logo: Optional[Any]

                idOrganismeEquipe2: Idorganismeequipe2Model
                gsId: Optional[Any]

                @dataclass
                class Idengagementequipe1Model:
                    nom: str
                    id: str
                    nomOfficiel: str
                    nomUsuel: str
                    codeAbrege: str
                    logo: Optional[Any]

                idEngagementEquipe1: Idengagementequipe1Model

                @dataclass
                class Idengagementequipe2Model:
                    nom: str
                    id: str
                    nomOfficiel: str
                    nomUsuel: str
                    codeAbrege: str
                    logo: Optional[Any]

                idEngagementEquipe2: Idengagementequipe2Model

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
                class OfficielsitemModel:
                    ordre: int

                    @dataclass
                    class FonctionModel:
                        libelle: str

                    fonction: FonctionModel

                    @dataclass
                    class OfficielModel:
                        nom: str
                        prenom: str

                    officiel: OfficielModel

                officiels: list[OfficielsitemModel]

            rencontres: list[RencontresitemModel]

            @dataclass
            class EngagementsitemModel:
                id: str

                @dataclass
                class IdorganismeModel:
                    id: str

                idOrganisme: IdorganismeModel

            engagements: list[EngagementsitemModel]

        poules: list[PoulesitemModel]

    phases: list[PhasesitemModel]
