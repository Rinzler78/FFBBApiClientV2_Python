class TournoisFields:
    """Default fields for tournois queries."""

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
    COMMUNE_CODE_POSTAL = "commune.codePostal"
    COMMUNE_LIBELLE = "commune.libelle"
    COMMUNE_DEPARTEMENT = "commune.departement"
    CARTOGRAPHIE_LATITUDE = "cartographie.latitude"
    CARTOGRAPHIE_LONGITUDE = "cartographie.longitude"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for tournois queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.CODE,
            cls.SEXE,
            cls.DEBUT,
            cls.FIN,
            cls.DESCRIPTION,
            cls.ADRESSE,
            cls.MAIL_ORGANISATEUR,
            cls.NOM_ORGANISATEUR,
            cls.TELEPHONE_ORGANISATEUR,
            cls.COMMUNE_CODE_POSTAL,
            cls.COMMUNE_LIBELLE,
            cls.CARTOGRAPHIE_LATITUDE,
            cls.CARTOGRAPHIE_LONGITUDE,
        ]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields for tournois queries."""
        return cls.get_default_fields() + [
            cls.ADRESSE_COMPLEMENT,
            cls.URL_ORGANISATEUR,
            cls.SITE_CHOISI,
            cls.NB_PARTICIPANT_PREVU,
            cls.TARIF_ORGANISATEUR,
            cls.AGE_MIN,
            cls.AGE_MAX,
            cls.TOURNOI_TYPE,
            cls.TOURNOI_TYPES_3X3,
            cls.COMMUNE_DEPARTEMENT,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]

    WILDCARD = "*.*"
