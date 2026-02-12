from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..utils.converter_utils import (
    from_bool,
    from_int,
    from_str,
)


@dataclass
class GetRencontresResponse:
    id: str
    date: str | None = None
    date_rencontre: str | None = None
    horaire: str | None = None
    numero: int | None = None
    numeroJournee: int | None = None
    nomEquipe1: str | None = None
    nomEquipe2: str | None = None
    resultatEquipe1: int | None = None
    resultatEquipe2: int | None = None
    joue: bool | None = None
    etat: str | None = None
    pratique: str | None = None
    status: str | None = None
    competitionId: dict[str, Any] | None = None
    idOrganismeEquipe1: dict[str, Any] | None = None
    idOrganismeEquipe2: dict[str, Any] | None = None
    idPoule: dict[str, Any] | None = None
    saison: dict[str, Any] | None = None
    salle: dict[str, Any] | None = None
    gsId: dict[str, Any] | None = None
    officiels: list[Any] = field(default_factory=list)
    idEngagementEquipe1: dict[str, Any] | None = None
    idEngagementEquipe2: dict[str, Any] | None = None
    creation: str | None = None
    modification: str | None = None
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
    date_created: str | None = None
    date_updated: str | None = None

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
            date=from_str(data, "date"),
            date_rencontre=from_str(data, "date_rencontre"),
            horaire=from_str(data, "horaire"),
            numero=from_int(data, "numero"),
            numeroJournee=from_int(data, "numeroJournee"),
            nomEquipe1=from_str(data, "nomEquipe1"),
            nomEquipe2=from_str(data, "nomEquipe2"),
            resultatEquipe1=from_int(data, "resultatEquipe1"),
            resultatEquipe2=from_int(data, "resultatEquipe2"),
            joue=from_bool(data, "joue"),
            etat=from_str(data, "etat"),
            pratique=from_str(data, "pratique"),
            status=from_str(data, "status"),
            competitionId=data.get("competitionId"),  # Keep as raw dict
            idOrganismeEquipe1=data.get("idOrganismeEquipe1"),
            idOrganismeEquipe2=data.get("idOrganismeEquipe2"),
            idPoule=data.get("idPoule"),
            saison=data.get("saison"),
            salle=data.get("salle"),
            gsId=data.get("gsId"),
            officiels=data.get("officiels", []) or [],
            idEngagementEquipe1=data.get("idEngagementEquipe1"),
            idEngagementEquipe2=data.get("idEngagementEquipe2"),
            creation=from_str(data, "creation"),
            modification=from_str(data, "modification"),
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
            date_created=from_str(data, "date_created"),
            date_updated=from_str(data, "date_updated"),
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
