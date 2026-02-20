from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from ...models.folder import Folder
from ...utils.converter_utils import (
    from_datetime,
    from_duration,
    from_int,
    from_obj,
    from_str,
    from_uuid,
)


@dataclass
class GetFormationsResponse:
    id: str
    title: str | None = None
    description: str | None = None
    mode: str | None = None
    level: str | None = None
    reference: str | None = None
    duration_hours: timedelta | None = None
    certification: str | None = None
    status: str | None = None
    sort: int | None = None
    domain: Folder | None = None
    theme: Folder | None = None
    sessions: list[str] = field(default_factory=list)
    public: str | None = None
    goals: str | None = None
    content: str | None = None
    pedagogy: str | None = None
    prerequisites: str | None = None
    results: str | None = None
    modalities: str | None = None
    image: UUID | None = None
    files: list[Any] = field(default_factory=list)
    user_created: UUID | None = None
    user_updated: UUID | None = None
    idOrigin: str | None = None
    idOriginHash: str | None = None
    programIdFbi: str | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None

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
            duration_hours=from_duration(data, "duration_hours"),
            certification=from_str(data, "certification"),
            status=from_str(data, "status"),
            sort=from_int(data, "sort"),
            domain=from_obj(Folder.from_dict, data, "domain"),
            theme=from_obj(Folder.from_dict, data, "theme"),
            sessions=[str(x) for x in (data.get("sessions") or []) if x is not None],
            public=from_str(data, "public"),
            goals=from_str(data, "goals"),
            content=from_str(data, "content"),
            pedagogy=from_str(data, "pedagogy"),
            prerequisites=from_str(data, "prerequisites"),
            results=from_str(data, "results"),
            modalities=from_str(data, "modalities"),
            image=from_uuid(data, "image"),
            files=data.get("files", []) or [],
            user_created=from_uuid(data, "user_created"),
            user_updated=from_uuid(data, "user_updated"),
            idOrigin=from_str(data, "idOrigin"),
            idOriginHash=from_str(data, "idOriginHash"),
            programIdFbi=from_str(data, "programIdFbi"),
            date_created=from_datetime(data, "date_created"),
            date_updated=from_datetime(data, "date_updated"),
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
