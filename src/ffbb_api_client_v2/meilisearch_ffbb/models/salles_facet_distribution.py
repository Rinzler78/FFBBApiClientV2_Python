from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...meilisearch.models.facet_distribution import FacetDistribution


@dataclass
class SallesFacetDistribution(FacetDistribution):
    type: dict[str, int] | None = None
    commune_code_postal: dict[str, int] | None = None
    commune_departement: dict[str, int] | None = None
    commune_libelle: dict[str, int] | None = None

    @staticmethod
    def from_dict(obj: Any) -> SallesFacetDistribution:
        assert isinstance(obj, dict)
        return SallesFacetDistribution(
            type=obj.get("type"),
            commune_code_postal=obj.get("commune.codePostal"),
            commune_departement=obj.get("commune.departement"),
            commune_libelle=obj.get("commune.libelle"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["type"] = self.type
        if self.commune_code_postal is not None:
            result["commune.codePostal"] = self.commune_code_postal
        if self.commune_departement is not None:
            result["commune.departement"] = self.commune_departement
        if self.commune_libelle is not None:
            result["commune.libelle"] = self.commune_libelle
        return result
