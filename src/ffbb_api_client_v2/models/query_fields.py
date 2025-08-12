from enum import Enum


class OrganismeFields:
    """Default fields for organisme queries."""

    # Basic fields
    ID = "id"
    NOM = "nom"
    CODE = "code"
    TELEPHONE = "telephone"
    ADRESSE = "adresse"
    MAIL = "mail"
    TYPE = "type"
    NOM_SIMPLE = "nom_simple"
    URL_SITE_WEB = "urlSiteWeb"

    # Commune fields
    COMMUNE_CODE_POSTAL = "commune.codePostal"
    COMMUNE_LIBELLE = "commune.libelle"

    # Competitions fields
    COMPETITIONS_ID = "competitions.id"
    COMPETITIONS_NOM = "competitions.nom"

    # Engagements fields
    ENGAGEMENTS_ID = "engagements.id"

    # Membres fields
    MEMBRES_ID = "membres.id"
    MEMBRES_NOM = "membres.nom"
    MEMBRES_PRENOM = "membres.prenom"

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for organisme queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.CODE,
            cls.TELEPHONE,
            cls.ADRESSE,
            cls.COMMUNE_CODE_POSTAL,
            cls.COMMUNE_LIBELLE,
            cls.MAIL,
            cls.TYPE,
            cls.NOM_SIMPLE,
            cls.URL_SITE_WEB,
            cls.COMPETITIONS_ID,
            cls.COMPETITIONS_NOM,
            cls.ENGAGEMENTS_ID,
            cls.MEMBRES_ID,
            cls.MEMBRES_NOM,
            cls.MEMBRES_PRENOM,
        ]

    @classmethod
    def get_basic_fields(cls) -> list[str]:
        """Get basic fields for simple organisme queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.CODE,
            cls.TELEPHONE,
            cls.ADRESSE,
            cls.MAIL,
        ]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields including nested relationships."""
        return cls.get_default_fields() + [
            "cartographie.latitude",
            "cartographie.longitude",
            "logo.id",
            "logo.gradient_color",
            "membres.mail",
            "membres.telephonePortable",
            "engagements.idPoule.id",
            "engagements.idCompetition.id",
            "engagements.idCompetition.nom",
        ]


class CompetitionFields:
    """Default fields for competition queries."""

    # Basic fields
    ID = "id"
    NOM = "nom"
    SEXE = "sexe"
    SAISON = "saison"
    CODE = "code"
    TYPE_COMPETITION = "typeCompetition"
    LIVE_STAT = "liveStat"
    COMPETITION_ORIGINE = "competition_origine"
    COMPETITION_ORIGINE_NOM = "competition_origine_nom"

    # Categorie fields
    CATEGORIE_CODE = "categorie.code"
    CATEGORIE_ORDRE = "categorie.ordre"

    # Phases fields
    PHASES_ID = "phases.id"
    PHASES_NOM = "phases.nom"

    # Poules fields (nested in phases)
    PHASES_POULES_ID = "phases.poules.id"
    PHASES_POULES_NOM = "phases.poules.nom"

    # Rencontres fields (nested in poules)
    PHASES_POULES_RENCONTRES_ID = "phases.poules.rencontres.id"
    PHASES_POULES_RENCONTRES_NUMERO = "phases.poules.rencontres.numero"
    PHASES_POULES_RENCONTRES_DATE = "phases.poules.rencontres.date_rencontre"

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for competition queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.SEXE,
            cls.CATEGORIE_CODE,
            cls.CATEGORIE_ORDRE,
            cls.SAISON,
            cls.CODE,
            cls.TYPE_COMPETITION,
            cls.LIVE_STAT,
            cls.COMPETITION_ORIGINE,
            cls.COMPETITION_ORIGINE_NOM,
            cls.PHASES_ID,
            cls.PHASES_NOM,
            cls.PHASES_POULES_RENCONTRES_ID,
        ]

    @classmethod
    def get_basic_fields(cls) -> list[str]:
        """Get basic fields for simple competition queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.SEXE,
            cls.SAISON,
            cls.CODE,
        ]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields including all nested relationships."""
        return cls.get_default_fields() + [
            cls.PHASES_POULES_ID,
            cls.PHASES_POULES_NOM,
            cls.PHASES_POULES_RENCONTRES_NUMERO,
            cls.PHASES_POULES_RENCONTRES_DATE,
            "phases.poules.rencontres.nomEquipe1",
            "phases.poules.rencontres.nomEquipe2",
            "phases.poules.rencontres.resultatEquipe1",
            "phases.poules.rencontres.resultatEquipe2",
            "phases.poules.rencontres.joue",
        ]


