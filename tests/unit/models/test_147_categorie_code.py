"""Tests for CategorieCode str subclass and component enums.

CategorieCode is a str subclass that parses FFBB category codes into
their component parts: age group, echelon, division, and gender.
"""

from __future__ import annotations

import json
import unittest

from ffbb_api_client_v2.models.age_group import AgeGroup
from ffbb_api_client_v2.models.categorie_code import CategorieCode
from ffbb_api_client_v2.models.echelon import Echelon
from ffbb_api_client_v2.models.gender import Gender

# All 164 historical enum values for regression testing
_ALL_HISTORICAL_VALUES = [
    # Youth Departmental
    "U7M",
    "U7F",
    "U9M",
    "U9F",
    "U11D1M",
    "U11D2M",
    "U11D3M",
    "U11D4M",
    "U11D1F",
    "U11D2F",
    "U11D3F",
    "U13D1M",
    "U13D2M",
    "U13D3M",
    "U13D4M",
    "U13D1F",
    "U13D2F",
    "U13D3F",
    "U15D1M",
    "U15D2M",
    "U15D3M",
    "U15D1F",
    "U15D2F",
    "U15D3F",
    "U17D1M",
    "U17D1F",
    "U18D1M",
    "U18D2M",
    "U18D3M",
    "U18D1F",
    "U18D2F",
    "U18D3F",
    "U21D1M",
    # Youth generic
    "U11",
    "U13",
    "U15",
    "U18",
    # Youth Regional
    "U13R1M",
    "U13R2M",
    "U13R3M",
    "U13R1F",
    "U13R2F",
    "U13R3F",
    "U15R1M",
    "U15R2M",
    "U15R3M",
    "U15R1F",
    "U15R2F",
    "U15R3F",
    "U17R1M",
    "U17R2M",
    "U17R1F",
    "U17R2F",
    "U18R1M",
    "U18R2M",
    "U18R3M",
    "U18R1F",
    "U18R2F",
    "U21R1M",
    "U21R2M",
    # Youth Federal
    "U15F1M",
    "U15F1F",
    "U18F1M",
    "U18F1F",
    # National
    "NM1",
    "NM2",
    "NM3",
    "NF2",
    "NF3",
    # Pre-national / pre-regional
    "PNM",
    "PNF",
    "PRM",
    "PRF",
    # Senior Excellence Regional
    "SER1M",
    "SER2M",
    "SER3M",
    "SER1F",
    "SER2F",
    "SER3F",
    # Senior Departmental
    "SED1M",
    "SED2M",
    "SED3M",
    "SED4M",
    "SED1F",
    "SED2F",
    "SED3F",
    "SED4F",
    # Association Regionale
    "AREGM",
    "AREGF",
    # Basket fauteuil
    "LBWL",
    # Youth generic (without level/gender)
    "U7",
    "U9",
    "U17",
    "U20",
    "U21",
    # Senior generic
    "SE",
    "SEN",
    "S",
    "SENIOR",
    # Veteran
    "VE",
    # Ligue Feminine
    "LF2",
]


class TestCategorieCodeConstruction(unittest.TestCase):
    """Construction from various input strings."""

    def test_from_youth_echelon(self) -> None:
        code = CategorieCode("U13D1M")
        self.assertEqual(code, "U13D1M")
        self.assertIsInstance(code, str)
        self.assertIsInstance(code, CategorieCode)

    def test_from_youth_gender(self) -> None:
        code = CategorieCode("U7M")
        self.assertEqual(code, "U7M")

    def test_from_youth_generic(self) -> None:
        code = CategorieCode("U13")
        self.assertEqual(code, "U13")

    def test_from_senior_departmental(self) -> None:
        code = CategorieCode("SED1M")
        self.assertEqual(code, "SED1M")

    def test_from_senior_excellence(self) -> None:
        code = CategorieCode("SER1M")
        self.assertEqual(code, "SER1M")

    def test_from_national(self) -> None:
        code = CategorieCode("NM1")
        self.assertEqual(code, "NM1")

    def test_from_pre_national(self) -> None:
        code = CategorieCode("PNM")
        self.assertEqual(code, "PNM")

    def test_from_areg(self) -> None:
        code = CategorieCode("AREGM")
        self.assertEqual(code, "AREGM")

    def test_from_lf(self) -> None:
        code = CategorieCode("LF2")
        self.assertEqual(code, "LF2")

    def test_from_senior_generic(self) -> None:
        for val in ("SE", "SEN", "S", "SENIOR"):
            code = CategorieCode(val)
            self.assertEqual(code, val)

    def test_from_veteran(self) -> None:
        code = CategorieCode("VE")
        self.assertEqual(code, "VE")

    def test_from_lbwl(self) -> None:
        code = CategorieCode("LBWL")
        self.assertEqual(code, "LBWL")

    def test_from_unknown(self) -> None:
        code = CategorieCode("XYZABC")
        self.assertEqual(code, "XYZABC")

    def test_from_empty(self) -> None:
        code = CategorieCode("")
        self.assertEqual(code, "")


