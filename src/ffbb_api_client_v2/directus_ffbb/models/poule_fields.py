from .query_fields_manager import QueryFieldsManager


class PouleFields(QueryFieldsManager):
    """Fields for poule queries."""

    # Basic fields
    ID = "id"
    NOM = "nom"

    # FK-only fields
    ID_COMPETITION = "id_competition"

    # FK-only: lists
    RENCONTRES = "rencontres"
    ENGAGEMENTS = "engagements"

    # Embedded: classements (scalar fields)
    CLASSEMENTS_ID = "classements.id"
    CLASSEMENTS_POSITION = "classements.position"
    CLASSEMENTS_POINTS = "classements.points"
    CLASSEMENTS_MATCH_JOUES = "classements.matchJoues"
    CLASSEMENTS_GAGNES = "classements.gagnes"
    CLASSEMENTS_PERDUS = "classements.perdus"
    CLASSEMENTS_NULS = "classements.nuls"
    CLASSEMENTS_NOMBRE_FORFAITS = "classements.nombreForfaits"
    CLASSEMENTS_NOMBRE_DEFAUTS = "classements.nombreDefauts"
    CLASSEMENTS_PANIERS_MARQUES = "classements.paniersMarques"
    CLASSEMENTS_PANIERS_ENCAISSES = "classements.paniersEncaisses"
    CLASSEMENTS_DIFFERENCE = "classements.difference"
    CLASSEMENTS_QUOTIENT = "classements.quotient"
    CLASSEMENTS_POINT_INITIAUX = "classements.pointInitiaux"
    CLASSEMENTS_PENALITES_ARBITRAGE = "classements.penalitesArbitrage"
    CLASSEMENTS_PENALITES_ENTRAINEUR = "classements.penalitesEntraineur"
    CLASSEMENTS_PENALITES_DIVERSES = "classements.penalitesDiverses"
    CLASSEMENTS_HORS_CLASSEMENT = "classements.horsClassement"
    CLASSEMENTS_ORGANISME_NOM = "classements.organisme_nom"
    # Embedded: classements FK-only nested
    CLASSEMENTS_ID_ENGAGEMENT = "classements.idEngagement"
    CLASSEMENTS_ORGANISME = "classements.organisme"
    CLASSEMENTS_ID_COMPETITION = "classements.idCompetition"
    CLASSEMENTS_ID_POULE = "classements.idPoule"

    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_fields(cls) -> list[str]:
        """Return the complete list of fields for poule queries."""
        return [
            # Basic fields
            cls.ID,
            cls.NOM,
            # FK-only
            cls.ID_COMPETITION,
            cls.RENCONTRES,
            cls.ENGAGEMENTS,
            # Classements scalars
            cls.CLASSEMENTS_ID,
            cls.CLASSEMENTS_POSITION,
            cls.CLASSEMENTS_POINTS,
            cls.CLASSEMENTS_MATCH_JOUES,
            cls.CLASSEMENTS_GAGNES,
            cls.CLASSEMENTS_PERDUS,
            cls.CLASSEMENTS_NULS,
            cls.CLASSEMENTS_NOMBRE_FORFAITS,
            cls.CLASSEMENTS_NOMBRE_DEFAUTS,
            cls.CLASSEMENTS_PANIERS_MARQUES,
            cls.CLASSEMENTS_PANIERS_ENCAISSES,
            cls.CLASSEMENTS_DIFFERENCE,
            cls.CLASSEMENTS_QUOTIENT,
            cls.CLASSEMENTS_POINT_INITIAUX,
            cls.CLASSEMENTS_PENALITES_ARBITRAGE,
            cls.CLASSEMENTS_PENALITES_ENTRAINEUR,
            cls.CLASSEMENTS_PENALITES_DIVERSES,
            cls.CLASSEMENTS_HORS_CLASSEMENT,
            cls.CLASSEMENTS_ORGANISME_NOM,
            # Classements FK-only nested
            cls.CLASSEMENTS_ID_ENGAGEMENT,
            cls.CLASSEMENTS_ORGANISME,
            cls.CLASSEMENTS_ID_COMPETITION,
            cls.CLASSEMENTS_ID_POULE,
            # Timestamps
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
