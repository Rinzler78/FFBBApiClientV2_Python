from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...meilisearch.models.facet_distribution import FacetDistribution
from ...utils.converter_utils import from_obj
from .pratiques_type_class import PratiquesTypeClass


@dataclass
class PratiquesFacetDistribution(FacetDistribution):
    label: dict[str, int] | None = None
    type: PratiquesTypeClass | None = None

    @staticmethod
    def from_dict(obj: Any) -> PratiquesFacetDistribution:
        assert isinstance(obj, dict)
        label = obj.get("label")
        type = from_obj(PratiquesTypeClass.from_dict, obj, "type")
        return PratiquesFacetDistribution(label=label, type=type)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.label is not None:
            result["label"] = self.label
        if self.type is not None:
            result["type"] = self.type.to_dict()
        return result
