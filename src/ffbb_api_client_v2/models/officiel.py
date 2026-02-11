from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_int, from_obj
from .fonction import Fonction
from .officiel_personne import OfficielPersonne


@dataclass
class Officiel:
    """Official in a competition rencontre."""

    ordre: int | None = None
    fonction: Fonction | None = None
    officiel: OfficielPersonne | None = None

    @staticmethod
    def from_dict(obj: Any) -> Officiel:
        assert isinstance(obj, dict)
        return Officiel(
            ordre=from_int(obj, "ordre"),
            fonction=from_obj(Fonction.from_dict, obj, "fonction"),
            officiel=from_obj(OfficielPersonne.from_dict, obj, "officiel"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.ordre is not None:
            result["ordre"] = self.ordre
        if self.fonction is not None:
            result["fonction"] = self.fonction.to_dict()
        if self.officiel is not None:
            result["officiel"] = self.officiel.to_dict()
        return result
