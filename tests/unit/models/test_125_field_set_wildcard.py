"""Tests for FieldSet enum and *Fields classes inheritance."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.directus.models.field_set import FieldSet
from ffbb_api_client_v2.directus_ffbb.models.competition_fields import CompetitionFields
from ffbb_api_client_v2.directus_ffbb.models.organisme_fields import OrganismeFields
from ffbb_api_client_v2.directus_ffbb.models.poule_fields import PouleFields
from ffbb_api_client_v2.directus_ffbb.models.query_fields_manager import (
    QueryFieldsManager,
)
from ffbb_api_client_v2.directus_ffbb.models.saison_fields import SaisonFields


class Test125FieldSetAndInheritance(unittest.TestCase):
    """Tests for FieldSet enum and *Fields ABC inheritance."""

    def test_000_field_set_default_exists(self) -> None:
        """Test that DEFAULT is a valid FieldSet value."""
        self.assertEqual(FieldSet.DEFAULT.value, "default")

    def test_001_field_set_has_only_default(self) -> None:
        """Test that FieldSet has exactly one member."""
        self.assertEqual(len(FieldSet), 1)

    def test_007_competition_fields_returns_explicit_list(self) -> None:
        """Test CompetitionFields.get_fields() returns explicit fields."""
        result = CompetitionFields.get_fields()
        self.assertIsInstance(result, list)
        self.assertIn("id", result)
        self.assertIn("nom", result)

    def test_008_organisme_fields_returns_explicit_list(self) -> None:
        """Test OrganismeFields.get_fields() returns explicit fields."""
        result = OrganismeFields.get_fields()
        self.assertIsInstance(result, list)
        self.assertIn("id", result)
        self.assertIn("nom", result)

    def test_009_poule_fields_returns_explicit_list(self) -> None:
        """Test PouleFields.get_fields() returns explicit fields."""
        result = PouleFields.get_fields()
        self.assertIsInstance(result, list)
        self.assertIn("id", result)
        self.assertIn("nom", result)

    def test_010_saison_fields_returns_explicit_list(self) -> None:
        """Test SaisonFields.get_fields() returns explicit fields."""
        result = SaisonFields.get_fields()
        self.assertIsInstance(result, list)
        self.assertIn("id", result)

    def test_011_competition_inherits_query_fields_manager(self) -> None:
        """Test CompetitionFields inherits from QueryFieldsManager."""
        self.assertTrue(issubclass(CompetitionFields, QueryFieldsManager))

    def test_012_organisme_inherits_query_fields_manager(self) -> None:
        """Test OrganismeFields inherits from QueryFieldsManager."""
        self.assertTrue(issubclass(OrganismeFields, QueryFieldsManager))

    def test_013_poule_inherits_query_fields_manager(self) -> None:
        """Test PouleFields inherits from QueryFieldsManager."""
        self.assertTrue(issubclass(PouleFields, QueryFieldsManager))

    def test_014_saison_inherits_query_fields_manager(self) -> None:
        """Test SaisonFields inherits from QueryFieldsManager."""
        self.assertTrue(issubclass(SaisonFields, QueryFieldsManager))


if __name__ == "__main__":
    unittest.main()
