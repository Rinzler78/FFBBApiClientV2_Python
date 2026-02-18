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

    # idOrganismeEquipe logo fields
    PHASES_POULES_RENCONTRES_ID_ORGANISME_EQUIPE1_LOGO_ID = (
        "phases.poules.rencontres.idOrganismeEquipe1.logo.id"
    )
    PHASES_POULES_RENCONTRES_ID_ORGANISME_EQUIPE2_LOGO_ID = (
        "phases.poules.rencontres.idOrganismeEquipe2.logo.id"
    )

    # idEngagementEquipe1 fields (model: Idengagementequipe1Model)
    PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE1_ID = (
        "phases.poules.rencontres.idEngagementEquipe1.id"
    )
    PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE1_NOM = (
        "phases.poules.rencontres.idEngagementEquipe1.nom"
    )
    PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE1_NOM_OFFICIEL = (
        "phases.poules.rencontres.idEngagementEquipe1.nomOfficiel"
    )
    PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE1_NOM_USUEL = (
        "phases.poules.rencontres.idEngagementEquipe1.nomUsuel"
    )
    PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE1_CODE_ABREGE = (
        "phases.poules.rencontres.idEngagementEquipe1.codeAbrege"
    )
    PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE1_LOGO = (
        "phases.poules.rencontres.idEngagementEquipe1.logo"
    )

    # idEngagementEquipe2 fields (model: Idengagementequipe2Model)
    PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE2_ID = (
        "phases.poules.rencontres.idEngagementEquipe2.id"
    )
    PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE2_NOM = (
        "phases.poules.rencontres.idEngagementEquipe2.nom"
    )
    PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE2_NOM_OFFICIEL = (
        "phases.poules.rencontres.idEngagementEquipe2.nomOfficiel"
    )
    PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE2_NOM_USUEL = (
        "phases.poules.rencontres.idEngagementEquipe2.nomUsuel"
    )
    PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE2_CODE_ABREGE = (
        "phases.poules.rencontres.idEngagementEquipe2.codeAbrege"
    )
    PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE2_LOGO = (
        "phases.poules.rencontres.idEngagementEquipe2.logo"
    )

    # Salle in rencontres (model: SalleModel)
    PHASES_POULES_RENCONTRES_SALLE_ID = "phases.poules.rencontres.salle.id"
    PHASES_POULES_RENCONTRES_SALLE_NUMERO = "phases.poules.rencontres.salle.numero"
    PHASES_POULES_RENCONTRES_SALLE_LIBELLE = "phases.poules.rencontres.salle.libelle"
    PHASES_POULES_RENCONTRES_SALLE_LIBELLE2 = "phases.poules.rencontres.salle.libelle2"
    PHASES_POULES_RENCONTRES_SALLE_ADRESSE = "phases.poules.rencontres.salle.adresse"
    PHASES_POULES_RENCONTRES_SALLE_ADRESSE_COMPLEMENT = (
        "phases.poules.rencontres.salle.adresseComplement"
    )
    PHASES_POULES_RENCONTRES_SALLE_COMMUNE_CP = (
        "phases.poules.rencontres.salle.commune.codePostal"
    )
    PHASES_POULES_RENCONTRES_SALLE_COMMUNE_LIBELLE = (
        "phases.poules.rencontres.salle.commune.libelle"
    )
    PHASES_POULES_RENCONTRES_SALLE_CARTO_LAT = (
        "phases.poules.rencontres.salle.cartographie.latitude"
    )
    PHASES_POULES_RENCONTRES_SALLE_CARTO_LNG = (
        "phases.poules.rencontres.salle.cartographie.longitude"
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
            # idOrganismeEquipe logo
            cls.PHASES_POULES_RENCONTRES_ID_ORGANISME_EQUIPE1_LOGO_ID,
            cls.PHASES_POULES_RENCONTRES_ID_ORGANISME_EQUIPE2_LOGO_ID,
            # idEngagementEquipe1
            cls.PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE1_ID,
            cls.PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE1_NOM,
            cls.PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE1_NOM_OFFICIEL,
            cls.PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE1_NOM_USUEL,
            cls.PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE1_CODE_ABREGE,
            cls.PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE1_LOGO,
            # idEngagementEquipe2
            cls.PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE2_ID,
            cls.PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE2_NOM,
            cls.PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE2_NOM_OFFICIEL,
            cls.PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE2_NOM_USUEL,
            cls.PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE2_CODE_ABREGE,
            cls.PHASES_POULES_RENCONTRES_ID_ENGAGEMENT_EQUIPE2_LOGO,
            # Salle in rencontres
            cls.PHASES_POULES_RENCONTRES_SALLE_ID,
            cls.PHASES_POULES_RENCONTRES_SALLE_NUMERO,
            cls.PHASES_POULES_RENCONTRES_SALLE_LIBELLE,
            cls.PHASES_POULES_RENCONTRES_SALLE_LIBELLE2,
            cls.PHASES_POULES_RENCONTRES_SALLE_ADRESSE,
            cls.PHASES_POULES_RENCONTRES_SALLE_ADRESSE_COMPLEMENT,
            cls.PHASES_POULES_RENCONTRES_SALLE_COMMUNE_CP,
            cls.PHASES_POULES_RENCONTRES_SALLE_COMMUNE_LIBELLE,
            cls.PHASES_POULES_RENCONTRES_SALLE_CARTO_LAT,
            cls.PHASES_POULES_RENCONTRES_SALLE_CARTO_LNG,
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
        """Get detailed fields (all fields now included in default)."""
        return cls.get_default_fields()

    WILDCARD = "*.*.*.*.*"
