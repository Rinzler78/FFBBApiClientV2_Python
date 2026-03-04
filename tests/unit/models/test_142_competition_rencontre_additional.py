"""
Tests additionnels pour le module CompetitionRencontre pour atteindre 90% de couverture
"""

import unittest
from datetime import datetime

from ffbb_api_client_v2.models.competition_rencontre import CompetitionRencontre
from ffbb_api_client_v2.models.engagement_equipe import EngagementEquipe
from ffbb_api_client_v2.models.fonction import Fonction
from ffbb_api_client_v2.models.game_stats_model import GameStatsModel
from ffbb_api_client_v2.models.id_organisme_equipe import IDOrganismeEquipe
from ffbb_api_client_v2.models.logo import Logo
from ffbb_api_client_v2.models.officiel import Officiel
from ffbb_api_client_v2.models.officiel_personne import OfficielPersonne
from ffbb_api_client_v2.models.salle import Salle


class Test142CompetitionRencontreAdditional(unittest.TestCase):
    """Tests additionnels pour le modèle CompetitionRencontre"""

    def test_001_competition_rencontre_full_initialization(self):
        """Test d'initialisation complète de CompetitionRencontre avec toutes les propriétés"""
        organisme_equipe1 = IDOrganismeEquipe(logo=Logo())
        organisme_equipe2 = IDOrganismeEquipe(logo=Logo())
        gs_id = GameStatsModel(match_id="gs123")
        engagement_equipe1 = EngagementEquipe(id="eng123", nom="Engagement 1")
        engagement_equipe2 = EngagementEquipe(id="eng456", nom="Engagement 2")
        salle = Salle(id="salle123", libelle="Salle Test")
        officiel = Officiel(
            ordre=1,
            fonction=Fonction(libelle="Arbitre"),
            officiel=OfficielPersonne(nom="Test"),
        )

        date_rencontre = datetime.now()

        rencontre = CompetitionRencontre(
            id="renc123",
            numero="1",
            numero_journee="J1",
            id_poule="poule123",
            competition_id="comp123",
            resultat_equipe1=85,
            resultat_equipe2=78,
            joue=True,
            nom_equipe1="Équipe A",
            nom_equipe2="Équipe B",
            date_rencontre=date_rencontre,
            id_organisme_equipe1=organisme_equipe1,
            id_organisme_equipe2=organisme_equipe2,
            gs_id=gs_id,
            id_engagement_equipe1=engagement_equipe1,
            id_engagement_equipe2=engagement_equipe2,
            salle=salle,
            officiels=[officiel],
        )

        assert rencontre.id == "renc123"
        assert rencontre.numero == "1"
        assert rencontre.numero_journee == "J1"
        assert rencontre.id_poule == "poule123"
        assert rencontre.competition_id == "comp123"
        assert rencontre.resultat_equipe1 == 85
        assert rencontre.resultat_equipe2 == 78
        assert rencontre.joue is True
        assert rencontre.nom_equipe1 == "Équipe A"
        assert rencontre.nom_equipe2 == "Équipe B"
        assert rencontre.date_rencontre == date_rencontre
        assert rencontre.id_organisme_equipe1 == organisme_equipe1
        assert rencontre.id_organisme_equipe2 == organisme_equipe2
        assert rencontre.gs_id == gs_id
        assert rencontre.id_engagement_equipe1 == engagement_equipe1
        assert rencontre.id_engagement_equipe2 == engagement_equipe2
        assert rencontre.salle == salle
        assert len(rencontre.officiels) == 1
        assert rencontre.officiels[0] == officiel

    def test_002_competition_rencontre_minimal_initialization(self):
        """Test d'initialisation minimale de CompetitionRencontre"""
        rencontre = CompetitionRencontre()

        assert rencontre.id is None
        assert rencontre.numero is None
        assert rencontre.numero_journee is None
        assert rencontre.id_poule is None
        assert rencontre.competition_id is None
        assert rencontre.resultat_equipe1 is None
        assert rencontre.resultat_equipe2 is None
        assert rencontre.joue is None
        assert rencontre.nom_equipe1 is None
        assert rencontre.nom_equipe2 is None
        assert rencontre.date_rencontre is None
        assert rencontre.id_organisme_equipe1 is None
        assert rencontre.id_organisme_equipe2 is None
        assert rencontre.gs_id is None
        assert rencontre.id_engagement_equipe1 is None
        assert rencontre.id_engagement_equipe2 is None
        assert rencontre.salle is None
        assert len(rencontre.officiels) == 0

    def test_003_competition_rencontre_from_dict_full(self):
        """Test de la méthode from_dict avec un dictionnaire complet"""
        data = {
            "id": "renc123",
            "numero": "1",
            "numeroJournee": "J1",
            "idPoule": "poule123",
            "competitionId": "comp123",
            "resultatEquipe1": "85",
            "resultatEquipe2": "78",
            "joue": True,
            "nomEquipe1": "Équipe A",
            "nomEquipe2": "Équipe B",
            "date_rencontre": "2023-04-15T14:30:00",
            "idOrganismeEquipe1": {"id": "org123", "nom": "Équipe 1"},
            "idOrganismeEquipe2": {"id": "org456", "nom": "Équipe 2"},
            "gsId": {"id": "gs123"},
            "idEngagementEquipe1": {"id": "eng123", "nom": "Engagement 1"},
            "idEngagementEquipe2": {"id": "eng456", "nom": "Engagement 2"},
            "salle": {"id": "salle123", "nom": "Salle Test"},
            "officiels": [{"id": "off123", "nom": "Officiel Test"}],
        }

        rencontre = CompetitionRencontre.from_dict(data)

        assert rencontre.id == "renc123"
        assert rencontre.numero == "1"
        assert rencontre.numero_journee == "J1"
        assert rencontre.id_poule == "poule123"
        assert rencontre.competition_id == "comp123"
        assert rencontre.resultat_equipe1 == 85
        assert rencontre.resultat_equipe2 == 78
        assert rencontre.joue is True
        assert rencontre.nom_equipe1 == "Équipe A"
        assert rencontre.nom_equipe2 == "Équipe B"
        assert rencontre.date_rencontre is not None
        assert rencontre.id_organisme_equipe1 is not None
        assert rencontre.id_organisme_equipe2 is not None
        assert rencontre.gs_id is not None
        assert rencontre.id_engagement_equipe1 is not None
        assert rencontre.id_engagement_equipe2 is not None
        assert rencontre.salle is not None
        assert len(rencontre.officiels) == 1

    def test_004_competition_rencontre_from_dict_minimal(self):
        """Test de la méthode from_dict avec un dictionnaire minimal"""
        data = {}

        rencontre = CompetitionRencontre.from_dict(data)

        assert rencontre.id is None
        assert rencontre.numero is None
        assert rencontre.numero_journee is None
        assert rencontre.id_poule is None
        assert rencontre.competition_id is None
        assert rencontre.resultat_equipe1 is None
        assert rencontre.resultat_equipe2 is None
        assert rencontre.joue is None
        assert rencontre.nom_equipe1 is None
        assert rencontre.nom_equipe2 is None
        assert rencontre.date_rencontre is None
        assert rencontre.id_organisme_equipe1 is None
        assert rencontre.id_organisme_equipe2 is None
        assert rencontre.gs_id is None
        assert rencontre.id_engagement_equipe1 is None
        assert rencontre.id_engagement_equipe2 is None
        assert rencontre.salle is None
        assert len(rencontre.officiels) == 0

    def test_005_competition_rencontre_to_dict_full(self):
        """Test de la méthode to_dict avec toutes les propriétés définies"""
        organisme_equipe1 = IDOrganismeEquipe(logo=Logo())
        organisme_equipe2 = IDOrganismeEquipe(logo=Logo())
        gs_id = GameStatsModel(match_id="gs123")
        engagement_equipe1 = EngagementEquipe(id="eng123", nom="Engagement 1")
        engagement_equipe2 = EngagementEquipe(id="eng456", nom="Engagement 2")
        salle = Salle(id="salle123", libelle="Salle Test")
        officiel = Officiel(
            ordre=1,
            fonction=Fonction(libelle="Arbitre"),
            officiel=OfficielPersonne(nom="Test"),
        )

        date_rencontre = datetime(2023, 4, 15, 14, 30, 0)

        rencontre = CompetitionRencontre(
            id="renc123",
            numero="1",
            numero_journee="J1",
            id_poule="poule123",
            competition_id="comp123",
            resultat_equipe1=85,
            resultat_equipe2=78,
            joue=True,
            nom_equipe1="Équipe A",
            nom_equipe2="Équipe B",
            date_rencontre=date_rencontre,
            id_organisme_equipe1=organisme_equipe1,
            id_organisme_equipe2=organisme_equipe2,
            gs_id=gs_id,
            id_engagement_equipe1=engagement_equipe1,
            id_engagement_equipe2=engagement_equipe2,
            salle=salle,
            officiels=[officiel],
        )

        result = rencontre.to_dict()

        assert result["id"] == "renc123"
        assert result["numero"] == "1"
        assert result["numeroJournee"] == "J1"
        assert result["idPoule"] == "poule123"
        assert result["competitionId"] == "comp123"
        assert result["resultatEquipe1"] == 85
        assert result["resultatEquipe2"] == 78
        assert result["joue"] is True
        assert result["nomEquipe1"] == "Équipe A"
        assert result["nomEquipe2"] == "Équipe B"
        assert result["date_rencontre"] == "2023-04-15T14:30:00"
        assert "idOrganismeEquipe1" in result
        assert "idOrganismeEquipe2" in result
        assert "gsId" in result
        assert "idEngagementEquipe1" in result
        assert "idEngagementEquipe2" in result
        assert "salle" in result
        assert "officiels" in result
        assert len(result["officiels"]) == 1

    def test_006_competition_rencontre_to_dict_minimal(self):
        """Test de la méthode to_dict avec un objet minimal"""
        rencontre = CompetitionRencontre()

        result = rencontre.to_dict()

        # Vérifie que le dictionnaire n'a que les champs non nuls
        assert result == {}

    def test_007_competition_rencontre_from_dict_with_none_values(self):
        """Test de la méthode from_dict avec des valeurs None"""
        data = {
            "id": None,
            "numero": None,
            "numeroJournee": None,
            "idPoule": None,
            "competitionId": None,
            "resultatEquipe1": None,
            "resultatEquipe2": None,
            "joue": None,
            "nomEquipe1": None,
            "nomEquipe2": None,
            "date_rencontre": None,
            "idOrganismeEquipe1": None,
            "idOrganismeEquipe2": None,
            "gsId": None,
            "idEngagementEquipe1": None,
            "idEngagementEquipe2": None,
            "salle": None,
            "officiels": None,
        }

        rencontre = CompetitionRencontre.from_dict(data)

        assert rencontre.id is None
        assert rencontre.numero is None
        assert rencontre.numero_journee is None
        assert rencontre.id_poule is None
        assert rencontre.competition_id is None
        assert rencontre.resultat_equipe1 is None
        assert rencontre.resultat_equipe2 is None
        assert rencontre.joue is None
        assert rencontre.nom_equipe1 is None
        assert rencontre.nom_equipe2 is None
        assert rencontre.date_rencontre is None
        assert rencontre.id_organisme_equipe1 is None
        assert rencontre.id_organisme_equipe2 is None
        assert rencontre.gs_id is None
        assert rencontre.id_engagement_equipe1 is None
        assert rencontre.id_engagement_equipe2 is None
        assert rencontre.salle is None
        assert len(rencontre.officiels) == 0  # La liste par défaut est vide

    def test_008_competition_rencontre_assertion_error(self):
        """Test de la méthode from_dict avec un objet non-dict (devrait lever une assertion)"""
        with self.assertRaises(AssertionError):
            CompetitionRencontre.from_dict("not_a_dict")

    def test_009_competition_rencontre_round_trip(self):
        """Test de conversion depuis/depuis un dictionnaire"""
        original_data = {
            "id": "renc123",
            "numero": "1",
            "numeroJournee": "J1",
            "idPoule": "poule123",
            "competitionId": "comp123",
            "resultatEquipe1": "85",
            "resultatEquipe2": "78",
            "joue": True,
            "nomEquipe1": "Équipe A",
            "nomEquipe2": "Équipe B",
            "date_rencontre": "2023-04-15T14:30:00",
            "idOrganismeEquipe1": {"id": "org123", "nom": "Équipe 1"},
            "idOrganismeEquipe2": {"id": "org456", "nom": "Équipe 2"},
            "gsId": {"id": "gs123"},
            "idEngagementEquipe1": {"id": "eng123", "nom": "Engagement 1"},
            "idEngagementEquipe2": {"id": "eng456", "nom": "Engagement 2"},
            "salle": {"id": "salle123", "nom": "Salle Test"},
            "officiels": [{"id": "off123", "nom": "Officiel Test"}],
        }

        # Convertir du dictionnaire à l'objet
        rencontre = CompetitionRencontre.from_dict(original_data)

        # Convertir de l'objet au dictionnaire
        result_data = rencontre.to_dict()

        # Vérifier que les champs essentiels sont présents
        assert result_data["id"] == "renc123"
        assert result_data["numero"] == "1"
        assert result_data["numeroJournee"] == "J1"
        assert result_data["idPoule"] == "poule123"
        assert result_data["competitionId"] == "comp123"
        assert result_data["resultatEquipe1"] == 85
        assert result_data["resultatEquipe2"] == 78
        assert result_data["joue"] is True
        assert result_data["nomEquipe1"] == "Équipe A"
        assert result_data["nomEquipe2"] == "Équipe B"
        assert "idOrganismeEquipe1" in result_data
        assert "idOrganismeEquipe2" in result_data
        assert "gsId" in result_data
        assert "idEngagementEquipe1" in result_data
        assert "idEngagementEquipe2" in result_data
        assert "salle" in result_data
        assert "officiels" in result_data
        assert len(result_data["officiels"]) == 1

    def test_010_competition_rencontre_officiels_empty_list(self):
        """Test de la gestion d'une liste vide d'officiels"""
        data = {"id": "renc123", "officiels": []}

        rencontre = CompetitionRencontre.from_dict(data)

        assert rencontre.id == "renc123"
        assert len(rencontre.officiels) == 0

    def test_011_competition_rencontre_date_rencontre_formats(self):
        """Test de la gestion de différentes formats de dates"""
        # Test avec une date ISO
        data = {"id": "renc123", "date_rencontre": "2023-04-15T14:30:00"}

        rencontre = CompetitionRencontre.from_dict(data)

        assert rencontre.id == "renc123"
        assert rencontre.date_rencontre is not None
