from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...meilisearch.models.facet_distribution import FacetDistribution
from ...models.labellisation import Labellisation
from ...models.type_association_libelle import TypeAssociationLibelle
from ...models.type_class import TypeClass
from ...utils.converter_utils import from_obj


@dataclass
class OrganismesFacetDistribution(FacetDistribution):
    labellisation: Labellisation | None = None
    offres_pratiques: dict[str, int] | None = None
    type: TypeClass | None = None
    type_association_libelle: TypeAssociationLibelle | None = None

    @staticmethod
    def from_dict(obj: Any) -> OrganismesFacetDistribution:
        assert isinstance(obj, dict)
        labellisation = from_obj(Labellisation.from_dict, obj, "labellisation")
        offres_pratiques = obj.get("offresPratiques")
        type = from_obj(TypeClass.from_dict, obj, "type")
        type_association_libelle = from_obj(
            TypeAssociationLibelle.from_dict, obj, "type_association.libelle"
        )
        return OrganismesFacetDistribution(
            labellisation=labellisation,
            offres_pratiques=offres_pratiques,
            type=type,
            type_association_libelle=type_association_libelle,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.labellisation is not None:
            result["labellisation"] = self.labellisation.to_dict()
        if self.offres_pratiques is not None:
            result["offresPratiques"] = self.offres_pratiques
        if self.type is not None:
            result["type"] = self.type.to_dict()
        if self.type_association_libelle is not None:
            result["type_association.libelle"] = self.type_association_libelle.to_dict()
        return result
