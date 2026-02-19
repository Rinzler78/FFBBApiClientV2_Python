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
    PUBLIC = "public"
    GOALS = "goals"
    CONTENT = "content"
    PEDAGOGY = "pedagogy"
    PREREQUISITES = "prerequisites"
    RESULTS = "results"
    MODALITIES = "modalities"
    FILES = "files"
    ID_ORIGIN = "idOrigin"
    ID_ORIGIN_HASH = "idOriginHash"
    PROGRAM_ID_FBI = "programIdFbi"
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    # Embedded: domain
    DOMAIN_ID = "domain.id"
    DOMAIN_NAME = "domain.name"
    DOMAIN_SORT = "domain.sort"
    # Embedded: theme
    THEME_ID = "theme.id"
    THEME_NAME = "theme.name"
    THEME_SORT = "theme.sort"
    # Embedded: image (Directus file, FK-only pattern: just id)
    IMAGE = "image"
    # Embedded: sessions
    SESSIONS = "sessions"
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
            cls.SORT,
            cls.PUBLIC,
            cls.GOALS,
            cls.CONTENT,
            cls.PEDAGOGY,
            cls.PREREQUISITES,
            cls.RESULTS,
            cls.MODALITIES,
            cls.FILES,
            cls.ID_ORIGIN,
            cls.ID_ORIGIN_HASH,
            cls.PROGRAM_ID_FBI,
            cls.USER_CREATED,
            cls.USER_UPDATED,
            cls.DOMAIN_ID,
            cls.DOMAIN_NAME,
            cls.DOMAIN_SORT,
            cls.THEME_ID,
            cls.THEME_NAME,
            cls.THEME_SORT,
            cls.IMAGE,
            cls.SESSIONS,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
