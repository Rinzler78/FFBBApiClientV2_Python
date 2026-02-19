from .query_fields_manager import QueryFieldsManager


class SallesFields(QueryFieldsManager):
    """Fields for salles queries."""

    ID = "id"
    LIBELLE = "libelle"
    LIBELLE2 = "libelle2"
    ADRESSE = "adresse"
    ADRESSE_COMPLEMENT = "adresseComplement"
    NUMERO = "numero"
    TELEPHONE = "telephone"
    MAIL = "mail"
    CAPACITE_SPECTATEUR = "capaciteSpectateur"
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
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_fields(cls) -> list[str]:
        """Return the complete list of fields for salles."""
        return [
            cls.ID,
            cls.LIBELLE,
            cls.LIBELLE2,
            cls.ADRESSE,
            cls.ADRESSE_COMPLEMENT,
            cls.NUMERO,
            cls.TELEPHONE,
            cls.MAIL,
            cls.CAPACITE_SPECTATEUR,
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
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
