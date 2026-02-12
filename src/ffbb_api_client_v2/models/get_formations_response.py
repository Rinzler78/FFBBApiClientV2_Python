from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..utils.converter_utils import from_float, from_int, from_str


@dataclass
class GetFormationsResponse:
    id: str
    title: str | None = None
    description: str | None = None
    mode: str | None = None
    level: str | None = None
    reference: str | None = None
    duration_hours: float | None = None
    certification: str | None = None
    status: str | None = None
    sort: int | None = None
    domain: dict[str, Any] | None = None
    theme: dict[str, Any] | None = None
    sessions: list[Any] = field(default_factory=list)
    public: str | None = None
    goals: str | None = None
    content: str | None = None
    pedagogy: str | None = None
    prerequisites: str | None = None
    results: str | None = None
    modalities: str | None = None
    image: dict[str, Any] | None = None
    files: list[Any] = field(default_factory=list)
    idOrigin: str | None = None
    idOriginHash: str | None = None
    programIdFbi: str | None = None
    date_created: str | None = None
    date_updated: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetFormationsResponse | None:
        """Convert dictionary to GetFormationsResponse instance."""
        if not data:
            return None
        if not isinstance(data, dict):
            return None
        if "errors" in data:
            return None

        return cls(
            id=from_str(data, "id") or "",
            title=from_str(data, "title"),
            description=from_str(data, "description"),
            mode=from_str(data, "mode"),
            level=from_str(data, "level"),
            reference=from_str(data, "reference"),
            duration_hours=from_float(data, "duration_hours"),
            certification=from_str(data, "certification"),
            status=from_str(data, "status"),
            sort=from_int(data, "sort"),
            domain=data.get("domain"),
            theme=data.get("theme"),
            sessions=data.get("sessions", []) or [],
            public=from_str(data, "public"),
            goals=from_str(data, "goals"),
            content=from_str(data, "content"),
            pedagogy=from_str(data, "pedagogy"),
            prerequisites=from_str(data, "prerequisites"),
            results=from_str(data, "results"),
            modalities=from_str(data, "modalities"),
            image=data.get("image"),
            files=data.get("files", []) or [],
            idOrigin=from_str(data, "idOrigin"),
            idOriginHash=from_str(data, "idOriginHash"),
            programIdFbi=from_str(data, "programIdFbi"),
            date_created=from_str(data, "date_created"),
            date_updated=from_str(data, "date_updated"),
        )

    @classmethod
    def from_list(cls, data_list: list[dict[str, Any]]) -> list[GetFormationsResponse]:
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
