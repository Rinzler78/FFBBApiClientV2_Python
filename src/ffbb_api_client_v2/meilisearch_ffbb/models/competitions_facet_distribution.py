from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...meilisearch.models.facet_distribution import FacetDistribution
from ...models.competition_id_type_competition import CompetitionIDTypeCompetition
from ...models.niveau_class import NiveauClass
from ...models.sexe_class import SexeClass
from ...utils.converter_utils import from_obj


@dataclass
class CompetitionsFacetDistribution(FacetDistribution):
    competition_id_categorie_code: dict[str, int] | None = None
    competition_id_nom_extended: dict[str, int] | None = None
    competition_id_sexe: SexeClass | None = None
    competition_id_type_competition: CompetitionIDTypeCompetition | None = None
    niveau: NiveauClass | None = None
    organisateur_id: dict[str, int] | None = None
    organisateur_nom: dict[str, int] | None = None

    @staticmethod
    def from_dict(obj: Any) -> CompetitionsFacetDistribution:
        assert isinstance(obj, dict)
        competition_id_categorie_code = obj.get("competitionId.categorie.code")
        competition_id_nom_extended = obj.get("competitionId.nomExtended")
        competition_id_sexe = from_obj(SexeClass.from_dict, obj, "competitionId.sexe")
        competition_id_type_competition = from_obj(
            CompetitionIDTypeCompetition.from_dict, obj, "competitionId.typeCompetition"
        )
        niveau = from_obj(NiveauClass.from_dict, obj, "niveau")
        organisateur_id = obj.get("organisateur.id")
        organisateur_nom = obj.get("organisateur.nom")
        return CompetitionsFacetDistribution(
            competition_id_categorie_code=competition_id_categorie_code,
            competition_id_nom_extended=competition_id_nom_extended,
            competition_id_sexe=competition_id_sexe,
            competition_id_type_competition=competition_id_type_competition,
            niveau=niveau,
            organisateur_id=organisateur_id,
            organisateur_nom=organisateur_nom,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.competition_id_categorie_code is not None:
            result["competitionId.categorie.code"] = self.competition_id_categorie_code
        if self.competition_id_nom_extended is not None:
            result["competitionId.nomExtended"] = self.competition_id_nom_extended
        if self.competition_id_sexe is not None:
            result["competitionId.sexe"] = self.competition_id_sexe.to_dict()
        if self.competition_id_type_competition is not None:
            result["competitionId.typeCompetition"] = (
                self.competition_id_type_competition.to_dict()
            )
        if self.niveau is not None:
            result["niveau"] = self.niveau.to_dict()
        if self.organisateur_id is not None:
            result["organisateur.id"] = self.organisateur_id
        if self.organisateur_nom is not None:
            result["organisateur.nom"] = self.organisateur_nom
        return result
