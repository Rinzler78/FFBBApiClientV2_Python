from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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
    date_debut: str | None = None
    date_fin: str | None = None
    horaires_seances: str | None = None
    jours: str | None = None
    nom_structure: str | None = None
    adresse_structure: str | None = None
    mail_structure: str | None = None
    nom_salle: str | None = None
    adresse_salle: str | None = None
    cp_salle: str | None = None
    ville_salle: str | None = None
    cartographie: dict[str, Any] | None = None
    latitude: float | None = None
    longitude: float | None = None
    nombre_personnes: int | None = None
    nombre_seances: int | None = None
    public: str | None = None
    objectif: str | None = None
    site_web: str | None = None
    facebook: str | None = None
    twitter: str | None = None
    date_created: str | None = None
    date_updated: str | None = None

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
            id=str(data.get("id", "")),
            titre=str(data.get("titre", "")) if data.get("titre") else None,
            type=str(data.get("type", "")) if data.get("type") else None,
            label=str(data.get("label", "")) if data.get("label") else None,
            description=data.get("description"),
            code=str(data.get("code", "")) if data.get("code") else None,
            adresse=data.get("adresse"),
            email=data.get("email"),
            telephone=data.get("telephone"),
            date_debut=(
                str(data.get("date_debut", "")) if data.get("date_debut") else None
            ),
            date_fin=(str(data.get("date_fin", "")) if data.get("date_fin") else None),
            horaires_seances=data.get("horaires_seances"),
            jours=data.get("jours"),
            nom_structure=data.get("nom_structure"),
            adresse_structure=data.get("adresse_structure"),
            mail_structure=data.get("mail_structure"),
            nom_salle=data.get("nom_salle"),
            adresse_salle=data.get("adresse_salle"),
            cp_salle=data.get("cp_salle"),
            ville_salle=data.get("ville_salle"),
            cartographie=data.get("cartographie"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            nombre_personnes=data.get("nombre_personnes"),
            nombre_seances=data.get("nombre_seances"),
            public=data.get("public"),
            objectif=data.get("objectif"),
            site_web=data.get("site_web"),
            facebook=data.get("facebook"),
            twitter=data.get("twitter"),
            date_created=(
                str(data.get("date_created", "")) if data.get("date_created") else None
            ),
            date_updated=(
                str(data.get("date_updated", "")) if data.get("date_updated") else None
            ),
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
