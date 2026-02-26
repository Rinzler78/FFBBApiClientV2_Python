"""Tests for PhoneNumber type."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.models.phone_number import PhoneNumber


class TestPhoneNumber(unittest.TestCase):
    # ------------------------------------------------------------------
    # Normalization
    # ------------------------------------------------------------------
    def test_000_strips_spaces(self) -> None:
        self.assertEqual(PhoneNumber("01 23 45 67 89"), "0123456789")

    def test_001_strips_dots(self) -> None:
        self.assertEqual(PhoneNumber("01.23.45.67.89"), "0123456789")

    def test_002_strips_dashes(self) -> None:
        self.assertEqual(PhoneNumber("01-23-45-67-89"), "0123456789")

    def test_003_keeps_plus(self) -> None:
        self.assertEqual(PhoneNumber("+33 1 23 45 67 89"), "+33123456789")

    def test_004_already_clean(self) -> None:
        self.assertEqual(PhoneNumber("0123456789"), "0123456789")

    def test_005_strips_leading_trailing_whitespace(self) -> None:
        self.assertEqual(PhoneNumber("  0123456789  "), "0123456789")

    def test_006_mixed_separators(self) -> None:
        self.assertEqual(PhoneNumber("01 23.45-67 89"), "0123456789")

    def test_007_empty_string(self) -> None:
        self.assertEqual(PhoneNumber(""), "")

    def test_008_whitespace_only(self) -> None:
        self.assertEqual(PhoneNumber("   "), "")

    # ------------------------------------------------------------------
    # raw property
    # ------------------------------------------------------------------
    def test_010_raw_preserves_original(self) -> None:
        p = PhoneNumber("01 23 45 67 89")
        self.assertEqual(p.raw, "01 23 45 67 89")

    def test_011_raw_preserves_original_international(self) -> None:
        p = PhoneNumber("+33 1 23 45 67 89")
        self.assertEqual(p.raw, "+33 1 23 45 67 89")

    # ------------------------------------------------------------------
    # is_french
    # ------------------------------------------------------------------
    def test_020_is_french_local(self) -> None:
        self.assertTrue(PhoneNumber("0123456789").is_french)

    def test_021_is_french_international(self) -> None:
        self.assertTrue(PhoneNumber("+33123456789").is_french)

    def test_022_not_french_short(self) -> None:
        self.assertFalse(PhoneNumber("012345").is_french)

    def test_023_not_french_foreign(self) -> None:
        self.assertFalse(PhoneNumber("+44123456789").is_french)

    # ------------------------------------------------------------------
    # international property
    # ------------------------------------------------------------------
    def test_030_international_from_local(self) -> None:
        self.assertEqual(PhoneNumber("0123456789").international, "+33123456789")

    def test_031_international_already_international(self) -> None:
        self.assertEqual(PhoneNumber("+33123456789").international, "+33123456789")

    def test_032_international_non_french(self) -> None:
        p = PhoneNumber("+44123456789")
        self.assertEqual(p.international, "+44123456789")

    # ------------------------------------------------------------------
    # formatted property
    # ------------------------------------------------------------------
    def test_040_formatted_local(self) -> None:
        self.assertEqual(PhoneNumber("0123456789").formatted, "01 23 45 67 89")

    def test_041_formatted_international(self) -> None:
        self.assertEqual(PhoneNumber("+33123456789").formatted, "01 23 45 67 89")

    def test_042_formatted_non_french_passthrough(self) -> None:
        p = PhoneNumber("+44123456789")
        self.assertEqual(p.formatted, "+44123456789")

    def test_043_formatted_from_spaced(self) -> None:
        self.assertEqual(PhoneNumber("01 23 45 67 89").formatted, "01 23 45 67 89")

    # ------------------------------------------------------------------
    # str subclass behavior
    # ------------------------------------------------------------------
    def test_050_isinstance_str(self) -> None:
        self.assertIsInstance(PhoneNumber("0123456789"), str)

    def test_051_equality_with_str(self) -> None:
        self.assertEqual(PhoneNumber("01 23 45 67 89"), "0123456789")

    def test_052_usable_as_dict_key(self) -> None:
        d = {PhoneNumber("0123456789"): "ok"}
        self.assertEqual(d["0123456789"], "ok")

    def test_053_bool_false_when_empty(self) -> None:
        self.assertFalse(PhoneNumber(""))

    def test_054_bool_true_when_nonempty(self) -> None:
        self.assertTrue(PhoneNumber("0123456789"))


if __name__ == "__main__":
    unittest.main()
