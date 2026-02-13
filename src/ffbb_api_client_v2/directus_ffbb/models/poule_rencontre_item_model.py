from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ...utils.converter_utils import from_bool, from_datetime, from_int, from_str


@dataclass
class PouleRencontreItemModel:
    id: str
    numero: int
    numeroJournee: int
    idPoule: str
    competitionId: str
    resultatEquipe1: int
    resultatEquipe2: int
    joue: bool
    nomEquipe1: str
    nomEquipe2: str
    date_rencontre: datetime

    @staticmethod
    def from_dict(obj: Any) -> PouleRencontreItemModel:
        assert isinstance(obj, dict)
        id = from_str(obj, "id") or ""
        numero = from_int(obj, "numero") or 0
        numeroJournee = from_int(obj, "numeroJournee") or 0
        idPoule = from_str(obj, "idPoule") or ""
        competitionId = from_str(obj, "competitionId") or ""
        resultatEquipe1 = from_int(obj, "resultatEquipe1") or 0
        resultatEquipe2 = from_int(obj, "resultatEquipe2") or 0
        joue = from_bool(obj, "joue") or False
        nomEquipe1 = from_str(obj, "nomEquipe1") or ""
        nomEquipe2 = from_str(obj, "nomEquipe2") or ""
        date_rencontre = from_datetime(obj, "date_rencontre") or datetime(1970, 1, 1)
        return PouleRencontreItemModel(
            id=id,
            numero=numero,
            numeroJournee=numeroJournee,
            idPoule=idPoule,
            competitionId=competitionId,
            resultatEquipe1=resultatEquipe1,
            resultatEquipe2=resultatEquipe2,
            joue=joue,
            nomEquipe1=nomEquipe1,
            nomEquipe2=nomEquipe2,
            date_rencontre=date_rencontre,
        )
