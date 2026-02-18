"""Tests for WILDCARD constants on entity fields classes."""

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


class Test125FieldSetWildcard(unittest.TestCase):
    """Tests for FieldSet.WILDCARD enum value and WILDCARD class constants."""

    def test_000_field_set_wildcard_exists(self) -> None:
        """Test that WILDCARD is a valid FieldSet value."""
        self.assertEqual(FieldSet.WILDCARD.value, "wildcard")

    def test_001_competition_wildcard_constant(self) -> None:
        """Test CompetitionFields.WILDCARD is a string with correct depth."""
        self.assertIsInstance(CompetitionFields.WILDCARD, str)
        self.assertEqual(CompetitionFields.WILDCARD, "*.*.*.*.*")

    def test_004_organisme_wildcard_constant(self) -> None:
        """Test OrganismeFields.WILDCARD is a string with correct depth."""
        self.assertIsInstance(OrganismeFields.WILDCARD, str)
        self.assertEqual(OrganismeFields.WILDCARD, "*.*.*.*")

    def test_005_poule_wildcard_constant(self) -> None:
        """Test PouleFields.WILDCARD is a string with correct depth."""
        self.assertIsInstance(PouleFields.WILDCARD, str)
        self.assertEqual(PouleFields.WILDCARD, "*.*.*")

    def test_006_saison_wildcard_constant(self) -> None:
        """Test SaisonFields.WILDCARD is a string with correct depth."""
        self.assertIsInstance(SaisonFields.WILDCARD, str)
        self.assertEqual(SaisonFields.WILDCARD, "*")

    def test_007_query_fields_manager_competition_explicit(self) -> None:
        """Test QueryFieldsManager returns explicit fields for competitions."""
        result = QueryFieldsManager.get_competition_fields()
        self.assertEqual(result, CompetitionFields.get_default_fields())
        self.assertNotIn(CompetitionFields.WILDCARD, result)

    def test_008_query_fields_manager_organisme_explicit(self) -> None:
        """Test QueryFieldsManager returns explicit fields for organismes."""
        result = QueryFieldsManager.get_organisme_fields()
        self.assertEqual(result, OrganismeFields.get_default_fields())
        self.assertNotIn(OrganismeFields.WILDCARD, result)

    def test_009_query_fields_manager_poule_explicit(self) -> None:
        """Test QueryFieldsManager returns explicit fields for poules."""
        result = QueryFieldsManager.get_poule_fields()
        self.assertEqual(result, PouleFields.get_default_fields())
        self.assertNotIn(PouleFields.WILDCARD, result)

    def test_010_query_fields_manager_saison_explicit(self) -> None:
        """Test QueryFieldsManager returns explicit fields for saisons."""
        result = QueryFieldsManager.get_saison_fields()
        self.assertEqual(result, SaisonFields.get_default_fields())
        self.assertNotIn(SaisonFields.WILDCARD, result)


if __name__ == "__main__":
    unittest.main()