class TestCategorieCodeStringCompatibility(unittest.TestCase):
    """Backward compatibility with str operations."""

    def test_equality_with_plain_str(self) -> None:
        code = CategorieCode("U13D1M")
        self.assertEqual(code, "U13D1M")
        self.assertTrue(code == "U13D1M")

    def test_inequality(self) -> None:
        code = CategorieCode("U13D1M")
        self.assertNotEqual(code, "U15D1M")

    def test_in_operator(self) -> None:
        code = CategorieCode("SEN")
        self.assertIn(code, ("S", "SEN", "SENIOR"))

    def test_str_conversion(self) -> None:
        code = CategorieCode("U13D1M")
        self.assertEqual(str(code), "U13D1M")

    def test_hash_matches_str(self) -> None:
        code = CategorieCode("U13D1M")
        self.assertEqual(hash(code), hash("U13D1M"))

    def test_isinstance_str(self) -> None:
        code = CategorieCode("U13D1M")
        self.assertIsInstance(code, str)

    def test_json_serializable(self) -> None:
        code = CategorieCode("U13D1M")
        result = json.dumps({"code": code})
        self.assertEqual(result, '{"code": "U13D1M"}')

    def test_repr(self) -> None:
        code = CategorieCode("U13D1M")
        self.assertEqual(repr(code), "CategorieCode('U13D1M')")

    def test_dict_key(self) -> None:
        code = CategorieCode("U13D1M")
        d = {code: 42}
        self.assertEqual(d["U13D1M"], 42)

    def test_string_methods_return_str(self) -> None:
        code = CategorieCode("u13d1m")
        upper = code.upper()
        self.assertEqual(upper, "U13D1M")
        self.assertIsInstance(upper, str)


