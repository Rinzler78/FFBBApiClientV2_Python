from .query_fields_manager import QueryFieldsManager


class FormationsFields(QueryFieldsManager):
    """Fields for formations queries."""

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
    def get_fields(cls) -> list[str]:
        """Return the complete list of fields for formations."""
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
