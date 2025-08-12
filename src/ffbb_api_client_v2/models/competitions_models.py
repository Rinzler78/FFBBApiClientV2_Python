from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


# Query Parameters Model
@dataclass
class CompetitionsQuery:
    deep_phases_poules_rencontres__limit: str | None = (
        "1000"  # Original: deep[phases][poules][rencontres][_limit]
    )
    fields_: list[str] = None  # Original: fields[]


# Response Model
@dataclass
class GetCompetitionResponse:
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
    logo: Any | None

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
                    logo: Any | None

                idOrganismeEquipe1: Idorganismeequipe1Model

                @dataclass
                class Idorganismeequipe2Model:
                    logo: Any | None

                idOrganismeEquipe2: Idorganismeequipe2Model
                gsId: Any | None

                @dataclass
                class Idengagementequipe1Model:
                    nom: str
                    id: str
                    nomOfficiel: str
                    nomUsuel: str
                    codeAbrege: str
                    logo: Any | None

                idEngagementEquipe1: Idengagementequipe1Model

                @dataclass
                class Idengagementequipe2Model:
                    nom: str
                    id: str
                    nomOfficiel: str
                    nomUsuel: str
                    codeAbrege: str
                    logo: Any | None

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

    @classmethod
    def from_dict(cls, data: dict) -> GetCompetitionResponse:
        """Convert dictionary to CompetitionsModel instance."""
        if not data:
            return None

        # Handle case where data is not a dictionary
        if not isinstance(data, dict):
            return None

        # Handle API error responses
        if "errors" in data:
            return None

        # Basic implementation - can be expanded later
        return cls(
            id=str(data.get("id", "")),
            nom=str(data.get("nom", "")),
            sexe=str(data.get("sexe", "")),
            saison=str(data.get("saison", "")),
            code=str(data.get("code", "")),
            typeCompetition=str(data.get("typeCompetition", "")),
            liveStat=int(data.get("liveStat", 0)),
            competition_origine=str(data.get("competition_origine", "")),
            competition_origine_nom=str(data.get("competition_origine_nom", "")),
            publicationInternet=str(data.get("publicationInternet", "")),
            categorie=None,  # Simplified for now
            typeCompetitionGenerique=None,  # Simplified for now
            logo=data.get("logo"),
            poules=[],  # Simplified for now
            phases=[],  # Simplified for now
        )
