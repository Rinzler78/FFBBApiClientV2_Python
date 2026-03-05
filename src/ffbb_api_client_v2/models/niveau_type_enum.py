from enum import Enum


class NiveauTypeEnum(Enum):
    """Enumeration of competition level types."""

    DEPARTEMENTAL = "departemental"
    REGIONAL = "regional"
    NATIONAL = "national"
    ELITE = "elite"  # ELITE maps to regional
