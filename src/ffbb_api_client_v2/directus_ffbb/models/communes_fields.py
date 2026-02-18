class CommunesFields:
    """Default fields for communes queries."""

    ID = "id"
    CODE_INSEE = "codeInsee"
    CODE_POSTAL = "codePostal"
    DEPARTEMENT = "departement"
    LIBELLE = "libelle"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for communes queries."""
        return [
            cls.ID,
            cls.CODE_INSEE,
            cls.CODE_POSTAL,
            cls.DEPARTEMENT,
            cls.LIBELLE,
        ]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields for communes queries."""
        return cls.get_default_fields() + [
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]

    WILDCARD = "*"
