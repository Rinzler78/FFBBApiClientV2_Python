class FormationsFields:
    """Default fields for formations queries."""

    ID = "id"
    TITLE = "title"
    DESCRIPTION = "description"
    MODE = "mode"
    LEVEL = "level"
    REFERENCE = "reference"
    DURATION_HOURS = "duration_hours"
    CERTIFICATION = "certification"
    STATUS = "status"
    SORT = "sort"
    DOMAIN = "domain"
    THEME = "theme"
    SESSIONS = "sessions"
    PUBLIC = "public"
    GOALS = "goals"
    CONTENT = "content"
    PEDAGOGY = "pedagogy"
    PREREQUISITES = "prerequisites"
    RESULTS = "results"
    MODALITIES = "modalities"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for formations queries."""
        return [
            cls.ID,
            cls.TITLE,
            cls.DESCRIPTION,
            cls.MODE,
            cls.LEVEL,
            cls.REFERENCE,
            cls.DURATION_HOURS,
            cls.CERTIFICATION,
            cls.STATUS,
            cls.DOMAIN,
            cls.THEME,
        ]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields for formations queries."""
        return cls.get_default_fields() + [
            cls.SESSIONS,
            cls.PUBLIC,
            cls.GOALS,
            cls.CONTENT,
            cls.PEDAGOGY,
            cls.PREREQUISITES,
            cls.RESULTS,
            cls.MODALITIES,
            cls.SORT,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]

    @staticmethod
    def get_wildcard(depth: int = 2) -> list[str]:
        """Get wildcard fields at the specified depth."""
        return [".".join(["*"] * min(depth, 5))]
