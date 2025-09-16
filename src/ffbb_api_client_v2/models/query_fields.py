from enum import Enum


class OrganismeFields:
    """Default fields for organisme queries."""

    # Basic fields
    ID = "id"
    NOM = "nom"
    CODE = "code"
    TELEPHONE = "telephone"
    ADRESSE = "adresse"
    MAIL = "mail"
    TYPE = "type"
    NOM_SIMPLE = "nom_simple"
    URL_SITE_WEB = "urlSiteWeb"

    # Commune fields
    COMMUNE_CODE_POSTAL = "commune.codePostal"
    COMMUNE_LIBELLE = "commune.libelle"

    # Competitions fields
    COMPETITIONS_ID = "competitions.id"
    COMPETITIONS_NOM = "competitions.nom"

    # Engagements fields
    ENGAGEMENTS_ID = "engagements.id"
    ENGAGEMENTS_ID_COMPETITION_ID = "engagements.idCompetition.id"
    ENGAGEMENTS_ID_COMPETITION_NOM = "engagements.idCompetition.nom"
    ENGAGEMENTS_ID_COMPETITION_CODE = "engagements.idCompetition.code"
    ENGAGEMENTS_ID_COMPETITION_SEXE = "engagements.idCompetition.sexe"
    ENGAGEMENTS_ID_COMPETITION_COMPETITION_ORIGINE = (
        "engagements.idCompetition.competition_origine"
    )
    ENGAGEMENTS_ID_COMPETITION_COMPETITION_ORIGINE_NOM = (
        "engagements.idCompetition.competition_origine_nom"
    )
    ENGAGEMENTS_ID_COMPETITION_COMPETITION_ORIGINE_NIVEAU = (
        "engagements.idCompetition.competition_origine_niveau"
    )
    ENGAGEMENTS_ID_COMPETITION_TYPE_COMPETITION = (
        "engagements.idCompetition.typeCompetition"
    )
    ENGAGEMENTS_ID_COMPETITION_LOGO_ID = "engagements.idCompetition.logo.id"
    ENGAGEMENTS_ID_COMPETITION_LOGO_GRADIENT_COLOR = (
        "engagements.idCompetition.logo.gradient_color"
    )
    ENGAGEMENTS_ID_COMPETITION_SAISON_ID = "engagements.idCompetition.saison.id"
    ENGAGEMENTS_ID_COMPETITION_SAISON_LIBELLE = (
        "engagements.idCompetition.saison.libelle"
    )
    ENGAGEMENTS_ID_COMPETITION_ID_COMPETITION_PERE = (
        "engagements.idCompetition.idCompetitionPere"
    )
    ENGAGEMENTS_ID_COMPETITION_ID_COMPETITION_PERE_ID = (
        "engagements.idCompetition.idCompetitionPere.id"
    )
    ENGAGEMENTS_ID_COMPETITION_ID_COMPETITION_PERE_NOM = (
        "engagements.idCompetition.idCompetitionPere.nom"
    )
    ENGAGEMENTS_ID_COMPETITION_ORGANISATEUR_TYPE = (
        "engagements.idCompetition.organisateur.type"
    )
    ENGAGEMENTS_ID_COMPETITION_TYPE_COMPETITION_GENERIQUE_LOGO_ID = (
        "engagements.idCompetition.typeCompetitionGenerique.logo.id"
    )
    ENGAGEMENTS_ID_COMPETITION_TYPE_COMPETITION_GENERIQUE_LOGO_GRADIENT_COLOR = (
        "engagements.idCompetition.typeCompetitionGenerique.logo.gradient_color"
    )
    ENGAGEMENTS_ID_COMPETITION_CATEGORIE_CODE = (
        "engagements.idCompetition.categorie.code"
    )
    ENGAGEMENTS_ID_COMPETITION_CATEGORIE_ORDRE = (
        "engagements.idCompetition.categorie.ordre"
    )
    ENGAGEMENTS_ID_POULE_ID = "engagements.idPoule.id"
    ENGAGEMENTS_ID_POULE_NOM = "engagements.idPoule.nom"

    # Membres fields
    MEMBRES_ID = "membres.id"
    MEMBRES_NOM = "membres.nom"
    MEMBRES_PRENOM = "membres.prenom"

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for organisme queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.CODE,
            cls.TELEPHONE,
            cls.ADRESSE,
            cls.COMMUNE_CODE_POSTAL,
            cls.COMMUNE_LIBELLE,
            cls.MAIL,
            cls.TYPE,
            cls.NOM_SIMPLE,
            cls.URL_SITE_WEB,
            cls.COMPETITIONS_ID,
            cls.COMPETITIONS_NOM,
            cls.ENGAGEMENTS_ID,
            # Complete idCompetition fields for proper model mapping
            cls.ENGAGEMENTS_ID_COMPETITION_ID,
            cls.ENGAGEMENTS_ID_COMPETITION_NOM,
            cls.ENGAGEMENTS_ID_COMPETITION_CODE,
            cls.ENGAGEMENTS_ID_COMPETITION_SEXE,
            cls.ENGAGEMENTS_ID_COMPETITION_COMPETITION_ORIGINE,
            cls.ENGAGEMENTS_ID_COMPETITION_COMPETITION_ORIGINE_NOM,
            cls.ENGAGEMENTS_ID_COMPETITION_COMPETITION_ORIGINE_NIVEAU,
            cls.ENGAGEMENTS_ID_COMPETITION_TYPE_COMPETITION,
            cls.ENGAGEMENTS_ID_COMPETITION_LOGO_ID,
            cls.ENGAGEMENTS_ID_COMPETITION_LOGO_GRADIENT_COLOR,
            cls.ENGAGEMENTS_ID_COMPETITION_SAISON_ID,
            cls.ENGAGEMENTS_ID_COMPETITION_SAISON_LIBELLE,
            cls.ENGAGEMENTS_ID_COMPETITION_ID_COMPETITION_PERE,
            cls.ENGAGEMENTS_ID_COMPETITION_ID_COMPETITION_PERE_ID,
            cls.ENGAGEMENTS_ID_COMPETITION_ID_COMPETITION_PERE_NOM,
            cls.ENGAGEMENTS_ID_COMPETITION_ORGANISATEUR_TYPE,
            cls.ENGAGEMENTS_ID_COMPETITION_TYPE_COMPETITION_GENERIQUE_LOGO_ID,
            cls.ENGAGEMENTS_ID_COMPETITION_TYPE_COMPETITION_GENERIQUE_LOGO_GRADIENT_COLOR,
            cls.ENGAGEMENTS_ID_COMPETITION_CATEGORIE_CODE,
            cls.ENGAGEMENTS_ID_COMPETITION_CATEGORIE_ORDRE,
            cls.ENGAGEMENTS_ID_POULE_ID,
            cls.ENGAGEMENTS_ID_POULE_NOM,
            cls.MEMBRES_ID,
            cls.MEMBRES_NOM,
            cls.MEMBRES_PRENOM,
        ]

    @classmethod
    def get_basic_fields(cls) -> list[str]:
        """Get basic fields for simple organisme queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.CODE,
            cls.TELEPHONE,
            cls.ADRESSE,
            cls.MAIL,
        ]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields including nested relationships."""
        return cls.get_default_fields() + [
            "cartographie.latitude",
            "cartographie.longitude",
            "logo.id",
            "logo.gradient_color",
            "membres.mail",
            "membres.telephonePortable",
            # Additional detailed fields beyond default
            "membres.adresse1",
            "membres.adresse2",
            "membres.codePostal",
            "membres.ville",
            "membres.telephoneFixe",
            "membres.codeFonction",
            "nomClubPro",
            "adresseClubPro",
            "communeClubPro",
        ]


