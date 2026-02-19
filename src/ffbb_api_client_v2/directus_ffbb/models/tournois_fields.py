from .query_fields_manager import QueryFieldsManager


class TournoisFields(QueryFieldsManager):
    """Fields for tournois queries."""

    ID = "id"
    NOM = "nom"
    CODE = "code"
    SEXE = "sexe"
    DEBUT = "debut"
    FIN = "fin"
    DESCRIPTION = "description"
    ADRESSE = "adresse"
    ADRESSE_COMPLEMENT = "adresseComplement"
    MAIL_ORGANISATEUR = "mailOrganisateur"
    NOM_ORGANISATEUR = "nomOrganisateur"
    TELEPHONE_ORGANISATEUR = "telephoneOrganisateur"
    URL_ORGANISATEUR = "urlOrganisateur"
    SITE_CHOISI = "siteChoisi"
    NB_PARTICIPANT_PREVU = "nbParticipantPrevu"
    TARIF_ORGANISATEUR = "tarifOrganisateur"
    AGE_MIN = "ageMin"
    AGE_MAX = "ageMax"
    TOURNOI_TYPE = "tournoiType"
    TOURNOI_TYPES_3X3 = "tournoiTypes3x3"
    COMMUNE = "commune"
    CARTOGRAPHIE_ID = "cartographie.id"
    CARTOGRAPHIE_LATITUDE = "cartographie.latitude"
    CARTOGRAPHIE_LONGITUDE = "cartographie.longitude"
    CARTOGRAPHIE_ADRESSE = "cartographie.adresse"
    CARTOGRAPHIE_CODE_POSTAL = "cartographie.codePostal"
    CARTOGRAPHIE_COORDONNEES = "cartographie.coordonnees"
    CARTOGRAPHIE_COORDONNEES_COORDINATES = "cartographie.coordonnees.coordinates"
    CARTOGRAPHIE_COORDONNEES_TYPE = "cartographie.coordonnees.type"
    CARTOGRAPHIE_STATUS = "cartographie.status"
    CARTOGRAPHIE_TITLE = "cartographie.title"
    CARTOGRAPHIE_VILLE = "cartographie.ville"
    DOCUMENT_FLYER = "document_flyer"
    CATEGORIE_CHAMPIONNAT_3X3_ID = "categorieChampionnat3x3Id"
    CATEGORIE_CHAMPIONNAT_3X3_LIBELLE = "categorieChampionnat3x3Libelle"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_fields(cls) -> list[str]:
        """Return the complete list of fields for tournois."""
        return [
            cls.ID,
            cls.NOM,
            cls.CODE,
            cls.SEXE,
            cls.DEBUT,
            cls.FIN,
            cls.DESCRIPTION,
            cls.ADRESSE,
            cls.ADRESSE_COMPLEMENT,
            cls.MAIL_ORGANISATEUR,
            cls.NOM_ORGANISATEUR,
            cls.TELEPHONE_ORGANISATEUR,
            cls.URL_ORGANISATEUR,
            cls.SITE_CHOISI,
            cls.NB_PARTICIPANT_PREVU,
            cls.TARIF_ORGANISATEUR,
            cls.AGE_MIN,
            cls.AGE_MAX,
            cls.TOURNOI_TYPE,
            cls.TOURNOI_TYPES_3X3,
            cls.COMMUNE,
            cls.CARTOGRAPHIE_ID,
            cls.CARTOGRAPHIE_LATITUDE,
            cls.CARTOGRAPHIE_LONGITUDE,
            cls.CARTOGRAPHIE_ADRESSE,
            cls.CARTOGRAPHIE_CODE_POSTAL,
            cls.CARTOGRAPHIE_COORDONNEES,
            cls.CARTOGRAPHIE_COORDONNEES_COORDINATES,
            cls.CARTOGRAPHIE_COORDONNEES_TYPE,
            cls.CARTOGRAPHIE_STATUS,
            cls.CARTOGRAPHIE_TITLE,
            cls.CARTOGRAPHIE_VILLE,
            cls.DOCUMENT_FLYER,
            cls.CATEGORIE_CHAMPIONNAT_3X3_ID,
            cls.CATEGORIE_CHAMPIONNAT_3X3_LIBELLE,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
