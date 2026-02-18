"""
Tests additionnels pour le module QueryFieldsManager pour atteindre 90% de couverture
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


class Test145QueryFieldsManagerAdditional(unittest.TestCase):
    """Tests additionnels pour le modèle QueryFieldsManager"""

    def test_001_query_fields_manager_get_organisme_fields(self):
        """Test de la méthode get_organisme_fields retourne des champs explicites"""
        fields = QueryFieldsManager.get_organisme_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields
        assert "nom" in fields
        assert OrganismeFields.WILDCARD not in fields

    def test_005_query_fields_manager_get_competition_fields(self):
        """Test de la méthode get_competition_fields retourne des champs explicites"""
        fields = QueryFieldsManager.get_competition_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields
        assert "nom" in fields
        assert CompetitionFields.WILDCARD not in fields

    def test_009_query_fields_manager_get_poule_fields(self):
        """Test de la méthode get_poule_fields retourne des champs explicites"""
        fields = QueryFieldsManager.get_poule_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields
        assert "nom" in fields
        assert PouleFields.WILDCARD not in fields

    def test_013_query_fields_manager_get_saison_fields(self):
        """Test de la méthode get_saison_fields retourne des champs explicites"""
        fields = QueryFieldsManager.get_saison_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields
        assert SaisonFields.WILDCARD not in fields

    def test_016_query_fields_manager_get_communes_fields(self):
        """Test de la méthode get_communes_fields retourne des champs explicites"""
        fields = QueryFieldsManager.get_communes_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields
        assert CommunesFields.WILDCARD not in fields

    def test_019_query_fields_manager_get_officiels_fields(self):
        """Test de la méthode get_officiels_fields retourne des champs explicites"""
        fields = QueryFieldsManager.get_officiels_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "nom" in fields
        assert OfficielsFields.WILDCARD not in fields

    def test_022_query_fields_manager_get_entraineurs_fields(self):
        """Test de la méthode get_entraineurs_fields retourne des champs explicites"""
        fields = QueryFieldsManager.get_entraineurs_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "nom" in fields
        assert EntraineursFields.WILDCARD not in fields

    def test_025_query_fields_manager_get_rencontres_fields(self):
        """Test de la méthode get_rencontres_fields retourne des champs explicites"""
        fields = QueryFieldsManager.get_rencontres_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields
        assert RencontresFields.WILDCARD not in fields

    def test_029_query_fields_manager_get_salles_fields(self):
        """Test de la méthode get_salles_fields retourne des champs explicites"""
        fields = QueryFieldsManager.get_salles_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields
        assert SallesFields.WILDCARD not in fields

    def test_032_query_fields_manager_get_terrains_fields(self):
        """Test de la méthode get_terrains_fields retourne des champs explicites"""
        fields = QueryFieldsManager.get_terrains_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields
        assert TerrainsFields.WILDCARD not in fields

    def test_035_query_fields_manager_get_tournois_fields(self):
        """Test de la méthode get_tournois_fields retourne des champs explicites"""
        fields = QueryFieldsManager.get_tournois_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields
        assert TournoisFields.WILDCARD not in fields

    def test_038_query_fields_manager_get_engagements_fields(self):
        """Test de la méthode get_engagements_fields retourne des champs explicites"""
        fields = QueryFieldsManager.get_engagements_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields
        assert EngagementsFields.WILDCARD not in fields

    def test_042_query_fields_manager_get_formations_fields(self):
        """Test de la méthode get_formations_fields retourne des champs explicites"""
        fields = QueryFieldsManager.get_formations_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields
        assert FormationsFields.WILDCARD not in fields

    def test_045_query_fields_manager_get_pratiques_fields(self):
        """Test de la méthode get_pratiques_fields retourne des champs explicites"""
        fields = QueryFieldsManager.get_pratiques_fields()
        assert isinstance(fields, list)
        assert len(fields) > 1
        assert "id" in fields
        assert PratiquesFields.WILDCARD not in fields