class CompetitionFields:
    """Default fields for competition queries."""

    # Basic fields
    ID = "id"
    NOM = "nom"
    SEXE = "sexe"
    SAISON = "saison"
    CODE = "code"
    TYPE_COMPETITION = "typeCompetition"
    LIVE_STAT = "liveStat"
    COMPETITION_ORIGINE = "competition_origine"
    COMPETITION_ORIGINE_NOM = "competition_origine_nom"

    # Categorie fields
    CATEGORIE_CODE = "categorie.code"
    CATEGORIE_ORDRE = "categorie.ordre"

    # Logo fields
    LOGO_ID = "logo.id"
    LOGO_GRADIENT_COLOR = "logo.gradient_color"
    TYPE_COMPETITION_GENERIQUE_LOGO_ID = "typeCompetitionGenerique.logo.id"
    TYPE_COMPETITION_GENERIQUE_LOGO_GRADIENT_COLOR = (
        "typeCompetitionGenerique.logo.gradient_color"
    )

    # Other fields
    PUBLICATION_INTERNET = "publicationInternet"
    POULES_ID = "poules.id"
    POULES_NOM = "poules.nom"

    # Phases fields (additional)
    PHASES_LIVE_STAT = "phases.liveStat"
    PHASES_PHASE_CODE = "phases.phase_code"

    # Additional rencontres fields
    PHASES_POULES_RENCONTRES_NUMERO_JOURNEE = "phases.poules.rencontres.numeroJournee"
    PHASES_POULES_RENCONTRES_ID_POULE = "phases.poules.rencontres.idPoule"
    PHASES_POULES_RENCONTRES_COMPETITION_ID = "phases.poules.rencontres.competitionId"
    PHASES_POULES_RENCONTRES_RESULTAT_EQUIPE1 = (
        "phases.poules.rencontres.resultatEquipe1"
    )
    PHASES_POULES_RENCONTRES_RESULTAT_EQUIPE2 = (
        "phases.poules.rencontres.resultatEquipe2"
    )
    PHASES_POULES_RENCONTRES_JOUE = "phases.poules.rencontres.joue"
    PHASES_POULES_RENCONTRES_NOM_EQUIPE1 = "phases.poules.rencontres.nomEquipe1"
    PHASES_POULES_RENCONTRES_NOM_EQUIPE2 = "phases.poules.rencontres.nomEquipe2"

    # Engagements fields
    PHASES_POULES_ENGAGEMENTS_ID = "phases.poules.engagements.id"
    PHASES_POULES_ENGAGEMENTS_ID_ORGANISME_ID = (
        "phases.poules.engagements.idOrganisme.id"
    )

    # Phases fields
    PHASES_ID = "phases.id"
    PHASES_NOM = "phases.nom"

    # Poules fields (nested in phases)
    PHASES_POULES_ID = "phases.poules.id"
    PHASES_POULES_NOM = "phases.poules.nom"

    # Rencontres fields (nested in poules)
    PHASES_POULES_RENCONTRES_ID = "phases.poules.rencontres.id"
    PHASES_POULES_RENCONTRES_NUMERO = "phases.poules.rencontres.numero"
    PHASES_POULES_RENCONTRES_DATE = "phases.poules.rencontres.date_rencontre"

    # GameStats fields (nested in rencontres)
    PHASES_POULES_RENCONTRES_GSID_MATCH_ID = "phases.poules.rencontres.gsId.matchId"
    PHASES_POULES_RENCONTRES_GSID_CURRENT_STATUS = (
        "phases.poules.rencontres.gsId.currentStatus"
    )
    PHASES_POULES_RENCONTRES_GSID_CURRENT_PERIOD = (
        "phases.poules.rencontres.gsId.currentPeriod"
    )
    PHASES_POULES_RENCONTRES_GSID_SCORE_Q1_HOME = (
        "phases.poules.rencontres.gsId.score_q1_home"
    )
    PHASES_POULES_RENCONTRES_GSID_SCORE_Q2_HOME = (
        "phases.poules.rencontres.gsId.score_q2_home"
    )
    PHASES_POULES_RENCONTRES_GSID_SCORE_Q3_HOME = (
        "phases.poules.rencontres.gsId.score_q3_home"
    )
    PHASES_POULES_RENCONTRES_GSID_SCORE_Q4_HOME = (
        "phases.poules.rencontres.gsId.score_q4_home"
    )
    PHASES_POULES_RENCONTRES_GSID_SCORE_OT1_HOME = (
        "phases.poules.rencontres.gsId.score_ot1_home"
    )
    PHASES_POULES_RENCONTRES_GSID_SCORE_OT2_HOME = (
        "phases.poules.rencontres.gsId.score_ot2_home"
    )
    PHASES_POULES_RENCONTRES_GSID_SCORE_Q1_OUT = (
        "phases.poules.rencontres.gsId.score_q1_out"
    )
    PHASES_POULES_RENCONTRES_GSID_SCORE_Q2_OUT = (
        "phases.poules.rencontres.gsId.score_q2_out"
    )
    PHASES_POULES_RENCONTRES_GSID_SCORE_Q3_OUT = (
        "phases.poules.rencontres.gsId.score_q3_out"
    )
    PHASES_POULES_RENCONTRES_GSID_SCORE_Q4_OUT = (
        "phases.poules.rencontres.gsId.score_q4_out"
    )
    PHASES_POULES_RENCONTRES_GSID_SCORE_OT1_OUT = (
        "phases.poules.rencontres.gsId.score_ot1_out"
    )
    PHASES_POULES_RENCONTRES_GSID_SCORE_OT2_OUT = (
        "phases.poules.rencontres.gsId.score_ot2_out"
    )

    # Officiels fields (nested in rencontres)
    PHASES_POULES_RENCONTRES_OFFICIELS_ORDRE = (
        "phases.poules.rencontres.officiels.ordre"
    )
    PHASES_POULES_RENCONTRES_OFFICIELS_FONCTION_LIBELLE = (
        "phases.poules.rencontres.officiels.fonction.libelle"
    )
    PHASES_POULES_RENCONTRES_OFFICIELS_OFFICIEL_NOM = (
        "phases.poules.rencontres.officiels.officiel.nom"
    )
    PHASES_POULES_RENCONTRES_OFFICIELS_OFFICIEL_PRENOM = (
        "phases.poules.rencontres.officiels.officiel.prenom"
    )

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for competition queries based on real API usage."""
        return [
            # Basic competition fields
            cls.ID,
            cls.NOM,
            cls.SEXE,
            cls.CATEGORIE_CODE,
            cls.CATEGORIE_ORDRE,
            cls.SAISON,
            cls.CODE,
            cls.TYPE_COMPETITION,
            cls.LIVE_STAT,
            cls.COMPETITION_ORIGINE,
            cls.COMPETITION_ORIGINE_NOM,
            cls.TYPE_COMPETITION_GENERIQUE_LOGO_ID,
            cls.TYPE_COMPETITION_GENERIQUE_LOGO_GRADIENT_COLOR,
            cls.LOGO_ID,
            cls.LOGO_GRADIENT_COLOR,
            cls.POULES_ID,
            cls.POULES_NOM,
            cls.PUBLICATION_INTERNET,
            # Phases fields
            cls.PHASES_ID,
            cls.PHASES_NOM,
            cls.PHASES_LIVE_STAT,
            cls.PHASES_PHASE_CODE,
            # Phases > Poules fields
            cls.PHASES_POULES_ID,
            cls.PHASES_POULES_NOM,
            # Phases > Poules > Rencontres essential fields
            cls.PHASES_POULES_RENCONTRES_ID,
            cls.PHASES_POULES_RENCONTRES_NUMERO,
            cls.PHASES_POULES_RENCONTRES_NUMERO_JOURNEE,
            cls.PHASES_POULES_RENCONTRES_ID_POULE,
            cls.PHASES_POULES_RENCONTRES_COMPETITION_ID,
            cls.PHASES_POULES_RENCONTRES_RESULTAT_EQUIPE1,
            cls.PHASES_POULES_RENCONTRES_RESULTAT_EQUIPE2,
            cls.PHASES_POULES_RENCONTRES_JOUE,
            cls.PHASES_POULES_RENCONTRES_NOM_EQUIPE1,
            cls.PHASES_POULES_RENCONTRES_NOM_EQUIPE2,
            cls.PHASES_POULES_RENCONTRES_DATE,
            # Phases > Poules > Engagements
            cls.PHASES_POULES_ENGAGEMENTS_ID,
            cls.PHASES_POULES_ENGAGEMENTS_ID_ORGANISME_ID,
        ]

    @classmethod
    def get_basic_fields(cls) -> list[str]:
        """Get basic fields for simple competition queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.SEXE,
            cls.SAISON,
            cls.CODE,
        ]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields including all nested relationships."""
        return cls.get_default_fields() + [
            cls.PHASES_POULES_ID,
            cls.PHASES_POULES_NOM,
            cls.PHASES_POULES_RENCONTRES_NUMERO,
            cls.PHASES_POULES_RENCONTRES_DATE,
            "phases.poules.rencontres.nomEquipe1",
            "phases.poules.rencontres.nomEquipe2",
            "phases.poules.rencontres.resultatEquipe1",
            "phases.poules.rencontres.resultatEquipe2",
            "phases.poules.rencontres.joue",
            # GameStats fields for live match data
            cls.PHASES_POULES_RENCONTRES_GSID_MATCH_ID,
            cls.PHASES_POULES_RENCONTRES_GSID_CURRENT_STATUS,
            cls.PHASES_POULES_RENCONTRES_GSID_CURRENT_PERIOD,
            cls.PHASES_POULES_RENCONTRES_GSID_SCORE_Q1_HOME,
            cls.PHASES_POULES_RENCONTRES_GSID_SCORE_Q2_HOME,
            cls.PHASES_POULES_RENCONTRES_GSID_SCORE_Q3_HOME,
            cls.PHASES_POULES_RENCONTRES_GSID_SCORE_Q4_HOME,
            cls.PHASES_POULES_RENCONTRES_GSID_SCORE_OT1_HOME,
            cls.PHASES_POULES_RENCONTRES_GSID_SCORE_OT2_HOME,
            cls.PHASES_POULES_RENCONTRES_GSID_SCORE_Q1_OUT,
            cls.PHASES_POULES_RENCONTRES_GSID_SCORE_Q2_OUT,
            cls.PHASES_POULES_RENCONTRES_GSID_SCORE_Q3_OUT,
            cls.PHASES_POULES_RENCONTRES_GSID_SCORE_Q4_OUT,
            cls.PHASES_POULES_RENCONTRES_GSID_SCORE_OT1_OUT,
            cls.PHASES_POULES_RENCONTRES_GSID_SCORE_OT2_OUT,
            # Officiels fields
            cls.PHASES_POULES_RENCONTRES_OFFICIELS_ORDRE,
            cls.PHASES_POULES_RENCONTRES_OFFICIELS_FONCTION_LIBELLE,
            cls.PHASES_POULES_RENCONTRES_OFFICIELS_OFFICIEL_NOM,
            cls.PHASES_POULES_RENCONTRES_OFFICIELS_OFFICIEL_PRENOM,
        ]


class PouleFields:
    """Default fields for poule queries."""

    # Basic fields
    ID = "id"
    NOM = "nom"
    LOGO_ID = "logo.id"

    # ID Competition fields
    ID_COMPETITION_ORGANISATEUR_CODE = "id_competition.organisateur.code"
    ID_COMPETITION_ORGANISATEUR_NOM = "id_competition.organisateur.nom"
    ID_COMPETITION_ORGANISATEUR_SAISON = "id_competition.organisateur.saison"
    ID_COMPETITION_ORGANISATEUR_COMMUNE_DEPARTEMENT_CODE = (
        "id_competition.organisateur.commune.departement.code"
    )
    ID_COMPETITION_ORGANISATEUR_COMMUNE_DEPARTEMENT_CODE_INSEE = (
        "id_competition.organisateur.commune.departement.codeInsee"
    )
    ID_COMPETITION_ORGANISATEUR_COMMUNE_DEPARTEMENT_LIBELLE = (
        "id_competition.organisateur.commune.departement.libelle"
    )

    # Rencontres fields
    RENCONTRES_ID = "rencontres.id"
    RENCONTRES_NUMERO = "rencontres.numero"
    RENCONTRES_NUMERO_JOURNEE = "rencontres.numeroJournee"
    RENCONTRES_ID_POULE = "rencontres.idPoule"
    RENCONTRES_COMPETITION_ID = "rencontres.competitionId"
    RENCONTRES_RESULTAT_EQUIPE1 = "rencontres.resultatEquipe1"
    RENCONTRES_RESULTAT_EQUIPE2 = "rencontres.resultatEquipe2"
    RENCONTRES_JOUE = "rencontres.joue"
    RENCONTRES_NOM_EQUIPE1 = "rencontres.nomEquipe1"
    RENCONTRES_NOM_EQUIPE2 = "rencontres.nomEquipe2"
    RENCONTRES_DATE_RENCONTRE = "rencontres.date_rencontre"

    # GameStats fields (live match data)
    RENCONTRES_GSID_MATCH_ID = "rencontres.gsId.matchId"
    RENCONTRES_GSID_CURRENT_STATUS = "rencontres.gsId.currentStatus"
    RENCONTRES_GSID_CURRENT_PERIOD = "rencontres.gsId.currentPeriod"
    RENCONTRES_GSID_SCORE_Q1_HOME = "rencontres.gsId.score_q1_home"
    RENCONTRES_GSID_SCORE_Q2_HOME = "rencontres.gsId.score_q2_home"
    RENCONTRES_GSID_SCORE_Q3_HOME = "rencontres.gsId.score_q3_home"
    RENCONTRES_GSID_SCORE_Q4_HOME = "rencontres.gsId.score_q4_home"
    RENCONTRES_GSID_SCORE_OT1_HOME = "rencontres.gsId.score_ot1_home"
    RENCONTRES_GSID_SCORE_OT2_HOME = "rencontres.gsId.score_ot2_home"
    RENCONTRES_GSID_SCORE_Q1_OUT = "rencontres.gsId.score_q1_out"
    RENCONTRES_GSID_SCORE_Q2_OUT = "rencontres.gsId.score_q2_out"
    RENCONTRES_GSID_SCORE_Q3_OUT = "rencontres.gsId.score_q3_out"
    RENCONTRES_GSID_SCORE_Q4_OUT = "rencontres.gsId.score_q4_out"
    RENCONTRES_GSID_SCORE_OT1_OUT = "rencontres.gsId.score_ot1_out"
    RENCONTRES_GSID_SCORE_OT2_OUT = "rencontres.gsId.score_ot2_out"

    # Classements fields
    CLASSEMENTS_ID = "classements.id"
    CLASSEMENTS_ID_ENGAGEMENT_ID = "classements.idEngagement.id"
    CLASSEMENTS_ID_ENGAGEMENT_NOM = "classements.idEngagement.nom"
    CLASSEMENTS_ID_ENGAGEMENT_NOM_USUEL = "classements.idEngagement.nomUsuel"
    CLASSEMENTS_ID_ENGAGEMENT_CODE_ABREGE = "classements.idEngagement.codeAbrege"
    CLASSEMENTS_ID_ENGAGEMENT_NUMERO_EQU = "classements.idEngagement.numeroEqu"
    CLASSEMENTS_ID_ENGAGEMENT_LOGO_ID = "classements.idEngagement.logo.id"
    CLASSEMENTS_ID_ENGAGEMENT_LOGO_GRADIENT = (
        "classements.idEngagement.logo.gradient_color"
    )
    CLASSEMENTS_ORGANISME_ID = "classements.organisme.id"
    CLASSEMENTS_ORGANISME_NOM = "classements.organisme.nom"
    CLASSEMENTS_ORGANISME_LOGO_ID = "classements.organisme.logo.id"
    CLASSEMENTS_ORGANISME_NOM_SIMPLE = "classements.organisme_nom"
    CLASSEMENTS_ID_COMPETITION = "classements.idCompetition"
    CLASSEMENTS_ID_POULE = "classements.idPoule"
    CLASSEMENTS_ID_POULE_ID = "classements.idPoule.id"
    CLASSEMENTS_POSITION = "classements.position"
    CLASSEMENTS_POINTS = "classements.points"
    CLASSEMENTS_MATCH_JOUES = "classements.matchJoues"
    CLASSEMENTS_GAGNES = "classements.gagnes"
    CLASSEMENTS_PERDUS = "classements.perdus"
    CLASSEMENTS_NULS = "classements.nuls"
    CLASSEMENTS_NOMBRE_FORFAITS = "classements.nombreForfaits"
    CLASSEMENTS_NOMBRE_DEFAUTS = "classements.nombreDefauts"
    CLASSEMENTS_PANIERS_MARQUES = "classements.paniersMarques"
    CLASSEMENTS_PANIERS_ENCAISSES = "classements.paniersEncaisses"
    CLASSEMENTS_DIFFERENCE = "classements.difference"
    CLASSEMENTS_QUOTIENT = "classements.quotient"
    CLASSEMENTS_POINT_INITIAUX = "classements.pointInitiaux"
    CLASSEMENTS_PENALITES_ARBITRAGE = "classements.penalitesArbitrage"
    CLASSEMENTS_PENALITES_ENTRAINEUR = "classements.penalitesEntraineur"
    CLASSEMENTS_PENALITES_DIVERSES = "classements.penalitesDiverses"
    CLASSEMENTS_HORS_CLASSEMENT = "classements.horsClassement"

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for poule queries based on real API usage."""
        return [
            # Basic fields
            cls.ID,
            cls.NOM,
            cls.LOGO_ID,
            # ID Competition fields
            cls.ID_COMPETITION_ORGANISATEUR_CODE,
            cls.ID_COMPETITION_ORGANISATEUR_NOM,
            cls.ID_COMPETITION_ORGANISATEUR_SAISON,
            cls.ID_COMPETITION_ORGANISATEUR_COMMUNE_DEPARTEMENT_CODE,
            cls.ID_COMPETITION_ORGANISATEUR_COMMUNE_DEPARTEMENT_CODE_INSEE,
            cls.ID_COMPETITION_ORGANISATEUR_COMMUNE_DEPARTEMENT_LIBELLE,
            # Rencontres - champs essentiels
            cls.RENCONTRES_ID,
            cls.RENCONTRES_NUMERO,
            cls.RENCONTRES_NUMERO_JOURNEE,
            cls.RENCONTRES_ID_POULE,
            "rencontres.competitionId.id",
            "rencontres.competitionId.competition_origine",
            "rencontres.idOrganismeEquipe1.logo.id",
            "rencontres.idOrganismeEquipe1.id",
            "rencontres.idOrganismeEquipe2.logo.id",
            "rencontres.idOrganismeEquipe2.id",
            cls.RENCONTRES_RESULTAT_EQUIPE1,
            cls.RENCONTRES_RESULTAT_EQUIPE2,
            cls.RENCONTRES_JOUE,
            cls.RENCONTRES_NOM_EQUIPE1,
            cls.RENCONTRES_NOM_EQUIPE2,
            cls.RENCONTRES_GSID_MATCH_ID,
            cls.RENCONTRES_GSID_CURRENT_STATUS,
            cls.RENCONTRES_GSID_SCORE_Q1_HOME,
            cls.RENCONTRES_GSID_SCORE_Q2_HOME,
            cls.RENCONTRES_GSID_SCORE_Q3_HOME,
            cls.RENCONTRES_GSID_SCORE_Q4_HOME,
            cls.RENCONTRES_GSID_SCORE_OT1_HOME,
            cls.RENCONTRES_GSID_SCORE_OT2_HOME,
            cls.RENCONTRES_GSID_SCORE_Q1_OUT,
            cls.RENCONTRES_GSID_SCORE_Q2_OUT,
            cls.RENCONTRES_GSID_SCORE_Q3_OUT,
            cls.RENCONTRES_GSID_SCORE_Q4_OUT,
            cls.RENCONTRES_GSID_SCORE_OT1_OUT,
            cls.RENCONTRES_GSID_SCORE_OT2_OUT,
            cls.RENCONTRES_GSID_CURRENT_PERIOD,
            "rencontres.idEngagementEquipe1.id",
            "rencontres.idEngagementEquipe1.nom",
            "rencontres.idEngagementEquipe1.nomOfficiel",
            "rencontres.idEngagementEquipe1.nomUsuel",
            "rencontres.idEngagementEquipe1.logo.id",
            "rencontres.idEngagementEquipe1.logo.gradient_color",
            "rencontres.idEngagementEquipe1.codeAbrege",
            "rencontres.idEngagementEquipe1.idOrganisme.code",
            "rencontres.idEngagementEquipe1.numeroEquipe",
            "rencontres.idEngagementEquipe2.id",
            "rencontres.idEngagementEquipe2.nom",
            "rencontres.idEngagementEquipe2.nomOfficiel",
            "rencontres.idEngagementEquipe2.nomUsuel",
            "rencontres.idEngagementEquipe2.logo.id",
            "rencontres.idEngagementEquipe2.logo.gradient_color",
            "rencontres.idEngagementEquipe2.codeAbrege",
            "rencontres.idEngagementEquipe2.idOrganisme.code",
            "rencontres.idEngagementEquipe2.numeroEquipe",
            "rencontres.salle.id",
            "rencontres.salle.numero",
            "rencontres.salle.libelle",
            "rencontres.salle.libelle2",
            "rencontres.salle.adresse",
            "rencontres.salle.adresseComplement",
            "rencontres.salle.commune.codePostal",
            "rencontres.salle.commune.libelle",
            "rencontres.salle.cartographie.latitude",
            "rencontres.salle.cartographie.longitude",
            cls.RENCONTRES_DATE_RENCONTRE,
            "rencontres.officiels.ordre",
            "rencontres.officiels.fonction.libelle",
            "rencontres.officiels.officiel.nom",
            "rencontres.officiels.officiel.prenom",
            # Classements - tous les champs
            cls.CLASSEMENTS_ID,
            cls.CLASSEMENTS_ID_ENGAGEMENT_NOM,
            cls.CLASSEMENTS_ID_ENGAGEMENT_NOM_USUEL,
            cls.CLASSEMENTS_ID_ENGAGEMENT_ID,
            cls.CLASSEMENTS_ID_ENGAGEMENT_LOGO_ID,
            cls.CLASSEMENTS_ID_ENGAGEMENT_LOGO_GRADIENT,
            cls.CLASSEMENTS_ID_ENGAGEMENT_CODE_ABREGE,
            "classements.idEngagement.numeroEquipe",
            cls.CLASSEMENTS_ORGANISME_ID,
            cls.CLASSEMENTS_ORGANISME_NOM,
            cls.CLASSEMENTS_ORGANISME_LOGO_ID,
            cls.CLASSEMENTS_ORGANISME_NOM_SIMPLE,
            cls.CLASSEMENTS_ID_COMPETITION,
            cls.CLASSEMENTS_ID_POULE,
            cls.CLASSEMENTS_ID_POULE_ID,
            cls.CLASSEMENTS_MATCH_JOUES,
            cls.CLASSEMENTS_POINTS,
            cls.CLASSEMENTS_POSITION,
            cls.CLASSEMENTS_GAGNES,
            cls.CLASSEMENTS_PERDUS,
            cls.CLASSEMENTS_NULS,
            cls.CLASSEMENTS_POINT_INITIAUX,
            cls.CLASSEMENTS_PENALITES_ARBITRAGE,
            cls.CLASSEMENTS_PENALITES_ENTRAINEUR,
            cls.CLASSEMENTS_PENALITES_DIVERSES,
            cls.CLASSEMENTS_NOMBRE_FORFAITS,
            cls.CLASSEMENTS_NOMBRE_DEFAUTS,
            cls.CLASSEMENTS_PANIERS_MARQUES,
            cls.CLASSEMENTS_PANIERS_ENCAISSES,
            cls.CLASSEMENTS_DIFFERENCE,
            cls.CLASSEMENTS_QUOTIENT,
            cls.CLASSEMENTS_HORS_CLASSEMENT,
        ]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields including all nested relationships."""
        return cls.get_default_fields() + [
            cls.CLASSEMENTS_ORGANISME_ID,
            cls.CLASSEMENTS_ORGANISME_NOM,
            cls.CLASSEMENTS_ORGANISME_LOGO_ID,
            cls.CLASSEMENTS_ORGANISME_NOM_SIMPLE,
            cls.CLASSEMENTS_ID_COMPETITION,
            cls.CLASSEMENTS_ID_POULE,
            cls.CLASSEMENTS_ID_POULE_ID,
        ]

    @classmethod
    def get_basic_fields(cls) -> list[str]:
        """Get basic fields for simple poule queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.RENCONTRES_ID,
        ]


