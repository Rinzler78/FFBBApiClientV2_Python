"""
Unit tests for niveau_info.py
"""

import unittest

from ffbb_api_client_v2.models.categorie_type_enum import CategorieTypeEnum
from ffbb_api_client_v2.models.niveau_info import NiveauInfo
from ffbb_api_client_v2.models.niveau_type_enum import NiveauTypeEnum


class TestNiveauInfo(unittest.TestCase):
    """Tests pour la classe NiveauInfo"""

    def test_001_init_basic(self):
        """Test d'initialisation basique"""
        info = NiveauInfo(type=NiveauTypeEnum.DEPARTEMENTAL)
        self.assertEqual(info.type, NiveauTypeEnum.DEPARTEMENTAL)
        self.assertIsNone(info.division)
        self.assertIsNone(info.categorie)
        self.assertEqual(info.raw_text, "")
        self.assertIsNone(info.zone_geographique)

    def test_002_init_full(self):
        """Test d'initialisation complète"""
        info = NiveauInfo(
            type=NiveauTypeEnum.REGIONAL,
            division=1,
            categorie=CategorieTypeEnum.SENIOR,
            raw_text="R1 Senior",
            zone_geographique="regional",
        )
        self.assertEqual(info.type, NiveauTypeEnum.REGIONAL)
        self.assertEqual(info.division, 1)
        self.assertEqual(info.categorie, CategorieTypeEnum.SENIOR)
        self.assertEqual(info.raw_text, "R1 Senior")
        self.assertEqual(info.zone_geographique, "regional")

    def test_003_is_elite_false(self):
        """Test is_elite pour niveau non ELITE"""
        info = NiveauInfo(type=NiveauTypeEnum.DEPARTEMENTAL)
        self.assertFalse(info.is_elite)

    def test_004_is_elite_true(self):
        """Test is_elite pour niveau ELITE"""
        info = NiveauInfo(type=NiveauTypeEnum.ELITE)
        self.assertTrue(info.is_elite)

    def test_005_zone_effective_departemental(self):
        """Test zone_effective pour départemental"""
        info = NiveauInfo(type=NiveauTypeEnum.DEPARTEMENTAL)
        self.assertEqual(info.zone_effective, "departemental")

    def test_006_zone_effective_regional(self):
        """Test zone_effective pour régional"""
        info = NiveauInfo(type=NiveauTypeEnum.REGIONAL)
        self.assertEqual(info.zone_effective, "regional")

    def test_007_zone_effective_national(self):
        """Test zone_effective pour national"""
        info = NiveauInfo(type=NiveauTypeEnum.NATIONAL)
        self.assertEqual(info.zone_effective, "national")

    def test_008_zone_effective_elite(self):
        """Test zone_effective pour ELITE"""
        info = NiveauInfo(type=NiveauTypeEnum.ELITE)
        self.assertEqual(info.zone_effective, "regional")

    def test_009_matches_filter_zone_only_match(self):
        """Test matches_filter avec seulement zone, match"""
        info = NiveauInfo(type=NiveauTypeEnum.DEPARTEMENTAL, division=1)
        self.assertTrue(info.matches_filter("departemental"))

    def test_010_matches_filter_zone_only_no_match(self):
        """Test matches_filter avec seulement zone, pas de match"""
        info = NiveauInfo(type=NiveauTypeEnum.DEPARTEMENTAL, division=1)
        self.assertFalse(info.matches_filter("regional"))

    def test_011_matches_filter_zone_and_division_match(self):
        """Test matches_filter avec zone et division, match"""
        info = NiveauInfo(type=NiveauTypeEnum.DEPARTEMENTAL, division=1)
        self.assertTrue(info.matches_filter("departemental", 1))

    def test_012_matches_filter_zone_and_division_no_match_zone(self):
        """Test matches_filter avec zone et division, zone ne match pas"""
        info = NiveauInfo(type=NiveauTypeEnum.DEPARTEMENTAL, division=1)
        self.assertFalse(info.matches_filter("regional", 1))

    def test_013_matches_filter_zone_and_division_no_match_division(self):
        """Test matches_filter avec zone et division, division ne match pas"""
        info = NiveauInfo(type=NiveauTypeEnum.DEPARTEMENTAL, division=1)
        self.assertFalse(info.matches_filter("departemental", 2))

    def test_014_matches_filter_zone_and_division_no_division(self):
        """Test matches_filter avec zone et division, pas de division dans info"""
        info = NiveauInfo(type=NiveauTypeEnum.DEPARTEMENTAL, division=None)
        self.assertFalse(info.matches_filter("departemental", 1))

    def test_015_matches_filter_elite_zone(self):
        """Test matches_filter pour ELITE avec zone regional"""
        info = NiveauInfo(type=NiveauTypeEnum.ELITE)
        self.assertTrue(info.matches_filter("regional"))

    def test_016_matches_filter_elite_zone_no_match(self):
        """Test matches_filter pour ELITE avec zone non regional"""
        info = NiveauInfo(type=NiveauTypeEnum.ELITE)
        self.assertFalse(info.matches_filter("national"))

    def test_017_matches_filter_elite_with_division(self):
        """Test matches_filter pour ELITE avec division (pas de division pour ELITE)"""
        info = NiveauInfo(type=NiveauTypeEnum.ELITE)
        self.assertFalse(info.matches_filter("regional", 1))


if __name__ == "__main__":
    unittest.main()
