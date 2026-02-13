from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...meilisearch.models.facet_distribution import FacetDistribution
from ...models.sexe_class import SexeClass
from ...utils.converter_utils import from_obj


@dataclass
class EngagementsFacetDistribution(FacetDistribution):
    club_pro: dict[str, int] | None = None
    id_competition_categorie_code: dict[str, int] | None = None
    id_competition_categorie_libelle: dict[str, int] | None = None
    id_competition_code: dict[str, int] | None = None
    id_competition_nom: dict[str, int] | None = None
    id_competition_sexe: SexeClass | None = None
    id_poule_nom: dict[str, int] | None = None
    niveau_code: dict[str, int] | None = None
    niveau_libelle: dict[str, int] | None = None

    @staticmethod
    def from_dict(obj: Any) -> EngagementsFacetDistribution:
        assert isinstance(obj, dict)
        club_pro = obj.get("clubPro")
        id_competition_categorie_code = obj.get("idCompetition.categorie.code")
        id_competition_categorie_libelle = obj.get("idCompetition.categorie.libelle")
        id_competition_code = obj.get("idCompetition.code")
        id_competition_nom = obj.get("idCompetition.nom")
        id_competition_sexe = from_obj(SexeClass.from_dict, obj, "idCompetition.sexe")
        id_poule_nom = obj.get("idPoule.nom")
        niveau_code = obj.get("niveau.code")
        niveau_libelle = obj.get("niveau.libelle")
        return EngagementsFacetDistribution(
            club_pro=club_pro,
            id_competition_categorie_code=id_competition_categorie_code,
            id_competition_categorie_libelle=id_competition_categorie_libelle,
            id_competition_code=id_competition_code,
            id_competition_nom=id_competition_nom,
            id_competition_sexe=id_competition_sexe,
            id_poule_nom=id_poule_nom,
            niveau_code=niveau_code,
            niveau_libelle=niveau_libelle,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.club_pro is not None:
            result["clubPro"] = self.club_pro
        if self.id_competition_categorie_code is not None:
            result["idCompetition.categorie.code"] = self.id_competition_categorie_code
        if self.id_competition_categorie_libelle is not None:
            result["idCompetition.categorie.libelle"] = (
                self.id_competition_categorie_libelle
            )
        if self.id_competition_code is not None:
            result["idCompetition.code"] = self.id_competition_code
        if self.id_competition_nom is not None:
            result["idCompetition.nom"] = self.id_competition_nom
        if self.id_competition_sexe is not None:
            result["idCompetition.sexe"] = self.id_competition_sexe.to_dict()
        if self.id_poule_nom is not None:
            result["idPoule.nom"] = self.id_poule_nom
        if self.niveau_code is not None:
            result["niveau.code"] = self.niveau_code
        if self.niveau_libelle is not None:
            result["niveau.libelle"] = self.niveau_libelle
        return result
