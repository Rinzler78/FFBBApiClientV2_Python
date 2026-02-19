from .query_fields_manager import QueryFieldsManager


class PratiquesFields(QueryFieldsManager):
    """Fields for pratiques queries."""

    ID = "id"
    TITRE = "titre"
    TYPE = "type"
    LABEL = "label"
    DESCRIPTION = "description"
    CODE = "code"
    ADRESSE = "adresse"
    EMAIL = "email"
    TELEPHONE = "telephone"
    DATE_DEBUT = "date_debut"
    DATE_FIN = "date_fin"
    HORAIRES_SEANCES = "horaires_seances"
    JOURS = "jours"
    NOM_STRUCTURE = "nom_structure"
    ADRESSE_STRUCTURE = "adresse_structure"
    MAIL_STRUCTURE = "mail_structure"
    NOM_SALLE = "nom_salle"
    ADRESSE_SALLE = "adresse_salle"
    CP_SALLE = "cp_salle"
    VILLE_SALLE = "ville_salle"
    ACTION = "action"
    AFFICHE = "affiche"
    AFFICHE_EXTERNE = "affiche_externe"
    ASSURANCE = "assurance"
    DATE_DEMANDE = "date_demande"
    DATE_INSCRIPTION = "date_inscription"
    ENGAGEMENT = "engagement"
    FACEBOOK = "facebook"
    INSCRIPTIONS = "inscriptions"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    MAIL_DEMANDEUR = "mail_demandeur"
    NOM_DEMANDEUR = "nom_demandeur"
    NOMBRE_PERSONNES = "nombre_personnes"
    NOMBRE_SEANCES = "nombre_seances"
    OBJECTIF = "objectif"
    PRENOM_DEMANDEUR = "prenom_demandeur"
    PUBLIC = "public"
    SITE_WEB = "site_web"
    TWITTER = "twitter"
    CARTOGRAPHIE_LATITUDE = "cartographie.latitude"
    CARTOGRAPHIE_LONGITUDE = "cartographie.longitude"
    CARTOGRAPHIE_CODE_POSTAL = "cartographie.codePostal"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_fields(cls) -> list[str]:
        """Return the complete list of fields for pratiques."""
        return [
            cls.ID,
            cls.TITRE,
            cls.TYPE,
            cls.LABEL,
            cls.DESCRIPTION,
            cls.CODE,
            cls.ADRESSE,
            cls.EMAIL,
            cls.TELEPHONE,
            cls.DATE_DEBUT,
            cls.DATE_FIN,
            cls.HORAIRES_SEANCES,
            cls.JOURS,
            cls.NOM_STRUCTURE,
            cls.ADRESSE_STRUCTURE,
            cls.MAIL_STRUCTURE,
            cls.NOM_SALLE,
            cls.ADRESSE_SALLE,
            cls.CP_SALLE,
            cls.VILLE_SALLE,
            cls.ACTION,
            cls.AFFICHE,
            cls.AFFICHE_EXTERNE,
            cls.ASSURANCE,
            cls.DATE_DEMANDE,
            cls.DATE_INSCRIPTION,
            cls.ENGAGEMENT,
            cls.FACEBOOK,
            cls.INSCRIPTIONS,
            cls.LATITUDE,
            cls.LONGITUDE,
            cls.MAIL_DEMANDEUR,
            cls.NOM_DEMANDEUR,
            cls.NOMBRE_PERSONNES,
            cls.NOMBRE_SEANCES,
            cls.OBJECTIF,
            cls.PRENOM_DEMANDEUR,
            cls.PUBLIC,
            cls.SITE_WEB,
            cls.TWITTER,
            cls.CARTOGRAPHIE_LATITUDE,
            cls.CARTOGRAPHIE_LONGITUDE,
            cls.CARTOGRAPHIE_CODE_POSTAL,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
