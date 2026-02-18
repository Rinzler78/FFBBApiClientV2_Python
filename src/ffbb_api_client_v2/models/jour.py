from enum import Enum


class Jour(Enum):
    SUNDAY = "dimanche"
    THURSDAY = "jeudi"
    MONDAY = "lundi"
    TUESDAY = "mardi"
    WEDNESDAY = "mercredi"
    SATURDAY = "samedi"
    FRIDAY = "vendredi"

    @classmethod
    def _missing_(cls, value: object) -> "Jour | None":
        if isinstance(value, str):
            lower = value.lower()
            for member in cls:
                if member.value == lower:
                    return member
        return None
