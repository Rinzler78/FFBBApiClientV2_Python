from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ...models.cartographie import Cartographie
from ...models.commune import Commune
from ...models.labellisation_item import LabellisationItem
from ...models.logo import Logo
from ...models.membre import Membre
from ...models.offre_pratique import OffrePratique
from ...models.organisme_engagement import OrganismeEngagement
from ...models.salle import Salle
from ...utils.converter_utils import from_list, from_obj, from_str


@dataclass
class GetOrganismeResponse:
    id: str | None = None
    nom: str | None = None
    code: str | None = None
    telephone: str | None = None
    adresse: str | None = None
    mail: str | None = None
    type: str | None = None
    nom_simple: Any | None = None
    url_site_web: str | None = None
    nom_club_pro: str | None = None
    adresse_club_pro: Any | None = None
    commune: Commune | None = None
    cartographie: Cartographie | None = None
    commune_club_pro: Any | None = None
    membres: list[Membre] = field(default_factory=list)
    competitions: list[Any] = field(default_factory=list)
    engagements: list[OrganismeEngagement] = field(default_factory=list)
    organismes_fils: list[Any] = field(default_factory=list)
    offres_pratiques: list[OffrePratique] = field(default_factory=list)
    labellisation: list[LabellisationItem] = field(default_factory=list)
    salle: Salle | None = None
    logo: Logo | None = None

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
        engagements_raw = from_list(OrganismeEngagement.from_dict, data, "engagements")
        offres_raw = from_list(OffrePratique.from_dict, data, "offresPratiques")
        labellisation_raw = from_list(
            LabellisationItem.from_dict, data, "labellisation"
        )

        return cls(
            id=from_str(data, "id"),
            nom=from_str(data, "nom"),
            code=from_str(data, "code"),
            telephone=from_str(data, "telephone"),
            adresse=from_str(data, "adresse"),
            mail=from_str(data, "mail"),
            type=from_str(data, "type"),
            nom_simple=data.get("nom_simple"),
            url_site_web=from_str(data, "urlSiteWeb"),
            nom_club_pro=from_str(data, "nomClubPro"),
            adresse_club_pro=data.get("adresseClubPro"),
            commune=from_obj(Commune.from_dict, data, "commune"),
            cartographie=from_obj(Cartographie.from_dict, data, "cartographie"),
            commune_club_pro=data.get("communeClubPro"),
            membres=membres_raw if membres_raw is not None else [],
            competitions=data.get("competitions", []),
            engagements=engagements_raw if engagements_raw is not None else [],
            organismes_fils=data.get("organismes_fils", []),
            offres_pratiques=offres_raw if offres_raw is not None else [],
            labellisation=labellisation_raw if labellisation_raw is not None else [],
            salle=from_obj(Salle.from_dict, data, "salle"),
            logo=from_obj(Logo.from_dict, data, "logo"),
        )
