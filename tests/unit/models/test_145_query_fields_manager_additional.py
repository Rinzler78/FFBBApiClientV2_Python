"""
Tests additionnels pour les *Fields classes (couverture get_fields).
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


class Test145FieldsClassesGetFields(unittest.TestCase):
    """Tests that each *Fields.get_fields() returns explicit field lists."""

    def test_001_organisme_get_fields(self):
        """Test OrganismeFields.get_fields() returns explicit fields."""
        fields = OrganismeFields.get_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields
        assert "nom" in fields

    def test_005_competition_get_fields(self):
        """Test CompetitionFields.get_fields() returns explicit fields."""
        fields = CompetitionFields.get_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields
        assert "nom" in fields

    def test_009_poule_get_fields(self):
        """Test PouleFields.get_fields() returns explicit fields."""
        fields = PouleFields.get_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields
        assert "nom" in fields

    def test_013_saison_get_fields(self):
        """Test SaisonFields.get_fields() returns explicit fields."""
        fields = SaisonFields.get_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields

    def test_016_communes_get_fields(self):
        """Test CommunesFields.get_fields() returns explicit fields."""
        fields = CommunesFields.get_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields

    def test_019_officiels_get_fields(self):
        """Test OfficielsFields.get_fields() returns explicit fields."""
        fields = OfficielsFields.get_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "nom" in fields

    def test_022_entraineurs_get_fields(self):
        """Test EntraineursFields.get_fields() returns explicit fields."""
        fields = EntraineursFields.get_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "nom" in fields

    def test_025_rencontres_get_fields(self):
        """Test RencontresFields.get_fields() returns explicit fields."""
        fields = RencontresFields.get_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields

    def test_029_salles_get_fields(self):
        """Test SallesFields.get_fields() returns explicit fields."""
        fields = SallesFields.get_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields

    def test_032_terrains_get_fields(self):
        """Test TerrainsFields.get_fields() returns explicit fields."""
        fields = TerrainsFields.get_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields

    def test_035_tournois_get_fields(self):
        """Test TournoisFields.get_fields() returns explicit fields."""
        fields = TournoisFields.get_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields

    def test_038_engagements_get_fields(self):
        """Test EngagementsFields.get_fields() returns explicit fields."""
        fields = EngagementsFields.get_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields

    def test_042_formations_get_fields(self):
        """Test FormationsFields.get_fields() returns explicit fields."""
        fields = FormationsFields.get_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields

    def test_045_pratiques_get_fields(self):
        """Test PratiquesFields.get_fields() returns explicit fields."""
        fields = PratiquesFields.get_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields
