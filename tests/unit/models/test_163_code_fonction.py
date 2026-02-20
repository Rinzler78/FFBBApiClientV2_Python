"""Tests for CodeFonction enum."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.models.code_fonction import (
    CODE_FONCTION_TO_CONTACT_ROLE,
    CodeFonction,
)
from ffbb_api_client_v2.models.contact_role import ContactRole


class Test163CodeFonction(unittest.TestCase):
    """Tests for CodeFonction enum."""

    def test_000_values(self) -> None:
        self.assertEqual(CodeFonction.PRESIDENT.value, "PRES")
        self.assertEqual(CodeFonction.CORRESPONDANT.value, "CP")
        self.assertEqual(CodeFonction.REFERENT_SECURITE.value, "PSB")

    def test_001_str_subclass(self) -> None:
        self.assertIsInstance(CodeFonction.PRESIDENT, str)
        self.assertEqual(CodeFonction.PRESIDENT, "PRES")

    def test_002_from_value(self) -> None:
        self.assertEqual(CodeFonction("PRES"), CodeFonction.PRESIDENT)
        self.assertEqual(CodeFonction("CP"), CodeFonction.CORRESPONDANT)
        self.assertEqual(CodeFonction("PSB"), CodeFonction.REFERENT_SECURITE)

    def test_003_unknown_value_raises(self) -> None:
        with self.assertRaises(ValueError):
            CodeFonction("UNKNOWN")

    def test_004_member_count(self) -> None:
        self.assertEqual(len(CodeFonction), 3)

    def test_005_mapping_coverage(self) -> None:
        for cf in CodeFonction:
            self.assertIn(cf, CODE_FONCTION_TO_CONTACT_ROLE)

    def test_006_mapping_values(self) -> None:
        self.assertEqual(
            CODE_FONCTION_TO_CONTACT_ROLE[CodeFonction.PRESIDENT],
            ContactRole.PRESIDENT,
        )
        self.assertEqual(
            CODE_FONCTION_TO_CONTACT_ROLE[CodeFonction.CORRESPONDANT],
            ContactRole.CORRESPONDANT_CLUB,
        )
        self.assertEqual(
            CODE_FONCTION_TO_CONTACT_ROLE[CodeFonction.REFERENT_SECURITE],
            ContactRole.REFERENT_SECURITE,
        )


if __name__ == "__main__":
    unittest.main()
