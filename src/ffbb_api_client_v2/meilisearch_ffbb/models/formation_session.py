from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ...utils.converter_utils import from_datetime, from_str


@dataclass
class FormationSession:
    """A session within a formation (MeiliSearch denormalized data)."""

    id: str | None = None
    title: str | None = None
    date_start: datetime | None = None
    date_end: datetime | None = None
    place: str | None = None
    postal_code: str | None = None
    reference: str | None = None
    entity: str | None = None
    subscribe_btn: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> FormationSession:
        assert isinstance(obj, dict)
        return FormationSession(
            id=from_str(obj, "id"),
            title=from_str(obj, "title"),
            date_start=from_datetime(obj, "date_start"),
            date_end=from_datetime(obj, "date_end"),
            place=from_str(obj, "place"),
            postal_code=from_str(obj, "postal_code"),
            reference=from_str(obj, "reference"),
            entity=from_str(obj, "entity"),
            subscribe_btn=from_str(obj, "subscribeBtn"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.title is not None:
            result["title"] = self.title
        if self.date_start is not None:
            result["date_start"] = self.date_start.isoformat()
        if self.date_end is not None:
            result["date_end"] = self.date_end.isoformat()
        if self.place is not None:
            result["place"] = self.place
        if self.postal_code is not None:
            result["postal_code"] = self.postal_code
        if self.reference is not None:
            result["reference"] = self.reference
        if self.entity is not None:
            result["entity"] = self.entity
        if self.subscribe_btn is not None:
            result["subscribeBtn"] = self.subscribe_btn
        return result
