from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID

from ...models.cartographie import Cartographie
from ...models.labellisation_item import LabellisationItem
from ...models.membre import Membre
from ...models.offre_pratique import OffrePratique
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
class GetOrganismeResponse:
    id: str | None = None
    nom: str | None = None
    code: str | None = None
    telephone: str | None = None
    adresse: str | None = None
    mail: str | None = None
    type: str | None = None
    nom_simple: str | None = None
    url_site_web: str | None = None
    nom_club_pro: str | None = None
    adresse_club_pro: str | None = None
    commune_club_pro: str | None = None
    # FK-only fields (int IDs)
    commune: int | None = None
    salle: int | None = None
    saison: int | None = None
    organisme_id_pere: int | None = None
    # FK-only: logo (Directus file UUID)
    logo: UUID | None = None
    # FK-only: lists
    engagements: list[int | Any] = field(default_factory=list)
    competitions: list[int | Any] = field(default_factory=list)
    organismes_fils: list[int | Any] = field(default_factory=list)
    # Scalar fields
    date_affiliation: datetime | None = None
    entreprise: bool | None = None
    handibasket: bool | None = None
    hors_association: bool | None = None
    logo_base64: UUID | None = None
    omnisport: bool | None = None
    saison_en_cours: bool | None = None
    url_competition: str | None = None
    # Embedded
    cartographie: Cartographie | None = None
    membres: list[Membre] = field(default_factory=list)
    offres_pratiques: list[OffrePratique] = field(default_factory=list)
    labellisation: list[LabellisationItem] = field(default_factory=list)
    date_created: datetime | None = None
    date_updated: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetOrganismeResponse | None:
        """Convert dictionary to GetOrganismeResponse instance."""
        if not data:
            return None
        if not isinstance(data, dict):
            return None
        if "errors" in data:
            return None

        membres_raw = from_list(Membre.from_dict, data, "membres")
        offres_raw = from_list(OffrePratique.from_dict, data, "offresPratiques")
        labellisation_raw = from_list(
            LabellisationItem.from_dict, data, "labellisation"
        )
        engagements_raw = data.get("engagements", []) or []
        competitions_raw = data.get("competitions", []) or []
        organismes_fils_raw = data.get("organismes_fils", []) or []

        return cls(
            id=from_str(data, "id"),
            nom=from_str(data, "nom"),
            code=from_str(data, "code"),
            telephone=from_str(data, "telephone"),
            adresse=from_str(data, "adresse"),
            mail=from_str(data, "mail"),
            type=from_str(data, "type"),
            nom_simple=from_str(data, "nom_simple"),
            url_site_web=from_str(data, "urlSiteWeb"),
            nom_club_pro=from_str(data, "nomClubPro"),
            adresse_club_pro=from_str(data, "adresseClubPro"),
            commune_club_pro=from_str(data, "communeClubPro"),
            commune=from_int(data, "commune"),
            salle=from_int(data, "salle"),
            saison=from_int(data, "saison"),
            organisme_id_pere=from_int(data, "organisme_id_pere"),
            logo=from_uuid(data, "logo"),
            date_affiliation=from_datetime(data, "dateAffiliation"),
            entreprise=from_bool(data, "entreprise"),
            handibasket=from_bool(data, "handibasket"),
            hors_association=from_bool(data, "horsAssociation"),
            logo_base64=from_uuid(data, "logo_base64"),
            omnisport=from_bool(data, "omnisport"),
            saison_en_cours=from_bool(data, "saison_en_cours"),
            url_competition=from_str(data, "url_competition"),
            engagements=engagements_raw if isinstance(engagements_raw, list) else [],
            competitions=competitions_raw if isinstance(competitions_raw, list) else [],
            organismes_fils=(
                organismes_fils_raw if isinstance(organismes_fils_raw, list) else []
            ),
            cartographie=from_obj(Cartographie.from_dict, data, "cartographie"),
            membres=membres_raw if membres_raw is not None else [],
            offres_pratiques=offres_raw if offres_raw is not None else [],
            labellisation=labellisation_raw if labellisation_raw is not None else [],
            date_created=from_datetime(data, "date_created"),
            date_updated=from_datetime(data, "date_updated"),
        )
