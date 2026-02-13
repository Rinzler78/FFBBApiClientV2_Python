from typing import Any

from ...directus.models.field_set import FieldSet
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

    @staticmethod
    def build_wildcard_depths_from_schema(
        fields: list[dict[str, Any]], max_depth: int = 5
    ) -> dict[str, list[str]]:
        """
        Build wildcard depths from Directus field schema.

        Analyzes field relationships to determine theoretical max depths.
        Returns a mapping of depth levels to the expanded paths they would generate.

        Args:
            fields: List of field definitions from get_fields()
            max_depth: Maximum depth to analyze

        Returns:
            dict mapping depth strings to lists of field paths
        """
        # Build relationship graph
        relationships: dict[str, str] = {}  # field_name -> target_collection

        for field in fields:
            field_name = field.get("field")
            meta = field.get("meta", {})
            schema = field.get("schema", {})
            field_type = field.get("type")

            # Check for relationships
            special = meta.get("special", [])
            if (
                "m2o" in special
                or field_type == "integer"
                and schema.get("foreign_key_table")
            ):
                target = schema.get("foreign_key_table")
                if target and field_name:
                    relationships[field_name] = target

        # Build depth paths
        depths: dict[str, list[str]] = {}

        for i in range(max_depth + 1):
            depth_pattern = "*." * i + "*" if i > 0 else "*"
            depths[depth_pattern] = []

            # For each level, generate potential paths
            if i == 0:
                # Direct fields only
                depths[depth_pattern] = [
                    f["field"]
                    for f in fields
                    if f.get("field") and not f["field"].startswith("_")
                ]
            else:
                # Generate nested paths based on relationships
                for field_name, target in relationships.items():
                    # These would need actual target collection fields to be complete
                    # This is a simplified representation
                    depths[depth_pattern].append(f"{field_name}.*")

        return depths
