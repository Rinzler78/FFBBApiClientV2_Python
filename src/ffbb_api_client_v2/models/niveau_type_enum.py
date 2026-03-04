from enum import Enum


class NiveauTypeEnum(Enum):
    """Enumération des types de niveau de compétition."""

    DEPARTEMENTAL = "departemental"
    REGIONAL = "regional"
    NATIONAL = "national"
    ELITE = "elite"  # ELITE est associé à régional
