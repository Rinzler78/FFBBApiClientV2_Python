from __future__ import annotations

from enum import Enum


class TypeCompetition(Enum):
    CHAMPIONNAT = "Championnat"
    CHAMPIONNAT_3_X3 = "Championnat 3x3"
    COUPE = "Coupe"
    DIV = "DIV"
    PLATEAU = "Plateau"

    @classmethod
    def _missing_(cls, value: object) -> TypeCompetition | None:
        if isinstance(value, str):
            for member in cls:
                if member.value.upper() == value.upper():
                    return member
        return None
