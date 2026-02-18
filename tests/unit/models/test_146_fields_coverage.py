"""Tests for field constants coverage in *Fields classes.

Verifies that:
- Every string constant appears in get_fields()
- No duplicates in get_fields()
- All classes inherit from QueryFieldsManager
"""

import unittest

from ffbb_api_client_v2.directus_ffbb.models.communes_fields import CommunesFields
from ffbb_api_client_v2.directus_ffbb.models.competition_fields import CompetitionFields
from ffbb_api_client_v2.directus_ffbb.models.engagements_fields import EngagementsFields
from ffbb_api_client_v2.directus_ffbb.models.entraineurs_fields import EntraineursFields
from ffbb_api_client_v2.directus_ffbb.models.formations_fields import FormationsFields
from ffbb_api_client_v2.directus_ffbb.models.officiels_fields import OfficielsFields
from ffbb_api_client_v2.directus_ffbb.models.organisme_fields import OrganismeFields
from ffbb_api_client_v2.directus_ffbb.models.poule_fields import PouleFields
from ffbb_api_client_v2.directus_ffbb.models.pratiques_fields import PratiquesFields
from ffbb_api_client_v2.directus_ffbb.models.query_fields_manager import (
    QueryFieldsManager,
)
from ffbb_api_client_v2.directus_ffbb.models.rencontres_fields import RencontresFields
from ffbb_api_client_v2.directus_ffbb.models.saison_fields import SaisonFields
from ffbb_api_client_v2.directus_ffbb.models.salles_fields import SallesFields
from ffbb_api_client_v2.directus_ffbb.models.terrains_fields import TerrainsFields
from ffbb_api_client_v2.directus_ffbb.models.tournois_fields import TournoisFields

ALL_FIELDS_CLASSES = [
    CompetitionFields,
    OrganismeFields,
    PouleFields,
    SaisonFields,
    CommunesFields,
    OfficielsFields,
    EntraineursFields,
    RencontresFields,
    SallesFields,
    TerrainsFields,
    TournoisFields,
    EngagementsFields,
    FormationsFields,
    PratiquesFields,
]


def _get_all_constants(cls: type) -> set[str]:
    """Get all string constants from a Fields class."""
    return {
        v for k, v in vars(cls).items() if isinstance(v, str) and not k.startswith("_")
    }


class Test146FieldsCoverage(unittest.TestCase):
    """Tests that field constants are covered by get_fields()."""

    # --- Per-entity coverage tests ---

    def test_001_competition_fields_coverage(self):
        """Each CompetitionFields constant appears in get_fields()."""
        all_constants = _get_all_constants(CompetitionFields)
        fields = set(CompetitionFields.get_fields())
        missing = all_constants - fields
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_fields(): {missing}",
        )

    def test_002_organisme_fields_coverage(self):
        """Each OrganismeFields constant appears in get_fields()."""
        all_constants = _get_all_constants(OrganismeFields)
        fields = set(OrganismeFields.get_fields())
        missing = all_constants - fields
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_fields(): {missing}",
        )

    def test_003_poule_fields_coverage(self):
        """Each PouleFields constant appears in get_fields()."""
        all_constants = _get_all_constants(PouleFields)
        fields = set(PouleFields.get_fields())
        missing = all_constants - fields
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_fields(): {missing}",
        )

    def test_004_saison_fields_coverage(self):
        """Each SaisonFields constant appears in get_fields()."""
        all_constants = _get_all_constants(SaisonFields)
        fields = set(SaisonFields.get_fields())
        missing = all_constants - fields
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_fields(): {missing}",
        )

    def test_005_communes_fields_coverage(self):
        """Each CommunesFields constant appears in get_fields()."""
        all_constants = _get_all_constants(CommunesFields)
        fields = set(CommunesFields.get_fields())
        missing = all_constants - fields
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_fields(): {missing}",
        )

    def test_006_officiels_fields_coverage(self):
        """Each OfficielsFields constant appears in get_fields()."""
        all_constants = _get_all_constants(OfficielsFields)
        fields = set(OfficielsFields.get_fields())
        missing = all_constants - fields
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_fields(): {missing}",
        )

    def test_007_entraineurs_fields_coverage(self):
        """Each EntraineursFields constant appears in get_fields()."""
        all_constants = _get_all_constants(EntraineursFields)
        fields = set(EntraineursFields.get_fields())
        missing = all_constants - fields
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_fields(): {missing}",
        )

    def test_008_rencontres_fields_coverage(self):
        """Each RencontresFields constant appears in get_fields()."""
        all_constants = _get_all_constants(RencontresFields)
        fields = set(RencontresFields.get_fields())
        missing = all_constants - fields
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_fields(): {missing}",
        )

    def test_009_salles_fields_coverage(self):
        """Each SallesFields constant appears in get_fields()."""
        all_constants = _get_all_constants(SallesFields)
        fields = set(SallesFields.get_fields())
        missing = all_constants - fields
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_fields(): {missing}",
        )

    def test_010_terrains_fields_coverage(self):
        """Each TerrainsFields constant appears in get_fields()."""
        all_constants = _get_all_constants(TerrainsFields)
        fields = set(TerrainsFields.get_fields())
        missing = all_constants - fields
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_fields(): {missing}",
        )

    def test_011_tournois_fields_coverage(self):
        """Each TournoisFields constant appears in get_fields()."""
        all_constants = _get_all_constants(TournoisFields)
        fields = set(TournoisFields.get_fields())
        missing = all_constants - fields
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_fields(): {missing}",
        )

    def test_012_engagements_fields_coverage(self):
        """Each EngagementsFields constant appears in get_fields()."""
        all_constants = _get_all_constants(EngagementsFields)
        fields = set(EngagementsFields.get_fields())
        missing = all_constants - fields
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_fields(): {missing}",
        )

    def test_013_formations_fields_coverage(self):
        """Each FormationsFields constant appears in get_fields()."""
        all_constants = _get_all_constants(FormationsFields)
        fields = set(FormationsFields.get_fields())
        missing = all_constants - fields
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_fields(): {missing}",
        )

    def test_014_pratiques_fields_coverage(self):
        """Each PratiquesFields constant appears in get_fields()."""
        all_constants = _get_all_constants(PratiquesFields)
        fields = set(PratiquesFields.get_fields())
        missing = all_constants - fields
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_fields(): {missing}",
        )

    # --- Structural tests ---

    def test_021_no_duplicates_in_get_fields(self):
        """get_fields() must have no duplicates for all."""
        for cls in ALL_FIELDS_CLASSES:
            with self.subTest(cls=cls.__name__):
                fields = cls.get_fields()
                self.assertEqual(
                    len(fields),
                    len(set(fields)),
                    f"{cls.__name__}: duplicates in get_fields()",
                )

    def test_025_all_classes_inherit_query_fields_manager(self):
        """All *Fields classes must inherit from QueryFieldsManager."""
        for cls in ALL_FIELDS_CLASSES:
            with self.subTest(cls=cls.__name__):
                self.assertTrue(
                    issubclass(cls, QueryFieldsManager),
                    f"{cls.__name__} does not inherit from QueryFieldsManager",
                )


if __name__ == "__main__":
    unittest.main()
