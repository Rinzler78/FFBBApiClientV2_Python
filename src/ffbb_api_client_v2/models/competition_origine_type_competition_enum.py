from enum import Enum


class CompetitionOrigineTypeCompetitionEnum(Enum):
    COUPE = "COUPE"
    DIV = "DIV"
    PLAT = "PLAT"

    @staticmethod
    def parse(str):
        try:
            return CompetitionOrigineTypeCompetitionEnum(str)
        except ValueError:
            return CompetitionOrigineTypeCompetitionEnum(str.upper())
