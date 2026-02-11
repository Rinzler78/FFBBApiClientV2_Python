from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class GetEngagementsResponse:
    id: str
    nom: str | None = None
    nomEquipe: str | None = None
    nomUsuel: str | None = None
    nomOfficiel: str | None = None
    numeroEquipe: str | None = None
    codeAbrege: str | None = None
    clubPro: bool | None = None
    position: int | None = None
    logo: dict[str, Any] | None = None
    idCompetition: dict[str, Any] | None = None
    idOrganisme: dict[str, Any] | None = None
    idPoule: dict[str, Any] | None = None
    niveau: dict[str, Any] | None = None
    classement: dict[str, Any] | None = None
    entraineur: dict[str, Any] | None = None
    entraineurAdjoint: dict[str, Any] | None = None
    positionVariation: int | None = None
    position_n1: int | None = None
    positions: list[Any] = field(default_factory=list)
    rencontres_domiciles: list[Any] = field(default_factory=list)
    rencontres_exterieur: list[Any] = field(default_factory=list)
    date_created: str | None = None
    date_updated: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetEngagementsResponse | None:
        """Convert dictionary to GetEngagementsResponse instance."""
        if not data:
            return None
        if not isinstance(data, dict):
            return None
        if "errors" in data:
            return None

        return cls(
            id=str(data.get("id", "")),
            nom=str(data.get("nom", "")) if data.get("nom") else None,
            nomEquipe=(
                str(data.get("nomEquipe", "")) if data.get("nomEquipe") else None
            ),
            nomUsuel=(str(data.get("nomUsuel", "")) if data.get("nomUsuel") else None),
            nomOfficiel=(
                str(data.get("nomOfficiel", "")) if data.get("nomOfficiel") else None
            ),
            numeroEquipe=(
                str(data.get("numeroEquipe", "")) if data.get("numeroEquipe") else None
            ),
            codeAbrege=(
                str(data.get("codeAbrege", "")) if data.get("codeAbrege") else None
            ),
            clubPro=data.get("clubPro"),
            position=data.get("position"),
            logo=data.get("logo"),
            idCompetition=data.get("idCompetition"),
            idOrganisme=data.get("idOrganisme"),
            idPoule=data.get("idPoule"),
            niveau=data.get("niveau"),
            classement=data.get("classement"),
            entraineur=data.get("entraineur"),
            entraineurAdjoint=data.get("entraineurAdjoint"),
            positionVariation=data.get("positionVariation"),
            position_n1=data.get("position_n1"),
            positions=data.get("positions", []) or [],
            rencontres_domiciles=data.get("rencontres_domiciles", []) or [],
            rencontres_exterieur=data.get("rencontres_exterieur", []) or [],
            date_created=(
                str(data.get("date_created", "")) if data.get("date_created") else None
            ),
            date_updated=(
                str(data.get("date_updated", "")) if data.get("date_updated") else None
            ),
        )

    @classmethod
    def from_list(cls, data_list: list[dict[str, Any]]) -> list[GetEngagementsResponse]:
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