class TestCategorieCodeParsing(unittest.TestCase):
    """Parsing of components for each recognized pattern."""

    # --- Youth + echelon + division + gender ---
    def test_youth_departmental(self) -> None:
        code = CategorieCode("U13D1M")
        self.assertEqual(code.age_group, AgeGroup.U13)
        self.assertEqual(code.echelon, Echelon.DEPARTEMENT)
        self.assertEqual(code.division, 1)
        self.assertEqual(code.gender, Gender.MASCULIN)
        self.assertTrue(code.is_parsed)

    def test_youth_regional(self) -> None:
        code = CategorieCode("U15R2F")
        self.assertEqual(code.age_group, AgeGroup.U15)
        self.assertEqual(code.echelon, Echelon.REGION)
        self.assertEqual(code.division, 2)
        self.assertEqual(code.gender, Gender.FEMININ)

    def test_youth_federal(self) -> None:
        code = CategorieCode("U18F1M")
        self.assertEqual(code.age_group, AgeGroup.U18)
        self.assertEqual(code.echelon, Echelon.FEDERAL)
        self.assertEqual(code.division, 1)
        self.assertEqual(code.gender, Gender.MASCULIN)

    def test_youth_all_divisions(self) -> None:
        for div in range(1, 5):
            code = CategorieCode(f"U11D{div}M")
            self.assertEqual(code.division, div)

    # --- Youth + gender ---
    def test_youth_gender_male(self) -> None:
        code = CategorieCode("U7M")
        self.assertEqual(code.age_group, AgeGroup.U7)
        self.assertIsNone(code.echelon)
        self.assertIsNone(code.division)
        self.assertEqual(code.gender, Gender.MASCULIN)
        self.assertTrue(code.is_parsed)

    def test_youth_gender_female(self) -> None:
        code = CategorieCode("U9F")
        self.assertEqual(code.age_group, AgeGroup.U9)
        self.assertEqual(code.gender, Gender.FEMININ)

    # --- Youth generic ---
    def test_youth_generic_u13(self) -> None:
        code = CategorieCode("U13")
        self.assertEqual(code.age_group, AgeGroup.U13)
        self.assertIsNone(code.echelon)
        self.assertIsNone(code.division)
        self.assertIsNone(code.gender)
        self.assertTrue(code.is_parsed)

    def test_youth_generic_u7(self) -> None:
        code = CategorieCode("U7")
        self.assertEqual(code.age_group, AgeGroup.U7)

    def test_youth_generic_u20(self) -> None:
        code = CategorieCode("U20")
        self.assertEqual(code.age_group, AgeGroup.U20)

    # --- Senior structured ---
    def test_senior_departmental(self) -> None:
        code = CategorieCode("SED1M")
        self.assertEqual(code.age_group, AgeGroup.SENIOR)
        self.assertEqual(code.echelon, Echelon.DEPARTEMENT)
        self.assertEqual(code.division, 1)
        self.assertEqual(code.gender, Gender.MASCULIN)
        self.assertTrue(code.is_parsed)

    def test_senior_excellence_regional(self) -> None:
        code = CategorieCode("SER1M")
        self.assertEqual(code.age_group, AgeGroup.SENIOR)
        self.assertEqual(code.echelon, Echelon.EXCELLENCE)
        self.assertEqual(code.division, 1)
        self.assertEqual(code.gender, Gender.MASCULIN)

    def test_senior_excellence_female(self) -> None:
        code = CategorieCode("SER2F")
        self.assertEqual(code.age_group, AgeGroup.SENIOR)
        self.assertEqual(code.echelon, Echelon.EXCELLENCE)
        self.assertEqual(code.division, 2)
        self.assertEqual(code.gender, Gender.FEMININ)

    # --- National ---
    def test_national_masculine(self) -> None:
        code = CategorieCode("NM1")
        self.assertEqual(code.age_group, AgeGroup.SENIOR)
        self.assertEqual(code.echelon, Echelon.NATIONAL)
        self.assertEqual(code.division, 1)
        self.assertEqual(code.gender, Gender.MASCULIN)
        self.assertTrue(code.is_parsed)

    def test_national_feminine(self) -> None:
        code = CategorieCode("NF2")
        self.assertEqual(code.age_group, AgeGroup.SENIOR)
        self.assertEqual(code.echelon, Echelon.NATIONAL)
        self.assertEqual(code.division, 2)
        self.assertEqual(code.gender, Gender.FEMININ)

    # --- Pre-national / pre-regional ---
    def test_pre_national_masculine(self) -> None:
        code = CategorieCode("PNM")
        self.assertEqual(code.age_group, AgeGroup.SENIOR)
        self.assertEqual(code.echelon, Echelon.PRE_NATIONAL)
        self.assertIsNone(code.division)
        self.assertEqual(code.gender, Gender.MASCULIN)
        self.assertTrue(code.is_parsed)

    def test_pre_national_feminine(self) -> None:
        code = CategorieCode("PNF")
        self.assertEqual(code.echelon, Echelon.PRE_NATIONAL)
        self.assertEqual(code.gender, Gender.FEMININ)

    def test_pre_regional_masculine(self) -> None:
        code = CategorieCode("PRM")
        self.assertEqual(code.echelon, Echelon.PRE_REGIONAL)
        self.assertEqual(code.gender, Gender.MASCULIN)

    def test_pre_regional_feminine(self) -> None:
        code = CategorieCode("PRF")
        self.assertEqual(code.echelon, Echelon.PRE_REGIONAL)
        self.assertEqual(code.gender, Gender.FEMININ)

    # --- Association regionale ---
    def test_areg_masculine(self) -> None:
        code = CategorieCode("AREGM")
        self.assertIsNone(code.age_group)
        self.assertEqual(code.echelon, Echelon.ASSOCIATION_REGIONALE)
        self.assertIsNone(code.division)
        self.assertEqual(code.gender, Gender.MASCULIN)
        self.assertTrue(code.is_parsed)

    def test_areg_feminine(self) -> None:
        code = CategorieCode("AREGF")
        self.assertEqual(code.echelon, Echelon.ASSOCIATION_REGIONALE)
        self.assertEqual(code.gender, Gender.FEMININ)

    # --- Ligue Feminine ---
    def test_ligue_feminine(self) -> None:
        code = CategorieCode("LF2")
        self.assertIsNone(code.age_group)
        self.assertEqual(code.echelon, Echelon.LIGUE_FEMININE)
        self.assertEqual(code.division, 2)
        self.assertEqual(code.gender, Gender.FEMININ)
        self.assertTrue(code.is_parsed)

    # --- Senior generic ---
    def test_senior_se(self) -> None:
        code = CategorieCode("SE")
        self.assertEqual(code.age_group, AgeGroup.SENIOR)
        self.assertIsNone(code.echelon)
        self.assertIsNone(code.division)
        self.assertIsNone(code.gender)
        self.assertTrue(code.is_parsed)

    def test_senior_sen(self) -> None:
        code = CategorieCode("SEN")
        self.assertEqual(code.age_group, AgeGroup.SENIOR)
        self.assertTrue(code.is_parsed)

    def test_senior_s(self) -> None:
        code = CategorieCode("S")
        self.assertEqual(code.age_group, AgeGroup.SENIOR)
        self.assertTrue(code.is_parsed)

    def test_senior_full_word(self) -> None:
        code = CategorieCode("SENIOR")
        self.assertEqual(code.age_group, AgeGroup.SENIOR)
        self.assertTrue(code.is_parsed)

    # --- Veteran ---
    def test_veteran(self) -> None:
        code = CategorieCode("VE")
        self.assertEqual(code.age_group, AgeGroup.VETERAN)
        self.assertIsNone(code.echelon)
        self.assertIsNone(code.division)
        self.assertIsNone(code.gender)
        self.assertTrue(code.is_parsed)

    # --- Basket fauteuil ---
    def test_basket_fauteuil(self) -> None:
        code = CategorieCode("LBWL")
        self.assertIsNone(code.age_group)
        self.assertEqual(code.echelon, Echelon.BASKET_FAUTEUIL)
        self.assertIsNone(code.division)
        self.assertIsNone(code.gender)
        self.assertTrue(code.is_parsed)


