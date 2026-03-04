from __future__ import annotations

from dataclasses import dataclass

from .categorie_type_enum import CategorieTypeEnum
from .niveau_type_enum import NiveauTypeEnum


@dataclass
class NiveauInfo:
    """
    Classe pour représenter le niveau d'une compétition extrait du nom.

    Attributes:
        type: Type de niveau (departemental, regional, national, elite)
        division: Division spécifique (D1, D2, R1, R2, etc.)
        categorie: Catégorie d'âge (U7, U11, U13, U15, U17, U18, U20, U21, SENIOR, etc.)
        raw_text: Texte brut extrait du nom de la compétition
        zone_geographique: Zone géographique associée (regional pour ELITE)
    """

    type: NiveauTypeEnum
    division: int | None = None
    categorie: CategorieTypeEnum | None = None
    raw_text: str = ""
    zone_geographique: str | None = None

    @property
    def is_elite(self) -> bool:
        """Vérifie si c'est un niveau ELITE."""
        return self.type == NiveauTypeEnum.ELITE

    @property
    def zone_effective(self) -> str:
        """Retourne la zone géographique effective (ELITE -> regional)."""
        if self.is_elite:
            return "regional"
        return self.type.value

    def matches_filter(
        self, zone_filter: str, division_filter: int | None = None
    ) -> bool:
        """
        Vérifie si ce niveau correspond aux filtres spécifiés.

        Args:
            zone_filter: Zone recherchée (departemental, regional, national)
            division_filter: Numéro de division recherchée (optionnel)

        Returns:
            True si le niveau correspond aux filtres
        """
        # Vérifier la zone (ELITE est considéré comme regional)
        if zone_filter.lower() != self.zone_effective:
            return False

        # Vérifier la division si spécifiée
        if division_filter is not None:
            if self.division is None:
                return False  # Pas de division mais division demandée
            if self.division != division_filter:
                return False

        return True
