from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_obj
from .logo import Logo


@dataclass
class OrganismeEquipe:
    """Organisme reference in a competition rencontre (carries logo only)."""

    logo: Logo | None = None

    @staticmethod
    def from_dict(obj: Any) -> OrganismeEquipe:
        assert isinstance(obj, dict)
        return OrganismeEquipe(
            logo=from_obj(Logo.from_dict, obj, "logo"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.logo is not None:
            result["logo"] = self.logo.to_dict()
        return result
