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
        """Get detailed fields including relation-level constants."""
        return cls.get_default_fields() + [
            cls.RENCONTRES_COMPETITION_ID,
            cls.CLASSEMENTS_ID_ENGAGEMENT_NUMERO_EQU,
        ]

    @classmethod
    def get_basic_fields(cls) -> list[str]:
        """Get basic fields for simple poule queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.RENCONTRES_ID,
        ]

    WILDCARD = "*.*.*"
