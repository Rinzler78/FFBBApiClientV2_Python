from enum import Enum


class CompetitionOrigineTypeCompetition(Enum):
    COUPE = "COUPE"
    DIV = "DIV"
    PLAT = "PLAT"

    @staticmethod
    def parse(str):
        try:
            return CompetitionOrigineTypeCompetition(str)
        except ValueError:
            return CompetitionOrigineTypeCompetition(str.upper())
