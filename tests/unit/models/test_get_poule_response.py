"""
Unit tests for get_poule_response.py
"""

import unittest
from datetime import datetime
from unittest.mock import patch

from ffbb_api_client_v2.models.get_poule_response import GetPouleResponse


class TestGetPouleResponse(unittest.TestCase):
    """Tests pour la classe GetPouleResponse"""

    def test_001_from_dict_none(self):
        """Test from_dict avec None"""
        result = GetPouleResponse.from_dict(None)  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_002_from_dict_empty_dict(self):
        """Test from_dict avec dict vide"""
        result = GetPouleResponse.from_dict({})
        self.assertIsNone(result)

    def test_003_from_dict_not_dict(self):
        """Test from_dict avec entrée non-dict"""
        result = GetPouleResponse.from_dict("not a dict")  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_004_from_dict_with_errors(self):
        """Test from_dict avec dict contenant 'errors'"""
        data = {"errors": ["some error"]}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNone(result)

    def test_005_from_dict_minimal(self):
        """Test from_dict avec données minimales"""
        data = {"id": "poule-001"}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "poule-001")
        self.assertEqual(result.rencontres, [])
        self.assertIsNone(result.classements)
        self.assertIsNone(result.nom)
        self.assertIsNone(result.engagements)
        self.assertIsNone(result.id_competition)
        self.assertIsNone(result.date_created)
        self.assertIsNone(result.date_updated)

    def test_006_from_dict_with_nom(self):
        """Test from_dict avec nom"""
        data = {"id": "poule-002", "nom": "Poule A"}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.nom, "Poule A")

    def test_007_from_dict_with_empty_nom(self):
        """Test from_dict avec nom vide"""
        data = {"id": "poule-003", "nom": ""}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertIsNone(result.nom)

    def test_008_from_dict_with_id_competition(self):
        """Test from_dict avec id_competition"""
        data = {"id": "poule-004", "id_competition": "comp-123"}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id_competition, "comp-123")

    def test_009_from_dict_with_empty_id_competition(self):
        """Test from_dict avec id_competition vide"""
        data = {"id": "poule-005", "id_competition": ""}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertIsNone(result.id_competition)

    def test_010_from_dict_with_date_created(self):
        """Test from_dict avec date_created"""
        data = {"id": "poule-006", "date_created": "2023-01-01"}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.date_created, "2023-01-01")

    def test_011_from_dict_with_empty_date_created(self):
        """Test from_dict avec date_created vide"""
        data = {"id": "poule-007", "date_created": ""}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertIsNone(result.date_created)

    def test_012_from_dict_with_date_updated(self):
        """Test from_dict avec date_updated"""
        data = {"id": "poule-008", "date_updated": "2023-01-02"}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.date_updated, "2023-01-02")

    def test_013_from_dict_with_engagements(self):
        """Test from_dict avec engagements"""
        engagements = [{"id": "eng-1"}, {"id": "eng-2"}]
        data = {"id": "poule-009", "engagements": engagements}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.engagements, engagements)

    def test_014_from_dict_with_empty_engagements(self):
        """Test from_dict avec engagements vide"""
        data = {"id": "poule-010", "engagements": []}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertIsNone(result.engagements)

    def test_015_from_dict_with_rencontres_empty(self):
        """Test from_dict avec rencontres vide"""
        data = {"id": "poule-011", "rencontres": []}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.rencontres, [])

    def test_016_from_dict_with_rencontre_minimal(self):
        """Test from_dict avec une rencontre minimale"""
        data = {
            "id": "poule-012",
            "rencontres": [
                {
                    "id": "ren-001",
                    "numero": "1",
                    "numeroJournee": "1",
                    "idPoule": "poule-012",
                    "competitionId": "comp-123",
                    "resultatEquipe1": "0",
                    "resultatEquipe2": "0",
                    "joue": False,
                    "nomEquipe1": "Team A",
                    "nomEquipe2": "Team B",
                    "date_rencontre": "2023-01-01T10:00:00",
                }
            ],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.rencontres), 1)
        rencontre = result.rencontres[0]
        self.assertEqual(rencontre.id, "ren-001")
        self.assertEqual(rencontre.numero, "1")
        self.assertEqual(rencontre.numeroJournee, "1")
        self.assertEqual(rencontre.idPoule, "poule-012")
        self.assertEqual(rencontre.competitionId, "comp-123")
        self.assertEqual(rencontre.resultatEquipe1, "0")
        self.assertEqual(rencontre.resultatEquipe2, "0")
        self.assertFalse(rencontre.joue)
        self.assertEqual(rencontre.nomEquipe1, "Team A")
        self.assertEqual(rencontre.nomEquipe2, "Team B")
        self.assertEqual(rencontre.date_rencontre, datetime(2023, 1, 1, 10, 0, 0))

    def test_017_from_dict_with_rencontre_missing_fields(self):
        """Test from_dict avec rencontre ayant des champs manquants"""
        data = {
            "id": "poule-013",
            "rencontres": [
                {
                    "id": "ren-002",
                    # numero, numeroJournee, etc. manquants
                }
            ],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.rencontres), 1)
        rencontre = result.rencontres[0]
        self.assertEqual(rencontre.id, "ren-002")
        self.assertEqual(rencontre.numero, "")
        self.assertEqual(rencontre.numeroJournee, "")
        self.assertEqual(rencontre.idPoule, "")
        self.assertEqual(rencontre.competitionId, "")
        self.assertEqual(rencontre.resultatEquipe1, "")
        self.assertEqual(rencontre.resultatEquipe2, "")
        self.assertFalse(rencontre.joue)
        self.assertEqual(rencontre.nomEquipe1, "")
        self.assertEqual(rencontre.nomEquipe2, "")
        self.assertEqual(rencontre.date_rencontre, datetime(1970, 1, 1))

    def test_018_from_dict_with_rencontre_invalid_date(self):
        """Test from_dict avec rencontre ayant une date invalide"""
        data = {
            "id": "poule-014",
            "rencontres": [
                {
                    "id": "ren-003",
                    "numero": "1",
                    "numeroJournee": "1",
                    "idPoule": "poule-014",
                    "competitionId": "comp-123",
                    "resultatEquipe1": "0",
                    "resultatEquipe2": "0",
                    "joue": False,
                    "nomEquipe1": "Team A",
                    "nomEquipe2": "Team B",
                    "date_rencontre": "invalid-date",
                }
            ],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.rencontres), 1)
        rencontre = result.rencontres[0]
        self.assertEqual(rencontre.date_rencontre, datetime(1970, 1, 1))

    def test_019_from_dict_with_multiple_rencontres(self):
        """Test from_dict avec plusieurs rencontres"""
        data = {
            "id": "poule-015",
            "rencontres": [
                {
                    "id": "ren-004",
                    "numero": "1",
                    "numeroJournee": "1",
                    "idPoule": "poule-015",
                    "competitionId": "comp-123",
                    "resultatEquipe1": "10",
                    "resultatEquipe2": "8",
                    "joue": True,
                    "nomEquipe1": "Team A",
                    "nomEquipe2": "Team B",
                    "date_rencontre": "2023-01-01T10:00:00",
                },
                {
                    "id": "ren-005",
                    "numero": "2",
                    "numeroJournee": "2",
                    "idPoule": "poule-015",
                    "competitionId": "comp-123",
                    "resultatEquipe1": "0",
                    "resultatEquipe2": "0",
                    "joue": False,
                    "nomEquipe1": "Team C",
                    "nomEquipe2": "Team D",
                    "date_rencontre": "2023-01-08T10:00:00",
                },
            ],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.rencontres), 2)

    def test_020_from_dict_with_empty_rencontre(self):
        """Test from_dict avec rencontre vide (None ou {})"""
        data = {
            "id": "poule-016",
            "rencontres": [None, {}],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        # Empty rencontre dicts are filtered out
        self.assertEqual(len(result.rencontres), 0)

    @patch("ffbb_api_client_v2.models.team_ranking.TeamRanking.from_dict")
    def test_021_from_dict_with_classements(self, mock_team_ranking_from_dict):
        """Test from_dict avec classements"""
        # Mock TeamRanking.from_dict to return a mock object
        mock_ranking = unittest.mock.MagicMock()
        mock_team_ranking_from_dict.return_value = mock_ranking

        data = {
            "id": "poule-017",
            "classements": [
                {"id": "rank-1", "position": 1},
                {"id": "rank-2", "position": 2},
            ],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.classements), 2)
        self.assertEqual(result.classements, [mock_ranking, mock_ranking])
        # Verify TeamRanking.from_dict was called for each classement
        self.assertEqual(mock_team_ranking_from_dict.call_count, 2)

    @patch("ffbb_api_client_v2.models.team_ranking.TeamRanking.from_dict")
    def test_022_from_dict_with_classements_none_returned(
        self, mock_team_ranking_from_dict
    ):
        """Test from_dict avec classements où from_dict retourne None"""
        mock_team_ranking_from_dict.return_value = None

        data = {
            "id": "poule-018",
            "classements": [
                {"id": "rank-1"},
                {"id": "rank-2"},
            ],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertIsNone(
            result.classements
        )  # Should be None when no valid classements

    def test_023_from_dict_with_empty_classements(self):
        """Test from_dict avec classements vide"""
        data = {"id": "poule-019", "classements": []}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertIsNone(result.classements)

    def test_025_from_dict_with_classements_empty_dict(self):
        """Test from_dict avec classements contenant un dict vide"""
        data = {
            "id": "poule-025",
            "classements": [{}],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertIsNone(result.classements)  # Empty dict should be filtered out

    @patch("ffbb_api_client_v2.models.team_ranking.TeamRanking.from_dict")
    def test_026_from_dict_with_classements_mixed(self, mock_team_ranking_from_dict):
        """Test from_dict avec classements mixtes (valid et invalid)"""
        mock_ranking = unittest.mock.MagicMock()
        mock_team_ranking_from_dict.side_effect = [mock_ranking, None, mock_ranking]

        data = {
            "id": "poule-026",
            "classements": [{"id": "rank-1"}, {"id": "rank-2"}, {"id": "rank-3"}],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.classements), 2)  # Only valid ones
        self.assertEqual(mock_team_ranking_from_dict.call_count, 3)

    def test_027_from_dict_with_rencontre_partial_data(self):
        """Test from_dict avec rencontre ayant des données partielles"""
        data = {
            "id": "poule-027",
            "rencontres": [
                {
                    "id": "ren-007",
                    "joue": True,
                    "nomEquipe1": "Team A",
                    # Missing other fields
                }
            ],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.rencontres), 1)
        rencontre = result.rencontres[0]
        self.assertEqual(rencontre.id, "ren-007")
        self.assertEqual(rencontre.numero, "")
        self.assertTrue(rencontre.joue)
        self.assertEqual(rencontre.nomEquipe1, "Team A")
        self.assertEqual(rencontre.nomEquipe2, "")

    def test_028_from_dict_with_rencontre_bool_conversion(self):
        """Test conversion des booléens dans rencontre"""
        data = {
            "id": "poule-028",
            "rencontres": [
                {
                    "id": "ren-008",
                    "numero": "1",
                    "numeroJournee": "1",
                    "idPoule": "poule-028",
                    "competitionId": "comp-123",
                    "resultatEquipe1": "10",
                    "resultatEquipe2": "8",
                    "joue": "true",  # String instead of bool
                    "nomEquipe1": "Team A",
                    "nomEquipe2": "Team B",
                    "date_rencontre": "2023-01-01T10:00:00",
                }
            ],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        rencontre = result.rencontres[0]
        self.assertTrue(rencontre.joue)  # Should be converted to bool

    def test_029_from_dict_minimal_with_all_optional_fields_none(self):
        """Test from_dict avec tous les champs optionnels à None/vide"""
        data = {
            "id": "poule-029",
            "nom": "",
            "id_competition": "",
            "date_created": "",
            "date_updated": "",
            "engagements": [],
            "rencontres": [],
            "classements": [],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "poule-029")
        self.assertIsNone(result.nom)
        self.assertIsNone(result.id_competition)
        self.assertIsNone(result.date_created)
        self.assertIsNone(result.date_updated)
        self.assertIsNone(result.engagements)
        self.assertEqual(result.rencontres, [])
        self.assertIsNone(result.classements)


if __name__ == "__main__":
    unittest.main()
