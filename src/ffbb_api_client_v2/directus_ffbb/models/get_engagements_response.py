from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID

from ...models.categorie import Categorie
from ...models.engagement_position import EngagementPosition
from ...models.team_ranking import TeamRanking
from ...utils.converter_utils import (
    from_bool,
    from_datetime,
    from_int,
    from_list,
    from_obj,
    from_str,
    from_uuid,
)


@dataclass
class GetEngagementsResponse:
    id: str
    nom: str | None = None
    nomEquipe: str | None = None
    nomUsuel: str | None = None
    nomOfficiel: str | None = None
    numeroEquipe: int | None = None
    codeAbrege: str | None = None
    clubPro: bool | None = None
    position: int | None = None
    positionVariation: int | None = None
    position_n1: int | None = None
    pouleId: str | None = None
    # FK-only fields (int IDs)
    idCompetition: int | None = None
    idOrganisme: int | None = None
    idOrganismeCtc: int | None = None
    idPoule: int | None = None
    entraineur: int | None = None
    entraineurAdjoint: int | None = None
    # FK-only: Directus file UUIDs
    logo: UUID | None = None
    logo_genius: UUID | None = None
    photo: UUID | None = None
    # FK-only: lists
    rencontres_domiciles: list[int | Any] = field(default_factory=list)
    rencontres_exterieur: list[int | Any] = field(default_factory=list)
    # Correspondant fields
    adresseCorrespondantEquipe: str | None = None
    complementAdresseCorrespondantEquipe: str | None = None
    communeCorrespondantEquipe: str | None = None
    emailCorrespondantEquipe: str | None = None
    nomCorrespondantEquipe: str | None = None
    telephoneFixeCorrespondantEquipe: str | None = None
    telephonePortableCorrespondantEquipe: str | None = None
    telephoneTravailCorrespondantEquipe: str | None = None
    # CTC fields
    nomCtc: str | None = None
    typeEntenteCtc: str | None = None
    # Other scalar fields
    toUpdate: bool | None = None
    url_competition: str | None = None
    # Embedded objects
    niveau: Categorie | None = None
    classement: list[TeamRanking] | None = None
    positions: list[EngagementPosition] = field(default_factory=list)
    date_created: datetime | None = None
    date_updated: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetEngagementsResponse | None:
        """Convert dictionary to GetEngagementsResponse instance."""
        if not data:
            return None
        if not isinstance(data, dict):
            return None
        if "errors" in data:
            return None

        domiciles_raw = data.get("rencontres_domiciles", []) or []
        exterieur_raw = data.get("rencontres_exterieur", []) or []
        classement_raw = from_list(TeamRanking.from_dict, data, "classement")

        return cls(
            id=from_str(data, "id") or "",
            nom=from_str(data, "nom"),
            nomEquipe=from_str(data, "nomEquipe"),
            nomUsuel=from_str(data, "nomUsuel"),
            nomOfficiel=from_str(data, "nomOfficiel"),
            numeroEquipe=from_int(data, "numeroEquipe"),
            codeAbrege=from_str(data, "codeAbrege"),
            clubPro=from_bool(data, "clubPro"),
            position=from_int(data, "position"),
            positionVariation=from_int(data, "positionVariation"),
            position_n1=from_int(data, "position_n1"),
            pouleId=from_str(data, "pouleId"),
            idCompetition=from_int(data, "idCompetition"),
            idOrganisme=from_int(data, "idOrganisme"),
            idOrganismeCtc=from_int(data, "idOrganismeCtc"),
            idPoule=from_int(data, "idPoule"),
            entraineur=from_int(data, "entraineur"),
            entraineurAdjoint=from_int(data, "entraineurAdjoint"),
            logo=from_uuid(data, "logo"),
            logo_genius=from_uuid(data, "logo_genius"),
            photo=from_uuid(data, "photo"),
            rencontres_domiciles=(
                domiciles_raw if isinstance(domiciles_raw, list) else []
            ),
            rencontres_exterieur=(
                exterieur_raw if isinstance(exterieur_raw, list) else []
            ),
            adresseCorrespondantEquipe=from_str(data, "adresseCorrespondantEquipe"),
            complementAdresseCorrespondantEquipe=from_str(
                data, "complementAdresseCorrespondantEquipe"
            ),
            communeCorrespondantEquipe=from_str(data, "communeCorrespondantEquipe"),
            emailCorrespondantEquipe=from_str(data, "emailCorrespondantEquipe"),
            nomCorrespondantEquipe=from_str(data, "nomCorrespondantEquipe"),
            telephoneFixeCorrespondantEquipe=from_str(
                data, "telephoneFixeCorrespondantEquipe"
            ),
            telephonePortableCorrespondantEquipe=from_str(
                data, "telephonePortableCorrespondantEquipe"
            ),
            telephoneTravailCorrespondantEquipe=from_str(
                data, "telephoneTravailCorrespondantEquipe"
            ),
            nomCtc=from_str(data, "nomCtc"),
            typeEntenteCtc=from_str(data, "typeEntenteCtc"),
            toUpdate=from_bool(data, "toUpdate"),
            url_competition=from_str(data, "url_competition"),
            niveau=from_obj(Categorie.from_dict, data, "niveau"),
            classement=(
                [c for c in classement_raw if c is not None] if classement_raw else None
            ),
            positions=from_list(EngagementPosition.from_dict, data, "positions") or [],
            date_created=from_datetime(data, "date_created"),
            date_updated=from_datetime(data, "date_updated"),
        )

    @classmethod
    def from_list(cls, data_list: list[dict[str, Any]]) -> list[GetEngagementsResponse]:
        """Convert list of dictionaries to list of instances."""
        if not data_list:
            return []
        return [
            result
            for item in data_list
            if item
            for result in [cls.from_dict(item)]
            if result is not None
        ]
