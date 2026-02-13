"""
Tests additionnels pour le module EngagementsFacetDistribution pour atteindre 90% de couverture
"""

import unittest

from ffbb_api_client_v2.meilisearch_ffbb.models.engagements_facet_distribution import (
    EngagementsFacetDistribution,
)
from ffbb_api_client_v2.models.sexe_class import SexeClass


class Test143EngagementsFacetDistributionAdditional(unittest.TestCase):
    """Tests additionnels pour le modèle EngagementsFacetDistribution"""

    def test_001_engagements_facet_distribution_full_initialization(self):
        """Test d'initialisation complète de EngagementsFacetDistribution avec toutes les propriétés"""
        sexe_class = SexeClass(masculine=5, feminine=3, mixed=2)

        facet_dist = EngagementsFacetDistribution(
            club_pro={"OUI": 10, "NON": 5},
            id_competition_categorie_code={"U15": 8, "U18": 7},
            id_competition_categorie_libelle={"Minimes": 6, "Cadets": 9},
            id_competition_code={"CHAMP": 4, "COUPE": 3},
            id_competition_nom={"Championnat National": 4, "Coupe de France": 3},
            id_competition_sexe=sexe_class,
            id_poule_nom={"Groupe A": 5, "Groupe B": 4},
            niveau_code={"EXC": 3, "DIV1": 4},
            niveau_libelle={"Excellence": 3, "Division 1": 4},
        )

        assert facet_dist.club_pro == {"OUI": 10, "NON": 5}
        assert facet_dist.id_competition_categorie_code == {"U15": 8, "U18": 7}
        assert facet_dist.id_competition_categorie_libelle == {
            "Minimes": 6,
            "Cadets": 9,
        }
        assert facet_dist.id_competition_code == {"CHAMP": 4, "COUPE": 3}
        assert facet_dist.id_competition_nom == {
            "Championnat National": 4,
            "Coupe de France": 3,
        }
        assert facet_dist.id_competition_sexe == sexe_class
        assert facet_dist.id_poule_nom == {"Groupe A": 5, "Groupe B": 4}
        assert facet_dist.niveau_code == {"EXC": 3, "DIV1": 4}
        assert facet_dist.niveau_libelle == {"Excellence": 3, "Division 1": 4}

    def test_002_engagements_facet_distribution_minimal_initialization(self):
        """Test d'initialisation minimale de EngagementsFacetDistribution"""
        facet_dist = EngagementsFacetDistribution()

        assert facet_dist.club_pro is None
        assert facet_dist.id_competition_categorie_code is None
        assert facet_dist.id_competition_categorie_libelle is None
        assert facet_dist.id_competition_code is None
        assert facet_dist.id_competition_nom is None
        assert facet_dist.id_competition_sexe is None
        assert facet_dist.id_poule_nom is None
        assert facet_dist.niveau_code is None
        assert facet_dist.niveau_libelle is None

    def test_003_engagements_facet_distribution_from_dict_full(self):
        """Test de la méthode from_dict avec un dictionnaire complet"""
        data = {
            "clubPro": {"OUI": 10, "NON": 5},
            "idCompetition.categorie.code": {"U15": 8, "U18": 7},
            "idCompetition.categorie.libelle": {"Minimes": 6, "Cadets": 9},
            "idCompetition.code": {"CHAMP": 4, "COUPE": 3},
            "idCompetition.nom": {"Championnat National": 4, "Coupe de France": 3},
            "idCompetition.sexe": {"libelle": "Masculin", "code": "M"},
            "idPoule.nom": {"Groupe A": 5, "Groupe B": 4},
            "niveau.code": {"EXC": 3, "DIV1": 4},
            "niveau.libelle": {"Excellence": 3, "Division 1": 4},
        }

        facet_dist = EngagementsFacetDistribution.from_dict(data)

        assert facet_dist.club_pro == {"OUI": 10, "NON": 5}
        assert facet_dist.id_competition_categorie_code == {"U15": 8, "U18": 7}
        assert facet_dist.id_competition_categorie_libelle == {
            "Minimes": 6,
            "Cadets": 9,
        }
        assert facet_dist.id_competition_code == {"CHAMP": 4, "COUPE": 3}
        assert facet_dist.id_competition_nom == {
            "Championnat National": 4,
            "Coupe de France": 3,
        }
        assert facet_dist.id_competition_sexe is not None
        assert facet_dist.id_poule_nom == {"Groupe A": 5, "Groupe B": 4}
        assert facet_dist.niveau_code == {"EXC": 3, "DIV1": 4}
        assert facet_dist.niveau_libelle == {"Excellence": 3, "Division 1": 4}

    def test_004_engagements_facet_distribution_from_dict_minimal(self):
        """Test de la méthode from_dict avec un dictionnaire minimal"""
        data = {}

        facet_dist = EngagementsFacetDistribution.from_dict(data)

        assert facet_dist.club_pro is None
        assert facet_dist.id_competition_categorie_code is None
        assert facet_dist.id_competition_categorie_libelle is None
        assert facet_dist.id_competition_code is None
        assert facet_dist.id_competition_nom is None
        assert facet_dist.id_competition_sexe is None
        assert facet_dist.id_poule_nom is None
        assert facet_dist.niveau_code is None
        assert facet_dist.niveau_libelle is None

    def test_005_engagements_facet_distribution_to_dict_full(self):
        """Test de la méthode to_dict avec toutes les propriétés définies"""
        sexe_class = SexeClass(masculine=5, feminine=3, mixed=2)

        facet_dist = EngagementsFacetDistribution(
            club_pro={"OUI": 10, "NON": 5},
            id_competition_categorie_code={"U15": 8, "U18": 7},
            id_competition_categorie_libelle={"Minimes": 6, "Cadets": 9},
            id_competition_code={"CHAMP": 4, "COUPE": 3},
            id_competition_nom={"Championnat National": 4, "Coupe de France": 3},
            id_competition_sexe=sexe_class,
            id_poule_nom={"Groupe A": 5, "Groupe B": 4},
            niveau_code={"EXC": 3, "DIV1": 4},
            niveau_libelle={"Excellence": 3, "Division 1": 4},
        )

        result = facet_dist.to_dict()

        assert result["clubPro"] == {"OUI": 10, "NON": 5}
        assert result["idCompetition.categorie.code"] == {"U15": 8, "U18": 7}
        assert result["idCompetition.categorie.libelle"] == {"Minimes": 6, "Cadets": 9}
        assert result["idCompetition.code"] == {"CHAMP": 4, "COUPE": 3}
        assert result["idCompetition.nom"] == {
            "Championnat National": 4,
            "Coupe de France": 3,
        }
        assert result["idCompetition.sexe"] is not None
        assert result["idPoule.nom"] == {"Groupe A": 5, "Groupe B": 4}
        assert result["niveau.code"] == {"EXC": 3, "DIV1": 4}
        assert result["niveau.libelle"] == {"Excellence": 3, "Division 1": 4}

    def test_006_engagements_facet_distribution_to_dict_minimal(self):
        """Test de la méthode to_dict avec un objet minimal"""
        facet_dist = EngagementsFacetDistribution()

        result = facet_dist.to_dict()

        # Vérifie que le dictionnaire est vide puisque toutes les propriétés sont None
        assert result == {}

    def test_007_engagements_facet_distribution_from_dict_with_none_values(self):
        """Test de la méthode from_dict avec des valeurs None"""
        data = {
            "clubPro": None,
            "idCompetition.categorie.code": None,
            "idCompetition.categorie.libelle": None,
            "idCompetition.code": None,
            "idCompetition.nom": None,
            "idCompetition.sexe": None,
            "idPoule.nom": None,
            "niveau.code": None,
            "niveau.libelle": None,
        }

        facet_dist = EngagementsFacetDistribution.from_dict(data)

        assert facet_dist.club_pro is None
        assert facet_dist.id_competition_categorie_code is None
        assert facet_dist.id_competition_categorie_libelle is None
        assert facet_dist.id_competition_code is None
        assert facet_dist.id_competition_nom is None
        assert facet_dist.id_competition_sexe is None
        assert facet_dist.id_poule_nom is None
        assert facet_dist.niveau_code is None
        assert facet_dist.niveau_libelle is None

    def test_008_engagements_facet_distribution_assertion_error(self):
        """Test de la méthode from_dict avec un objet non-dict (devrait lever une assertion)"""
        with self.assertRaises(AssertionError):
            EngagementsFacetDistribution.from_dict("not_a_dict")

    def test_009_engagements_facet_distribution_round_trip(self):
        """Test de conversion depuis/depuis un dictionnaire"""
        original_data = {
            "clubPro": {"OUI": 10, "NON": 5},
            "idCompetition.categorie.code": {"U15": 8, "U18": 7},
            "idCompetition.categorie.libelle": {"Minimes": 6, "Cadets": 9},
            "idCompetition.code": {"CHAMP": 4, "COUPE": 3},
            "idCompetition.nom": {"Championnat National": 4, "Coupe de France": 3},
            "idCompetition.sexe": {"libelle": "Masculin", "code": "M"},
            "idPoule.nom": {"Groupe A": 5, "Groupe B": 4},
            "niveau.code": {"EXC": 3, "DIV1": 4},
            "niveau.libelle": {"Excellence": 3, "Division 1": 4},
        }

        # Convertir du dictionnaire à l'objet
        facet_dist = EngagementsFacetDistribution.from_dict(original_data)

        # Convertir de l'objet au dictionnaire
        result_data = facet_dist.to_dict()

        # Vérifier que les champs essentiels sont présents
        assert result_data["clubPro"] == {"OUI": 10, "NON": 5}
        assert result_data["idCompetition.categorie.code"] == {"U15": 8, "U18": 7}
        assert result_data["idCompetition.categorie.libelle"] == {
            "Minimes": 6,
            "Cadets": 9,
        }
        assert result_data["idCompetition.code"] == {"CHAMP": 4, "COUPE": 3}
        assert result_data["idCompetition.nom"] == {
            "Championnat National": 4,
            "Coupe de France": 3,
        }
        assert "idCompetition.sexe" in result_data
        assert result_data["idPoule.nom"] == {"Groupe A": 5, "Groupe B": 4}
        assert result_data["niveau.code"] == {"EXC": 3, "DIV1": 4}
        assert result_data["niveau.libelle"] == {"Excellence": 3, "Division 1": 4}

    def test_010_engagements_facet_distribution_partial_data(self):
        """Test de la méthode from_dict avec des données partielles"""
        data = {
            "clubPro": {"OUI": 10, "NON": 5}
            # Seulement un champ pour tester le traitement partiel
        }

        facet_dist = EngagementsFacetDistribution.from_dict(data)

        assert facet_dist.club_pro == {"OUI": 10, "NON": 5}
        assert facet_dist.id_competition_categorie_code is None
        assert facet_dist.id_competition_categorie_libelle is None
        assert facet_dist.id_competition_code is None
        assert facet_dist.id_competition_nom is None
        assert facet_dist.id_competition_sexe is None
        assert facet_dist.id_poule_nom is None
        assert facet_dist.niveau_code is None
        assert facet_dist.niveau_libelle is None
