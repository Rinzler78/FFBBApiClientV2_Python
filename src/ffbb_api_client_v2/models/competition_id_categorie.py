from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_categorie_code, from_int, from_str
from .categorie_code import CategorieCode


@dataclass
class CompetitionIDCategorie:
    code: CategorieCode | None = None
    libelle: str | None = None
    ordre: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> CompetitionIDCategorie:
        assert isinstance(obj, dict)
        code = from_categorie_code(obj, "code")
        libelle = from_str(obj, "libelle")
        ordre = from_int(obj, "ordre")
        return CompetitionIDCategorie(code=code, libelle=libelle, ordre=ordre)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = self.code
        if self.libelle is not None:
            result["libelle"] = self.libelle
        if self.ordre is not None:
            result["ordre"] = self.ordre
        return result
