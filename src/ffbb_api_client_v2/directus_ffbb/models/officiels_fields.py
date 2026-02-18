class OfficielsFields:
    """Default fields for officiels queries."""

    NOM = "nom"
    PRENOM = "prenom"
    NUMERO_NATIONAL = "numeroNational"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for officiels queries."""
        return [
            cls.NOM,
            cls.PRENOM,
            cls.NUMERO_NATIONAL,
        ]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields for officiels queries."""
        return cls.get_default_fields() + [
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]

    WILDCARD = "*"
