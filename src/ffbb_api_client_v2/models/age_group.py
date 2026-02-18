"""Tranche d'age pour les codes categorie FFBB."""

from __future__ import annotations

from enum import Enum


class AgeGroup(str, Enum):
    """Tranche d'age extraite d'un code categorie FFBB.

    Valeurs correspondant aux prefixes age dans les codes categorie
    (ex: U13 dans U13D1M, SE dans SED1M).
    """

    U7 = "U7"
    U9 = "U9"
    U11 = "U11"
    U13 = "U13"
    U15 = "U15"
    U17 = "U17"
    U18 = "U18"
    U20 = "U20"
    U21 = "U21"
    SENIOR = "SE"
    VETERAN = "VE"
