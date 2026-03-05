from __future__ import annotations

from dataclasses import dataclass

from .categorie_type_enum import CategorieTypeEnum
from .niveau_type_enum import NiveauTypeEnum


@dataclass
class NiveauInfo:
    """
    Class representing the level of a competition extracted from its name.

    Attributes:
        type: Level type (departemental, regional, national, elite)
        division: Specific division (D1, D2, R1, R2, etc.)
        categorie: Age category (U7, U11, U13, U15, U17, U18, U20, U21, SENIOR, etc.)
        raw_text: Raw text extracted from the competition name
        zone_geographique: Associated geographic zone (regional for ELITE)
    """

    type: NiveauTypeEnum
    division: int | None = None
    categorie: CategorieTypeEnum | None = None
    raw_text: str = ""
    zone_geographique: str | None = None

    @property
    def is_elite(self) -> bool:
        """Check if this is an ELITE level."""
        return self.type == NiveauTypeEnum.ELITE

    @property
    def zone_effective(self) -> str:
        """Return the effective geographic zone (ELITE -> regional)."""
        if self.is_elite:
            return "regional"
        return self.type.value

    def matches_filter(
        self, zone_filter: str, division_filter: int | None = None
    ) -> bool:
        """
        Check if this level matches the specified filters.

        Args:
            zone_filter: Target zone (departemental, regional, national)
            division_filter: Target division number (optional)

        Returns:
            True if the level matches the filters
        """
        # Check the zone (ELITE is considered as regional)
        if zone_filter.lower() != self.zone_effective:
            return False

        # Check the division if specified
        if division_filter is not None:
            if self.division is None:
                return False  # No division but division was requested
            if self.division != division_filter:
                return False

        return True
