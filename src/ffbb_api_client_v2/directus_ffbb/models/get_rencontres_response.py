from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ...utils.converter_utils import (
    from_bool,
    from_datetime,
    from_int,
    from_str,
)


@dataclass
class GetRencontresResponse:
    id: str
    date: datetime | None = None
    date_rencontre: datetime | None = None
    horaire: str | None = None
    numero: str | None = None
    numeroJournee: str | None = None
    nomEquipe1: str | None = None
    nomEquipe2: str | None = None
    resultatEquipe1: int | None = None
    resultatEquipe2: int | None = None
    joue: bool | None = None
    etat: str | None = None
    pratique: str | None = None
    status: str | None = None
    validee: bool | None = None
    forfaitEquipe1: bool | None = None
    forfaitEquipe2: bool | None = None
    defautEquipe1: bool | None = None
    defautEquipe2: bool | None = None
    penaliteEquipe1: int | None = None
    penaliteEquipe2: int | None = None
    handicap1: int | None = None
    handicap2: int | None = None
    remise: bool | None = None
    dateSaisieResultat: str | None = None
    creation: str | None = None
    modification: str | None = None
    toUpdate: bool | None = None
    uniqueKey: str | None = None
    url_competition: str | None = None
    rematch_videos: str | None = None
    # FK-only fields (int IDs)
    competitionId: int | None = None
    idEngagementEquipe1: int | None = None
    idEngagementEquipe2: int | None = None
    idOrganismeEquipe1: int | None = None
    idOrganismeEquipe2: int | None = None
    idPoule: int | None = None
    saison: int | None = None
    salle: int | None = None
    gsId: str | None = None
    # Embedded objects
    officiels: list[str] = field(default_factory=list)
    date_created: datetime | None = None
    date_updated: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetRencontresResponse | None:
        """Convert dictionary to GetRencontresResponse instance."""
        if not data:
            return None
        if not isinstance(data, dict):
            return None
        if "errors" in data:
            return None

        return cls(
            id=from_str(data, "id") or "",
            date=from_datetime(data, "date"),
            date_rencontre=from_datetime(data, "date_rencontre"),
            horaire=from_str(data, "horaire"),
            numero=from_str(data, "numero"),
            numeroJournee=from_str(data, "numeroJournee"),
            nomEquipe1=from_str(data, "nomEquipe1"),
            nomEquipe2=from_str(data, "nomEquipe2"),
            resultatEquipe1=from_int(data, "resultatEquipe1"),
            resultatEquipe2=from_int(data, "resultatEquipe2"),
            joue=from_bool(data, "joue"),
            etat=from_str(data, "etat"),
            pratique=from_str(data, "pratique"),
            status=from_str(data, "status"),
            validee=from_bool(data, "validee"),
            forfaitEquipe1=from_bool(data, "forfaitEquipe1"),
            forfaitEquipe2=from_bool(data, "forfaitEquipe2"),
            defautEquipe1=from_bool(data, "defautEquipe1"),
            defautEquipe2=from_bool(data, "defautEquipe2"),
            penaliteEquipe1=from_int(data, "penaliteEquipe1"),
            penaliteEquipe2=from_int(data, "penaliteEquipe2"),
            handicap1=from_int(data, "handicap1"),
            handicap2=from_int(data, "handicap2"),
            remise=from_bool(data, "remise"),
            dateSaisieResultat=from_str(data, "dateSaisieResultat"),
            creation=from_str(data, "creation"),
            modification=from_str(data, "modification"),
            toUpdate=from_bool(data, "toUpdate"),
            uniqueKey=from_str(data, "uniqueKey"),
            url_competition=from_str(data, "url_competition"),
            rematch_videos=from_str(data, "rematch_videos"),
            competitionId=from_int(data, "competitionId"),
            idEngagementEquipe1=from_int(data, "idEngagementEquipe1"),
            idEngagementEquipe2=from_int(data, "idEngagementEquipe2"),
            idOrganismeEquipe1=from_int(data, "idOrganismeEquipe1"),
            idOrganismeEquipe2=from_int(data, "idOrganismeEquipe2"),
            idPoule=from_int(data, "idPoule"),
            saison=from_int(data, "saison"),
            salle=from_int(data, "salle"),
            gsId=from_str(data, "gsId"),
            officiels=[str(x) for x in (data.get("officiels") or []) if x is not None],
            date_created=from_datetime(data, "date_created"),
            date_updated=from_datetime(data, "date_updated"),
        )

    @classmethod
    def from_list(cls, data_list: list[dict[str, Any]]) -> list[GetRencontresResponse]:
        """Convert list of dictionaries to list of instances."""
        if not data_list:
            return []
        return [
            result
            for item in data_list
            if item
            for result in [cls.from_dict(item)]
            if result is not None
        ]
