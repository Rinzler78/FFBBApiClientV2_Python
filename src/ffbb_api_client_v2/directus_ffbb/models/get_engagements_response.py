from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ...models.categorie import Categorie
from ...models.document_flyer import DocumentFlyer
from ...models.organisateur import Organisateur
from ...utils.converter_utils import (
    from_bool,
    from_datetime,
    from_int,
    from_list,
    from_obj,
    from_str,
)
from .get_entraineurs_response import GetEntraineursResponse
from .get_poule_response import GetPouleResponse
from .get_rencontres_response import GetRencontresResponse


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
    logo: DocumentFlyer | None = None
    idCompetition: dict[str, Any] | None = None
    idOrganisme: Organisateur | None = None
    idPoule: GetPouleResponse | None = None
    niveau: Categorie | None = None
    classement: dict[str, Any] | None = None
    entraineur: GetEntraineursResponse | None = None
    entraineurAdjoint: GetEntraineursResponse | None = None
    positionVariation: int | None = None
    position_n1: int | None = None
    positions: list[Any] = field(default_factory=list)
    rencontres_domiciles: list[GetRencontresResponse] = field(default_factory=list)
    rencontres_exterieur: list[GetRencontresResponse] = field(default_factory=list)
    date_created: datetime | None = None
    date_updated: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetEngagementsResponse | None:
        """Convert dictionary to GetEngagementsResponse instance."""
        if not data:
            return None
        if not isinstance(data, dict):
            return None
        if "errors" in data:
            return None

        domiciles_raw = from_list(
            GetRencontresResponse.from_dict, data, "rencontres_domiciles"
        )
        exterieur_raw = from_list(
            GetRencontresResponse.from_dict, data, "rencontres_exterieur"
        )

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
            logo=from_obj(DocumentFlyer.from_dict, data, "logo"),
            idCompetition=data.get("idCompetition"),
            idOrganisme=from_obj(Organisateur.from_dict, data, "idOrganisme"),
            idPoule=from_obj(GetPouleResponse.from_dict, data, "idPoule"),
            niveau=from_obj(Categorie.from_dict, data, "niveau"),
            classement=data.get("classement"),
            entraineur=from_obj(GetEntraineursResponse.from_dict, data, "entraineur"),
            entraineurAdjoint=from_obj(
                GetEntraineursResponse.from_dict, data, "entraineurAdjoint"
            ),
            positionVariation=from_int(data, "positionVariation"),
            position_n1=from_int(data, "position_n1"),
            positions=data.get("positions", []) or [],
            rencontres_domiciles=[r for r in (domiciles_raw or []) if r is not None],
            rencontres_exterieur=[r for r in (exterieur_raw or []) if r is not None],
            date_created=from_datetime(data, "date_created"),
            date_updated=from_datetime(data, "date_updated"),
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
