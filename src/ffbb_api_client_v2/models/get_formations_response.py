from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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
            id=str(data.get("id", "")),
            title=str(data.get("title", "")) if data.get("title") else None,
            description=data.get("description"),
            mode=str(data.get("mode", "")) if data.get("mode") else None,
            level=data.get("level"),
            reference=data.get("reference"),
            duration_hours=data.get("duration_hours"),
            certification=data.get("certification"),
            status=data.get("status"),
            sort=data.get("sort"),
            domain=data.get("domain"),
            theme=data.get("theme"),
            sessions=data.get("sessions", []) or [],
            public=data.get("public"),
            goals=data.get("goals"),
            content=data.get("content"),
            pedagogy=data.get("pedagogy"),
            prerequisites=data.get("prerequisites"),
            results=data.get("results"),
            modalities=data.get("modalities"),
            image=data.get("image"),
            files=data.get("files", []) or [],
            idOrigin=data.get("idOrigin"),
            idOriginHash=data.get("idOriginHash"),
            programIdFbi=data.get("programIdFbi"),
            date_created=(
                str(data.get("date_created", "")) if data.get("date_created") else None
            ),
            date_updated=(
                str(data.get("date_updated", "")) if data.get("date_updated") else None
            ),
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
