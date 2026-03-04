from __future__ import annotations

from enum import Enum


class TypeCompetitionEnum(Enum):
    CHAMPIONNAT = "Championnat"
    CHAMPIONNAT_3_X3 = "Championnat 3x3"
    COUPE = "Coupe"
    DIV = "DIV"
    DIV_3X3 = "DIV 3x3"
    PLAT = "PLAT"
    PLATEAU = "Plateau"

    @classmethod
    def _missing_(cls, value: object) -> TypeCompetitionEnum | None:
        if isinstance(value, str):
            for member in cls:
                if member.value.upper() == value.upper():
                    return member
        return None
