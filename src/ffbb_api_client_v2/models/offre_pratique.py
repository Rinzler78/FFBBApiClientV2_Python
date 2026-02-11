from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_obj, from_str


@dataclass
class OffrePratiqueDetail:
    """Detail of a practice offer (ffbbserver_offres_pratiques_id)."""

    id: str | None = None
    title: str | None = None
    categorie_pratique: str | None = None
    type_pratique: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> OffrePratiqueDetail:
        assert isinstance(obj, dict)
        return OffrePratiqueDetail(
            id=from_str(obj, "id"),
            title=from_str(obj, "title"),
            categorie_pratique=from_str(obj, "categoriePratique"),
            type_pratique=from_str(obj, "typePratique"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.title is not None:
            result["title"] = self.title
        if self.categorie_pratique is not None:
            result["categoriePratique"] = self.categorie_pratique
        if self.type_pratique is not None:
            result["typePratique"] = self.type_pratique
        return result


@dataclass
class OffrePratique:
    """Junction model linking an organisme to an offer detail."""

    ffbbserver_offres_pratiques_id: OffrePratiqueDetail | None = None

    @staticmethod
    def from_dict(obj: Any) -> OffrePratique:
        assert isinstance(obj, dict)
        return OffrePratique(
            ffbbserver_offres_pratiques_id=from_obj(
                OffrePratiqueDetail.from_dict, obj, "ffbbserver_offres_pratiques_id"
            ),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.ffbbserver_offres_pratiques_id is not None:
            result["ffbbserver_offres_pratiques_id"] = (
                self.ffbbserver_offres_pratiques_id.to_dict()
            )
        return result
