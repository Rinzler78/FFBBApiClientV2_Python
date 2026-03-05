from enum import Enum


class NiveauType(Enum):
    """Enumeration of competition level types."""

    DEPARTEMENTAL = "departemental"
    REGIONAL = "regional"
    NATIONAL = "national"
    ELITE = "elite"  # ELITE is associated with regional
