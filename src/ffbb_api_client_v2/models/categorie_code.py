from enum import Enum


class CategorieCode(str, Enum):
    """Codes de categorie d'age retournes par l'API FFBB dans categorie.code.

    Extends str for backward compatibility with string comparisons.
    Format: {AGE}{NIVEAU}{SEXE} where:
      - AGE: U7, U9, U11, U13, U15, U17, U18, U21
      - NIVEAU: D (Départemental), R (Régional), E (Excellence), S (Senior)
      - SEXE: M (Masculin), F (Féminin)
    """

    # ==================== JEUNES - DÉPARTEMENTAL (D) ====================
    # U7
    U7M = "U7M"
    U7F = "U7F"

    # U9
    U9M = "U9M"
    U9F = "U9F"

    # U11 Départemental
    U11D1M = "U11D1M"
    U11D2M = "U11D2M"
    U11D3M = "U11D3M"
    U11D4M = "U11D4M"
    U11D1F = "U11D1F"
    U11D2F = "U11D2F"
    U11D3F = "U11D3F"

    # U13 Départemental
    U13D1M = "U13D1M"
    U13D2M = "U13D2M"
    U13D3M = "U13D3M"
    U13D4M = "U13D4M"
    U13D1F = "U13D1F"
    U13D2F = "U13D2F"
    U13D3F = "U13D3F"

    # U15 Départemental
    U15D1M = "U15D1M"
    U15D2M = "U15D2M"
    U15D3M = "U15D3M"
    U15D1F = "U15D1F"
    U15D2F = "U15D2F"
    U15D3F = "U15D3F"

    # U17 Départemental
    U17D1M = "U17D1M"
    U17D1F = "U17D1F"

    # U18 Départemental
    U18D1M = "U18D1M"
    U18D2M = "U18D2M"
    U18D3M = "U18D3M"
    U18D1F = "U18D1F"
    U18D2F = "U18D2F"
    U18D3F = "U18D3F"

    # U21 Départemental
    U21D1M = "U21D1M"

    # ==================== JEUNES - GÉNÉRIQUE (sans niveau) ====================
    U11 = "U11"
    U13 = "U13"
    U15 = "U15"
    U18 = "U18"

    # ==================== JEUNES - RÉGIONAL (R) ====================
    # U13 Régional
    U13R1M = "U13R1M"
    U13R2M = "U13R2M"
    U13R3M = "U13R3M"
    U13R1F = "U13R1F"
    U13R2F = "U13R2F"
    U13R3F = "U13R3F"

    # U15 Régional
    U15R1M = "U15R1M"
    U15R2M = "U15R2M"
    U15R3M = "U15R3M"
    U15R1F = "U15R1F"
    U15R2F = "U15R2F"
    U15R3F = "U15R3F"

    # U17 Régional
    U17R1M = "U17R1M"
    U17R2M = "U17R2M"
    U17R1F = "U17R1F"
    U17R2F = "U17R2F"

    # U18 Régional
    U18R1M = "U18R1M"
    U18R2M = "U18R2M"
    U18R3M = "U18R3M"
    U18R1F = "U18R1F"
    U18R2F = "U18R2F"

    # U21 Régional
    U21R1M = "U21R1M"
    U21R2M = "U21R2M"

    # ==================== JEUNES - FÉDÉRAL (F) ====================
    U15F1M = "U15F1M"
    U15F1F = "U15F1F"
    U18F1M = "U18F1M"
    U18F1F = "U18F1F"

    # ==================== NATIONAL (N) ====================
    NM1 = "NM1"  # National Masculin 1
    NM2 = "NM2"  # National Masculin 2
    NM3 = "NM3"  # National Masculin 3
    NF2 = "NF2"  # National Féminin 2
    NF3 = "NF3"  # National Féminin 3

    # ==================== PRÉ-NATIONAL / PRÉ-RÉGIONAL ====================
    PNM = "PNM"  # Pré-national Masculin
    PNF = "PNF"  # Pré-national Féminin
    PRM = "PRM"  # Pré-régional Masculin
    PRF = "PRF"  # Pré-régional Féminin

    # ==================== SENIOR EXCELLENCE RÉGIONAL (SER) ====================
    SER1M = "SER1M"
    SER2M = "SER2M"
    SER3M = "SER3M"
    SER1F = "SER1F"
    SER2F = "SER2F"
    SER3F = "SER3F"

    # ==================== SENIOR DÉPARTEMENTAL (SED) ====================
    SED1M = "SED1M"
    SED2M = "SED2M"
    SED3M = "SED3M"
    SED4M = "SED4M"
    SED1F = "SED1F"
    SED2F = "SED2F"
    SED3F = "SED3F"
    SED4F = "SED4F"

    # ==================== ASSOCIATION RÉGIONALE ====================
    AREGM = "AREGM"  # Association Régionale Masculin
    AREGF = "AREGF"  # Association Régionale Féminin

    # ==================== BASKET FAUTEUIL ====================
    LBWL = "LBWL"  # Ligue Basket Wheelchair

    # ==================== JEUNES (codes génériques sans niveau/sexe) ====================
    U7 = "U7"
    U9 = "U9"
    U17 = "U17"
    U20 = "U20"
    U21 = "U21"

    # ==================== SÉNIORS (codes génériques) ====================
    SE = "SE"
    SEN = "SEN"
    S = "S"
    SENIOR = "SENIOR"
    VE = "VE"  # Vétérans

    # ==================== LIGUE FÉMININE ====================
    LF2 = "LF2"  # Ligue Féminine 2
