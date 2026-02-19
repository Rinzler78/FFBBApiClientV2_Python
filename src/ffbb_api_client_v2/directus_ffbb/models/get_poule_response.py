from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ...models.team_ranking import TeamRanking
from ...utils.converter_utils import from_datetime, from_int, from_list, from_str


@dataclass
class GetPouleResponse:
    id: str
    nom: str | None = None
    # FK-only fields
    id_competition: int | None = None
    # FK-only: lists
    rencontres: list[int | Any] = field(default_factory=list)
    engagements: list[int | Any] = field(default_factory=list)
    # Embedded
    classements: list[TeamRanking] | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetPouleResponse | None:
        """Convert dictionary to GetPouleResponse instance."""
        if not data:
            return None
        if not isinstance(data, dict):
            return None
        if "errors" in data:
            return None

        classements_raw = from_list(TeamRanking.from_dict, data, "classements")
        classements = (
            [c for c in classements_raw if c is not None] if classements_raw else None
        )
        rencontres_raw = data.get("rencontres", []) or []
        engagements_raw = data.get("engagements", []) or []

        return cls(
            id=from_str(data, "id") or "",
            nom=from_str(data, "nom"),
            id_competition=from_int(data, "id_competition"),
            rencontres=rencontres_raw if isinstance(rencontres_raw, list) else [],
            engagements=engagements_raw if isinstance(engagements_raw, list) else [],
            classements=classements,
            date_created=from_datetime(data, "date_created"),
            date_updated=from_datetime(data, "date_updated"),
        )
