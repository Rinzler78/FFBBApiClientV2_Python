"""Tests for CodeFonctionEnum enum."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.models.code_fonction_enum import (
    CODE_FONCTION_TO_CONTACT_ROLE,
    CodeFonctionEnum,
)
from ffbb_api_client_v2.models.contact_role_enum import ContactRoleEnum


class Test163CodeFonction(unittest.TestCase):
    """Tests for CodeFonctionEnum enum."""

    def test_000_values(self) -> None:
        self.assertEqual(CodeFonctionEnum.PRESIDENT.value, "PRES")
        self.assertEqual(CodeFonctionEnum.CORRESPONDANT.value, "CP")
        self.assertEqual(CodeFonctionEnum.REFERENT_SECURITE.value, "PSB")

    def test_001_str_subclass(self) -> None:
        self.assertIsInstance(CodeFonctionEnum.PRESIDENT, str)
        self.assertEqual(CodeFonctionEnum.PRESIDENT, "PRES")

    def test_002_from_value(self) -> None:
        self.assertEqual(CodeFonctionEnum("PRES"), CodeFonctionEnum.PRESIDENT)
        self.assertEqual(CodeFonctionEnum("CP"), CodeFonctionEnum.CORRESPONDANT)
        self.assertEqual(CodeFonctionEnum("PSB"), CodeFonctionEnum.REFERENT_SECURITE)

    def test_003_unknown_value_raises(self) -> None:
        with self.assertRaises(ValueError):
            CodeFonctionEnum("UNKNOWN")

    def test_004_member_count(self) -> None:
        self.assertEqual(len(CodeFonctionEnum), 3)

    def test_005_mapping_coverage(self) -> None:
        for cf in CodeFonctionEnum:
            self.assertIn(cf, CODE_FONCTION_TO_CONTACT_ROLE)

    def test_006_mapping_values(self) -> None:
        self.assertEqual(
            CODE_FONCTION_TO_CONTACT_ROLE[CodeFonctionEnum.PRESIDENT],
            ContactRoleEnum.PRESIDENT,
        )
        self.assertEqual(
            CODE_FONCTION_TO_CONTACT_ROLE[CodeFonctionEnum.CORRESPONDANT],
            ContactRoleEnum.CORRESPONDANT_CLUB,
        )
        self.assertEqual(
            CODE_FONCTION_TO_CONTACT_ROLE[CodeFonctionEnum.REFERENT_SECURITE],
            ContactRoleEnum.REFERENT_SECURITE,
        )


if __name__ == "__main__":
    unittest.main()
