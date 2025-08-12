from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_none, from_union, to_class
from .IDOrganismeEquipe1Logo import IDOrganismeEquipe1Logo


class CompetitionIDTypeCompetitionGenerique:
    logo: IDOrganismeEquipe1Logo | None = None

    def __init__(self, logo: IDOrganismeEquipe1Logo | None) -> None:
        self.logo = logo

    @staticmethod
    def from_dict(obj: Any) -> CompetitionIDTypeCompetitionGenerique:
        assert isinstance(obj, dict)
        logo = from_union(
            [IDOrganismeEquipe1Logo.from_dict, from_none], obj.get("logo")
        )
        return CompetitionIDTypeCompetitionGenerique(logo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.logo is not None:
            result["logo"] = from_union(
                [lambda x: to_class(IDOrganismeEquipe1Logo, x), from_none], self.logo
            )
        return result
