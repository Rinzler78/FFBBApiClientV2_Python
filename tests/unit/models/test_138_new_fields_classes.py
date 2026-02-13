"""Unit tests for the 10 new Fields classes for Directus collections."""

import unittest

from ffbb_api_client_v2.directus_ffbb.models.communes_fields import CommunesFields
from ffbb_api_client_v2.directus_ffbb.models.engagements_fields import EngagementsFields
from ffbb_api_client_v2.directus_ffbb.models.entraineurs_fields import EntraineursFields
from ffbb_api_client_v2.directus_ffbb.models.formations_fields import FormationsFields
from ffbb_api_client_v2.directus_ffbb.models.officiels_fields import OfficielsFields
from ffbb_api_client_v2.directus_ffbb.models.pratiques_fields import PratiquesFields
from ffbb_api_client_v2.directus_ffbb.models.rencontres_fields import RencontresFields
from ffbb_api_client_v2.directus_ffbb.models.salles_fields import SallesFields
from ffbb_api_client_v2.directus_ffbb.models.terrains_fields import TerrainsFields
from ffbb_api_client_v2.directus_ffbb.models.tournois_fields import TournoisFields


class Test138CommunesFields(unittest.TestCase):
    """Tests for CommunesFields."""

    def test_049_get_default_fields_non_empty(self):
        """Test get_default_fields returns a non-empty list."""
        fields = CommunesFields.get_default_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_050_get_detailed_fields_non_empty(self):
        """Test get_detailed_fields returns a non-empty list."""
        fields = CommunesFields.get_detailed_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_051_detailed_superset_of_default(self):
        """Test get_detailed_fields is a superset of get_default_fields."""
        default = CommunesFields.get_default_fields()
        detailed = CommunesFields.get_detailed_fields()
        for field in default:
            self.assertIn(field, detailed)

    def test_052_get_wildcard_default(self):
        """Test get_wildcard returns list with single '*' entry (depth=1)."""
        wildcard = CommunesFields.get_wildcard()
        self.assertEqual(wildcard, ["*"])

    def test_053_get_wildcard_depth_3(self):
        """Test get_wildcard(3) returns ['*.*.*']."""
        wildcard = CommunesFields.get_wildcard(3)
        self.assertEqual(wildcard, ["*.*.*"])


class Test138OfficielsFields(unittest.TestCase):
    """Tests for OfficielsFields."""

    def test_049_get_default_fields_non_empty(self):
        """Test get_default_fields returns a non-empty list."""
        fields = OfficielsFields.get_default_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_050_get_detailed_fields_non_empty(self):
        """Test get_detailed_fields returns a non-empty list."""
        fields = OfficielsFields.get_detailed_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_051_detailed_superset_of_default(self):
        """Test get_detailed_fields is a superset of get_default_fields."""
        default = OfficielsFields.get_default_fields()
        detailed = OfficielsFields.get_detailed_fields()
        for field in default:
            self.assertIn(field, detailed)

    def test_052_get_wildcard_default(self):
        """Test get_wildcard returns list with single '*' entry (depth=1)."""
        wildcard = OfficielsFields.get_wildcard()
        self.assertEqual(wildcard, ["*"])

    def test_053_get_wildcard_depth_3(self):
        """Test get_wildcard(3) returns ['*.*.*']."""
        wildcard = OfficielsFields.get_wildcard(3)
        self.assertEqual(wildcard, ["*.*.*"])


class Test138EntraineursFields(unittest.TestCase):
    """Tests for EntraineursFields."""

    def test_049_get_default_fields_non_empty(self):
        """Test get_default_fields returns a non-empty list."""
        fields = EntraineursFields.get_default_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_050_get_detailed_fields_non_empty(self):
        """Test get_detailed_fields returns a non-empty list."""
        fields = EntraineursFields.get_detailed_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_051_detailed_superset_of_default(self):
        """Test get_detailed_fields is a superset of get_default_fields."""
        default = EntraineursFields.get_default_fields()
        detailed = EntraineursFields.get_detailed_fields()
        for field in default:
            self.assertIn(field, detailed)

    def test_052_get_wildcard_default(self):
        """Test get_wildcard returns list with single '*.*' entry (depth=2)."""
        wildcard = EntraineursFields.get_wildcard()
        self.assertEqual(wildcard, ["*.*"])

    def test_053_get_wildcard_depth_3(self):
        """Test get_wildcard(3) returns ['*.*.*']."""
        wildcard = EntraineursFields.get_wildcard(3)
        self.assertEqual(wildcard, ["*.*.*"])


