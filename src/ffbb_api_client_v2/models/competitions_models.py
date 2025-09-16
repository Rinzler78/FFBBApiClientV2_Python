from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .game_stats_models import GameStatsModel


# Query Parameters Model
@dataclass
class CompetitionsQuery:
    deep_phases_poules_rencontres__limit: str | None = (
        "1000"  # Original: deep[phases][poules][rencontres][_limit]
    )
    fields_: list[str] | None = field(default=None)  # Original: fields[]


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
                gsId: GameStatsModel | None

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

        # Extract nested categorie data
        categorie_data = data.get("categorie", {})
        categorie = (
            cls.CategorieModel(
                code=str(categorie_data.get("code", "")),
                ordre=int(categorie_data.get("ordre", 0)),
            )
            if categorie_data
            else None
        )

        # Extract nested typeCompetitionGenerique data
        type_comp_generique_data = data.get("typeCompetitionGenerique", {})
        type_comp_generique = None
        if type_comp_generique_data:
            logo_data = type_comp_generique_data.get("logo", {})
            logo_tcg = (
                cls.TypecompetitiongeneriqueModel.LogoModel(
                    id=str(logo_data.get("id", "")),
                    gradient_color=str(logo_data.get("gradient_color", "")),
                )
                if logo_data
                else None
            )
            type_comp_generique = cls.TypecompetitiongeneriqueModel(logo=logo_tcg)

        # Extract poules data (basic level)
        poules = []
        for poule_data in data.get("poules", []):
            if poule_data:
                poule = cls.PoulesitemModel(
                    id=str(poule_data.get("id", "")),
                    nom=str(poule_data.get("nom", "")),
                )
                poules.append(poule)

        # Extract phases data with complete nested structure
        phases = []
        for phase_data in data.get("phases", []):
            if phase_data:
                # Process poules within phases
                phase_poules = []
                for phase_poule_data in phase_data.get("poules", []):
                    if phase_poule_data:
                        # Process rencontres within phase poules
                        rencontres = []
                        for rencontre_data in phase_poule_data.get("rencontres", []):
                            if rencontre_data:
                                # Extract gsId (GameStats) data
                                gs_id_data = rencontre_data.get("gsId", {})
                                gs_id = (
                                    GameStatsModel.from_dict(gs_id_data)
                                    if gs_id_data
                                    else None
                                )

                                # Extract idOrganismeEquipe1 data
                                org_equipe1_data = rencontre_data.get(
                                    "idOrganismeEquipe1", {}
                                )
                                id_organisme_equipe1 = (
                                    cls.PhasesitemModel.PoulesitemModel.RencontresitemModel.Idorganismeequipe1Model(
                                        logo=org_equipe1_data.get("logo")
                                    )
                                    if org_equipe1_data
                                    else None
                                )

                                # Extract idOrganismeEquipe2 data
                                org_equipe2_data = rencontre_data.get(
                                    "idOrganismeEquipe2", {}
                                )
                                id_organisme_equipe2 = (
                                    cls.PhasesitemModel.PoulesitemModel.RencontresitemModel.Idorganismeequipe2Model(
                                        logo=org_equipe2_data.get("logo")
                                    )
                                    if org_equipe2_data
                                    else None
                                )

                                # Extract idEngagementEquipe1 data
                                eng_equipe1_data = rencontre_data.get(
                                    "idEngagementEquipe1", {}
                                )
                                id_engagement_equipe1 = (
                                    cls.PhasesitemModel.PoulesitemModel.RencontresitemModel.Idengagementequipe1Model(
                                        nom=str(eng_equipe1_data.get("nom", "")),
                                        id=str(eng_equipe1_data.get("id", "")),
                                        nomOfficiel=str(
                                            eng_equipe1_data.get("nomOfficiel", "")
                                        ),
                                        nomUsuel=str(
                                            eng_equipe1_data.get("nomUsuel", "")
                                        ),
                                        codeAbrege=str(
                                            eng_equipe1_data.get("codeAbrege", "")
                                        ),
                                        logo=eng_equipe1_data.get("logo"),
                                    )
                                    if eng_equipe1_data
                                    else None
                                )

                                # Extract idEngagementEquipe2 data
                                eng_equipe2_data = rencontre_data.get(
                                    "idEngagementEquipe2", {}
                                )
                                id_engagement_equipe2 = (
                                    cls.PhasesitemModel.PoulesitemModel.RencontresitemModel.Idengagementequipe2Model(
                                        nom=str(eng_equipe2_data.get("nom", "")),
                                        id=str(eng_equipe2_data.get("id", "")),
                                        nomOfficiel=str(
                                            eng_equipe2_data.get("nomOfficiel", "")
                                        ),
                                        nomUsuel=str(
                                            eng_equipe2_data.get("nomUsuel", "")
                                        ),
                                        codeAbrege=str(
                                            eng_equipe2_data.get("codeAbrege", "")
                                        ),
                                        logo=eng_equipe2_data.get("logo"),
                                    )
                                    if eng_equipe2_data
                                    else None
                                )

                                # Extract salle data
                                salle_data = rencontre_data.get("salle", {})
                                salle = None
                                if salle_data:
                                    salle_commune_data = salle_data.get("commune", {})
                                    salle_commune = (
                                        cls.PhasesitemModel.PoulesitemModel.RencontresitemModel.SalleModel.CommuneModel(
                                            codePostal=str(
                                                salle_commune_data.get("codePostal", "")
                                            ),
                                            libelle=str(
                                                salle_commune_data.get("libelle", "")
                                            ),
                                        )
                                        if salle_commune_data
                                        else None
                                    )

                                    salle_cartographie_data = salle_data.get(
                                        "cartographie", {}
                                    )
                                    salle_cartographie = (
                                        (
                                            cls.PhasesitemModel.PoulesitemModel.RencontresitemModel.SalleModel.CartographieModel
                                        )(
                                            latitude=float(
                                                salle_cartographie_data.get(
                                                    "latitude", 0.0
                                                )
                                            ),
                                            longitude=float(
                                                salle_cartographie_data.get(
                                                    "longitude", 0.0
                                                )
                                            ),
                                        )
                                        if salle_cartographie_data
                                        else None
                                    )

                                    salle = cls.PhasesitemModel.PoulesitemModel.RencontresitemModel.SalleModel(
                                        id=str(salle_data.get("id", "")),
                                        numero=str(salle_data.get("numero", "")),
                                        libelle=str(salle_data.get("libelle", "")),
                                        libelle2=str(salle_data.get("libelle2", "")),
                                        adresse=str(salle_data.get("adresse", "")),
                                        adresseComplement=str(
                                            salle_data.get("adresseComplement", "")
                                        ),
                                        commune=salle_commune,
                                        cartographie=salle_cartographie,
                                    )

                                # Extract officiels data
                                officiels = []
                                for officiel_data in rencontre_data.get(
                                    "officiels", []
                                ):
                                    if officiel_data:
                                        fonction_data = officiel_data.get(
                                            "fonction", {}
                                        )
                                        fonction = (
                                            (
                                                cls.PhasesitemModel.PoulesitemModel.RencontresitemModel.OfficielsitemModel.FonctionModel
                                            )(
                                                libelle=str(
                                                    fonction_data.get("libelle", "")
                                                ),
                                            )
                                            if fonction_data
                                            else None
                                        )

                                        officiel_person_data = officiel_data.get(
                                            "officiel", {}
                                        )
                                        officiel_person = (
                                            (
                                                cls.PhasesitemModel.PoulesitemModel.RencontresitemModel.OfficielsitemModel.OfficielModel
                                            )(
                                                nom=str(
                                                    officiel_person_data.get("nom", "")
                                                ),
                                                prenom=str(
                                                    officiel_person_data.get(
                                                        "prenom", ""
                                                    )
                                                ),
                                            )
                                            if officiel_person_data
                                            else None
                                        )

                                        officiel = (
                                            cls.PhasesitemModel.PoulesitemModel.RencontresitemModel.OfficielsitemModel
                                        )(
                                            ordre=int(officiel_data.get("ordre", 0)),
                                            fonction=fonction,
                                            officiel=officiel_person,
                                        )
                                        officiels.append(officiel)

                                # Create the rencontre object with proper date handling
                                date_str = rencontre_data.get(
                                    "date_rencontre", "1970-01-01T00:00:00"
                                )
                                try:
                                    date_rencontre = datetime.fromisoformat(
                                        date_str.replace("Z", "+00:00")
                                    )
                                except (ValueError, AttributeError):
                                    date_rencontre = datetime.fromisoformat(
                                        "1970-01-01T00:00:00"
                                    )

                                rencontre = cls.PhasesitemModel.PoulesitemModel.RencontresitemModel(
                                    id=str(rencontre_data.get("id", "")),
                                    numero=str(rencontre_data.get("numero", "")),
                                    numeroJournee=str(
                                        rencontre_data.get("numeroJournee", "")
                                    ),
                                    idPoule=str(rencontre_data.get("idPoule", "")),
                                    competitionId=str(
                                        rencontre_data.get("competitionId", "")
                                    ),
                                    resultatEquipe1=str(
                                        rencontre_data.get("resultatEquipe1", "")
                                    ),
                                    resultatEquipe2=str(
                                        rencontre_data.get("resultatEquipe2", "")
                                    ),
                                    joue=int(rencontre_data.get("joue", 0)),
                                    nomEquipe1=str(
                                        rencontre_data.get("nomEquipe1", "")
                                    ),
                                    nomEquipe2=str(
                                        rencontre_data.get("nomEquipe2", "")
                                    ),
                                    date_rencontre=date_rencontre,
                                    idOrganismeEquipe1=id_organisme_equipe1,
                                    idOrganismeEquipe2=id_organisme_equipe2,
                                    gsId=gs_id,
                                    idEngagementEquipe1=id_engagement_equipe1,
                                    idEngagementEquipe2=id_engagement_equipe2,
                                    salle=salle,
                                    officiels=officiels,
                                )
                                rencontres.append(rencontre)

                        # Extract engagements within phase poules
                        engagements = []
                        for engagement_data in phase_poule_data.get("engagements", []):
                            if engagement_data:
                                id_organisme_data = engagement_data.get(
                                    "idOrganisme", {}
                                )
                                id_organisme = (
                                    cls.PhasesitemModel.PoulesitemModel.EngagementsitemModel.IdorganismeModel(
                                        id=str(id_organisme_data.get("id", "")),
                                    )
                                    if id_organisme_data
                                    else None
                                )

                                engagement = cls.PhasesitemModel.PoulesitemModel.EngagementsitemModel(
                                    id=str(engagement_data.get("id", "")),
                                    idOrganisme=id_organisme,
                                )
                                engagements.append(engagement)

                        phase_poule = cls.PhasesitemModel.PoulesitemModel(
                            id=str(phase_poule_data.get("id", "")),
                            nom=str(phase_poule_data.get("nom", "")),
                            rencontres=rencontres,
                            engagements=engagements,
                        )
                        phase_poules.append(phase_poule)

                phase = cls.PhasesitemModel(
                    id=str(phase_data.get("id", "")),
                    nom=str(phase_data.get("nom", "")),
                    liveStat=int(phase_data.get("liveStat", 0)),
                    phase_code=str(phase_data.get("phase_code", "")),
                    poules=phase_poules,
                )
                phases.append(phase)

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
            categorie=categorie,
            typeCompetitionGenerique=type_comp_generique,
            logo=data.get("logo"),
            poules=poules,
            phases=phases,
        )
