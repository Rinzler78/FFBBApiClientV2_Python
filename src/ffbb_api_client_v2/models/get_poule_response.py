from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_list, from_str
from .poule_rencontre_item_model import PouleRencontreItemModel
from .team_ranking import TeamRanking


@dataclass
class GetPouleResponse:
    id: str

    # Keep nested alias for backward compatibility
    RencontresitemModel = PouleRencontreItemModel

    rencontres: list[PouleRencontreItemModel]
    classements: list[TeamRanking] | None = None
    nom: str | None = None
    engagements: list[dict[str, Any]] | None = None
    id_competition: str | None = None
    date_created: str | None = None
    date_updated: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetPouleResponse | None:
        """Convert dictionary to PoulesModel instance."""
        if not data:
            return None

        # Handle case where data is not a dictionary
        if not isinstance(data, dict):
            return None

        # Handle API error responses
        if "errors" in data:
            return None

        # Process rencontres
        rencontres = (
            from_list(PouleRencontreItemModel.from_dict, data, "rencontres") or []
        )

        # Process classements
        classements_raw = from_list(TeamRanking.from_dict, data, "classements")
        classements = (
            [c for c in classements_raw if c is not None] if classements_raw else None
        )

        return cls(
            id=from_str(data, "id") or "",
            rencontres=rencontres,
            classements=classements,
            nom=from_str(data, "nom"),
            engagements=data.get("engagements"),  # Keep as is, it's a raw list
            id_competition=from_str(data, "id_competition"),
            date_created=from_str(data, "date_created"),
            date_updated=from_str(data, "date_updated"),
        )
