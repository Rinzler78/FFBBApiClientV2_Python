from .query_fields_manager import QueryFieldsManager


class SaisonFields(QueryFieldsManager):
    """Fields for saison queries."""

    # Basic fields
    ID = "id"
    ACTIF = "actif"
    DEBUT = "debut"
    FIN = "fin"
    CODE = "code"
    LIBELLE = "libelle"
    EN_COURS = "enCours"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_fields(cls) -> list[str]:
        """Return the complete list of fields for saison."""
        return [
            cls.ID,
            cls.ACTIF,
            cls.DEBUT,
            cls.FIN,
            cls.CODE,
            cls.LIBELLE,
            cls.EN_COURS,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
