from enum import Enum


class CategorieTypeEnum(Enum):
    """Enumeration of age categories in basketball."""

    # Youth categories
    U7 = "U7"
    U9 = "U9"
    U11 = "U11"
    U13 = "U13"
    U15 = "U15"
    U17 = "U17"
    U18 = "U18"
    U20 = "U20"
    U21 = "U21"

    # Senior categories
    SENIOR = "SENIOR"
    SENIORS = "SENIORS"

    # Veteran categories
    VETERAN = "VETERAN"
    VETERANS = "VETERANS"
    V35 = "V35"
    V40 = "V40"
    V45 = "V45"
    V50 = "V50"

    # Special categories
    ESPOIR = "ESPOIR"
    ESPOIRS = "ESPOIRS"
    CADET = "CADET"
    CADETS = "CADETS"
    MINIME = "MINIME"
    MINIMES = "MINIMES"
    BENJAMIN = "BENJAMIN"
    BENJAMINS = "BENJAMINS"
    POUSSIN = "POUSSIN"
    POUSSINS = "POUSSINS"
    MINI_POUSSIN = "MINI_POUSSIN"
    MINI_POUSSINS = "MINI_POUSSINS"
