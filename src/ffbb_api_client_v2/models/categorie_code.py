from enum import Enum


class CategorieCode(str, Enum):
    """Codes de categorie d'age retournes par l'API FFBB dans categorie.code.

    Extends str for backward compatibility with string comparisons.
    Values will be completed from discover_types.py enum_candidates.json.
    """

    # Jeunes
    U7 = "U7"
    U9 = "U9"
    U11 = "U11"
    U13 = "U13"
    U15 = "U15"
    U17 = "U17"
    U18 = "U18"
    U20 = "U20"
    U21 = "U21"

    # Seniors
    SE = "SE"
    SEN = "SEN"
    S = "S"
    SENIOR = "SENIOR"
