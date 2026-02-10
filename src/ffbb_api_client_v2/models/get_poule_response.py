from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .poule_rencontre_item_model import PouleRencontreItemModel
from .team_ranking import TeamRanking


@dataclass
class GetPouleResponse:
    id: str

    # Keep nested alias for backward compatibility
    RencontresitemModel = PouleRencontreItemModel

    rencontres: list[PouleRencontreItemModel]
    classements: list[TeamRanking] | None = None
    nom: str | None = None
    engagements: list[dict[str, Any]] | None = None
    id_competition: str | None = None
    date_created: str | None = None
    date_updated: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetPouleResponse | None:
        """Convert dictionary to PoulesModel instance."""
        if not data:
            return None

        # Handle case where data is not a dictionary
        if not isinstance(data, dict):
            return None

        # Handle API error responses
        if "errors" in data:
            return None

        # Basic implementation - can be expanded later
        rencontres = []
        for rencontre_data in data.get("rencontres", []):
            if rencontre_data:
                rencontre = PouleRencontreItemModel(
                    id=str(rencontre_data.get("id", "")),
                    numero=str(rencontre_data.get("numero", "")),
                    numeroJournee=str(rencontre_data.get("numeroJournee", "")),
                    idPoule=str(rencontre_data.get("idPoule", "")),
                    competitionId=str(rencontre_data.get("competitionId", "")),
                    resultatEquipe1=str(rencontre_data.get("resultatEquipe1", "")),
                    resultatEquipe2=str(rencontre_data.get("resultatEquipe2", "")),
                    joue=int(rencontre_data.get("joue", 0)),
                    nomEquipe1=str(rencontre_data.get("nomEquipe1", "")),
                    nomEquipe2=str(rencontre_data.get("nomEquipe2", "")),
                    date_rencontre=datetime.fromisoformat(
                        rencontre_data.get("date_rencontre", "1970-01-01")
                    ),
                )
                rencontres.append(rencontre)

        # Process classements
        classements = []
        for classement_data in data.get("classements", []):
            if classement_data:
                classement = TeamRanking.from_dict(classement_data)
                if classement:
                    classements.append(classement)

        return cls(
            id=str(data.get("id", "")),
            rencontres=rencontres,
            classements=classements if classements else None,
            nom=str(data.get("nom", "")) if data.get("nom") else None,
            engagements=data.get("engagements") if data.get("engagements") else None,
            id_competition=(
                str(data.get("id_competition", ""))
                if data.get("id_competition")
                else None
            ),
            date_created=(
                str(data.get("date_created", "")) if data.get("date_created") else None
            ),
            date_updated=(
                str(data.get("date_updated", "")) if data.get("date_updated") else None
            ),
        )
