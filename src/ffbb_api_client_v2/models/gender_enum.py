"""Genre (sexe) pour les codes categorie FFBB."""

from __future__ import annotations

from enum import Enum


class GenderEnum(str, Enum):
    """Genre extrait d'un code categorie FFBB.

    Codes courts utilises dans les codes categorie
    (ex: M dans U13D1M, F dans NF2).
    Distinct de SexeEnum qui utilise les libelles francais ("Feminin", "Masculin").
    """

    MASCULIN = "M"
    FEMININ = "F"
