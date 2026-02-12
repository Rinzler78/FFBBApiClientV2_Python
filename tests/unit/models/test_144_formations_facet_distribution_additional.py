"""
Tests additionnels pour le module FormationsFacetDistribution pour atteindre 90% de couverture
"""

import unittest

from ffbb_api_client_v2.models.formations_facet_distribution import (
    FormationsFacetDistribution,
)


class Test144FormationsFacetDistributionAdditional(unittest.TestCase):
    """Tests additionnels pour le modèle FormationsFacetDistribution"""

    def test_001_formations_facet_distribution_full_initialization(self):
        """Test d'initialisation complète de FormationsFacetDistribution avec toutes les propriétés"""
        facet_dist = FormationsFacetDistribution(
            domain={"Technique": 10, "Tactique": 5},
            mode={"Presentiel": 8, "Distanciel": 7},
            theme={"Défense": 6, "Attaque": 9},
            type={"Stage": 4, "Formation": 3},
            place={"Paris": 5, "Lyon": 4},
            places={"Gymnase A": 3, "Salle B": 4},
            postal_code={"75000": 2, "69000": 3},
            postal_codes={"75001": 1, "69002": 2},
            date_start_formatted={"2023-01-01": 1, "2023-02-01": 2},
            date_end_formatted={"2023-01-07": 1, "2023-02-07": 2},
        )

        assert facet_dist.domain == {"Technique": 10, "Tactique": 5}
        assert facet_dist.mode == {"Presentiel": 8, "Distanciel": 7}
        assert facet_dist.theme == {"Défense": 6, "Attaque": 9}
        assert facet_dist.type == {"Stage": 4, "Formation": 3}
        assert facet_dist.place == {"Paris": 5, "Lyon": 4}
        assert facet_dist.places == {"Gymnase A": 3, "Salle B": 4}
        assert facet_dist.postal_code == {"75000": 2, "69000": 3}
        assert facet_dist.postal_codes == {"75001": 1, "69002": 2}
        assert facet_dist.date_start_formatted == {"2023-01-01": 1, "2023-02-01": 2}
        assert facet_dist.date_end_formatted == {"2023-01-07": 1, "2023-02-07": 2}

    def test_002_formations_facet_distribution_minimal_initialization(self):
        """Test d'initialisation minimale de FormationsFacetDistribution"""
        facet_dist = FormationsFacetDistribution()

        assert facet_dist.domain is None
        assert facet_dist.mode is None
        assert facet_dist.theme is None
        assert facet_dist.type is None
        assert facet_dist.place is None
        assert facet_dist.places is None
        assert facet_dist.postal_code is None
        assert facet_dist.postal_codes is None
        assert facet_dist.date_start_formatted is None
        assert facet_dist.date_end_formatted is None

    def test_003_formations_facet_distribution_from_dict_full(self):
        """Test de la méthode from_dict avec un dictionnaire complet"""
        data = {
            "domain": {"Technique": 10, "Tactique": 5},
            "mode": {"Presentiel": 8, "Distanciel": 7},
            "theme": {"Défense": 6, "Attaque": 9},
            "type": {"Stage": 4, "Formation": 3},
            "place": {"Paris": 5, "Lyon": 4},
            "places": {"Gymnase A": 3, "Salle B": 4},
            "postal_code": {"75000": 2, "69000": 3},
            "postal_codes": {"75001": 1, "69002": 2},
            "date_start_formatted": {"2023-01-01": 1, "2023-02-01": 2},
            "date_end_formatted": {"2023-01-07": 1, "2023-02-07": 2},
        }

        facet_dist = FormationsFacetDistribution.from_dict(data)

        assert facet_dist.domain == {"Technique": 10, "Tactique": 5}
        assert facet_dist.mode == {"Presentiel": 8, "Distanciel": 7}
        assert facet_dist.theme == {"Défense": 6, "Attaque": 9}
        assert facet_dist.type == {"Stage": 4, "Formation": 3}
        assert facet_dist.place == {"Paris": 5, "Lyon": 4}
        assert facet_dist.places == {"Gymnase A": 3, "Salle B": 4}
        assert facet_dist.postal_code == {"75000": 2, "69000": 3}
        assert facet_dist.postal_codes == {"75001": 1, "69002": 2}
        assert facet_dist.date_start_formatted == {"2023-01-01": 1, "2023-02-01": 2}
        assert facet_dist.date_end_formatted == {"2023-01-07": 1, "2023-02-07": 2}

    def test_004_formations_facet_distribution_from_dict_minimal(self):
        """Test de la méthode from_dict avec un dictionnaire minimal"""
        data = {}

        facet_dist = FormationsFacetDistribution.from_dict(data)

        assert facet_dist.domain is None
        assert facet_dist.mode is None
        assert facet_dist.theme is None
        assert facet_dist.type is None
        assert facet_dist.place is None
        assert facet_dist.places is None
        assert facet_dist.postal_code is None
        assert facet_dist.postal_codes is None
        assert facet_dist.date_start_formatted is None
        assert facet_dist.date_end_formatted is None

    def test_005_formations_facet_distribution_to_dict_full(self):
        """Test de la méthode to_dict avec toutes les propriétés définies"""
        facet_dist = FormationsFacetDistribution(
            domain={"Technique": 10, "Tactique": 5},
            mode={"Presentiel": 8, "Distanciel": 7},
            theme={"Défense": 6, "Attaque": 9},
            type={"Stage": 4, "Formation": 3},
            place={"Paris": 5, "Lyon": 4},
            places={"Gymnase A": 3, "Salle B": 4},
            postal_code={"75000": 2, "69000": 3},
            postal_codes={"75001": 1, "69002": 2},
            date_start_formatted={"2023-01-01": 1, "2023-02-01": 2},
            date_end_formatted={"2023-01-07": 1, "2023-02-07": 2},
        )

        result = facet_dist.to_dict()

        assert result["domain"] == {"Technique": 10, "Tactique": 5}
        assert result["mode"] == {"Presentiel": 8, "Distanciel": 7}
        assert result["theme"] == {"Défense": 6, "Attaque": 9}
        assert result["type"] == {"Stage": 4, "Formation": 3}
        assert result["place"] == {"Paris": 5, "Lyon": 4}
        assert result["places"] == {"Gymnase A": 3, "Salle B": 4}
        assert result["postal_code"] == {"75000": 2, "69000": 3}
        assert result["postal_codes"] == {"75001": 1, "69002": 2}
        assert result["date_start_formatted"] == {"2023-01-01": 1, "2023-02-01": 2}
        assert result["date_end_formatted"] == {"2023-01-07": 1, "2023-02-07": 2}

    def test_006_formations_facet_distribution_to_dict_minimal(self):
        """Test de la méthode to_dict avec un objet minimal"""
        facet_dist = FormationsFacetDistribution()

        result = facet_dist.to_dict()

        # Vérifie que le dictionnaire est vide puisque toutes les propriétés sont None
        assert result == {}

    def test_007_formations_facet_distribution_from_dict_with_none_values(self):
        """Test de la méthode from_dict avec des valeurs None"""
        data = {
            "domain": None,
            "mode": None,
            "theme": None,
            "type": None,
            "place": None,
            "places": None,
            "postal_code": None,
            "postal_codes": None,
            "date_start_formatted": None,
            "date_end_formatted": None,
        }

        facet_dist = FormationsFacetDistribution.from_dict(data)

        assert facet_dist.domain is None
        assert facet_dist.mode is None
        assert facet_dist.theme is None
        assert facet_dist.type is None
        assert facet_dist.place is None
        assert facet_dist.places is None
        assert facet_dist.postal_code is None
        assert facet_dist.postal_codes is None
        assert facet_dist.date_start_formatted is None
        assert facet_dist.date_end_formatted is None

    def test_008_formations_facet_distribution_assertion_error(self):
        """Test de la méthode from_dict avec un objet non-dict (devrait lever une assertion)"""
        with self.assertRaises(AssertionError):
            FormationsFacetDistribution.from_dict("not_a_dict")

    def test_009_formations_facet_distribution_round_trip(self):
        """Test de conversion depuis/depuis un dictionnaire"""
        original_data = {
            "domain": {"Technique": 10, "Tactique": 5},
            "mode": {"Presentiel": 8, "Distanciel": 7},
            "theme": {"Défense": 6, "Attaque": 9},
            "type": {"Stage": 4, "Formation": 3},
            "place": {"Paris": 5, "Lyon": 4},
            "places": {"Gymnase A": 3, "Salle B": 4},
            "postal_code": {"75000": 2, "69000": 3},
            "postal_codes": {"75001": 1, "69002": 2},
            "date_start_formatted": {"2023-01-01": 1, "2023-02-01": 2},
            "date_end_formatted": {"2023-01-07": 1, "2023-02-07": 2},
        }

        # Convertir du dictionnaire à l'objet
        facet_dist = FormationsFacetDistribution.from_dict(original_data)

        # Convertir de l'objet au dictionnaire
        result_data = facet_dist.to_dict()

        # Vérifier que les champs essentiels sont présents
        assert result_data["domain"] == {"Technique": 10, "Tactique": 5}
        assert result_data["mode"] == {"Presentiel": 8, "Distanciel": 7}
        assert result_data["theme"] == {"Défense": 6, "Attaque": 9}
        assert result_data["type"] == {"Stage": 4, "Formation": 3}
        assert result_data["place"] == {"Paris": 5, "Lyon": 4}
        assert result_data["places"] == {"Gymnase A": 3, "Salle B": 4}
        assert result_data["postal_code"] == {"75000": 2, "69000": 3}
        assert result_data["postal_codes"] == {"75001": 1, "69002": 2}
        assert result_data["date_start_formatted"] == {"2023-01-01": 1, "2023-02-01": 2}
        assert result_data["date_end_formatted"] == {"2023-01-07": 1, "2023-02-07": 2}

    def test_010_formations_facet_distribution_partial_data(self):
        """Test de la méthode from_dict avec des données partielles"""
        data = {
            "domain": {"Technique": 10, "Tactique": 5}
            # Seulement un champ pour tester le traitement partiel
        }

        facet_dist = FormationsFacetDistribution.from_dict(data)

        assert facet_dist.domain == {"Technique": 10, "Tactique": 5}
        assert facet_dist.mode is None
        assert facet_dist.theme is None
        assert facet_dist.type is None
        assert facet_dist.place is None
        assert facet_dist.places is None
        assert facet_dist.postal_code is None
        assert facet_dist.postal_codes is None
        assert facet_dist.date_start_formatted is None
        assert facet_dist.date_end_formatted is None
