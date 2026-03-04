from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any

from ..utils.converter_utils import (
    from_bool,
    from_datetime,
    from_int,
    from_list,
    from_obj,
    from_str,
)
from .engagement_equipe import EngagementEquipe
from .game_stats_model import GameStatsModel
from .officiel import Officiel
from .organisme_equipe import OrganismeEquipe
from .salle import Salle


@dataclass
class CompetitionRencontre:
    id: str | None = None
    numero: str | None = None
    numero_journee: str | None = None
    id_poule: str | None = None
    competition_id: str | None = None
    resultat_equipe1: int | None = None
    resultat_equipe2: int | None = None
    joue: bool | None = None
    nom_equipe1: str | None = None
    nom_equipe2: str | None = None
    date_rencontre: datetime | None = None
    id_organisme_equipe1: OrganismeEquipe | None = None
    id_organisme_equipe2: OrganismeEquipe | None = None
    gs_id: GameStatsModel | None = None
    id_engagement_equipe1: EngagementEquipe | None = None
    id_engagement_equipe2: EngagementEquipe | None = None
    salle: Salle | None = None
    officiels: list[Officiel] = field(default_factory=list)

    @staticmethod
    def from_dict(obj: Any) -> CompetitionRencontre:
        assert isinstance(obj, dict)
        # Handle date_rencontre with fallback
        date_rencontre = from_datetime(obj, "date_rencontre")

        officiels_raw = from_list(Officiel.from_dict, obj, "officiels")
        return CompetitionRencontre(
            id=from_str(obj, "id"),
            numero=from_str(obj, "numero"),
            numero_journee=from_str(obj, "numeroJournee"),
            id_poule=from_str(obj, "idPoule"),
            competition_id=from_str(obj, "competitionId"),
            resultat_equipe1=from_int(obj, "resultatEquipe1"),
            resultat_equipe2=from_int(obj, "resultatEquipe2"),
            joue=from_bool(obj, "joue"),
            nom_equipe1=from_str(obj, "nomEquipe1"),
            nom_equipe2=from_str(obj, "nomEquipe2"),
            date_rencontre=date_rencontre,
            id_organisme_equipe1=from_obj(
                OrganismeEquipe.from_dict, obj, "idOrganismeEquipe1"
            ),
            id_organisme_equipe2=from_obj(
                OrganismeEquipe.from_dict, obj, "idOrganismeEquipe2"
            ),
            gs_id=from_obj(GameStatsModel.from_dict, obj, "gsId"),
            id_engagement_equipe1=from_obj(
                EngagementEquipe.from_dict, obj, "idEngagementEquipe1"
            ),
            id_engagement_equipe2=from_obj(
                EngagementEquipe.from_dict, obj, "idEngagementEquipe2"
            ),
            salle=from_obj(Salle.from_dict, obj, "salle"),
            officiels=officiels_raw if officiels_raw is not None else [],
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.numero is not None:
            result["numero"] = self.numero
        if self.numero_journee is not None:
            result["numeroJournee"] = self.numero_journee
        if self.id_poule is not None:
            result["idPoule"] = self.id_poule
        if self.competition_id is not None:
            result["competitionId"] = self.competition_id
        if self.resultat_equipe1 is not None:
            result["resultatEquipe1"] = self.resultat_equipe1
        if self.resultat_equipe2 is not None:
            result["resultatEquipe2"] = self.resultat_equipe2
        if self.joue is not None:
            result["joue"] = self.joue
        if self.nom_equipe1 is not None:
            result["nomEquipe1"] = self.nom_equipe1
        if self.nom_equipe2 is not None:
            result["nomEquipe2"] = self.nom_equipe2
        if self.date_rencontre is not None:
            result["date_rencontre"] = self.date_rencontre.isoformat()
        if self.id_organisme_equipe1 is not None:
            result["idOrganismeEquipe1"] = self.id_organisme_equipe1.to_dict()
        if self.id_organisme_equipe2 is not None:
            result["idOrganismeEquipe2"] = self.id_organisme_equipe2.to_dict()
        if self.gs_id is not None:
            result["gsId"] = asdict(self.gs_id)
        if self.id_engagement_equipe1 is not None:
            result["idEngagementEquipe1"] = self.id_engagement_equipe1.to_dict()
        if self.id_engagement_equipe2 is not None:
            result["idEngagementEquipe2"] = self.id_engagement_equipe2.to_dict()
        if self.salle is not None:
            result["salle"] = self.salle.to_dict()
        if self.officiels:
            result["officiels"] = [o.to_dict() for o in self.officiels]
        return result
