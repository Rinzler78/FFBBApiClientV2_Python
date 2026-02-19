from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from ...models.categorie import Categorie
from ...models.type_competition_generique import TypeCompetitionGenerique
from ...utils.converter_utils import from_bool, from_int, from_obj, from_str, from_uuid


@dataclass
class GetCompetitionResponse:
    id: str | None = None
    nom: str | None = None
    sexe: str | None = None
    code: str | None = None
    type_competition: str | None = None
    live_stat: bool | None = None
    publication_internet: str | None = None
    etat: str | None = None
    creation_en_cours: bool | None = None
    compare_old_site: bool | None = None
    emarque_v2: bool | None = None
    ordre: int | None = None
    pro: bool | None = None
    slug: str | None = None
    to_update: bool | None = None
    phase_code: str | None = None
    competition_origine_nom: str | None = None
    competition_origine_niveau: str | None = None
    # FK-only fields (int IDs)
    saison: int | None = None
    competition_origine: int | None = None
    id_competition_pere: int | None = None
    organisateur: int | None = None
    logo: UUID | None = None
    # FK-only: poules (list of int IDs)
    poules: list[int | Any] = field(default_factory=list)
    # Embedded
    categorie: Categorie | None = None
    type_competition_generique: TypeCompetitionGenerique | None = None
    phases: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetCompetitionResponse | None:
        """Convert dictionary to GetCompetitionResponse instance."""
        if not data:
            return None
        if not isinstance(data, dict):
            return None
        if "errors" in data:
            return None

        poules_raw = data.get("poules", []) or []
        phases_raw = data.get("phases", []) or []

        return cls(
            id=from_str(data, "id"),
            nom=from_str(data, "nom"),
            sexe=from_str(data, "sexe"),
            code=from_str(data, "code"),
            type_competition=from_str(data, "typeCompetition"),
            live_stat=from_bool(data, "liveStat"),
            publication_internet=from_str(data, "publicationInternet"),
            etat=from_str(data, "etat"),
            creation_en_cours=from_bool(data, "creationEnCours"),
            compare_old_site=from_bool(data, "compare_old_site"),
            emarque_v2=from_bool(data, "emarqueV2"),
            ordre=from_int(data, "ordre"),
            pro=from_bool(data, "pro"),
            slug=from_str(data, "slug"),
            to_update=from_bool(data, "toUpdate"),
            phase_code=from_str(data, "phase_code"),
            competition_origine_nom=from_str(data, "competition_origine_nom"),
            competition_origine_niveau=from_str(data, "competition_origine_niveau"),
            saison=from_int(data, "saison"),
            competition_origine=from_int(data, "competition_origine"),
            id_competition_pere=from_int(data, "idCompetitionPere"),
            organisateur=from_int(data, "organisateur"),
            logo=from_uuid(data, "logo"),
            poules=poules_raw if isinstance(poules_raw, list) else [],
            categorie=from_obj(Categorie.from_dict, data, "categorie"),
            type_competition_generique=from_obj(
                TypeCompetitionGenerique.from_dict, data, "typeCompetitionGenerique"
            ),
            phases=phases_raw if isinstance(phases_raw, list) else [],
        )
