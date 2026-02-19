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
    COMMUNE = "commune"
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
            cls.ADRESSE1,
            cls.ADRESSE2,
            cls.TELEPHONE_DOMICILE,
            cls.TELEPHONE_TRAVAIL,
            cls.COMMUNE,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