class SaisonFields:
    """Default fields for saison queries."""

    # Basic fields
    ID = "id"
    NOM = "nom"
    ACTIF = "actif"
    DEBUT = "debut"
    FIN = "fin"

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for saison queries."""
        return [cls.ID]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields for saison queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.ACTIF,
            cls.DEBUT,
            cls.FIN,
        ]


# Enum for common field sets
class FieldSet(Enum):
    """Enum for different field sets."""

    BASIC = "basic"
    DEFAULT = "default"
    DETAILED = "detailed"
    MINIMAL = "minimal"


class QueryFieldsManager:
    """Manager class for handling query fields across different entity types."""

    @staticmethod
    def get_organisme_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get organisme fields based on field set."""
        if field_set == FieldSet.BASIC:
            return OrganismeFields.get_basic_fields()
        elif field_set == FieldSet.DETAILED:
            return OrganismeFields.get_detailed_fields()
        else:
            return OrganismeFields.get_default_fields()

    @staticmethod
    def get_competition_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get competition fields based on field set."""
        if field_set == FieldSet.BASIC:
            return CompetitionFields.get_basic_fields()
        elif field_set == FieldSet.DETAILED:
            return CompetitionFields.get_detailed_fields()
        else:
            return CompetitionFields.get_default_fields()

    @staticmethod
    def get_poule_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get poule fields based on field set."""
        if field_set == FieldSet.BASIC:
            return PouleFields.get_basic_fields()
        elif field_set == FieldSet.DETAILED:
            return PouleFields.get_detailed_fields()
        else:
            return PouleFields.get_default_fields()

    @staticmethod
    def get_saison_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get saison fields based on field set."""
        if field_set == FieldSet.DETAILED:
            return SaisonFields.get_detailed_fields()
        else:
            return SaisonFields.get_default_fields()
