from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


# Query Parameters Model
@dataclass
class OrganismesQuery:
    fields_: list[str] = None  # Original: fields[]


# Response Model
@dataclass
class GetOrganismeResponse:
    id: str
    nom: str
    code: str
    telephone: str
    adresse: str
    mail: str
    type: str
    nom_simple: Any | None
    urlSiteWeb: str
    nomClubPro: str
    adresseClubPro: Any | None

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
    communeClubPro: Any | None

    @dataclass
    class MembresitemModel:
        id: str
        nom: str
        prenom: str
        adresse1: str
        adresse2: Any | None
        codePostal: str
        ville: str
        mail: str
        telephoneFixe: Any | None
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
            logo: Any | None

            @dataclass
            class SaisonModel:
                id: str

            saison: SaisonModel
            idCompetitionPere: Any | None

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
            logo_vertical: Any | None

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

    @classmethod
    def from_dict(cls, data: dict) -> GetOrganismeResponse:
        """Convert dictionary to OrganismesModel instance."""
        if not data:
            return None

        # Handle case where data is not a dictionary
        if not isinstance(data, dict):
            return None

        # Handle API error responses
        if "errors" in data:
            return None

        # Extract nested commune data
        commune_data = data.get("commune", {})
        commune = (
            cls.CommuneModel(
                codePostal=commune_data.get("codePostal", ""),
                libelle=commune_data.get("libelle", ""),
            )
            if commune_data
            else None
        )

        # Extract nested cartographie data
        cartographie_data = data.get("cartographie", {})
        cartographie = (
            cls.CartographieModel(
                latitude=float(cartographie_data.get("latitude", 0.0)),
                longitude=float(cartographie_data.get("longitude", 0.0)),
            )
            if cartographie_data
            else None
        )

        # Extract membres data
        membres = []
        for membre_data in data.get("membres", []):
            if membre_data:
                membre = cls.MembresitemModel(
                    id=str(membre_data.get("id", "")),
                    nom=str(membre_data.get("nom", "")),
                    prenom=str(membre_data.get("prenom", "")),
                    adresse1=str(membre_data.get("adresse1", "")),
                    adresse2=membre_data.get("adresse2"),
                    codePostal=str(membre_data.get("codePostal", "")),
                    ville=str(membre_data.get("ville", "")),
                    mail=str(membre_data.get("mail", "")),
                    telephoneFixe=membre_data.get("telephoneFixe"),
                    telephonePortable=str(membre_data.get("telephonePortable", "")),
                    codeFonction=str(membre_data.get("codeFonction", "")),
                )
                membres.append(membre)

        # Extract engagements data
        engagements = []
        for engagement_data in data.get("engagements", []):
            if engagement_data:
                # Extract idPoule
                poule_data = engagement_data.get("idPoule", {})
                id_poule = (
                    cls.EngagementsitemModel.IdpouleModel(
                        id=str(poule_data.get("id", ""))
                    )
                    if poule_data
                    else None
                )

                # Extract idCompetition
                competition_data = engagement_data.get("idCompetition", {})
                id_competition = None
                if competition_data:
                    saison_data = competition_data.get("saison", {})
                    saison = (
                        cls.EngagementsitemModel.IdcompetitionModel.SaisonModel(
                            id=str(saison_data.get("id", ""))
                        )
                        if saison_data
                        else None
                    )

                    organisateur_data = competition_data.get("organisateur", {})
                    organisateur = (
                        cls.EngagementsitemModel.IdcompetitionModel.OrganisateurModel(
                            type=str(organisateur_data.get("type", ""))
                        )
                        if organisateur_data
                        else None
                    )

                    type_comp_generique_data = competition_data.get(
                        "typeCompetitionGenerique", {}
                    )
                    type_comp_generique = None
                    if type_comp_generique_data:
                        logo_data = type_comp_generique_data.get("logo", {})
                        # Use shorter aliases to avoid line length issues
                        IdComp = cls.EngagementsitemModel.IdcompetitionModel
                        LogoClass = IdComp.TypecompetitiongeneriqueModel.LogoModel
                        logo_tcg = (
                            LogoClass(
                                id=str(logo_data.get("id", "")),
                                gradient_color=str(logo_data.get("gradient_color", "")),
                            )
                            if logo_data
                            else None
                        )

                        TypeCompGenClass = IdComp.TypecompetitiongeneriqueModel
                        type_comp_generique = TypeCompGenClass(logo=logo_tcg)

                    categorie_data = competition_data.get("categorie", {})
                    categorie = (
                        cls.EngagementsitemModel.IdcompetitionModel.CategorieModel(
                            code=str(categorie_data.get("code", "")),
                            ordre=int(categorie_data.get("ordre", 0)),
                        )
                        if categorie_data
                        else None
                    )

                    id_competition = cls.EngagementsitemModel.IdcompetitionModel(
                        id=str(competition_data.get("id", "")),
                        nom=str(competition_data.get("nom", "")),
                        code=str(competition_data.get("code", "")),
                        sexe=str(competition_data.get("sexe", "")),
                        competition_origine=str(
                            competition_data.get("competition_origine", "")
                        ),
                        competition_origine_nom=str(
                            competition_data.get("competition_origine_nom", "")
                        ),
                        competition_origine_niveau=int(
                            competition_data.get("competition_origine_niveau", 0)
                        ),
                        typeCompetition=str(
                            competition_data.get("typeCompetition", "")
                        ),
                        logo=competition_data.get("logo"),
                        saison=saison,
                        idCompetitionPere=competition_data.get("idCompetitionPere"),
                        organisateur=organisateur,
                        typeCompetitionGenerique=type_comp_generique,
                        categorie=categorie,
                    )

                engagement = cls.EngagementsitemModel(
                    id=str(engagement_data.get("id", "")),
                    idPoule=id_poule,
                    idCompetition=id_competition,
                )
                engagements.append(engagement)

        # Extract offres pratiques
        offres_pratiques = []
        for offre_data in data.get("offresPratiques", []):
            if offre_data:
                ffbb_pratique_data = offre_data.get(
                    "ffbbserver_offres_pratiques_id", {}
                )
                ffbb_pratique = (
                    cls.OffrespratiquesitemModel.Ffbbserver_Offres_Pratiques_IdModel(
                        id=str(ffbb_pratique_data.get("id", "")),
                        title=str(ffbb_pratique_data.get("title", "")),
                        categoriePratique=str(
                            ffbb_pratique_data.get("categoriePratique", "")
                        ),
                        typePratique=str(ffbb_pratique_data.get("typePratique", "")),
                    )
                    if ffbb_pratique_data
                    else None
                )

                offre = cls.OffrespratiquesitemModel(
                    ffbbserver_offres_pratiques_id=ffbb_pratique
                )
                offres_pratiques.append(offre)

        # Extract labellisation
        labellisations = []
        for label_data in data.get("labellisation", []):
            if label_data:
                programme_data = label_data.get("idLabellisationProgramme", {})
                programme = (
                    cls.LabellisationitemModel.IdlabellisationprogrammeModel(
                        id=str(programme_data.get("id", "")),
                        libelle=str(programme_data.get("libelle", "")),
                        labellisationLabel=str(
                            programme_data.get("labellisationLabel", "")
                        ),
                        logo_vertical=programme_data.get("logo_vertical"),
                    )
                    if programme_data
                    else None
                )

                label = cls.LabellisationitemModel(
                    id=str(label_data.get("id", "")),
                    debut=datetime.fromisoformat(label_data.get("debut", "1970-01-01")),
                    fin=datetime.fromisoformat(label_data.get("fin", "1970-01-01")),
                    idLabellisationProgramme=programme,
                )
                labellisations.append(label)

        # Extract salle
        salle_data = data.get("salle", {})
        salle = None
        if salle_data:
            salle_commune_data = salle_data.get("commune", {})
            salle_commune = (
                cls.SalleModel.CommuneModel(
                    codePostal=str(salle_commune_data.get("codePostal", "")),
                    libelle=str(salle_commune_data.get("libelle", "")),
                )
                if salle_commune_data
                else None
            )

            salle_cartographie_data = salle_data.get("cartographie", {})
            salle_cartographie = (
                cls.SalleModel.CartographieModel(
                    latitude=float(salle_cartographie_data.get("latitude", 0.0)),
                    longitude=float(salle_cartographie_data.get("longitude", 0.0)),
                )
                if salle_cartographie_data
                else None
            )

            salle = cls.SalleModel(
                id=str(salle_data.get("id", "")),
                numero=str(salle_data.get("numero", "")),
                libelle=str(salle_data.get("libelle", "")),
                libelle2=str(salle_data.get("libelle2", "")),
                adresse=str(salle_data.get("adresse", "")),
                adresseComplement=str(salle_data.get("adresseComplement", "")),
                commune=salle_commune,
                cartographie=salle_cartographie,
            )

        # Extract logo
        logo_data = data.get("logo", {})
        logo = (
            cls.LogoModel(
                id=str(logo_data.get("id", "")),
                gradient_color=str(logo_data.get("gradient_color", "")),
            )
            if logo_data
            else None
        )

        return cls(
            id=str(data.get("id", "")),
            nom=str(data.get("nom", "")),
            code=str(data.get("code", "")),
            telephone=str(data.get("telephone", "")),
            adresse=str(data.get("adresse", "")),
            mail=str(data.get("mail", "")),
            type=str(data.get("type", "")),
            nom_simple=data.get("nom_simple"),
            urlSiteWeb=str(data.get("urlSiteWeb", "")),
            nomClubPro=str(data.get("nomClubPro", "")),
            adresseClubPro=data.get("adresseClubPro"),
            commune=commune,
            cartographie=cartographie,
            communeClubPro=data.get("communeClubPro"),
            membres=membres,
            competitions=data.get("competitions", []),
            engagements=engagements,
            organismes_fils=data.get("organismes_fils", []),
            offresPratiques=offres_pratiques,
            labellisation=labellisations,
            salle=salle,
            logo=logo,
        )
