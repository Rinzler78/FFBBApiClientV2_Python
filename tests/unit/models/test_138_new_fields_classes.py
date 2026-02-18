"""Unit tests for the 10 new Fields classes for Directus collections."""

import unittest

from ffbb_api_client_v2.directus_ffbb.models.communes_fields import CommunesFields
from ffbb_api_client_v2.directus_ffbb.models.engagements_fields import EngagementsFields
from ffbb_api_client_v2.directus_ffbb.models.entraineurs_fields import EntraineursFields
from ffbb_api_client_v2.directus_ffbb.models.formations_fields import FormationsFields
from ffbb_api_client_v2.directus_ffbb.models.officiels_fields import OfficielsFields
from ffbb_api_client_v2.directus_ffbb.models.pratiques_fields import PratiquesFields
from ffbb_api_client_v2.directus_ffbb.models.query_fields_manager import (
    QueryFieldsManager,
)
from ffbb_api_client_v2.directus_ffbb.models.rencontres_fields import RencontresFields
from ffbb_api_client_v2.directus_ffbb.models.salles_fields import SallesFields
from ffbb_api_client_v2.directus_ffbb.models.terrains_fields import TerrainsFields
from ffbb_api_client_v2.directus_ffbb.models.tournois_fields import TournoisFields


class Test138CommunesFields(unittest.TestCase):
    """Tests for CommunesFields."""

    def test_049_get_fields_non_empty(self):
        """Test get_fields returns a non-empty list."""
        fields = CommunesFields.get_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_053_inherits_query_fields_manager(self):
        """Test CommunesFields inherits from QueryFieldsManager."""
        self.assertTrue(issubclass(CommunesFields, QueryFieldsManager))


class Test138OfficielsFields(unittest.TestCase):
    """Tests for OfficielsFields."""

    def test_049_get_fields_non_empty(self):
        """Test get_fields returns a non-empty list."""
        fields = OfficielsFields.get_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_053_inherits_query_fields_manager(self):
        """Test OfficielsFields inherits from QueryFieldsManager."""
        self.assertTrue(issubclass(OfficielsFields, QueryFieldsManager))


class Test138EntraineursFields(unittest.TestCase):
    """Tests for EntraineursFields."""

    def test_049_get_fields_non_empty(self):
        """Test get_fields returns a non-empty list."""
        fields = EntraineursFields.get_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_053_inherits_query_fields_manager(self):
        """Test EntraineursFields inherits from QueryFieldsManager."""
        self.assertTrue(issubclass(EntraineursFields, QueryFieldsManager))


class Test138RencontresFields(unittest.TestCase):
    """Tests for RencontresFields."""

    def test_049_get_fields_non_empty(self):
        """Test get_fields returns a non-empty list."""
        fields = RencontresFields.get_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_053_inherits_query_fields_manager(self):
        """Test RencontresFields inherits from QueryFieldsManager."""
        self.assertTrue(issubclass(RencontresFields, QueryFieldsManager))


class Test138SallesFields(unittest.TestCase):
    """Tests for SallesFields."""

    def test_049_get_fields_non_empty(self):
        """Test get_fields returns a non-empty list."""
        fields = SallesFields.get_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_053_inherits_query_fields_manager(self):
        """Test SallesFields inherits from QueryFieldsManager."""
        self.assertTrue(issubclass(SallesFields, QueryFieldsManager))


class Test138TerrainsFields(unittest.TestCase):
    """Tests for TerrainsFields."""

    def test_049_get_fields_non_empty(self):
        """Test get_fields returns a non-empty list."""
        fields = TerrainsFields.get_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_053_inherits_query_fields_manager(self):
        """Test TerrainsFields inherits from QueryFieldsManager."""
        self.assertTrue(issubclass(TerrainsFields, QueryFieldsManager))


class Test138TournoisFields(unittest.TestCase):
    """Tests for TournoisFields."""

    def test_049_get_fields_non_empty(self):
        """Test get_fields returns a non-empty list."""
        fields = TournoisFields.get_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_053_inherits_query_fields_manager(self):
        """Test TournoisFields inherits from QueryFieldsManager."""
        self.assertTrue(issubclass(TournoisFields, QueryFieldsManager))


class Test138EngagementsFields(unittest.TestCase):
    """Tests for EngagementsFields."""

    def test_049_get_fields_non_empty(self):
        """Test get_fields returns a non-empty list."""
        fields = EngagementsFields.get_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_053_inherits_query_fields_manager(self):
        """Test EngagementsFields inherits from QueryFieldsManager."""
        self.assertTrue(issubclass(EngagementsFields, QueryFieldsManager))


class Test138FormationsFields(unittest.TestCase):
    """Tests for FormationsFields."""

    def test_049_get_fields_non_empty(self):
        """Test get_fields returns a non-empty list."""
        fields = FormationsFields.get_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_053_inherits_query_fields_manager(self):
        """Test FormationsFields inherits from QueryFieldsManager."""
        self.assertTrue(issubclass(FormationsFields, QueryFieldsManager))


class Test138PratiquesFields(unittest.TestCase):
    """Tests for PratiquesFields."""

    def test_049_get_fields_non_empty(self):
        """Test get_fields returns a non-empty list."""
        fields = PratiquesFields.get_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_053_inherits_query_fields_manager(self):
        """Test PratiquesFields inherits from QueryFieldsManager."""
        self.assertTrue(issubclass(PratiquesFields, QueryFieldsManager))


if __name__ == "__main__":
    unittest.main()
