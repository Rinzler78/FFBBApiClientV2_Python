from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ...models.cartographie import Cartographie
from ...utils.converter_utils import (
    from_datetime,
    from_float,
    from_int,
    from_obj,
    from_str,
    from_timestamp,
)


@dataclass
class GetPratiquesResponse:
    id: str
    titre: str | None = None
    type: str | None = None
    label: str | None = None
    description: str | None = None
    code: str | None = None
    adresse: str | None = None
    email: str | None = None
    telephone: str | None = None
    date_debut: datetime | None = None
    date_fin: datetime | None = None
    horaires_seances: str | None = None
    jours: str | None = None
    nom_structure: str | None = None
    adresse_structure: str | None = None
    mail_structure: str | None = None
    nom_salle: str | None = None
    adresse_salle: str | None = None
    cp_salle: str | None = None
    ville_salle: str | None = None
    action: str | None = None
    affiche: str | None = None
    affiche_externe: str | None = None
    assurance: str | None = None
    date_demande: datetime | None = None
    date_inscription: datetime | None = None
    engagement: str | None = None
    inscriptions: str | None = None
    mail_demandeur: str | None = None
    nom_demandeur: str | None = None
    prenom_demandeur: str | None = None
    cartographie: Cartographie | None = None
    latitude: float | None = None
    longitude: float | None = None
    nombre_personnes: int | None = None
    nombre_seances: int | None = None
    public: str | None = None
    objectif: str | None = None
    site_web: str | None = None
    facebook: str | None = None
    twitter: str | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GetPratiquesResponse | None:
        """Convert dictionary to GetPratiquesResponse instance."""
        if not data:
            return None
        if not isinstance(data, dict):
            return None
        if "errors" in data:
            return None

        return cls(
            id=from_str(data, "id") or "",
            titre=from_str(data, "titre"),
            type=from_str(data, "type"),
            label=from_str(data, "label"),
            description=data.get("description"),  # Keep as raw
            code=from_str(data, "code"),
            adresse=data.get("adresse"),  # Keep as raw
            email=data.get("email"),  # Keep as raw
            telephone=data.get("telephone"),  # Keep as raw
            date_debut=from_datetime(data, "date_debut"),
            date_fin=from_datetime(data, "date_fin"),
            horaires_seances=data.get("horaires_seances"),  # Keep as raw
            jours=data.get("jours"),  # Keep as raw
            nom_structure=data.get("nom_structure"),  # Keep as raw
            adresse_structure=data.get("adresse_structure"),  # Keep as raw
            mail_structure=data.get("mail_structure"),  # Keep as raw
            nom_salle=data.get("nom_salle"),  # Keep as raw
            adresse_salle=data.get("adresse_salle"),  # Keep as raw
            cp_salle=data.get("cp_salle"),  # Keep as raw
            ville_salle=data.get("ville_salle"),  # Keep as raw
            action=data.get("action"),
            affiche=data.get("affiche"),
            affiche_externe=data.get("affiche_externe"),
            assurance=data.get("assurance"),
            date_demande=from_timestamp(data, "date_demande"),
            date_inscription=from_timestamp(data, "date_inscription"),
            engagement=data.get("engagement"),
            inscriptions=data.get("inscriptions"),
            mail_demandeur=data.get("mail_demandeur"),
            nom_demandeur=data.get("nom_demandeur"),
            prenom_demandeur=data.get("prenom_demandeur"),
            cartographie=from_obj(Cartographie.from_dict, data, "cartographie"),
            latitude=from_float(data, "latitude"),
            longitude=from_float(data, "longitude"),
            nombre_personnes=from_int(data, "nombre_personnes"),
            nombre_seances=from_int(data, "nombre_seances"),
            public=data.get("public"),  # Keep as raw
            objectif=data.get("objectif"),  # Keep as raw
            site_web=data.get("site_web"),  # Keep as raw
            facebook=data.get("facebook"),  # Keep as raw
            twitter=data.get("twitter"),  # Keep as raw
            date_created=from_datetime(data, "date_created"),
            date_updated=from_datetime(data, "date_updated"),
        )

    @classmethod
    def from_list(cls, data_list: list[dict[str, Any]]) -> list[GetPratiquesResponse]:
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