class Test138RencontresFields(unittest.TestCase):
    """Tests for RencontresFields."""

    def test_049_get_default_fields_non_empty(self):
        """Test get_default_fields returns a non-empty list."""
        fields = RencontresFields.get_default_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_050_get_detailed_fields_non_empty(self):
        """Test get_detailed_fields returns a non-empty list."""
        fields = RencontresFields.get_detailed_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_051_detailed_superset_of_default(self):
        """Test get_detailed_fields is a superset of get_default_fields."""
        default = RencontresFields.get_default_fields()
        detailed = RencontresFields.get_detailed_fields()
        for field in default:
            self.assertIn(field, detailed)

    def test_052_get_wildcard_default(self):
        """Test get_wildcard returns list with single '*.*' entry (depth=2)."""
        wildcard = RencontresFields.get_wildcard()
        self.assertEqual(wildcard, ["*.*"])

    def test_053_get_wildcard_depth_3(self):
        """Test get_wildcard(3) returns ['*.*.*']."""
        wildcard = RencontresFields.get_wildcard(3)
        self.assertEqual(wildcard, ["*.*.*"])

    def test_042_get_basic_fields_non_empty(self):
        """Test get_basic_fields returns a non-empty list."""
        fields = RencontresFields.get_basic_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_043_basic_subset_of_default(self):
        """Test get_basic_fields is a subset of get_default_fields."""
        basic = RencontresFields.get_basic_fields()
        default = RencontresFields.get_default_fields()
        for field in basic:
            self.assertIn(field, default)


class Test138SallesFields(unittest.TestCase):
    """Tests for SallesFields."""

    def test_049_get_default_fields_non_empty(self):
        """Test get_default_fields returns a non-empty list."""
        fields = SallesFields.get_default_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_050_get_detailed_fields_non_empty(self):
        """Test get_detailed_fields returns a non-empty list."""
        fields = SallesFields.get_detailed_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_051_detailed_superset_of_default(self):
        """Test get_detailed_fields is a superset of get_default_fields."""
        default = SallesFields.get_default_fields()
        detailed = SallesFields.get_detailed_fields()
        for field in default:
            self.assertIn(field, detailed)

    def test_052_get_wildcard_default(self):
        """Test get_wildcard returns list with single '*.*' entry (depth=2)."""
        wildcard = SallesFields.get_wildcard()
        self.assertEqual(wildcard, ["*.*"])

    def test_053_get_wildcard_depth_3(self):
        """Test get_wildcard(3) returns ['*.*.*']."""
        wildcard = SallesFields.get_wildcard(3)
        self.assertEqual(wildcard, ["*.*.*"])


class Test138TerrainsFields(unittest.TestCase):
    """Tests for TerrainsFields."""

    def test_049_get_default_fields_non_empty(self):
        """Test get_default_fields returns a non-empty list."""
        fields = TerrainsFields.get_default_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_050_get_detailed_fields_non_empty(self):
        """Test get_detailed_fields returns a non-empty list."""
        fields = TerrainsFields.get_detailed_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_051_detailed_superset_of_default(self):
        """Test get_detailed_fields is a superset of get_default_fields."""
        default = TerrainsFields.get_default_fields()
        detailed = TerrainsFields.get_detailed_fields()
        for field in default:
            self.assertIn(field, detailed)

    def test_052_get_wildcard_default(self):
        """Test get_wildcard returns list with single '*.*' entry (depth=2)."""
        wildcard = TerrainsFields.get_wildcard()
        self.assertEqual(wildcard, ["*.*"])

    def test_053_get_wildcard_depth_3(self):
        """Test get_wildcard(3) returns ['*.*.*']."""
        wildcard = TerrainsFields.get_wildcard(3)
        self.assertEqual(wildcard, ["*.*.*"])


