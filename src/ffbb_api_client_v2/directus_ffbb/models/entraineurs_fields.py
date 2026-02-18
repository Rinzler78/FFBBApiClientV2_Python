from .query_fields_manager import QueryFieldsManager


class EntraineursFields(QueryFieldsManager):
    """Fields for entraineurs queries."""

    ID_LICENCE = "idLicence"
    NOM = "nom"
    PRENOM = "prenom"
    ADRESSE1 = "adresse1"
    ADRESSE2 = "adresse2"
    EMAIL = "email"
    TELEPHONE_DOMICILE = "telephoneDomicile"
    TELEPHONE_PORTABLE = "telephonePortable"
    TELEPHONE_TRAVAIL = "telephoneTravail"
    COMMUNE_ID = "commune.id"
    COMMUNE_CODE_POSTAL = "commune.codePostal"
    COMMUNE_LIBELLE = "commune.libelle"
    COMMUNE_DEPARTEMENT = "commune.departement"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_fields(cls) -> list[str]:
        """Return the complete list of fields for entraineurs."""
        return [
            cls.ID_LICENCE,
            cls.NOM,
            cls.PRENOM,
            cls.EMAIL,
            cls.TELEPHONE_PORTABLE,
            cls.COMMUNE_CODE_POSTAL,
            cls.COMMUNE_LIBELLE,
            cls.ADRESSE1,
            cls.ADRESSE2,
            cls.TELEPHONE_DOMICILE,
            cls.TELEPHONE_TRAVAIL,
            cls.COMMUNE_ID,
            cls.COMMUNE_DEPARTEMENT,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