class PouleFields:
    """Default fields for poule queries."""

    # Basic fields
    ID = "id"
    NOM = "nom"

    # Rencontres fields
    RENCONTRES_ID = "rencontres.id"
    RENCONTRES_NUMERO = "rencontres.numero"
    RENCONTRES_NUMERO_JOURNEE = "rencontres.numeroJournee"
    RENCONTRES_ID_POULE = "rencontres.idPoule"
    RENCONTRES_COMPETITION_ID = "rencontres.competitionId"
    RENCONTRES_RESULTAT_EQUIPE1 = "rencontres.resultatEquipe1"
    RENCONTRES_RESULTAT_EQUIPE2 = "rencontres.resultatEquipe2"
    RENCONTRES_JOUE = "rencontres.joue"
    RENCONTRES_NOM_EQUIPE1 = "rencontres.nomEquipe1"
    RENCONTRES_NOM_EQUIPE2 = "rencontres.nomEquipe2"
    RENCONTRES_DATE_RENCONTRE = "rencontres.date_rencontre"

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for poule queries."""
        return [
            cls.ID,
            cls.RENCONTRES_ID,
            cls.RENCONTRES_NUMERO,
            cls.RENCONTRES_NUMERO_JOURNEE,
            cls.RENCONTRES_ID_POULE,
            cls.RENCONTRES_COMPETITION_ID,
            cls.RENCONTRES_RESULTAT_EQUIPE1,
            cls.RENCONTRES_RESULTAT_EQUIPE2,
            cls.RENCONTRES_JOUE,
            cls.RENCONTRES_NOM_EQUIPE1,
            cls.RENCONTRES_NOM_EQUIPE2,
            cls.RENCONTRES_DATE_RENCONTRE,
        ]

    @classmethod
    def get_basic_fields(cls) -> list[str]:
        """Get basic fields for simple poule queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.RENCONTRES_ID,
        ]


class SaisonFields:
    """Default fields for saison queries."""

    # Basic fields
    ID = "id"
    NOM = "nom"
    ACTIF = "actif"
    DEBUT = "debut"
    FIN = "fin"

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for saison queries."""
        return [cls.ID]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields for saison queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.ACTIF,
            cls.DEBUT,
            cls.FIN,
        ]


# Enum for common field sets
class FieldSet(Enum):
    """Enum for different field sets."""

    BASIC = "basic"
    DEFAULT = "default"
    DETAILED = "detailed"
    MINIMAL = "minimal"


class QueryFieldsManager:
    """Manager class for handling query fields across different entity types."""

    @staticmethod
    def get_organisme_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get organisme fields based on field set."""
        if field_set == FieldSet.BASIC:
            return OrganismeFields.get_basic_fields()
        elif field_set == FieldSet.DETAILED:
            return OrganismeFields.get_detailed_fields()
        else:
            return OrganismeFields.get_default_fields()

    @staticmethod
    def get_competition_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get competition fields based on field set."""
        if field_set == FieldSet.BASIC:
            return CompetitionFields.get_basic_fields()
        elif field_set == FieldSet.DETAILED:
            return CompetitionFields.get_detailed_fields()
        else:
            return CompetitionFields.get_default_fields()

    @staticmethod
    def get_poule_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get poule fields based on field set."""
        if field_set == FieldSet.BASIC:
            return PouleFields.get_basic_fields()
        else:
            return PouleFields.get_default_fields()

    @staticmethod
    def get_saison_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get saison fields based on field set."""
        if field_set == FieldSet.DETAILED:
            return SaisonFields.get_detailed_fields()
        else:
            return SaisonFields.get_default_fields()
