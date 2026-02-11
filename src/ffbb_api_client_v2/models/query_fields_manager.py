from .communes_fields import CommunesFields
from .competition_fields import CompetitionFields
from .engagements_fields import EngagementsFields
from .entraineurs_fields import EntraineursFields
from .field_set import FieldSet
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
    """Manager class for handling query fields across different entity types."""

    @staticmethod
    def get_organisme_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get organisme fields based on field set."""
        if field_set == FieldSet.WILDCARD:
            return OrganismeFields.get_wildcard()
        elif field_set == FieldSet.BASIC:
            return OrganismeFields.get_basic_fields()
        elif field_set == FieldSet.DETAILED:
            return OrganismeFields.get_detailed_fields()
        else:
            return OrganismeFields.get_default_fields()

    @staticmethod
    def get_competition_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get competition fields based on field set."""
        if field_set == FieldSet.WILDCARD:
            return CompetitionFields.get_wildcard()
        elif field_set == FieldSet.BASIC:
            return CompetitionFields.get_basic_fields()
        elif field_set == FieldSet.DETAILED:
            return CompetitionFields.get_detailed_fields()
        else:
            return CompetitionFields.get_default_fields()

    @staticmethod
    def get_poule_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get poule fields based on field set."""
        if field_set == FieldSet.WILDCARD:
            return PouleFields.get_wildcard()
        elif field_set == FieldSet.BASIC:
            return PouleFields.get_basic_fields()
        elif field_set == FieldSet.DETAILED:
            return PouleFields.get_detailed_fields()
        else:
            return PouleFields.get_default_fields()

    @staticmethod
    def get_saison_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get saison fields based on field set."""
        if field_set == FieldSet.WILDCARD:
            return SaisonFields.get_wildcard()
        elif field_set == FieldSet.DETAILED:
            return SaisonFields.get_detailed_fields()
        else:
            return SaisonFields.get_default_fields()

    @staticmethod
    def get_communes_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get communes fields based on field set."""
        if field_set == FieldSet.WILDCARD:
            return CommunesFields.get_wildcard()
        elif field_set == FieldSet.DETAILED:
            return CommunesFields.get_detailed_fields()
        else:
            return CommunesFields.get_default_fields()

    @staticmethod
    def get_officiels_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get officiels fields based on field set."""
        if field_set == FieldSet.WILDCARD:
            return OfficielsFields.get_wildcard()
        elif field_set == FieldSet.DETAILED:
            return OfficielsFields.get_detailed_fields()
        else:
            return OfficielsFields.get_default_fields()

    @staticmethod
    def get_entraineurs_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get entraineurs fields based on field set."""
        if field_set == FieldSet.WILDCARD:
            return EntraineursFields.get_wildcard()
        elif field_set == FieldSet.DETAILED:
            return EntraineursFields.get_detailed_fields()
        else:
            return EntraineursFields.get_default_fields()

    @staticmethod
    def get_rencontres_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get rencontres fields based on field set."""
        if field_set == FieldSet.WILDCARD:
            return RencontresFields.get_wildcard()
        elif field_set == FieldSet.BASIC:
            return RencontresFields.get_basic_fields()
        elif field_set == FieldSet.DETAILED:
            return RencontresFields.get_detailed_fields()
        else:
            return RencontresFields.get_default_fields()

    @staticmethod
    def get_salles_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get salles fields based on field set."""
        if field_set == FieldSet.WILDCARD:
            return SallesFields.get_wildcard()
        elif field_set == FieldSet.DETAILED:
            return SallesFields.get_detailed_fields()
        else:
            return SallesFields.get_default_fields()

    @staticmethod
    def get_terrains_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get terrains fields based on field set."""
        if field_set == FieldSet.WILDCARD:
            return TerrainsFields.get_wildcard()
        elif field_set == FieldSet.DETAILED:
            return TerrainsFields.get_detailed_fields()
        else:
            return TerrainsFields.get_default_fields()

    @staticmethod
    def get_tournois_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get tournois fields based on field set."""
        if field_set == FieldSet.WILDCARD:
            return TournoisFields.get_wildcard()
        elif field_set == FieldSet.DETAILED:
            return TournoisFields.get_detailed_fields()
        else:
            return TournoisFields.get_default_fields()

    @staticmethod
    def get_engagements_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get engagements fields based on field set."""
        if field_set == FieldSet.WILDCARD:
            return EngagementsFields.get_wildcard()
        elif field_set == FieldSet.BASIC:
            return EngagementsFields.get_basic_fields()
        elif field_set == FieldSet.DETAILED:
            return EngagementsFields.get_detailed_fields()
        else:
            return EngagementsFields.get_default_fields()

    @staticmethod
    def get_formations_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get formations fields based on field set."""
        if field_set == FieldSet.WILDCARD:
            return FormationsFields.get_wildcard()
        elif field_set == FieldSet.DETAILED:
            return FormationsFields.get_detailed_fields()
        else:
            return FormationsFields.get_default_fields()

    @staticmethod
    def get_pratiques_fields(field_set: FieldSet = FieldSet.DEFAULT) -> list[str]:
        """Get pratiques fields based on field set."""
        if field_set == FieldSet.WILDCARD:
            return PratiquesFields.get_wildcard()
        elif field_set == FieldSet.DETAILED:
            return PratiquesFields.get_detailed_fields()
        else:
            return PratiquesFields.get_default_fields()
