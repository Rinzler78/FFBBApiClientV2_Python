class RencontresFields:
    """Default fields for rencontres queries."""

    ID = "id"
    DATE = "date"
    DATE_RENCONTRE = "date_rencontre"
    HORAIRE = "horaire"
    NUMERO = "numero"
    NUMERO_JOURNEE = "numeroJournee"
    NOM_EQUIPE1 = "nomEquipe1"
    NOM_EQUIPE2 = "nomEquipe2"
    RESULTAT_EQUIPE1 = "resultatEquipe1"
    RESULTAT_EQUIPE2 = "resultatEquipe2"
    JOUE = "joue"
    ETAT = "etat"
    PRATIQUE = "pratique"
    STATUS = "status"
    COMPETITION_ID = "competitionId"
    ID_ORGANISME_EQUIPE1 = "idOrganismeEquipe1"
    ID_ORGANISME_EQUIPE2 = "idOrganismeEquipe2"
    ID_POULE = "idPoule"
    SAISON = "saison"
    SALLE = "salle"
    OFFICIELS = "officiels"
    GS_ID = "gsId"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for rencontres queries."""
        return [
            cls.ID,
            cls.DATE,
            cls.DATE_RENCONTRE,
            cls.HORAIRE,
            cls.NUMERO,
            cls.NUMERO_JOURNEE,
            cls.NOM_EQUIPE1,
            cls.NOM_EQUIPE2,
            cls.RESULTAT_EQUIPE1,
            cls.RESULTAT_EQUIPE2,
            cls.JOUE,
            cls.ETAT,
            cls.PRATIQUE,
            cls.STATUS,
        ]

    @classmethod
    def get_basic_fields(cls) -> list[str]:
        """Get basic fields for simple rencontres queries."""
        return [
            cls.ID,
            cls.DATE_RENCONTRE,
            cls.NOM_EQUIPE1,
            cls.NOM_EQUIPE2,
            cls.RESULTAT_EQUIPE1,
            cls.RESULTAT_EQUIPE2,
            cls.JOUE,
        ]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields for rencontres queries."""
        return cls.get_default_fields() + [
            cls.COMPETITION_ID,
            cls.ID_ORGANISME_EQUIPE1,
            cls.ID_ORGANISME_EQUIPE2,
            cls.ID_POULE,
            cls.SAISON,
            cls.SALLE,
            cls.OFFICIELS,
            cls.GS_ID,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]

    @staticmethod
    def get_wildcard(depth: int = 2) -> list[str]:
        """Get wildcard fields at the specified depth."""
        return [".".join(["*"] * min(depth, 5))]
