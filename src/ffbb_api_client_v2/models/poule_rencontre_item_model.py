from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class PouleRencontreItemModel:
    id: str
    numero: str
    numeroJournee: str
    idPoule: str
    competitionId: str
    resultatEquipe1: str
    resultatEquipe2: str
    joue: bool
    nomEquipe1: str
    nomEquipe2: str
    date_rencontre: datetime
