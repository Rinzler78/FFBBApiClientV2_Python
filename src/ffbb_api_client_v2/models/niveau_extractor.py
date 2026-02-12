from __future__ import annotations

import re

from .categorie_type import CategorieType
from .niveau_info import NiveauInfo
from .niveau_type import NiveauType


class NiveauExtractor:
    """Extracteur de niveau depuis le nom d'une compétition."""

    # Patterns pour identifier les niveaux
    PATTERNS = {
        NiveauType.ELITE: [
            r"\bELITE\b",
            r"\bÉLITE\b",
            r"\bELITE\s+MASCULIN\b",
            r"\bELITE\s+FEMININ\b",
        ],
        NiveauType.NATIONAL: [
            r"\bNATIONAL\b",
            r"\bNATIONALE\b",
            r"\bN1\b",
            r"\bN2\b",
            r"\bN3\b",
            r"\bPRE\s*NATIONAL\b",
            r"\bPRÉ\s*NATIONAL\b",
        ],
        NiveauType.REGIONAL: [
            r"\bREGIONAL\b",
            r"\bRÉGIONAL\b",
            r"\bR1\b",
            r"\bR2\b",
            r"\bR3\b",
            r"\bREGIONALE\b",
            r"^RÉGIONALE\b",  # Format simple: "Régionale masculine seniors"
        ],
        NiveauType.DEPARTEMENTAL: [
            r"\bDEPARTEMENTAL\b",
            r"\bDÉPARTEMENTAL\b",
            r"\bD1\b",
            r"\bD2\b",
            r"\bD3\b",
            r"\bDEPARTEMENTALE\b",
            r"^DÉPARTEMENTALE\b",  # Format simple: "Départementale masculine seniors"
        ],
    }

    # Patterns pour extraire les numéros de division
    DIVISION_PATTERNS = [
        r"\b[DRN](\d+)\b",  # R1, R2, D1, D2, N1, N2, etc.
        r"\bREGIONAL\s+(\d+)\b",  # REGIONAL 1, REGIONAL 2
        r"\bDEPARTEMENTAL\s+(\d+)\b",  # DEPARTEMENTAL 1, DEPARTEMENTAL 2
        r"(?i)-\s*division\s+(\d+)\b",  # - Division 3, - division 1 (case insensitive)
    ]

    # Patterns pour les catégories
    CATEGORIE_PATTERNS = {
        # Catégories jeunes
        CategorieType.U7: [r"\bU7\b", r"\bU-7\b"],
        CategorieType.U9: [r"\bU9\b", r"\bU-9\b"],
        CategorieType.U11: [r"\bU11\b", r"\bU-11\b"],
        CategorieType.U13: [r"\bU13\b", r"\bU-13\b"],
        CategorieType.U15: [r"\bU15\b", r"\bU-15\b"],
        CategorieType.U17: [r"\bU17\b", r"\bU-17\b"],
        CategorieType.U18: [r"\bU18\b", r"\bU-18\b"],
        CategorieType.U20: [r"\bU20\b", r"\bU-20\b"],
        CategorieType.U21: [r"\bU21\b", r"\bU-21\b"],
        # Catégories seniors
        CategorieType.SENIOR: [r"\bSENIOR\b"],
        CategorieType.SENIORS: [r"\bSENIORS\b"],
        # Catégories vétérans
        CategorieType.VETERAN: [r"\bVETERAN\b", r"\bVÉTÉRAN\b"],
        CategorieType.VETERANS: [r"\bVETERANS\b", r"\bVÉTÉRANS\b"],
        CategorieType.V35: [r"\bV35\b", r"\bV-35\b"],
        CategorieType.V40: [r"\bV40\b", r"\bV-40\b"],
        CategorieType.V45: [r"\bV45\b", r"\bV-45\b"],
        CategorieType.V50: [r"\bV50\b", r"\bV-50\b"],
        # Catégories spéciales (anciennes dénominations)
        CategorieType.ESPOIR: [r"\bESPOIR\b"],
        CategorieType.ESPOIRS: [r"\bESPOIRS\b"],
        CategorieType.CADET: [r"\bCADET\b"],
        CategorieType.CADETS: [r"\bCADETS\b"],
        CategorieType.MINIME: [r"\bMINIME\b"],
        CategorieType.MINIMES: [r"\bMINIMES\b"],
        CategorieType.BENJAMIN: [r"\bBENJAMIN\b"],
        CategorieType.BENJAMINS: [r"\bBENJAMINS\b"],
        CategorieType.MINI_POUSSIN: [r"\bMINI\s*POUSSIN\b"],
        CategorieType.MINI_POUSSINS: [r"\bMINI\s*POUSSINS\b"],
        CategorieType.POUSSIN: [r"\bPOUSSIN\b"],
        CategorieType.POUSSINS: [r"\bPOUSSINS\b"],
    }

    @classmethod
    def extract_niveau(cls, competition_name: str) -> NiveauInfo | None:
        """
        Extrait le niveau d'une compétition depuis son nom.

        Args:
            competition_name: Nom de la compétition

        Returns:
            Objet Niveau ou None si aucun niveau n'est détecté
        """
        if not competition_name:
            return None

        name_upper = competition_name.upper()

        # Détection du type de niveau
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

        # Détection de la division
        detected_division = None
        for pattern in cls.DIVISION_PATTERNS:
            match = re.search(pattern, name_upper)
            if match:
                detected_division = int(match.group(1))
                break

        # Détection de la catégorie
        detected_categorie = None
        for categorie_type, patterns in cls.CATEGORIE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, name_upper):
                    detected_categorie = categorie_type
                    break
            if detected_categorie:
                break

        # Si aucune catégorie spécifique n'est trouvée, essayer de déduire SENIOR
        if not detected_categorie:
            # Si pas de catégorie jeune détectée et que c'est une compétition, on assume SENIOR
            if not any(re.search(r"\bU\d+\b", name_upper) for _ in [1]):
                detected_categorie = CategorieType.SENIOR

        # Déterminer la zone géographique
        zone_geo = None
        if detected_type == NiveauType.ELITE:
            zone_geo = "regional"  # ELITE est associé à régional

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
        Extrait le niveau depuis les données complètes de compétition.

        Args:
            competition_data: Dictionnaire avec les données de compétition

        Returns:
            Objet Niveau ou None
        """
        if not competition_data:
            return None

        # Essayer d'abord avec le nom de la compétition
        nom = competition_data.get("nom", "")
        niveau = cls.extract_niveau(nom)

        if niveau:
            return niveau

        # Essayer avec le code de la compétition
        code = competition_data.get("code", "")
        if code:
            niveau = cls.extract_niveau(code)

        return niveau


# Fonctions utilitaires pour l'analyse
def get_niveau_from_idcompetition(idcompetition) -> NiveauInfo | None:
    """
    Extrait le niveau depuis un objet IdCompetitionModel.

    Args:
        idcompetition: Instance de IdCompetitionModel

    Returns:
        Objet Niveau ou None
    """
    if not idcompetition or not idcompetition.nom:
        return None

    return NiveauExtractor.extract_niveau(idcompetition.nom)
