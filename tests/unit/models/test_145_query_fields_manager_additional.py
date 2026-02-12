"""
Tests additionnels pour le module QueryFieldsManager pour atteindre 90% de couverture
"""

import unittest

from ffbb_api_client_v2.models.field_set import FieldSet
from ffbb_api_client_v2.models.query_fields_manager import QueryFieldsManager


class Test145QueryFieldsManagerAdditional(unittest.TestCase):
    """Tests additionnels pour le modèle QueryFieldsManager"""

    def test_001_query_fields_manager_get_organisme_fields_default(self):
        """Test de la méthode get_organisme_fields avec FieldSet.DEFAULT"""
        fields = QueryFieldsManager.get_organisme_fields(FieldSet.DEFAULT)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_002_query_fields_manager_get_organisme_fields_basic(self):
        """Test de la méthode get_organisme_fields avec FieldSet.BASIC"""
        fields = QueryFieldsManager.get_organisme_fields(FieldSet.BASIC)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_003_query_fields_manager_get_organisme_fields_detailed(self):
        """Test de la méthode get_organisme_fields avec FieldSet.DETAILED"""
        fields = QueryFieldsManager.get_organisme_fields(FieldSet.DETAILED)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_004_query_fields_manager_get_organisme_fields_wildcard(self):
        """Test de la méthode get_organisme_fields avec FieldSet.WILDCARD"""
        fields = QueryFieldsManager.get_organisme_fields(FieldSet.WILDCARD)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_005_query_fields_manager_get_competition_fields_default(self):
        """Test de la méthode get_competition_fields avec FieldSet.DEFAULT"""
        fields = QueryFieldsManager.get_competition_fields(FieldSet.DEFAULT)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_006_query_fields_manager_get_competition_fields_basic(self):
        """Test de la méthode get_competition_fields avec FieldSet.BASIC"""
        fields = QueryFieldsManager.get_competition_fields(FieldSet.BASIC)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_007_query_fields_manager_get_competition_fields_detailed(self):
        """Test de la méthode get_competition_fields avec FieldSet.DETAILED"""
        fields = QueryFieldsManager.get_competition_fields(FieldSet.DETAILED)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_008_query_fields_manager_get_competition_fields_wildcard(self):
        """Test de la méthode get_competition_fields avec FieldSet.WILDCARD"""
        fields = QueryFieldsManager.get_competition_fields(FieldSet.WILDCARD)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_009_query_fields_manager_get_poule_fields_default(self):
        """Test de la méthode get_poule_fields avec FieldSet.DEFAULT"""
        fields = QueryFieldsManager.get_poule_fields(FieldSet.DEFAULT)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_010_query_fields_manager_get_poule_fields_basic(self):
        """Test de la méthode get_poule_fields avec FieldSet.BASIC"""
        fields = QueryFieldsManager.get_poule_fields(FieldSet.BASIC)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_011_query_fields_manager_get_poule_fields_detailed(self):
        """Test de la méthode get_poule_fields avec FieldSet.DETAILED"""
        fields = QueryFieldsManager.get_poule_fields(FieldSet.DETAILED)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_012_query_fields_manager_get_poule_fields_wildcard(self):
        """Test de la méthode get_poule_fields avec FieldSet.WILDCARD"""
        fields = QueryFieldsManager.get_poule_fields(FieldSet.WILDCARD)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_013_query_fields_manager_get_saison_fields_default(self):
        """Test de la méthode get_saison_fields avec FieldSet.DEFAULT"""
        fields = QueryFieldsManager.get_saison_fields(FieldSet.DEFAULT)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_014_query_fields_manager_get_saison_fields_detailed(self):
        """Test de la méthode get_saison_fields avec FieldSet.DETAILED"""
        fields = QueryFieldsManager.get_saison_fields(FieldSet.DETAILED)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_015_query_fields_manager_get_saison_fields_wildcard(self):
        """Test de la méthode get_saison_fields avec FieldSet.WILDCARD"""
        fields = QueryFieldsManager.get_saison_fields(FieldSet.WILDCARD)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_016_query_fields_manager_get_communes_fields_default(self):
        """Test de la méthode get_communes_fields avec FieldSet.DEFAULT"""
        fields = QueryFieldsManager.get_communes_fields(FieldSet.DEFAULT)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_017_query_fields_manager_get_communes_fields_detailed(self):
        """Test de la méthode get_communes_fields avec FieldSet.DETAILED"""
        fields = QueryFieldsManager.get_communes_fields(FieldSet.DETAILED)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_018_query_fields_manager_get_communes_fields_wildcard(self):
        """Test de la méthode get_communes_fields avec FieldSet.WILDCARD"""
        fields = QueryFieldsManager.get_communes_fields(FieldSet.WILDCARD)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_019_query_fields_manager_get_officiels_fields_default(self):
        """Test de la méthode get_officiels_fields avec FieldSet.DEFAULT"""
        fields = QueryFieldsManager.get_officiels_fields(FieldSet.DEFAULT)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_020_query_fields_manager_get_officiels_fields_detailed(self):
        """Test de la méthode get_officiels_fields avec FieldSet.DETAILED"""
        fields = QueryFieldsManager.get_officiels_fields(FieldSet.DETAILED)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_021_query_fields_manager_get_officiels_fields_wildcard(self):
        """Test de la méthode get_officiels_fields avec FieldSet.WILDCARD"""
        fields = QueryFieldsManager.get_officiels_fields(FieldSet.WILDCARD)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_022_query_fields_manager_get_entraineurs_fields_default(self):
        """Test de la méthode get_entraineurs_fields avec FieldSet.DEFAULT"""
        fields = QueryFieldsManager.get_entraineurs_fields(FieldSet.DEFAULT)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_023_query_fields_manager_get_entraineurs_fields_detailed(self):
        """Test de la méthode get_entraineurs_fields avec FieldSet.DETAILED"""
        fields = QueryFieldsManager.get_entraineurs_fields(FieldSet.DETAILED)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_024_query_fields_manager_get_entraineurs_fields_wildcard(self):
        """Test de la méthode get_entraineurs_fields avec FieldSet.WILDCARD"""
        fields = QueryFieldsManager.get_entraineurs_fields(FieldSet.WILDCARD)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_025_query_fields_manager_get_rencontres_fields_default(self):
        """Test de la méthode get_rencontres_fields avec FieldSet.DEFAULT"""
        fields = QueryFieldsManager.get_rencontres_fields(FieldSet.DEFAULT)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_026_query_fields_manager_get_rencontres_fields_basic(self):
        """Test de la méthode get_rencontres_fields avec FieldSet.BASIC"""
        fields = QueryFieldsManager.get_rencontres_fields(FieldSet.BASIC)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_027_query_fields_manager_get_rencontres_fields_detailed(self):
        """Test de la méthode get_rencontres_fields avec FieldSet.DETAILED"""
        fields = QueryFieldsManager.get_rencontres_fields(FieldSet.DETAILED)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_028_query_fields_manager_get_rencontres_fields_wildcard(self):
        """Test de la méthode get_rencontres_fields avec FieldSet.WILDCARD"""
        fields = QueryFieldsManager.get_rencontres_fields(FieldSet.WILDCARD)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_029_query_fields_manager_get_salles_fields_default(self):
        """Test de la méthode get_salles_fields avec FieldSet.DEFAULT"""
        fields = QueryFieldsManager.get_salles_fields(FieldSet.DEFAULT)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_030_query_fields_manager_get_salles_fields_detailed(self):
        """Test de la méthode get_salles_fields avec FieldSet.DETAILED"""
        fields = QueryFieldsManager.get_salles_fields(FieldSet.DETAILED)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_031_query_fields_manager_get_salles_fields_wildcard(self):
        """Test de la méthode get_salles_fields avec FieldSet.WILDCARD"""
        fields = QueryFieldsManager.get_salles_fields(FieldSet.WILDCARD)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_032_query_fields_manager_get_terrains_fields_default(self):
        """Test de la méthode get_terrains_fields avec FieldSet.DEFAULT"""
        fields = QueryFieldsManager.get_terrains_fields(FieldSet.DEFAULT)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_033_query_fields_manager_get_terrains_fields_detailed(self):
        """Test de la méthode get_terrains_fields avec FieldSet.DETAILED"""
        fields = QueryFieldsManager.get_terrains_fields(FieldSet.DETAILED)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_034_query_fields_manager_get_terrains_fields_wildcard(self):
        """Test de la méthode get_terrains_fields avec FieldSet.WILDCARD"""
        fields = QueryFieldsManager.get_terrains_fields(FieldSet.WILDCARD)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_035_query_fields_manager_get_tournois_fields_default(self):
        """Test de la méthode get_tournois_fields avec FieldSet.DEFAULT"""
        fields = QueryFieldsManager.get_tournois_fields(FieldSet.DEFAULT)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_036_query_fields_manager_get_tournois_fields_detailed(self):
        """Test de la méthode get_tournois_fields avec FieldSet.DETAILED"""
        fields = QueryFieldsManager.get_tournois_fields(FieldSet.DETAILED)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_037_query_fields_manager_get_tournois_fields_wildcard(self):
        """Test de la méthode get_tournois_fields avec FieldSet.WILDCARD"""
        fields = QueryFieldsManager.get_tournois_fields(FieldSet.WILDCARD)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_038_query_fields_manager_get_engagements_fields_default(self):
        """Test de la méthode get_engagements_fields avec FieldSet.DEFAULT"""
        fields = QueryFieldsManager.get_engagements_fields(FieldSet.DEFAULT)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_039_query_fields_manager_get_engagements_fields_basic(self):
        """Test de la méthode get_engagements_fields avec FieldSet.BASIC"""
        fields = QueryFieldsManager.get_engagements_fields(FieldSet.BASIC)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_040_query_fields_manager_get_engagements_fields_detailed(self):
        """Test de la méthode get_engagements_fields avec FieldSet.DETAILED"""
        fields = QueryFieldsManager.get_engagements_fields(FieldSet.DETAILED)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_041_query_fields_manager_get_engagements_fields_wildcard(self):
        """Test de la méthode get_engagements_fields avec FieldSet.WILDCARD"""
        fields = QueryFieldsManager.get_engagements_fields(FieldSet.WILDCARD)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_042_query_fields_manager_get_formations_fields_default(self):
        """Test de la méthode get_formations_fields avec FieldSet.DEFAULT"""
        fields = QueryFieldsManager.get_formations_fields(FieldSet.DEFAULT)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_043_query_fields_manager_get_formations_fields_detailed(self):
        """Test de la méthode get_formations_fields avec FieldSet.DETAILED"""
        fields = QueryFieldsManager.get_formations_fields(FieldSet.DETAILED)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_044_query_fields_manager_get_formations_fields_wildcard(self):
        """Test de la méthode get_formations_fields avec FieldSet.WILDCARD"""
        fields = QueryFieldsManager.get_formations_fields(FieldSet.WILDCARD)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_045_query_fields_manager_get_pratiques_fields_default(self):
        """Test de la méthode get_pratiques_fields avec FieldSet.DEFAULT"""
        fields = QueryFieldsManager.get_pratiques_fields(FieldSet.DEFAULT)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_046_query_fields_manager_get_pratiques_fields_detailed(self):
        """Test de la méthode get_pratiques_fields avec FieldSet.DETAILED"""
        fields = QueryFieldsManager.get_pratiques_fields(FieldSet.DETAILED)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_047_query_fields_manager_get_pratiques_fields_wildcard(self):
        """Test de la méthode get_pratiques_fields avec FieldSet.WILDCARD"""
        fields = QueryFieldsManager.get_pratiques_fields(FieldSet.WILDCARD)
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_048_query_fields_manager_get_fields_with_invalid_field_set(self):
        """Test de la méthode get_organisme_fields avec un FieldSet invalide (devrait utiliser DEFAULT)"""

        # Utiliser un objet arbitraire comme FieldSet invalide
        class InvalidFieldSet:
            pass

        # Tester avec un appel direct à la méthode pour vérifier le comportement par défaut
        # Puisque le code utilise une comparaison avec des constantes FieldSet,
        # un objet différent devrait utiliser la branche else (DEFAULT)
        fields = QueryFieldsManager.get_organisme_fields(InvalidFieldSet())
        assert isinstance(fields, list)
        assert len(fields) > 0