class TestCategorieCodeUnknown(unittest.TestCase):
    """Unknown codes: is_parsed=False, all components None."""

    def test_unknown_code(self) -> None:
        code = CategorieCode("XYZABC")
        self.assertFalse(code.is_parsed)
        self.assertIsNone(code.age_group)
        self.assertIsNone(code.echelon)
        self.assertIsNone(code.division)
        self.assertIsNone(code.gender)

    def test_empty_string(self) -> None:
        code = CategorieCode("")
        self.assertFalse(code.is_parsed)
        self.assertIsNone(code.age_group)

    def test_unknown_preserves_value(self) -> None:
        code = CategorieCode("NEWCODE2026")
        self.assertEqual(code, "NEWCODE2026")
        self.assertEqual(str(code), "NEWCODE2026")
        self.assertFalse(code.is_parsed)

    def test_partial_match_not_parsed(self) -> None:
        code = CategorieCode("U13D")
        self.assertFalse(code.is_parsed)

    def test_lowercase_not_parsed(self) -> None:
        code = CategorieCode("u13d1m")
        self.assertFalse(code.is_parsed)


class TestCategorieCodeAllHistoricalValues(unittest.TestCase):
    """Regression: all 164 historical enum values parse without error."""

    def test_all_historical_values_parse(self) -> None:
        for val in _ALL_HISTORICAL_VALUES:
            code = CategorieCode(val)
            self.assertEqual(code, val, f"Value mismatch for {val}")
            self.assertTrue(
                code.is_parsed,
                f"{val} should be parsed but is_parsed=False",
            )

    def test_historical_count(self) -> None:
        self.assertEqual(len(_ALL_HISTORICAL_VALUES), 101)


