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
    COMMUNE_ID = "commune.id"
    COMMUNE_CODE_POSTAL = "commune.codePostal"
    COMMUNE_LIBELLE = "commune.libelle"
    COMMUNE_DEPARTEMENT = "commune.departement"
    CARTOGRAPHIE_LATITUDE = "cartographie.latitude"
    CARTOGRAPHIE_LONGITUDE = "cartographie.longitude"
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
            cls.COMMUNE_CODE_POSTAL,
            cls.COMMUNE_LIBELLE,
            cls.CARTOGRAPHIE_LATITUDE,
            cls.CARTOGRAPHIE_LONGITUDE,
            cls.COMMUNE_ID,
            cls.COMMUNE_DEPARTEMENT,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
