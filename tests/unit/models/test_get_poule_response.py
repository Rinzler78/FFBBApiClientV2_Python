"""
Unit tests for get_poule_response.py
"""

import unittest
from datetime import datetime
from unittest.mock import patch

from ffbb_api_client_v2.directus_ffbb.models.get_poule_response import GetPouleResponse


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
        self.assertEqual(result.engagements, [])
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
        """Test from_dict avec nom vide — from_str preserves empty string"""
        data = {"id": "poule-003", "nom": ""}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.nom, "")

    def test_008_from_dict_with_id_competition(self):
        """Test from_dict avec id_competition (FK int)"""
        data = {"id": "poule-004", "id_competition": 2800001}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id_competition, 2800001)

    def test_009_from_dict_with_none_id_competition(self):
        """Test from_dict avec id_competition None"""
        data = {"id": "poule-005", "id_competition": None}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertIsNone(result.id_competition)

    def test_010_from_dict_with_date_created(self):
        """Test from_dict avec date_created"""
        data = {"id": "poule-006", "date_created": "2023-01-01"}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result.date_created, datetime)

    def test_011_from_dict_with_empty_date_created(self):
        """Test from_dict avec date_created vide — from_datetime returns None for empty string"""
        data = {"id": "poule-007", "date_created": ""}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertIsNone(result.date_created)

    def test_012_from_dict_with_date_updated(self):
        """Test from_dict avec date_updated"""
        data = {"id": "poule-008", "date_updated": "2023-01-02"}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result.date_updated, datetime)

    def test_013_from_dict_with_engagements(self):
        """Test from_dict avec engagements (FK-only ints)"""
        engagements = [5001, 5002, 5003]
        data = {"id": "poule-009", "engagements": engagements}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.engagements, engagements)

    def test_014_from_dict_with_empty_engagements(self):
        """Test from_dict avec engagements vide"""
        data = {"id": "poule-010", "engagements": []}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.engagements, [])

    def test_015_from_dict_with_rencontres_empty(self):
        """Test from_dict avec rencontres vide"""
        data = {"id": "poule-011", "rencontres": []}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.rencontres, [])

    def test_016_from_dict_with_rencontres_fk_ints(self):
        """Test from_dict avec rencontres FK-only (list of ints)"""
        data = {
            "id": "poule-012",
            "rencontres": [200000012345678, 200000012345679],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.rencontres), 2)
        self.assertEqual(result.rencontres[0], 200000012345678)
        self.assertEqual(result.rencontres[1], 200000012345679)

    def test_017_from_dict_with_rencontres_raw_dicts(self):
        """Test from_dict avec rencontres as raw dicts (not parsed into models)"""
        data = {
            "id": "poule-013",
            "rencontres": [
                {"id": "ren-002", "joue": True},
            ],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.rencontres), 1)
        self.assertIsInstance(result.rencontres[0], dict)
        self.assertEqual(result.rencontres[0]["id"], "ren-002")

    def test_018_from_dict_with_rencontres_none_defaults_empty(self):
        """Test from_dict avec rencontres None defaults to []"""
        data = {"id": "poule-014", "rencontres": None}
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.rencontres, [])

    def test_019_from_dict_with_multiple_rencontres(self):
        """Test from_dict avec plusieurs rencontres FK ints"""
        data = {
            "id": "poule-015",
            "rencontres": [100001, 100002, 100003],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.rencontres), 3)

    def test_020_from_dict_with_rencontres_containing_none(self):
        """Test from_dict avec rencontre None dans la liste — kept as-is"""
        data = {
            "id": "poule-016",
            "rencontres": [None],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.rencontres, [None])

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
        self.assertEqual(
            result.classements, []
        )  # All from_dict returned None, filtered to empty list

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
        self.assertEqual(
            result.classements, []
        )  # Empty dict → from_dict returns None → filtered out

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

    def test_027_from_dict_minimal_with_all_optional_fields_none(self):
        """Test from_dict avec tous les champs optionnels à None/vide"""
        data = {
            "id": "poule-029",
            "nom": "",
            "id_competition": None,
            "date_created": "",
            "date_updated": "",
            "engagements": [],
            "rencontres": [],
            "classements": [],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "poule-029")
        self.assertEqual(result.nom, "")
        self.assertIsNone(result.id_competition)
        self.assertIsNone(result.date_created)
        self.assertIsNone(result.date_updated)
        self.assertEqual(result.engagements, [])
        self.assertEqual(result.rencontres, [])
        self.assertIsNone(result.classements)


if __name__ == "__main__":
    unittest.main()
