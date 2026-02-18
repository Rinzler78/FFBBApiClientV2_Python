from .query_fields_manager import QueryFieldsManager


class EngagementsFields(QueryFieldsManager):
    """Fields for engagements queries."""

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
    def get_fields(cls) -> list[str]:
        """Return the complete list of fields for engagements."""
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
