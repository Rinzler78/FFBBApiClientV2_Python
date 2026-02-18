from .query_fields_manager import QueryFieldsManager


class OfficielsFields(QueryFieldsManager):
    """Fields for officiels queries."""

    NOM = "nom"
    PRENOM = "prenom"
    NUMERO_NATIONAL = "numeroNational"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_fields(cls) -> list[str]:
        """Return the complete list of fields for officiels."""
        return [
            cls.NOM,
            cls.PRENOM,
            cls.NUMERO_NATIONAL,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
