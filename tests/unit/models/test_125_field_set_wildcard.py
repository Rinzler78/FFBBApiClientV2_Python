"""Tests for FieldSet.WILDCARD and get_wildcard() methods."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.models.competition_fields import CompetitionFields
from ffbb_api_client_v2.models.field_set import FieldSet
from ffbb_api_client_v2.models.organisme_fields import OrganismeFields
from ffbb_api_client_v2.models.poule_fields import PouleFields
from ffbb_api_client_v2.models.query_fields_manager import QueryFieldsManager
from ffbb_api_client_v2.models.saison_fields import SaisonFields


class Test125FieldSetWildcard(unittest.TestCase):
    """Tests for FieldSet.WILDCARD enum value and get_wildcard() class methods."""

    def test_001_field_set_wildcard_exists(self) -> None:
        """Test that WILDCARD is a valid FieldSet value."""
        self.assertEqual(FieldSet.WILDCARD.value, "wildcard")

    def test_002_competition_wildcard_default_depth(self) -> None:
        """Test CompetitionFields.get_wildcard() default depth is 3."""
        result = CompetitionFields.get_wildcard()
        self.assertEqual(result, ["*.*.*"])

    def test_003_competition_wildcard_custom_depth(self) -> None:
        """Test CompetitionFields.get_wildcard() with custom depth."""
        self.assertEqual(CompetitionFields.get_wildcard(1), ["*"])
        self.assertEqual(CompetitionFields.get_wildcard(2), ["*.*"])
        self.assertEqual(CompetitionFields.get_wildcard(4), ["*.*.*.*"])

    def test_004_competition_wildcard_max_depth_capped(self) -> None:
        """Test CompetitionFields.get_wildcard() caps at depth 5."""
        self.assertEqual(CompetitionFields.get_wildcard(10), ["*.*.*.*.*"])

    def test_005_organisme_wildcard_default_depth(self) -> None:
        """Test OrganismeFields.get_wildcard() default depth is 4."""
        result = OrganismeFields.get_wildcard()
        self.assertEqual(result, ["*.*.*.*"])

    def test_006_poule_wildcard_default_depth(self) -> None:
        """Test PouleFields.get_wildcard() default depth is 1."""
        result = PouleFields.get_wildcard()
        self.assertEqual(result, ["*"])

    def test_007_saison_wildcard_default_depth(self) -> None:
        """Test SaisonFields.get_wildcard() default depth is 1."""
        result = SaisonFields.get_wildcard()
        self.assertEqual(result, ["*"])

    def test_008_query_fields_manager_competition_wildcard(self) -> None:
        """Test QueryFieldsManager returns wildcard for competitions."""
        result = QueryFieldsManager.get_competition_fields(FieldSet.WILDCARD)
        self.assertEqual(result, ["*.*.*"])

    def test_009_query_fields_manager_organisme_wildcard(self) -> None:
        """Test QueryFieldsManager returns wildcard for organismes."""
        result = QueryFieldsManager.get_organisme_fields(FieldSet.WILDCARD)
        self.assertEqual(result, ["*.*.*.*"])

    def test_010_query_fields_manager_poule_wildcard(self) -> None:
        """Test QueryFieldsManager returns wildcard for poules."""
        result = QueryFieldsManager.get_poule_fields(FieldSet.WILDCARD)
        self.assertEqual(result, ["*"])

    def test_011_query_fields_manager_saison_wildcard(self) -> None:
        """Test QueryFieldsManager returns wildcard for saisons."""
        result = QueryFieldsManager.get_saison_fields(FieldSet.WILDCARD)
        self.assertEqual(result, ["*"])

    def test_012_query_fields_manager_default_unchanged(self) -> None:
        """Test that DEFAULT field set still works correctly."""
        comp = QueryFieldsManager.get_competition_fields(FieldSet.DEFAULT)
        self.assertIn("id", comp)
        self.assertIn("nom", comp)
        self.assertNotIn("*", comp)

    def test_013_query_fields_manager_basic_unchanged(self) -> None:
        """Test that BASIC field set still works correctly."""
        comp = QueryFieldsManager.get_competition_fields(FieldSet.BASIC)
        self.assertIn("id", comp)
        self.assertIn("nom", comp)
        self.assertTrue(len(comp) < 10)


if __name__ == "__main__":
    unittest.main()
