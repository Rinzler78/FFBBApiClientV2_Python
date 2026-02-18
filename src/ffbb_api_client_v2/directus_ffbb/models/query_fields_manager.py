from .communes_fields import CommunesFields
from .competition_fields import CompetitionFields
from .engagements_fields import EngagementsFields
from .entraineurs_fields import EntraineursFields
from .formations_fields import FormationsFields
from .officiels_fields import OfficielsFields
from .organisme_fields import OrganismeFields
from .poule_fields import PouleFields
from .pratiques_fields import PratiquesFields
from .rencontres_fields import RencontresFields
from .saison_fields import SaisonFields
from .salles_fields import SallesFields
from .terrains_fields import TerrainsFields
from .tournois_fields import TournoisFields


class QueryFieldsManager:
    """Returns the query fields for each entity type.

    All entities use explicit field lists from get_default_fields() to
    avoid deep wildcard resolution that can cause 504 timeouts on the
    Directus API and to maintain explicit control over queried fields.
    """

    @staticmethod
    def get_organisme_fields() -> list[str]:
        return OrganismeFields.get_default_fields()

    @staticmethod
    def get_competition_fields() -> list[str]:
        return CompetitionFields.get_default_fields()

    @staticmethod
    def get_poule_fields() -> list[str]:
        return PouleFields.get_default_fields()

    @staticmethod
    def get_saison_fields() -> list[str]:
        return SaisonFields.get_default_fields()

    @staticmethod
    def get_communes_fields() -> list[str]:
        return CommunesFields.get_default_fields()

    @staticmethod
    def get_officiels_fields() -> list[str]:
        return OfficielsFields.get_default_fields()

    @staticmethod
    def get_entraineurs_fields() -> list[str]:
        return EntraineursFields.get_default_fields()

    @staticmethod
    def get_rencontres_fields() -> list[str]:
        return RencontresFields.get_default_fields()

    @staticmethod
    def get_salles_fields() -> list[str]:
        return SallesFields.get_default_fields()

    @staticmethod
    def get_terrains_fields() -> list[str]:
        return TerrainsFields.get_default_fields()

    @staticmethod
    def get_tournois_fields() -> list[str]:
        return TournoisFields.get_default_fields()

    @staticmethod
    def get_engagements_fields() -> list[str]:
        return EngagementsFields.get_default_fields()

    @staticmethod
    def get_formations_fields() -> list[str]:
        return FormationsFields.get_default_fields()

    @staticmethod
    def get_pratiques_fields() -> list[str]:
        return PratiquesFields.get_default_fields()