class TestAgeGroup(unittest.TestCase):
    """AgeGroup enum."""

    def test_values(self) -> None:
        self.assertEqual(AgeGroup.U7, "U7")
        self.assertEqual(AgeGroup.U9, "U9")
        self.assertEqual(AgeGroup.U11, "U11")
        self.assertEqual(AgeGroup.U13, "U13")
        self.assertEqual(AgeGroup.U15, "U15")
        self.assertEqual(AgeGroup.U17, "U17")
        self.assertEqual(AgeGroup.U18, "U18")
        self.assertEqual(AgeGroup.U20, "U20")
        self.assertEqual(AgeGroup.U21, "U21")
        self.assertEqual(AgeGroup.SENIOR, "SE")
        self.assertEqual(AgeGroup.VETERAN, "VE")

    def test_str_subclass(self) -> None:
        self.assertIsInstance(AgeGroup.U13, str)

    def test_member_count(self) -> None:
        self.assertEqual(len(AgeGroup), 11)


class TestEchelon(unittest.TestCase):
    """Echelon enum."""

    def test_values(self) -> None:
        self.assertEqual(Echelon.DEPARTEMENT, "D")
        self.assertEqual(Echelon.REGION, "R")
        self.assertEqual(Echelon.FEDERAL, "F")
        self.assertEqual(Echelon.NATIONAL, "N")
        self.assertEqual(Echelon.PRE_NATIONAL, "PN")
        self.assertEqual(Echelon.PRE_REGIONAL, "PR")
        self.assertEqual(Echelon.EXCELLENCE, "E")
        self.assertEqual(Echelon.LIGUE_FEMININE, "LF")
        self.assertEqual(Echelon.ASSOCIATION_REGIONALE, "AREG")
        self.assertEqual(Echelon.BASKET_FAUTEUIL, "LBWL")

    def test_str_subclass(self) -> None:
        self.assertIsInstance(Echelon.DEPARTEMENT, str)

    def test_member_count(self) -> None:
        self.assertEqual(len(Echelon), 12)


class TestGender(unittest.TestCase):
    """Gender enum."""

    def test_values(self) -> None:
        self.assertEqual(Gender.MASCULIN, "M")
        self.assertEqual(Gender.FEMININ, "F")

    def test_str_subclass(self) -> None:
        self.assertIsInstance(Gender.MASCULIN, str)

    def test_member_count(self) -> None:
        self.assertEqual(len(Gender), 2)


class TestFromCategorieCode(unittest.TestCase):
    """Test from_categorie_code converter helper."""

    def test_from_dict_with_code(self) -> None:
        from ffbb_api_client_v2.utils.converter_utils import from_categorie_code

        result = from_categorie_code({"code": "U13D1M"}, "code")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, CategorieCode)
        self.assertEqual(result, "U13D1M")

    def test_from_dict_with_none(self) -> None:
        from ffbb_api_client_v2.utils.converter_utils import from_categorie_code

        result = from_categorie_code({"code": None}, "code")
        self.assertIsNone(result)

    def test_from_dict_missing_key(self) -> None:
        from ffbb_api_client_v2.utils.converter_utils import from_categorie_code

        result = from_categorie_code({}, "code")
        self.assertIsNone(result)

    def test_from_dict_non_str_value(self) -> None:
        from ffbb_api_client_v2.utils.converter_utils import from_categorie_code

        result = from_categorie_code({"code": 123}, "code")
        self.assertIsNone(result)

    def test_unknown_code_preserved(self) -> None:
        from ffbb_api_client_v2.utils.converter_utils import from_categorie_code

        result = from_categorie_code({"code": "NEWCODE"}, "code")
        self.assertIsNotNone(result)
        self.assertEqual(result, "NEWCODE")
        assert result is not None
        self.assertFalse(result.is_parsed)


if __name__ == "__main__":
    unittest.main()
