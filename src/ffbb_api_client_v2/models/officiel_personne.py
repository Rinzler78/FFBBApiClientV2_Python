from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_str


@dataclass
class OfficielPersonne:
    nom: str | None = None
    prenom: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> OfficielPersonne:
        assert isinstance(obj, dict)
        return OfficielPersonne(
            nom=from_str(obj, "nom"),
            prenom=from_str(obj, "prenom"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom is not None:
            result["nom"] = self.nom
        if self.prenom is not None:
            result["prenom"] = self.prenom
        return result
