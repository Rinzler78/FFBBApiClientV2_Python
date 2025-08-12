from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_list, from_none, from_str, from_union, to_class
from .multi_search_result_rencontres import Engagement


class Poule:
    nom: str | None = None
    id: str | None = None
    engagements: list[Engagement] | None = None

    def __init__(
        self,
        nom: str | None,
        id: str | None,
        engagements: list[Engagement] | None,
    ):
        self.nom = nom
        self.id = id
        self.engagements = engagements

    @staticmethod
    def from_dict(obj: Any) -> Poule:
        assert isinstance(obj, dict)
        nom = from_union([from_str, from_none], obj.get("nom"))
        id = from_union([from_str, from_none], obj.get("id"))
        engagements = from_union(
            [lambda x: from_list(Engagement.from_dict, x), from_none],
            obj.get("engagements"),
        )
        return Poule(nom, id, engagements)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.engagements is not None:
            result["engagements"] = from_union(
                [lambda x: from_list(lambda x: to_class(Engagement, x), x), from_none],
                self.engagements,
            )
        return result
