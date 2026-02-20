"""Echelon territorial de competition FFBB."""

from __future__ import annotations

from enum import Enum


class Echelon(str, Enum):
    """Echelon territorial extrait d'un code categorie FFBB.

    Valeurs correspondant au composant echelon dans les codes categorie
    (ex: D dans U13D1M, N dans NM1, PN dans PNM).
    """

    PRO = "PRO"
    DEPARTEMENT = "D"
    REGION = "R"
    FEDERAL = "F"
    NATIONAL = "N"
    PRE_NATIONAL = "PN"
    PRE_REGIONAL = "PR"
    EXCELLENCE = "E"
    LIGUE_FEMININE = "LF"
    ASSOCIATION_DEPARTEMENTALE = "ADEP"
    ASSOCIATION_REGIONALE = "AREG"
    BASKET_FAUTEUIL = "LBWL"
