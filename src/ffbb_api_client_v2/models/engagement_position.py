from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ..utils.converter_utils import from_datetime, from_str


@dataclass
class EngagementPosition:
    """Position snapshot for an engagement at a given date."""

    position: str | None = None
    key: str | None = None
    date: datetime | None = None

    @staticmethod
    def from_dict(obj: Any) -> EngagementPosition:
        assert isinstance(obj, dict)
        return EngagementPosition(
            position=from_str(obj, "position"),
            key=from_str(obj, "key"),
            date=from_datetime(obj, "date"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.position is not None:
            result["position"] = self.position
        if self.key is not None:
            result["key"] = self.key
        if self.date is not None:
            result["date"] = self.date.isoformat()
        return result
