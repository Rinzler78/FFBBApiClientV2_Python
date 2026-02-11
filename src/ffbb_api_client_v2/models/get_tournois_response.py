from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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
            id=str(data.get("id", "")),
            nom=str(data.get("nom", "")) if data.get("nom") else None,
            code=str(data.get("code", "")) if data.get("code") else None,
            sexe=str(data.get("sexe", "")) if data.get("sexe") else None,
            debut=str(data.get("debut", "")) if data.get("debut") else None,
            fin=str(data.get("fin", "")) if data.get("fin") else None,
            description=data.get("description"),
            adresse=(str(data.get("adresse", "")) if data.get("adresse") else None),
            adresseComplement=data.get("adresseComplement"),
            mailOrganisateur=data.get("mailOrganisateur"),
            nomOrganisateur=data.get("nomOrganisateur"),
            telephoneOrganisateur=data.get("telephoneOrganisateur"),
            urlOrganisateur=data.get("urlOrganisateur"),
            siteChoisi=data.get("siteChoisi"),
            nbParticipantPrevu=data.get("nbParticipantPrevu"),
            tarifOrganisateur=data.get("tarifOrganisateur"),
            ageMin=data.get("ageMin"),
            ageMax=data.get("ageMax"),
            tournoiType=data.get("tournoiType"),
            commune=data.get("commune"),
            cartographie=data.get("cartographie"),
            tournoiTypes3x3=data.get("tournoiTypes3x3", []) or [],
            document_flyer=data.get("document_flyer"),
            categorieChampionnat3x3Id=data.get("categorieChampionnat3x3Id"),
            categorieChampionnat3x3Libelle=data.get("categorieChampionnat3x3Libelle"),
            date_created=(
                str(data.get("date_created", "")) if data.get("date_created") else None
            ),
            date_updated=(
                str(data.get("date_updated", "")) if data.get("date_updated") else None
            ),
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
