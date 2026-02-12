from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..utils.converter_utils import (
    from_bool,
    from_int,
    from_str,
)


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
            id=from_str(data, "id") or "",
            nom=from_str(data, "nom"),
            nomEquipe=from_str(data, "nomEquipe"),
            nomUsuel=from_str(data, "nomUsuel"),
            nomOfficiel=from_str(data, "nomOfficiel"),
            numeroEquipe=from_str(data, "numeroEquipe"),
            codeAbrege=from_str(data, "codeAbrege"),
            clubPro=from_bool(data, "clubPro"),
            position=from_int(data, "position"),
            logo=data.get("logo"),  # Keep as raw dict
            idCompetition=data.get("idCompetition"),  # Keep as raw dict
            idOrganisme=data.get("idOrganisme"),  # Keep as raw dict
            idPoule=data.get("idPoule"),  # Keep as raw dict
            niveau=data.get("niveau"),  # Keep as raw dict
            classement=data.get("classement"),  # Keep as raw dict
            entraineur=data.get("entraineur"),  # Keep as raw dict
            entraineurAdjoint=data.get("entraineurAdjoint"),  # Keep as raw dict
            positionVariation=from_int(data, "positionVariation"),
            position_n1=from_int(data, "position_n1"),
            positions=data.get("positions", []) or [],
            rencontres_domiciles=data.get("rencontres_domiciles", []) or [],
            rencontres_exterieur=data.get("rencontres_exterieur", []) or [],
            date_created=from_str(data, "date_created"),
            date_updated=from_str(data, "date_updated"),
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