class Test138TournoisFields(unittest.TestCase):
    """Tests for TournoisFields."""

    def test_049_get_default_fields_non_empty(self):
        """Test get_default_fields returns a non-empty list."""
        fields = TournoisFields.get_default_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_050_get_detailed_fields_non_empty(self):
        """Test get_detailed_fields returns a non-empty list."""
        fields = TournoisFields.get_detailed_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_051_detailed_superset_of_default(self):
        """Test get_detailed_fields is a superset of get_default_fields."""
        default = TournoisFields.get_default_fields()
        detailed = TournoisFields.get_detailed_fields()
        for field in default:
            self.assertIn(field, detailed)

    def test_052_get_wildcard_default(self):
        """Test get_wildcard returns list with single '*.*' entry (depth=2)."""
        wildcard = TournoisFields.get_wildcard()
        self.assertEqual(wildcard, ["*.*"])

    def test_053_get_wildcard_depth_3(self):
        """Test get_wildcard(3) returns ['*.*.*']."""
        wildcard = TournoisFields.get_wildcard(3)
        self.assertEqual(wildcard, ["*.*.*"])


class Test138EngagementsFields(unittest.TestCase):
    """Tests for EngagementsFields."""

    def test_049_get_default_fields_non_empty(self):
        """Test get_default_fields returns a non-empty list."""
        fields = EngagementsFields.get_default_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_050_get_detailed_fields_non_empty(self):
        """Test get_detailed_fields returns a non-empty list."""
        fields = EngagementsFields.get_detailed_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_051_detailed_superset_of_default(self):
        """Test get_detailed_fields is a superset of get_default_fields."""
        default = EngagementsFields.get_default_fields()
        detailed = EngagementsFields.get_detailed_fields()
        for field in default:
            self.assertIn(field, detailed)

    def test_052_get_wildcard_default(self):
        """Test get_wildcard returns list with single '*.*' entry (depth=2)."""
        wildcard = EngagementsFields.get_wildcard()
        self.assertEqual(wildcard, ["*.*"])

    def test_053_get_wildcard_depth_3(self):
        """Test get_wildcard(3) returns ['*.*.*']."""
        wildcard = EngagementsFields.get_wildcard(3)
        self.assertEqual(wildcard, ["*.*.*"])

    def test_042_get_basic_fields_non_empty(self):
        """Test get_basic_fields returns a non-empty list."""
        fields = EngagementsFields.get_basic_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_043_basic_subset_of_default(self):
        """Test get_basic_fields is a subset of get_default_fields."""
        basic = EngagementsFields.get_basic_fields()
        default = EngagementsFields.get_default_fields()
        for field in basic:
            self.assertIn(field, default)


class Test138FormationsFields(unittest.TestCase):
    """Tests for FormationsFields."""

    def test_049_get_default_fields_non_empty(self):
        """Test get_default_fields returns a non-empty list."""
        fields = FormationsFields.get_default_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_050_get_detailed_fields_non_empty(self):
        """Test get_detailed_fields returns a non-empty list."""
        fields = FormationsFields.get_detailed_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_051_detailed_superset_of_default(self):
        """Test get_detailed_fields is a superset of get_default_fields."""
        default = FormationsFields.get_default_fields()
        detailed = FormationsFields.get_detailed_fields()
        for field in default:
            self.assertIn(field, detailed)

    def test_052_get_wildcard_default(self):
        """Test get_wildcard returns list with single '*.*' entry (depth=2)."""
        wildcard = FormationsFields.get_wildcard()
        self.assertEqual(wildcard, ["*.*"])

    def test_053_get_wildcard_depth_3(self):
        """Test get_wildcard(3) returns ['*.*.*']."""
        wildcard = FormationsFields.get_wildcard(3)
        self.assertEqual(wildcard, ["*.*.*"])


class Test138PratiquesFields(unittest.TestCase):
    """Tests for PratiquesFields."""

    def test_049_get_default_fields_non_empty(self):
        """Test get_default_fields returns a non-empty list."""
        fields = PratiquesFields.get_default_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_050_get_detailed_fields_non_empty(self):
        """Test get_detailed_fields returns a non-empty list."""
        fields = PratiquesFields.get_detailed_fields()
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_051_detailed_superset_of_default(self):
        """Test get_detailed_fields is a superset of get_default_fields."""
        default = PratiquesFields.get_default_fields()
        detailed = PratiquesFields.get_detailed_fields()
        for field in default:
            self.assertIn(field, detailed)

    def test_052_get_wildcard_default(self):
        """Test get_wildcard returns list with single '*.*' entry (depth=2)."""
        wildcard = PratiquesFields.get_wildcard()
        self.assertEqual(wildcard, ["*.*"])

    def test_053_get_wildcard_depth_3(self):
        """Test get_wildcard(3) returns ['*.*.*']."""
        wildcard = PratiquesFields.get_wildcard(3)
        self.assertEqual(wildcard, ["*.*.*"])


if __name__ == "__main__":
    unittest.main()
