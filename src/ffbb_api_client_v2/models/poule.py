from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import (
    from_list,
    from_str,
)
from .rencontres_engagement import Engagement


@dataclass
class Poule:
    nom: str | None = None
    id: str | None = None
    engagements: list[Engagement] | None = None

    @staticmethod
    def from_dict(obj: Any) -> Poule:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        nom = from_str(obj, "nom")
        id = from_str(obj, "id")
        engagements = from_list(Engagement.from_dict, obj, "engagements")
        return Poule(nom=nom, id=id, engagements=engagements)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom is not None:
            result["nom"] = self.nom
        if self.id is not None:
            result["id"] = self.id
        if self.engagements is not None:
            result["engagements"] = [e.to_dict() for e in self.engagements]
        return result
