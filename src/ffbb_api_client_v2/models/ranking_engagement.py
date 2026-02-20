from __future__ import annotations

from dataclasses import dataclass

from ..utils.converter_utils import from_int, from_str


@dataclass
class RankingEngagement:
    """Modèle pour l'engagement d'une équipe dans un classement."""

    id: str
    nom: str
    nom_usuel: str | None = None
    code_abrege: str | None = None
    numero_equ: int | None = None
    numero_equipe: int | None = None
    logo_id: str | None = None
    logo_gradient: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> RankingEngagement | None:
        """Convert dictionary to RankingEngagement instance."""
        if not data:
            return None

        # Handle logo data
        logo_data = data.get("logo", {})
        if not isinstance(logo_data, dict):
            logo_data = {}
        logo_id = from_str(logo_data, "id")
        logo_gradient = from_str(logo_data, "gradient_color")

        return cls(
            id=from_str(data, "id") or "",
            nom=from_str(data, "nom") or "",
            nom_usuel=from_str(data, "nomUsuel"),
            code_abrege=from_str(data, "codeAbrege"),
            numero_equ=from_int(data, "numeroEqu"),
            numero_equipe=from_int(data, "numeroEquipe"),
            logo_id=logo_id,
            logo_gradient=logo_gradient,
        )
