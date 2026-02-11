from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class GetRencontresResponse:
    id: str
    date: str | None = None
    date_rencontre: str | None = None
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
            id=str(data.get("id", "")),
            date=str(data.get("date", "")) if data.get("date") else None,
            date_rencontre=(
                str(data.get("date_rencontre", ""))
                if data.get("date_rencontre")
                else None
            ),
            horaire=(str(data.get("horaire", "")) if data.get("horaire") else None),
            numero=(str(data.get("numero", "")) if data.get("numero") else None),
            numeroJournee=(
                str(data.get("numeroJournee", ""))
                if data.get("numeroJournee")
                else None
            ),
            nomEquipe1=(
                str(data.get("nomEquipe1", "")) if data.get("nomEquipe1") else None
            ),
            nomEquipe2=(
                str(data.get("nomEquipe2", "")) if data.get("nomEquipe2") else None
            ),
            resultatEquipe1=data.get("resultatEquipe1"),
            resultatEquipe2=data.get("resultatEquipe2"),
            joue=data.get("joue"),
            etat=str(data.get("etat", "")) if data.get("etat") else None,
            pratique=(str(data.get("pratique", "")) if data.get("pratique") else None),
            status=(str(data.get("status", "")) if data.get("status") else None),
            competitionId=data.get("competitionId"),
            idOrganismeEquipe1=data.get("idOrganismeEquipe1"),
            idOrganismeEquipe2=data.get("idOrganismeEquipe2"),
            idPoule=data.get("idPoule"),
            saison=data.get("saison"),
            salle=data.get("salle"),
            gsId=data.get("gsId"),
            officiels=data.get("officiels", []) or [],
            idEngagementEquipe1=data.get("idEngagementEquipe1"),
            idEngagementEquipe2=data.get("idEngagementEquipe2"),
            creation=(str(data.get("creation", "")) if data.get("creation") else None),
            modification=(
                str(data.get("modification", "")) if data.get("modification") else None
            ),
            validee=data.get("validee"),
            forfaitEquipe1=data.get("forfaitEquipe1"),
            forfaitEquipe2=data.get("forfaitEquipe2"),
            defautEquipe1=data.get("defautEquipe1"),
            defautEquipe2=data.get("defautEquipe2"),
            penaliteEquipe1=data.get("penaliteEquipe1"),
            penaliteEquipe2=data.get("penaliteEquipe2"),
            handicap1=data.get("handicap1"),
            handicap2=data.get("handicap2"),
            remise=data.get("remise"),
            dateSaisieResultat=(
                str(data.get("dateSaisieResultat", ""))
                if data.get("dateSaisieResultat")
                else None
            ),
            date_created=(
                str(data.get("date_created", "")) if data.get("date_created") else None
            ),
            date_updated=(
                str(data.get("date_updated", "")) if data.get("date_updated") else None
            ),
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
