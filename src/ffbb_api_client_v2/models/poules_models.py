from dataclasses import dataclass
from datetime import datetime
from typing import Optional


# Query Parameters Model
@dataclass
class PoulesQuery:
    deep_rencontres__limit: Optional[str] = "1000"  # Original: deep[rencontres][_limit]
    fields_: list[str] = None  # Original: fields[]


# Response Model
@dataclass
class PoulesModel:
    id: str

    @dataclass
    class RencontresitemModel:
        id: str
        numero: str
        numeroJournee: str
        idPoule: str
        competitionId: str
        resultatEquipe1: str
        resultatEquipe2: str
        joue: int
        nomEquipe1: str
        nomEquipe2: str
        date_rencontre: datetime

    rencontres: list[RencontresitemModel]
