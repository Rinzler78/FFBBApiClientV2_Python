class EngagementsFields:
    """Default fields for engagements queries."""

    ID = "id"
    NOM = "nom"
    NOM_EQUIPE = "nomEquipe"
    NOM_USUEL = "nomUsuel"
    NOM_OFFICIEL = "nomOfficiel"
    NUMERO_EQUIPE = "numeroEquipe"
    CODE_ABREGE = "codeAbrege"
    CLUB_PRO = "clubPro"
    POSITION = "position"
    LOGO = "logo"
    ID_COMPETITION = "idCompetition"
    ID_ORGANISME = "idOrganisme"
    ID_POULE = "idPoule"
    NIVEAU = "niveau"
    CLASSEMENT = "classement"
    ENTRAINEUR = "entraineur"
    ENTRAINEUR_ADJOINT = "entraineurAdjoint"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for engagements queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.NOM_EQUIPE,
            cls.NOM_USUEL,
            cls.NOM_OFFICIEL,
            cls.NUMERO_EQUIPE,
            cls.CODE_ABREGE,
            cls.CLUB_PRO,
            cls.POSITION,
            cls.LOGO,
        ]

    @classmethod
    def get_basic_fields(cls) -> list[str]:
        """Get basic fields for simple engagements queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.NOM_EQUIPE,
            cls.POSITION,
        ]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields for engagements queries."""
        return cls.get_default_fields() + [
            cls.ID_COMPETITION,
            cls.ID_ORGANISME,
            cls.ID_POULE,
            cls.NIVEAU,
            cls.CLASSEMENT,
            cls.ENTRAINEUR,
            cls.ENTRAINEUR_ADJOINT,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]

    @staticmethod
    def get_wildcard(depth: int = 2) -> list[str]:
        """Get wildcard fields at the specified depth."""
        return [".".join(["*"] * min(depth, 5))]
