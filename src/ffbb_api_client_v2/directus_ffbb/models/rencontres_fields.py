from .query_fields_manager import QueryFieldsManager


class RencontresFields(QueryFieldsManager):
    """Fields for rencontres queries."""

    ID = "id"
    DATE = "date"
    DATE_RENCONTRE = "date_rencontre"
    HORAIRE = "horaire"
    NUMERO = "numero"
    NUMERO_JOURNEE = "numeroJournee"
    NOM_EQUIPE1 = "nomEquipe1"
    NOM_EQUIPE2 = "nomEquipe2"
    RESULTAT_EQUIPE1 = "resultatEquipe1"
    RESULTAT_EQUIPE2 = "resultatEquipe2"
    JOUE = "joue"
    ETAT = "etat"
    PRATIQUE = "pratique"
    STATUS = "status"
    VALIDEE = "validee"
    FORFAIT_EQUIPE1 = "forfaitEquipe1"
    FORFAIT_EQUIPE2 = "forfaitEquipe2"
    DEFAUT_EQUIPE1 = "defautEquipe1"
    DEFAUT_EQUIPE2 = "defautEquipe2"
    PENALITE_EQUIPE1 = "penaliteEquipe1"
    PENALITE_EQUIPE2 = "penaliteEquipe2"
    HANDICAP1 = "handicap1"
    HANDICAP2 = "handicap2"
    REMISE = "remise"
    DATE_SAISIE_RESULTAT = "dateSaisieResultat"
    CREATION = "creation"
    MODIFICATION = "modification"
    TO_UPDATE = "toUpdate"
    UNIQUE_KEY = "uniqueKey"
    URL_COMPETITION = "url_competition"
    REMATCH_VIDEOS = "rematch_videos"
    COMPETITION_ID = "competitionId"
    ID_ENGAGEMENT_EQUIPE1 = "idEngagementEquipe1"
    ID_ENGAGEMENT_EQUIPE2 = "idEngagementEquipe2"
    ID_ORGANISME_EQUIPE1 = "idOrganismeEquipe1"
    ID_ORGANISME_EQUIPE2 = "idOrganismeEquipe2"
    ID_POULE = "idPoule"
    SAISON = "saison"
    SALLE = "salle"
    OFFICIELS = "officiels"
    GS_ID = "gsId"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_fields(cls) -> list[str]:
        """Return the complete list of fields for rencontres."""
        return [
            cls.ID,
            cls.DATE,
            cls.DATE_RENCONTRE,
            cls.HORAIRE,
            cls.NUMERO,
            cls.NUMERO_JOURNEE,
            cls.NOM_EQUIPE1,
            cls.NOM_EQUIPE2,
            cls.RESULTAT_EQUIPE1,
            cls.RESULTAT_EQUIPE2,
            cls.JOUE,
            cls.ETAT,
            cls.PRATIQUE,
            cls.STATUS,
            cls.VALIDEE,
            cls.FORFAIT_EQUIPE1,
            cls.FORFAIT_EQUIPE2,
            cls.DEFAUT_EQUIPE1,
            cls.DEFAUT_EQUIPE2,
            cls.PENALITE_EQUIPE1,
            cls.PENALITE_EQUIPE2,
            cls.HANDICAP1,
            cls.HANDICAP2,
            cls.REMISE,
            cls.DATE_SAISIE_RESULTAT,
            cls.CREATION,
            cls.MODIFICATION,
            cls.TO_UPDATE,
            cls.UNIQUE_KEY,
            cls.URL_COMPETITION,
            cls.REMATCH_VIDEOS,
            cls.COMPETITION_ID,
            cls.ID_ENGAGEMENT_EQUIPE1,
            cls.ID_ENGAGEMENT_EQUIPE2,
            cls.ID_ORGANISME_EQUIPE1,
            cls.ID_ORGANISME_EQUIPE2,
            cls.ID_POULE,
            cls.SAISON,
            cls.SALLE,
            cls.OFFICIELS,
            cls.GS_ID,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
