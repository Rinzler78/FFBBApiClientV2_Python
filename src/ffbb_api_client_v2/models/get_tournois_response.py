from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..utils.converter_utils import (
    from_int,
    from_str,
)


@dataclass
class GetTournoisResponse:
    id: str
    nom: str | None = None
    code: str | None = None
    sexe: str | None = None
    debut: str | None = None
    fin: str | None = None
    description: str | None = None
    adresse: str | None = None
    adresseComplement: str | None = None
    mailOrganisateur: str | None = None
    nomOrganisateur: str | None = None
    telephoneOrganisateur: str | None = None
    urlOrganisateur: str | None = None
    siteChoisi: str | None = None
    nbParticipantPrevu: int | None = None
    tarifOrganisateur: str | None = None
    ageMin: int | None = None
    ageMax: int | None = None
    tournoiType: dict[str, Any] | None = None
    commune: dict[str, Any] | None = None
    cartographie: dict[str, Any] | None = None
    tournoiTypes3x3: list[Any] = field(default_factory=list)
    document_flyer: dict[str, Any] | None = None
    categorieChampionnat3x3Id: str | None = None
    categorieChampionnat3x3Libelle: str | None = None
    date_created: str | None = None
    date_updated: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetTournoisResponse | None:
        """Convert dictionary to GetTournoisResponse instance."""
        if not data:
            return None
        if not isinstance(data, dict):
            return None
        if "errors" in data:
            return None

        return cls(
            id=from_str(data, "id") or "",
            nom=from_str(data, "nom"),
            code=from_str(data, "code"),
            sexe=from_str(data, "sexe"),
            debut=from_str(data, "debut"),
            fin=from_str(data, "fin"),
            description=data.get("description"),  # Keep as raw
            adresse=from_str(data, "adresse"),
            adresseComplement=data.get("adresseComplement"),  # Keep as raw
            mailOrganisateur=data.get("mailOrganisateur"),  # Keep as raw
            nomOrganisateur=data.get("nomOrganisateur"),  # Keep as raw
            telephoneOrganisateur=data.get("telephoneOrganisateur"),  # Keep as raw
            urlOrganisateur=data.get("urlOrganisateur"),  # Keep as raw
            siteChoisi=data.get("siteChoisi"),  # Keep as raw
            nbParticipantPrevu=from_int(data, "nbParticipantPrevu"),
            tarifOrganisateur=data.get("tarifOrganisateur"),  # Keep as raw
            ageMin=from_int(data, "ageMin"),
            ageMax=from_int(data, "ageMax"),
            tournoiType=data.get("tournoiType"),  # Keep as raw dict
            commune=data.get("commune"),  # Keep as raw dict
            cartographie=data.get("cartographie"),  # Keep as raw dict
            tournoiTypes3x3=data.get("tournoiTypes3x3", []) or [],
            document_flyer=data.get("document_flyer"),  # Keep as raw dict
            categorieChampionnat3x3Id=data.get(
                "categorieChampionnat3x3Id"
            ),  # Keep as raw
            categorieChampionnat3x3Libelle=data.get(
                "categorieChampionnat3x3Libelle"
            ),  # Keep as raw
            date_created=from_str(data, "date_created"),
            date_updated=from_str(data, "date_updated"),
        )

    @classmethod
    def from_list(cls, data_list: list[dict[str, Any]]) -> list[GetTournoisResponse]:
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
