"""
Unit tests for niveau_extractor.py
"""

import unittest
from unittest.mock import Mock

from ffbb_api_client_v2.models.categorie_type import CategorieType
from ffbb_api_client_v2.models.niveau_extractor import (
    NiveauExtractor,
    get_niveau_from_idcompetition,
)
from ffbb_api_client_v2.models.niveau_type import NiveauType


class TestNiveauExtractor(unittest.TestCase):
    """Tests pour la classe NiveauExtractor"""

    def test_001_extract_niveau_none(self):
        """Test extract_niveau avec None"""
        result = NiveauExtractor.extract_niveau(None)  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_002_extract_niveau_empty_string(self):
        """Test extract_niveau avec chaîne vide"""
        result = NiveauExtractor.extract_niveau("")
        self.assertIsNone(result)

    def test_003_extract_niveau_whitespace_only(self):
        """Test extract_niveau avec espaces seulement"""
        result = NiveauExtractor.extract_niveau("   ")
        self.assertIsNone(result)

    def test_004_extract_niveau_elite_basic(self):
        """Test extraction niveau ELITE basique"""
        result = NiveauExtractor.extract_niveau("Championnat ELITE Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.ELITE)
        self.assertEqual(result.raw_text, "ELITE")
        self.assertEqual(result.zone_geographique, "regional")
        self.assertIsNone(result.division)
        self.assertEqual(result.categorie, CategorieType.SENIOR)

    def test_005_extract_niveau_elite_accented(self):
        """Test extraction niveau ÉLITE avec accent"""
        result = NiveauExtractor.extract_niveau("Championnat ÉLITE Féminin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.ELITE)

    def test_006_extract_niveau_national_basic(self):
        """Test extraction niveau NATIONAL basique"""
        result = NiveauExtractor.extract_niveau("Championnat NATIONAL Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.NATIONAL)
        self.assertEqual(result.raw_text, "NATIONAL")

    def test_007_extract_niveau_national_accented(self):
        """Test extraction niveau NATIONALE avec accent"""
        result = NiveauExtractor.extract_niveau("Championnat NATIONALE Féminin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.NATIONAL)

    def test_008_extract_niveau_national_division(self):
        """Test extraction niveau NATIONAL avec division"""
        result = NiveauExtractor.extract_niveau("Championnat N1 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.NATIONAL)
        self.assertEqual(result.division, 1)

    def test_009_extract_niveau_regional_basic(self):
        """Test extraction niveau REGIONAL basique"""
        result = NiveauExtractor.extract_niveau("Championnat REGIONAL Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.REGIONAL)
        self.assertEqual(result.raw_text, "REGIONAL")

    def test_010_extract_niveau_regional_accented(self):
        """Test extraction niveau RÉGIONAL avec accent"""
        result = NiveauExtractor.extract_niveau("Championnat RÉGIONAL Féminin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.REGIONAL)

    def test_011_extract_niveau_regional_division_r(self):
        """Test extraction niveau REGIONAL avec division R1"""
        result = NiveauExtractor.extract_niveau("Championnat R1 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.REGIONAL)
        self.assertEqual(result.division, 1)

    def test_012_extract_niveau_regional_division_regional_space(self):
        """Test extraction niveau REGIONAL avec 'REGIONAL 2'"""
        result = NiveauExtractor.extract_niveau("Championnat REGIONAL 2 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.REGIONAL)
        self.assertEqual(result.division, 2)

    def test_013_extract_niveau_departemental_basic(self):
        """Test extraction niveau DEPARTEMENTAL basique"""
        result = NiveauExtractor.extract_niveau("Championnat DEPARTEMENTAL Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.DEPARTEMENTAL)
        self.assertEqual(result.raw_text, "DEPARTEMENTAL")

    def test_014_extract_niveau_departemental_accented(self):
        """Test extraction niveau DÉPARTEMENTAL avec accent"""
        result = NiveauExtractor.extract_niveau("Championnat DÉPARTEMENTAL Féminin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.DEPARTEMENTAL)

    def test_015_extract_niveau_departemental_division_d(self):
        """Test extraction niveau DEPARTEMENTAL avec division D1"""
        result = NiveauExtractor.extract_niveau("Championnat D1 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.DEPARTEMENTAL)
        self.assertEqual(result.division, 1)

    def test_016_extract_niveau_departemental_division_departemental_space(self):
        """Test extraction niveau DEPARTEMENTAL avec 'DEPARTEMENTAL 3'"""
        result = NiveauExtractor.extract_niveau("Championnat DEPARTEMENTAL 3 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.DEPARTEMENTAL)
        self.assertEqual(result.division, 3)

    def test_017_extract_niveau_departemental_division_dash(self):
        """Test extraction niveau avec '- Division 2'"""
        result = NiveauExtractor.extract_niveau(
            "Championnat Départemental Masculin - Division 2"
        )
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.DEPARTEMENTAL)
        self.assertEqual(result.division, 2)

    def test_018_extract_niveau_regionale_simple(self):
        """Test extraction niveau RÉGIONALE simple"""
        result = NiveauExtractor.extract_niveau("RÉGIONALE masculine seniors")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.REGIONAL)

    def test_019_extract_niveau_departementale_simple(self):
        """Test extraction niveau DÉPARTEMENTALE simple"""
        result = NiveauExtractor.extract_niveau("DÉPARTEMENTALE masculine seniors")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.DEPARTEMENTAL)

    def test_020_extract_niveau_categorie_u13(self):
        """Test extraction catégorie U13"""
        result = NiveauExtractor.extract_niveau("Championnat Régional U13 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.U13)

    def test_021_extract_niveau_categorie_u15(self):
        """Test extraction catégorie U15"""
        result = NiveauExtractor.extract_niveau("Championnat Régional U15 Féminin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.U15)

    def test_022_extract_niveau_categorie_u18(self):
        """Test extraction catégorie U18"""
        result = NiveauExtractor.extract_niveau("Championnat Régional U18 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.U18)

    def test_023_extract_niveau_categorie_senior_explicit(self):
        """Test extraction catégorie SENIOR explicite"""
        result = NiveauExtractor.extract_niveau("Championnat Régional SENIOR Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.SENIOR)

    def test_024_extract_niveau_categorie_seniors(self):
        """Test extraction catégorie SENIORS"""
        result = NiveauExtractor.extract_niveau("Championnat Régional SENIORS Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.SENIORS)

    def test_025_extract_niveau_categorie_veteran(self):
        """Test extraction catégorie VETERAN"""
        result = NiveauExtractor.extract_niveau("Championnat Régional VETERAN Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.VETERAN)

    def test_026_extract_niveau_categorie_veterans(self):
        """Test extraction catégorie VETERANS"""
        result = NiveauExtractor.extract_niveau(
            "Championnat Régional VETERANS Masculin"
        )
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.VETERANS)

    def test_027_extract_niveau_categorie_v35(self):
        """Test extraction catégorie V35"""
        result = NiveauExtractor.extract_niveau("Championnat Régional V35 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.V35)

    def test_028_extract_niveau_categorie_minime(self):
        """Test extraction catégorie MINIME"""
        result = NiveauExtractor.extract_niveau("Championnat Régional MINIME Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.MINIME)

    def test_029_extract_niveau_categorie_cadet(self):
        """Test extraction catégorie CADET"""
        result = NiveauExtractor.extract_niveau("Championnat Régional CADET Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.CADET)

    def test_030_extract_niveau_categorie_poussin(self):
        """Test extraction catégorie POUSSIN"""
        result = NiveauExtractor.extract_niveau("Championnat Régional POUSSIN Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.POUSSIN)

    def test_031_extract_niveau_categorie_mini_poussin(self):
        """Test extraction catégorie MINI POUSSIN"""
        result = NiveauExtractor.extract_niveau(
            "Championnat Régional MINI POUSSIN Masculin"
        )
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.MINI_POUSSIN)

    def test_032_extract_niveau_full_example(self):
        """Test extraction complète avec tous les éléments"""
        result = NiveauExtractor.extract_niveau("Championnat Régional R2 U15 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.REGIONAL)
        self.assertEqual(result.division, 2)
        self.assertEqual(result.categorie, CategorieType.U15)

    def test_033_extract_niveau_no_niveau_detected(self):
        """Test quand aucun niveau n'est détecté"""
        result = NiveauExtractor.extract_niveau("Tournoi Amical Entre Amis")
        self.assertIsNone(result)

    def test_034_extract_niveau_case_insensitive(self):
        """Test insensibilité à la casse"""
        result = NiveauExtractor.extract_niveau("championnat elite masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.ELITE)

    def test_035_extract_niveau_u_dash_format(self):
        """Test format U-13"""
        result = NiveauExtractor.extract_niveau("Championnat Régional U-13 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.U13)

    def test_036_extract_niveau_v_dash_format(self):
        """Test format V-35"""
        result = NiveauExtractor.extract_niveau("Championnat Régional V-35 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.V35)

    def test_037_extract_niveau_pre_national(self):
        """Test PRE NATIONAL"""
        result = NiveauExtractor.extract_niveau("Championnat PRE NATIONAL Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.NATIONAL)

    def test_038_extract_niveau_pre_national_accented(self):
        """Test PRÉ NATIONAL"""
        result = NiveauExtractor.extract_niveau("Championnat PRÉ NATIONAL Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.NATIONAL)

    def test_039_extract_from_competition_data_none(self):
        """Test extract_from_competition_data avec None"""
        result = NiveauExtractor.extract_from_competition_data(None)  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_040_extract_from_competition_data_empty_dict(self):
        """Test extract_from_competition_data avec dict vide"""
        result = NiveauExtractor.extract_from_competition_data({})
        self.assertIsNone(result)

    def test_041_extract_from_competition_data_with_nom(self):
        """Test extract_from_competition_data avec nom"""
        data = {"nom": "Championnat Régional R1 U13 Masculin"}
        result = NiveauExtractor.extract_from_competition_data(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.REGIONAL)
        self.assertEqual(result.division, 1)
        self.assertEqual(result.categorie, CategorieType.U13)

    def test_042_extract_from_competition_data_nom_no_match_use_code(self):
        """Test extract_from_competition_data quand nom ne match pas, utilise code"""
        data = {"nom": "Tournoi Amical", "code": "REGIONAL R2 U15"}
        result = NiveauExtractor.extract_from_competition_data(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.REGIONAL)
        self.assertEqual(result.division, 2)
        self.assertEqual(result.categorie, CategorieType.U15)

    def test_043_extract_from_competition_data_nom_matches_ignore_code(self):
        """Test extract_from_competition_data quand nom match, ignore code"""
        data = {"nom": "Championnat ELITE Masculin", "code": "DEPARTEMENTAL D1"}
        result = NiveauExtractor.extract_from_competition_data(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.ELITE)

    def test_044_extract_from_competition_data_only_code(self):
        """Test extract_from_competition_data seulement avec code"""
        data = {"code": "NATIONAL N3 SENIOR"}
        result = NiveauExtractor.extract_from_competition_data(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.NATIONAL)
        self.assertEqual(result.division, 3)
        self.assertEqual(result.categorie, CategorieType.SENIOR)


class TestGetNiveauFromIdcompetition(unittest.TestCase):
    """Tests pour la fonction get_niveau_from_idcompetition"""

    def test_045_get_niveau_from_idcompetition_none(self):
        """Test get_niveau_from_idcompetition avec None"""
        result = get_niveau_from_idcompetition(None)
        self.assertIsNone(result)

    def test_046_get_niveau_from_idcompetition_no_nom(self):
        """Test get_niveau_from_idcompetition sans nom"""
        mock_idcomp = Mock()
        mock_idcomp.nom = None
        result = get_niveau_from_idcompetition(mock_idcomp)
        self.assertIsNone(result)

    def test_048_extract_niveau_no_categorie_defaults_to_senior(self):
        """Test quand aucune catégorie n'est trouvée, SENIOR est utilisé par défaut"""
        result = NiveauExtractor.extract_niveau("Championnat Régional Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.SENIOR)

    def test_049_extract_niveau_with_u_category_no_default_senior(self):
        """Test avec catégorie U présente, pas de default SENIOR"""
        result = NiveauExtractor.extract_niveau("Championnat Régional U13 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.U13)

    def test_050_extract_niveau_zone_geo_elite(self):
        """Test zone géographique pour ELITE"""
        result = NiveauExtractor.extract_niveau("Championnat ELITE Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.zone_geographique, "regional")

    def test_051_extract_niveau_zone_geo_other(self):
        """Test zone géographique pour autres niveaux (None)"""
        result = NiveauExtractor.extract_niveau("Championnat NATIONAL Masculin")
        self.assertIsNotNone(result)
        self.assertIsNone(result.zone_geographique)

    def test_052_extract_niveau_division_regional_space_number(self):
        """Test division avec 'REGIONAL 1'"""
        result = NiveauExtractor.extract_niveau("Championnat REGIONAL 1 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.division, 1)

    def test_053_extract_niveau_division_departemental_space_number(self):
        """Test division avec 'DEPARTEMENTAL 2'"""
        result = NiveauExtractor.extract_niveau("Championnat DEPARTEMENTAL 2 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.division, 2)

    def test_054_extract_niveau_categorie_espoir(self):
        """Test extraction catégorie ESPOIR"""
        result = NiveauExtractor.extract_niveau("Championnat Régional ESPOIR Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.ESPOIR)

    def test_055_extract_niveau_categorie_benjamin(self):
        """Test extraction catégorie BENJAMIN"""
        result = NiveauExtractor.extract_niveau(
            "Championnat Régional BENJAMIN Masculin"
        )
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.BENJAMIN)

    def test_056_extract_niveau_categorie_u7(self):
        """Test extraction catégorie U7"""
        result = NiveauExtractor.extract_niveau("Championnat Régional U7 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.U7)

    def test_057_extract_niveau_categorie_u20(self):
        """Test extraction catégorie U20"""
        result = NiveauExtractor.extract_niveau("Championnat Régional U20 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.U20)

    def test_058_extract_niveau_categorie_u21(self):
        """Test extraction catégorie U21"""
        result = NiveauExtractor.extract_niveau("Championnat Régional U21 Masculin")
        self.assertIsNotNone(result)
        self.assertEqual(result.categorie, CategorieType.U21)

    def test_059_extract_from_competition_data_nom_empty_code_valid(self):
        """Test extract_from_competition_data avec nom vide mais code valide"""
        data = {"nom": "", "code": "REGIONAL R2 U15"}
        result = NiveauExtractor.extract_from_competition_data(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.REGIONAL)
        self.assertEqual(result.division, 2)
        self.assertEqual(result.categorie, CategorieType.U15)

    def test_060_extract_from_competition_data_nom_none_code_valid(self):
        """Test extract_from_competition_data avec nom None mais code valide"""
        data = {"nom": None, "code": "NATIONAL N3 SENIOR"}
        result = NiveauExtractor.extract_from_competition_data(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.NATIONAL)
        self.assertEqual(result.division, 3)
        self.assertEqual(result.categorie, CategorieType.SENIOR)

    def test_061_get_niveau_from_idcompetition_empty_nom(self):
        """Test get_niveau_from_idcompetition avec nom vide"""
        mock_idcomp = Mock()
        mock_idcomp.nom = ""
        result = get_niveau_from_idcompetition(mock_idcomp)
        self.assertIsNone(result)

    def test_062_get_niveau_from_idcompetition_whitespace_nom(self):
        """Test get_niveau_from_idcompetition avec nom whitespace seulement"""
        mock_idcomp = Mock()
        mock_idcomp.nom = "   "
        result = get_niveau_from_idcompetition(mock_idcomp)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
