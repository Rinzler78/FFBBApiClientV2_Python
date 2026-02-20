from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ...models.cartographie import Cartographie
from ...models.document_flyer import DocumentFlyer
from ...utils.converter_utils import (
    from_datetime,
    from_int,
    from_obj,
    from_str,
)


@dataclass
class GetTournoisResponse:
    id: str
    nom: str | None = None
    code: str | None = None
    sexe: str | None = None
    debut: datetime | None = None
    fin: datetime | None = None
    description: str | None = None
    adresse: str | None = None
    adresseComplement: str | None = None
    mailOrganisateur: str | None = None
    nomOrganisateur: str | None = None
    telephoneOrganisateur: str | None = None
    urlOrganisateur: str | None = None
    siteChoisi: str | None = None
    nbParticipantPrevu: int | None = None
    tarifOrganisateur: int | None = None
    ageMin: int | None = None
    ageMax: int | None = None
    tournoiType: str | None = None
    commune: int | None = None
    cartographie: Cartographie | None = None
    tournoiTypes3x3: list[int] = field(default_factory=list)
    document_flyer: DocumentFlyer | None = None
    categorieChampionnat3x3Id: str | None = None
    categorieChampionnat3x3Libelle: str | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None

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
            debut=from_datetime(data, "debut"),
            fin=from_datetime(data, "fin"),
            description=data.get("description"),  # Keep as raw
            adresse=from_str(data, "adresse"),
            adresseComplement=data.get("adresseComplement"),  # Keep as raw
            mailOrganisateur=data.get("mailOrganisateur"),  # Keep as raw
            nomOrganisateur=data.get("nomOrganisateur"),  # Keep as raw
            telephoneOrganisateur=data.get("telephoneOrganisateur"),  # Keep as raw
            urlOrganisateur=data.get("urlOrganisateur"),  # Keep as raw
            siteChoisi=data.get("siteChoisi"),  # Keep as raw
            nbParticipantPrevu=from_int(data, "nbParticipantPrevu"),
            tarifOrganisateur=from_int(data, "tarifOrganisateur"),
            ageMin=from_int(data, "ageMin"),
            ageMax=from_int(data, "ageMax"),
            tournoiType=from_str(data, "tournoiType"),
            commune=from_int(data, "commune"),
            cartographie=from_obj(Cartographie.from_dict, data, "cartographie"),
            tournoiTypes3x3=[
                int(x) for x in (data.get("tournoiTypes3x3") or []) if x is not None
            ],
            document_flyer=from_obj(DocumentFlyer.from_dict, data, "document_flyer"),
            categorieChampionnat3x3Id=data.get(
                "categorieChampionnat3x3Id"
            ),  # Keep as raw
            categorieChampionnat3x3Libelle=data.get(
                "categorieChampionnat3x3Libelle"
            ),  # Keep as raw
            date_created=from_datetime(data, "date_created"),
            date_updated=from_datetime(data, "date_updated"),
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
