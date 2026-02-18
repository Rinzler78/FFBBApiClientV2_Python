from .query_fields_manager import QueryFieldsManager


class CommunesFields(QueryFieldsManager):
    """Fields for communes queries."""

    ID = "id"
    CODE_INSEE = "codeInsee"
    CODE_POSTAL = "codePostal"
    DEPARTEMENT = "departement"
    LIBELLE = "libelle"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_fields(cls) -> list[str]:
        """Return the complete list of fields for communes."""
        return [
            cls.ID,
            cls.CODE_INSEE,
            cls.CODE_POSTAL,
            cls.DEPARTEMENT,
            cls.LIBELLE,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
