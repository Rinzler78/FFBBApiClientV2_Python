from __future__ import annotations

from dataclasses import dataclass

from ..utils.converter_utils import from_bool, from_float, from_int, from_obj, from_str
from .ranking_engagement import RankingEngagement


@dataclass
class TeamRanking:
    """Modèle pour un classement d'équipe."""

    # Required fields first
    id: str
    id_engagement: RankingEngagement | None
    position: int
    points: int
    match_joues: int
    gagnes: int
    perdus: int
    nombre_forfaits: int
    paniers_marques: int
    paniers_encaisses: int
    difference: int
    quotient: float
    # Optional fields with defaults
    nuls: int | None = None
    nombre_defauts: int | None = None
    point_initiaux: int | None = None
    penalites_arbitrage: int | None = None
    penalites_entraineur: int | None = None
    penalites_diverses: int | None = None
    hors_classement: bool | None = None
    # Relation fields
    organisme_id: str | None = None
    organisme_nom: str | None = None
    organisme_logo_id: str | None = None
    organisme_nom_simple: str | None = None
    id_competition: str | None = None
    id_poule: str | None = None
    id_poule_id: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> TeamRanking | None:
        """Convert dictionary to TeamRanking instance."""
        if not data:
            return None

        # Handle case where data is not a dictionary
        if not isinstance(data, dict):
            return None

        id_engagement = from_obj(RankingEngagement.from_dict, data, "idEngagement")

        # Handle organisme data
        organisme_data = data.get("organisme", {})
        if not isinstance(organisme_data, dict):
            organisme_data = {}
        organisme_id = from_str(organisme_data, "id")
        organisme_nom = from_str(organisme_data, "nom")
        organisme_nom_simple = from_str(organisme_data, "nom_simple")

        # Handle organisme logo
        organisme_logo_data = organisme_data.get("logo", {})
        if not isinstance(organisme_logo_data, dict):
            organisme_logo_data = {}
        organisme_logo_id = from_str(organisme_logo_data, "id")

        # Handle idPoule data
        id_poule_data = data.get("idPoule", {})
        if not isinstance(id_poule_data, dict):
            id_poule_data = {}
        id_poule_id = from_str(id_poule_data, "id")

        return cls(
            id=from_str(data, "id") or "",
            id_engagement=id_engagement,
            position=from_int(data, "position") or 0,
            points=from_int(data, "points") or 0,
            match_joues=from_int(data, "matchJoues") or 0,
            gagnes=from_int(data, "gagnes") or 0,
            perdus=from_int(data, "perdus") or 0,
            nuls=from_int(data, "nuls"),
            nombre_forfaits=from_int(data, "nombreForfaits") or 0,
            nombre_defauts=from_int(data, "nombreDefauts"),
            paniers_marques=from_int(data, "paniersMarques") or 0,
            paniers_encaisses=from_int(data, "paniersEncaisses") or 0,
            difference=from_int(data, "difference") or 0,
            quotient=from_float(data, "quotient") or 0.0,
            point_initiaux=from_int(data, "pointInitiaux"),
            penalites_arbitrage=from_int(data, "penalitesArbitrage"),
            penalites_entraineur=from_int(data, "penalitesEntraineur"),
            penalites_diverses=from_int(data, "penalitesDiverses"),
            hors_classement=from_bool(data, "horsClassement"),
            organisme_id=organisme_id,
            organisme_nom=organisme_nom,
            organisme_logo_id=organisme_logo_id,
            organisme_nom_simple=organisme_nom_simple,
            id_competition=from_str(data, "idCompetition"),
            id_poule=from_str(
                data, "idPoule"
            ),  # Note: this was str(dict), likely a bug, but keeping for now
            id_poule_id=id_poule_id,
        )
