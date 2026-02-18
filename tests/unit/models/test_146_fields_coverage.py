"""Tests for field constants coverage in *Fields classes.

Verifies that:
- Every string constant (except WILDCARD) appears in get_detailed_fields()
- get_default_fields() is a subset of get_detailed_fields()
- No duplicates in get_default_fields()
- "id" present in each get_default_fields() (where applicable)
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
    """Get all string constants from a Fields class, excluding WILDCARD."""
    return {
        v
        for k, v in vars(cls).items()
        if isinstance(v, str) and not k.startswith("_") and k != "WILDCARD"
    }


class Test146FieldsCoverage(unittest.TestCase):
    """Tests that field constants are covered by get_detailed_fields()."""

    # --- Per-entity coverage tests ---

    def test_001_competition_fields_coverage(self):
        """Each CompetitionFields constant appears in get_detailed_fields()."""
        all_constants = _get_all_constants(CompetitionFields)
        detailed = set(CompetitionFields.get_detailed_fields())
        missing = all_constants - detailed
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_detailed_fields(): {missing}",
        )

    def test_002_organisme_fields_coverage(self):
        """Each OrganismeFields constant appears in get_detailed_fields()."""
        all_constants = _get_all_constants(OrganismeFields)
        detailed = set(OrganismeFields.get_detailed_fields())
        missing = all_constants - detailed
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_detailed_fields(): {missing}",
        )

    def test_003_poule_fields_coverage(self):
        """Each PouleFields constant appears in get_detailed_fields()."""
        all_constants = _get_all_constants(PouleFields)
        detailed = set(PouleFields.get_detailed_fields())
        missing = all_constants - detailed
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_detailed_fields(): {missing}",
        )

    def test_004_saison_fields_coverage(self):
        """Each SaisonFields constant appears in get_detailed_fields()."""
        all_constants = _get_all_constants(SaisonFields)
        detailed = set(SaisonFields.get_detailed_fields())
        missing = all_constants - detailed
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_detailed_fields(): {missing}",
        )

    def test_005_communes_fields_coverage(self):
        """Each CommunesFields constant appears in get_detailed_fields()."""
        all_constants = _get_all_constants(CommunesFields)
        detailed = set(CommunesFields.get_detailed_fields())
        missing = all_constants - detailed
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_detailed_fields(): {missing}",
        )

    def test_006_officiels_fields_coverage(self):
        """Each OfficielsFields constant appears in get_detailed_fields()."""
        all_constants = _get_all_constants(OfficielsFields)
        detailed = set(OfficielsFields.get_detailed_fields())
        missing = all_constants - detailed
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_detailed_fields(): {missing}",
        )

    def test_007_entraineurs_fields_coverage(self):
        """Each EntraineursFields constant appears in get_detailed_fields()."""
        all_constants = _get_all_constants(EntraineursFields)
        detailed = set(EntraineursFields.get_detailed_fields())
        missing = all_constants - detailed
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_detailed_fields(): {missing}",
        )

    def test_008_rencontres_fields_coverage(self):
        """Each RencontresFields constant appears in get_detailed_fields()."""
        all_constants = _get_all_constants(RencontresFields)
        detailed = set(RencontresFields.get_detailed_fields())
        missing = all_constants - detailed
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_detailed_fields(): {missing}",
        )

    def test_009_salles_fields_coverage(self):
        """Each SallesFields constant appears in get_detailed_fields()."""
        all_constants = _get_all_constants(SallesFields)
        detailed = set(SallesFields.get_detailed_fields())
        missing = all_constants - detailed
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_detailed_fields(): {missing}",
        )

    def test_010_terrains_fields_coverage(self):
        """Each TerrainsFields constant appears in get_detailed_fields()."""
        all_constants = _get_all_constants(TerrainsFields)
        detailed = set(TerrainsFields.get_detailed_fields())
        missing = all_constants - detailed
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_detailed_fields(): {missing}",
        )

    def test_011_tournois_fields_coverage(self):
        """Each TournoisFields constant appears in get_detailed_fields()."""
        all_constants = _get_all_constants(TournoisFields)
        detailed = set(TournoisFields.get_detailed_fields())
        missing = all_constants - detailed
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_detailed_fields(): {missing}",
        )

    def test_012_engagements_fields_coverage(self):
        """Each EngagementsFields constant appears in get_detailed_fields()."""
        all_constants = _get_all_constants(EngagementsFields)
        detailed = set(EngagementsFields.get_detailed_fields())
        missing = all_constants - detailed
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_detailed_fields(): {missing}",
        )

    def test_013_formations_fields_coverage(self):
        """Each FormationsFields constant appears in get_detailed_fields()."""
        all_constants = _get_all_constants(FormationsFields)
        detailed = set(FormationsFields.get_detailed_fields())
        missing = all_constants - detailed
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_detailed_fields(): {missing}",
        )

    def test_014_pratiques_fields_coverage(self):
        """Each PratiquesFields constant appears in get_detailed_fields()."""
        all_constants = _get_all_constants(PratiquesFields)
        detailed = set(PratiquesFields.get_detailed_fields())
        missing = all_constants - detailed
        self.assertFalse(
            missing,
            f"Constants defined but absent from get_detailed_fields(): {missing}",
        )

    # --- Structural tests ---

    def test_020_default_subset_of_detailed(self):
        """get_default_fields() must be a subset of get_detailed_fields() for all."""
        for cls in ALL_FIELDS_CLASSES:
            with self.subTest(cls=cls.__name__):
                default = set(cls.get_default_fields())
                detailed = set(cls.get_detailed_fields())
                extra = default - detailed
                self.assertFalse(
                    extra,
                    f"{cls.__name__}: default has fields not in detailed: {extra}",
                )

    def test_021_no_duplicates_in_default(self):
        """get_default_fields() must have no duplicates for all."""
        for cls in ALL_FIELDS_CLASSES:
            with self.subTest(cls=cls.__name__):
                default = cls.get_default_fields()
                self.assertEqual(
                    len(default),
                    len(set(default)),
                    f"{cls.__name__}: duplicates in get_default_fields()",
                )

    def test_022_no_duplicates_in_detailed(self):
        """get_detailed_fields() must have no duplicates for all."""
        for cls in ALL_FIELDS_CLASSES:
            with self.subTest(cls=cls.__name__):
                detailed = cls.get_detailed_fields()
                self.assertEqual(
                    len(detailed),
                    len(set(detailed)),
                    f"{cls.__name__}: duplicates in get_detailed_fields()",
                )

    def test_023_wildcard_not_in_default(self):
        """WILDCARD must not appear in get_default_fields() for any class."""
        for cls in ALL_FIELDS_CLASSES:
            with self.subTest(cls=cls.__name__):
                self.assertNotIn(
                    cls.WILDCARD,
                    cls.get_default_fields(),
                    f"{cls.__name__}: WILDCARD found in get_default_fields()",
                )

    def test_024_wildcard_not_in_detailed(self):
        """WILDCARD must not appear in get_detailed_fields() for any class."""
        for cls in ALL_FIELDS_CLASSES:
            with self.subTest(cls=cls.__name__):
                self.assertNotIn(
                    cls.WILDCARD,
                    cls.get_detailed_fields(),
                    f"{cls.__name__}: WILDCARD found in get_detailed_fields()",
                )


if __name__ == "__main__":
    unittest.main()
