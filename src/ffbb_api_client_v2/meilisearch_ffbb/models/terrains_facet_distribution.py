from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...meilisearch.models.facet_distribution import FacetDistribution
from ...models.sexe_class import SexeClass
from ...models.tournoi_type_class import TournoiTypeClass
from ...models.tournoi_types_3x3_libelle import TournoiTypes3X3Libelle
from ...utils.converter_utils import from_obj


@dataclass
class TerrainsFacetDistribution(FacetDistribution):
    sexe: SexeClass | None = None
    tournoi_type: TournoiTypeClass | None = None
    tournoi_types3_x3_libelle: TournoiTypes3X3Libelle | None = None

    @staticmethod
    def from_dict(obj: Any) -> TerrainsFacetDistribution:
        assert isinstance(obj, dict)
        sexe = from_obj(SexeClass.from_dict, obj, "sexe")
        tournoi_type = from_obj(TournoiTypeClass.from_dict, obj, "tournoiType")
        tournoi_types3_x3_libelle = from_obj(
            TournoiTypes3X3Libelle.from_dict, obj, "tournoiTypes3x3.libelle"
        )
        return TerrainsFacetDistribution(
            sexe=sexe,
            tournoi_type=tournoi_type,
            tournoi_types3_x3_libelle=tournoi_types3_x3_libelle,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.sexe is not None:
            result["sexe"] = self.sexe.to_dict()
        if self.tournoi_type is not None:
            result["tournoiType"] = self.tournoi_type.to_dict()
        if self.tournoi_types3_x3_libelle is not None:
            result["tournoiTypes3x3.libelle"] = self.tournoi_types3_x3_libelle.to_dict()
        return result
