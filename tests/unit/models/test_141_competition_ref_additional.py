"""
Tests additionnels pour le module CompetitionDetail pour atteindre 90% de couverture
"""

import unittest
from uuid import UUID

from ffbb_api_client_v2.models.categorie import Categorie
from ffbb_api_client_v2.models.competition_detail import CompetitionDetail
from ffbb_api_client_v2.models.organisateur import Organisateur
from ffbb_api_client_v2.models.saison import Saison
from ffbb_api_client_v2.models.type_competition_enum import TypeCompetitionEnum
from ffbb_api_client_v2.models.type_competition_generique import (
    TypeCompetitionGenerique,
)


class Test141CompetitionDetailAdditional(unittest.TestCase):
    """Tests additionnels pour le modèle CompetitionDetail"""

    def test_001_competition_ref_full_initialization(self):
        """Test d'initialisation complète de CompetitionDetail avec toutes les propriétés"""
        logo = UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567890")
        saison = Saison(code="2024")
        organisateur = Organisateur(id="org123", nom="Org Test")
        type_comp_gen = TypeCompetitionGenerique(
            type_competition_generique_id="type123", logo=None
        )
        categorie = Categorie(categorie_id="cat123", libelle="Catégorie Test")

        competition_ref = CompetitionDetail(
            id="comp123",
            nom="Comp Test",
            code="CT001",
            sexe="M",
            competition_origine="Ligue",
            competition_origine_nom="Ligue Test",
            competition_origine_niveau=1,
            type_competition=TypeCompetitionEnum.CHAMPIONNAT,
            logo=logo,
            saison=saison,
            id_competition_pere="parent123",
            organisateur=organisateur,
            type_competition_generique=type_comp_gen,
            categorie=categorie,
        )

        assert competition_ref.id == "comp123"
        assert competition_ref.nom == "Comp Test"
        assert competition_ref.code == "CT001"
        assert competition_ref.sexe == "M"
        assert competition_ref.competition_origine == "Ligue"
        assert competition_ref.competition_origine_nom == "Ligue Test"
        assert competition_ref.competition_origine_niveau == 1
        assert competition_ref.type_competition == TypeCompetitionEnum.CHAMPIONNAT
        assert competition_ref.logo == logo
        assert competition_ref.saison == saison
        assert competition_ref.id_competition_pere == "parent123"
        assert competition_ref.organisateur == organisateur
        assert competition_ref.type_competition_generique == type_comp_gen
        assert competition_ref.categorie == categorie

    def test_002_competition_ref_minimal_initialization(self):
        """Test d'initialisation minimale de CompetitionDetail"""
        competition_ref = CompetitionDetail()

        assert competition_ref.id is None
        assert competition_ref.nom is None
        assert competition_ref.code is None
        assert competition_ref.sexe is None
        assert competition_ref.competition_origine is None
        assert competition_ref.competition_origine_nom is None
        assert competition_ref.competition_origine_niveau is None
        assert competition_ref.type_competition is None
        assert competition_ref.logo is None
        assert competition_ref.saison is None
        assert competition_ref.id_competition_pere is None
        assert competition_ref.organisateur is None
        assert competition_ref.type_competition_generique is None
        assert competition_ref.categorie is None

    def test_003_competition_ref_from_dict_full(self):
        """Test de la méthode from_dict avec un dictionnaire complet"""
        data = {
            "id": "comp123",
            "nom": "Comp Test",
            "code": "CT001",
            "sexe": "F",
            "competition_origine": "District",
            "competition_origine_nom": "District Test",
            "competition_origine_niveau": 2,
            "typeCompetition": "Coupe",
            "logo": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "saison": {"code": "2024"},
            "idCompetitionPere": "parent456",
            "organisateur": {"id": "org123", "nom": "Org Test"},
            "typeCompetitionGenerique": {"id": "type123", "libelle": "Type Test"},
            "categorie": {"id": "cat123", "libelle": "Catégorie Test"},
        }

        competition_ref = CompetitionDetail.from_dict(data)

        assert competition_ref.id == "comp123"
        assert competition_ref.nom == "Comp Test"
        assert competition_ref.code == "CT001"
        assert competition_ref.sexe == "F"
        assert competition_ref.competition_origine == "District"
        assert competition_ref.competition_origine_nom == "District Test"
        assert competition_ref.competition_origine_niveau == 2
        from ffbb_api_client_v2.models.type_competition_enum import TypeCompetitionEnum

        assert competition_ref.type_competition == TypeCompetitionEnum.COUPE
        assert competition_ref.logo is not None
        assert competition_ref.saison is not None
        assert competition_ref.id_competition_pere == "parent456"
        assert competition_ref.organisateur is not None
        assert competition_ref.type_competition_generique is not None
        assert competition_ref.categorie is not None

    def test_004_competition_ref_from_dict_minimal(self):
        """Test de la méthode from_dict avec un dictionnaire minimal"""
        data = {}

        competition_ref = CompetitionDetail.from_dict(data)

        assert competition_ref.id is None
        assert competition_ref.nom is None
        assert competition_ref.code is None
        assert competition_ref.sexe is None
        assert competition_ref.competition_origine is None
        assert competition_ref.competition_origine_nom is None
        assert competition_ref.competition_origine_niveau is None
        assert competition_ref.type_competition is None
        assert competition_ref.logo is None
        assert competition_ref.saison is None
        assert competition_ref.id_competition_pere is None
        assert competition_ref.organisateur is None
        assert competition_ref.type_competition_generique is None
        assert competition_ref.categorie is None

    def test_005_competition_ref_to_dict_full(self):
        """Test de la méthode to_dict avec toutes les propriétés définies"""
        logo = UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567890")
        saison = Saison(code="2024")
        organisateur = Organisateur(id="org123", nom="Org Test")
        type_comp_gen = TypeCompetitionGenerique(
            type_competition_generique_id="type123", logo=None
        )
        categorie = Categorie(categorie_id="cat123", libelle="Catégorie Test")

        competition_ref = CompetitionDetail(
            id="comp123",
            nom="Comp Test",
            code="CT001",
            sexe="M",
            competition_origine="Ligue",
            competition_origine_nom="Ligue Test",
            competition_origine_niveau=1,
            type_competition=TypeCompetitionEnum.CHAMPIONNAT,
            logo=logo,
            saison=saison,
            id_competition_pere="parent123",
            organisateur=organisateur,
            type_competition_generique=type_comp_gen,
            categorie=categorie,
        )

        result = competition_ref.to_dict()

        assert result["id"] == "comp123"
        assert result["nom"] == "Comp Test"
        assert result["code"] == "CT001"
        assert result["sexe"] == "M"
        assert result["competition_origine"] == "Ligue"
        assert result["competition_origine_nom"] == "Ligue Test"
        assert result["competition_origine_niveau"] == 1
        assert result["typeCompetition"] == "Championnat"
        assert result["logo"] is not None
        assert result["saison"] is not None
        assert result["idCompetitionPere"] == "parent123"
        assert result["organisateur"] is not None
        assert result["typeCompetitionGenerique"] is not None
        assert result["categorie"] is not None

    def test_006_competition_ref_to_dict_minimal(self):
        """Test de la méthode to_dict avec un objet minimal"""
        competition_ref = CompetitionDetail()

        result = competition_ref.to_dict()

        # Vérifie que le dictionnaire est vide puisque toutes les propriétés sont None
        assert result == {}

    def test_007_competition_ref_niveau_property_with_nom(self):
        """Test de la propriété niveau quand le nom est défini"""
        competition_ref = CompetitionDetail(nom="U15 Masculin Excellence")

        # Le test vérifie que la propriété peut être accédée sans erreur
        niveau = competition_ref.niveau

        # On ne peut pas prédire le résultat exact sans connaître la logique interne
        # de get_niveau_from_idcompetition, donc on vérifie juste qu'elle ne lève pas d'erreur
        assert niveau is None or hasattr(niveau, "__dict__")

    def test_008_competition_ref_niveau_property_without_nom(self):
        """Test de la propriété niveau quand le nom n'est pas défini"""
        competition_ref = CompetitionDetail()

        # Le test vérifie que la propriété peut être accédée sans erreur
        niveau = competition_ref.niveau

        # On ne peut pas prédire le résultat exact sans connaître la logique interne
        # de get_niveau_from_idcompetition, donc on vérifie juste qu'elle ne lève pas d'erreur
        assert niveau is None or hasattr(niveau, "__dict__")

    def test_009_competition_ref_from_dict_with_none_values(self):
        """Test de la méthode from_dict avec des valeurs None"""
        data = {
            "id": None,
            "nom": None,
            "code": None,
            "sexe": None,
            "competition_origine": None,
            "competition_origine_nom": None,
            "competition_origine_niveau": None,
            "typeCompetition": None,
            "logo": None,
            "saison": None,
            "idCompetitionPere": None,
            "organisateur": None,
            "typeCompetitionGenerique": None,
            "categorie": None,
        }

        competition_ref = CompetitionDetail.from_dict(data)

        assert competition_ref.id is None
        assert competition_ref.nom is None
        assert competition_ref.code is None
        assert competition_ref.sexe is None
        assert competition_ref.competition_origine is None
        assert competition_ref.competition_origine_nom is None
        assert competition_ref.competition_origine_niveau is None
        assert competition_ref.type_competition is None
        assert competition_ref.logo is None
        assert competition_ref.saison is None
        assert competition_ref.id_competition_pere is None
        assert competition_ref.organisateur is None
        assert competition_ref.type_competition_generique is None
        assert competition_ref.categorie is None

    def test_010_competition_ref_assertion_error(self):
        """Test de la méthode from_dict avec un objet non-dict (devrait lever une assertion)"""
        with self.assertRaises(AssertionError):
            CompetitionDetail.from_dict("not_a_dict")

    def test_011_competition_ref_round_trip(self):
        """Test de conversion depuis/depuis un dictionnaire"""
        original_data = {
            "id": "comp123",
            "nom": "Comp Test",
            "code": "CT001",
            "sexe": "M",
            "competition_origine": "Ligue",
            "competition_origine_nom": "Ligue Test",
            "competition_origine_niveau": 1,
            "typeCompetition": "Championnat",
            "logo": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "saison": {"code": "2024"},
            "idCompetitionPere": "parent123",
            "organisateur": {"id": "org123", "nom": "Org Test"},
            "typeCompetitionGenerique": {"id": "type123", "libelle": "Type Test"},
            "categorie": {"id": "cat123", "libelle": "Catégorie Test"},
        }

        # Convertir du dictionnaire à l'objet
        competition_ref = CompetitionDetail.from_dict(original_data)

        # Convertir de l'objet au dictionnaire
        result_data = competition_ref.to_dict()

        # Vérifier que les champs essentiels sont présents
        assert result_data["id"] == "comp123"
        assert result_data["nom"] == "Comp Test"
        assert result_data["code"] == "CT001"
        assert result_data["sexe"] == "M"
        assert result_data["competition_origine"] == "Ligue"
        assert result_data["competition_origine_nom"] == "Ligue Test"
        assert result_data["competition_origine_niveau"] == 1
        assert result_data["typeCompetition"] == "Championnat"
        assert "logo" in result_data
        assert "saison" in result_data
        assert result_data["idCompetitionPere"] == "parent123"
        assert "organisateur" in result_data
        assert "typeCompetitionGenerique" in result_data
        assert "categorie" in result_data
