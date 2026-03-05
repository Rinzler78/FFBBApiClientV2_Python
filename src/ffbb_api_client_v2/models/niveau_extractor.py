from __future__ import annotations

import re

from .categorie_type_enum import CategorieTypeEnum
from .niveau_info import NiveauInfo
from .niveau_type_enum import NiveauTypeEnum


class NiveauExtractor:
    """Extract competition level from a competition name."""

    # Patterns for identifying levels
    PATTERNS = {
        NiveauTypeEnum.ELITE: [
            r"\bELITE\b",
            r"\bÉLITE\b",
            r"\bELITE\s+MASCULIN\b",
            r"\bELITE\s+FEMININ\b",
        ],
        NiveauTypeEnum.NATIONAL: [
            r"\bNATIONAL\b",
            r"\bNATIONALE\b",
            r"\bN1\b",
            r"\bN2\b",
            r"\bN3\b",
            r"\bPRE\s*NATIONAL\b",
            r"\bPRÉ\s*NATIONAL\b",
        ],
        NiveauTypeEnum.REGIONAL: [
            r"\bREGIONAL\b",
            r"\bRÉGIONAL\b",
            r"\bR1\b",
            r"\bR2\b",
            r"\bR3\b",
            r"\bREGIONALE\b",
            r"^RÉGIONALE\b",  # Simple format: "Régionale masculine seniors"
        ],
        NiveauTypeEnum.DEPARTEMENTAL: [
            r"\bDEPARTEMENTAL\b",
            r"\bDÉPARTEMENTAL\b",
            r"\bD1\b",
            r"\bD2\b",
            r"\bD3\b",
            r"\bDEPARTEMENTALE\b",
            r"^DÉPARTEMENTALE\b",  # Simple format: "Départementale masculine seniors"
        ],
    }

    # Patterns for extracting division numbers
    DIVISION_PATTERNS = [
        r"\b[DRN](\d+)\b",  # R1, R2, D1, D2, N1, N2, etc.
        r"\bREGIONAL\s+(\d+)\b",  # REGIONAL 1, REGIONAL 2
        r"\bDEPARTEMENTAL\s+(\d+)\b",  # DEPARTEMENTAL 1, DEPARTEMENTAL 2
        r"(?i)-\s*division\s+(\d+)\b",  # - Division 3, - division 1 (case insensitive)
    ]

    # Patterns for categories
    CATEGORIE_PATTERNS = {
        # Youth categories
        CategorieTypeEnum.U7: [r"\bU7\b", r"\bU-7\b"],
        CategorieTypeEnum.U9: [r"\bU9\b", r"\bU-9\b"],
        CategorieTypeEnum.U11: [r"\bU11\b", r"\bU-11\b"],
        CategorieTypeEnum.U13: [r"\bU13\b", r"\bU-13\b"],
        CategorieTypeEnum.U15: [r"\bU15\b", r"\bU-15\b"],
        CategorieTypeEnum.U17: [r"\bU17\b", r"\bU-17\b"],
        CategorieTypeEnum.U18: [r"\bU18\b", r"\bU-18\b"],
        CategorieTypeEnum.U20: [r"\bU20\b", r"\bU-20\b"],
        CategorieTypeEnum.U21: [r"\bU21\b", r"\bU-21\b"],
        # Senior categories
        CategorieTypeEnum.SENIOR: [r"\bSENIOR\b"],
        CategorieTypeEnum.SENIORS: [r"\bSENIORS\b"],
        # Veteran categories
        CategorieTypeEnum.VETERAN: [r"\bVETERAN\b", r"\bVÉTÉRAN\b"],
        CategorieTypeEnum.VETERANS: [r"\bVETERANS\b", r"\bVÉTÉRANS\b"],
        CategorieTypeEnum.V35: [r"\bV35\b", r"\bV-35\b"],
        CategorieTypeEnum.V40: [r"\bV40\b", r"\bV-40\b"],
        CategorieTypeEnum.V45: [r"\bV45\b", r"\bV-45\b"],
        CategorieTypeEnum.V50: [r"\bV50\b", r"\bV-50\b"],
        # Special categories (legacy names)
        CategorieTypeEnum.ESPOIR: [r"\bESPOIR\b"],
        CategorieTypeEnum.ESPOIRS: [r"\bESPOIRS\b"],
        CategorieTypeEnum.CADET: [r"\bCADET\b"],
        CategorieTypeEnum.CADETS: [r"\bCADETS\b"],
        CategorieTypeEnum.MINIME: [r"\bMINIME\b"],
        CategorieTypeEnum.MINIMES: [r"\bMINIMES\b"],
        CategorieTypeEnum.BENJAMIN: [r"\bBENJAMIN\b"],
        CategorieTypeEnum.BENJAMINS: [r"\bBENJAMINS\b"],
        CategorieTypeEnum.MINI_POUSSIN: [r"\bMINI\s*POUSSIN\b"],
        CategorieTypeEnum.MINI_POUSSINS: [r"\bMINI\s*POUSSINS\b"],
        CategorieTypeEnum.POUSSIN: [r"\bPOUSSIN\b"],
        CategorieTypeEnum.POUSSINS: [r"\bPOUSSINS\b"],
    }

    @classmethod
    def extract_niveau(cls, competition_name: str) -> NiveauInfo | None:
        """
        Extract the level of a competition from its name.

        Args:
            competition_name: Competition name

        Returns:
            NiveauInfo object or None if no level is detected
        """
        if not competition_name:
            return None

        name_upper = competition_name.upper()

        # Detect level type
        detected_type = None
        matched_text = ""

        for niveau_type, patterns in cls.PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, name_upper)
                if match:
                    detected_type = niveau_type
                    matched_text = match.group(0)
                    break
            if detected_type:
                break

        if not detected_type:
            return None

        # Detect division
        detected_division = None
        for pattern in cls.DIVISION_PATTERNS:
            match = re.search(pattern, name_upper)
            if match:
                detected_division = int(match.group(1))
                break

        # Detect category
        detected_categorie = None
        for categorie_type, patterns in cls.CATEGORIE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, name_upper):
                    detected_categorie = categorie_type
                    break
            if detected_categorie:
                break

        # If no specific category found, try to infer SENIOR
        if not detected_categorie:
            # No youth category detected, assume SENIOR
            if not re.search(r"\bU\d+\b", name_upper):
                detected_categorie = CategorieTypeEnum.SENIOR

        # Determine geographic zone
        zone_geo = None
        if detected_type == NiveauTypeEnum.ELITE:
            zone_geo = "regional"  # ELITE maps to regional

        return NiveauInfo(
            type=detected_type,
            division=detected_division,
            categorie=detected_categorie,
            raw_text=matched_text,
            zone_geographique=zone_geo,
        )

    @classmethod
    def extract_from_competition_data(cls, competition_data: dict) -> NiveauInfo | None:
        """
        Extract level from full competition data.

        Args:
            competition_data: Dictionary with competition data

        Returns:
            NiveauInfo object or None
        """
        if not competition_data:
            return None

        # Try with competition name first
        nom = competition_data.get("nom", "")
        niveau = cls.extract_niveau(nom)

        if niveau:
            return niveau

        # Try with competition code
        code = competition_data.get("code", "")
        if code:
            niveau = cls.extract_niveau(code)

        return niveau


# Utility functions for analysis
def get_niveau_from_idcompetition(idcompetition) -> NiveauInfo | None:
    """
    Extract level from an IdCompetitionModel object.

    Args:
        idcompetition: IdCompetitionModel instance

    Returns:
        NiveauInfo object or None
    """
    if not idcompetition or not idcompetition.nom:
        return None

    return NiveauExtractor.extract_niveau(idcompetition.nom)
