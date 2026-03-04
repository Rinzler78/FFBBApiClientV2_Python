from enum import Enum


class JourEnum(Enum):
    SUNDAY = "dimanche"
    THURSDAY = "jeudi"
    MONDAY = "lundi"
    TUESDAY = "mardi"
    WEDNESDAY = "mercredi"
    SATURDAY = "samedi"
    FRIDAY = "vendredi"

    @classmethod
    def _missing_(cls, value: object) -> "JourEnum | None":
        if isinstance(value, str):
            lower = value.lower()
            for member in cls:
                if member.value == lower:
                    return member
        return None
