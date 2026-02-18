class SaisonFields:
    """Default fields for saison queries."""

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
    def get_default_fields(cls) -> list[str]:
        """Get default fields for saison queries."""
        return [
            cls.ID,
            cls.ACTIF,
            cls.DEBUT,
            cls.FIN,
            cls.CODE,
            cls.LIBELLE,
            cls.EN_COURS,
        ]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields for saison queries."""
        return cls.get_default_fields() + [
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]

    WILDCARD = "*"
