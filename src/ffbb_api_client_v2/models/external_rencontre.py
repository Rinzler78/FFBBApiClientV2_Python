from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import (
    from_int,
    from_obj,
    from_str,
)
from .salle import Salle


@dataclass
class ExternalRencontre:
    nom_equipe1: str | None = None
    nom_equipe2: str | None = None
    numero_journee: int | None = None
    competition_id: str | None = None
    id_organisme_equipe1: str | None = None
    id_organisme_equipe2: str | None = None
    salle: Salle | None = None
    id_poule: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> ExternalRencontre:
        assert isinstance(obj, dict)
        return ExternalRencontre(
            nom_equipe1=from_str(obj, "nomEquipe1"),
            nom_equipe2=from_str(obj, "nomEquipe2"),
            numero_journee=from_int(obj, "numeroJournee"),
            competition_id=from_str(obj, "competitionId"),
            id_organisme_equipe1=from_str(obj, "idOrganismeEquipe1"),
            id_organisme_equipe2=from_str(obj, "idOrganismeEquipe2"),
            salle=from_obj(Salle.from_dict, obj, "salle"),
            id_poule=from_str(obj, "idPoule"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom_equipe1 is not None:
            result["nomEquipe1"] = self.nom_equipe1
        if self.nom_equipe2 is not None:
            result["nomEquipe2"] = self.nom_equipe2
        if self.numero_journee is not None:
            result["numeroJournee"] = str(self.numero_journee)
        if self.competition_id is not None:
            result["competitionId"] = self.competition_id
        if self.id_organisme_equipe1 is not None:
            result["idOrganismeEquipe1"] = self.id_organisme_equipe1
        if self.id_organisme_equipe2 is not None:
            result["idOrganismeEquipe2"] = self.id_organisme_equipe2
        if self.salle is not None:
            result["salle"] = self.salle.to_dict()
        if self.id_poule is not None:
            result["idPoule"] = self.id_poule
        return result
