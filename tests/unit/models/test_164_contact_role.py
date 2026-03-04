"""Tests for ContactRoleEnum enum."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.models.contact_role_enum import ContactRoleEnum


class Test164ContactRole(unittest.TestCase):
    """Tests for ContactRoleEnum enum."""

    def test_000_values(self) -> None:
        self.assertEqual(ContactRoleEnum.CLUB.value, "Club")
        self.assertEqual(ContactRoleEnum.CORRESPONDANT_EQUIPE.value, "Correspondant")
        self.assertEqual(ContactRoleEnum.ENTRAINEUR.value, "Entraîneur")
        self.assertEqual(ContactRoleEnum.ENTRAINEUR_ADJOINT.value, "Entraîneur adjoint")
        self.assertEqual(ContactRoleEnum.PRESIDENT.value, "Président")
        self.assertEqual(ContactRoleEnum.CORRESPONDANT_CLUB.value, "Correspondant club")
        self.assertEqual(ContactRoleEnum.REFERENT_SECURITE.value, "Référent sécurité")
        self.assertEqual(ContactRoleEnum.MEMBRE.value, "Membre")

    def test_001_str_subclass(self) -> None:
        self.assertIsInstance(ContactRoleEnum.CLUB, str)
        self.assertEqual(ContactRoleEnum.CLUB, "Club")

    def test_002_member_count(self) -> None:
        self.assertEqual(len(ContactRoleEnum), 8)

    def test_003_human_readable(self) -> None:
        for role in ContactRoleEnum:
            self.assertTrue(len(role.value) > 0)
            self.assertFalse(role.value.startswith("_"))


if __name__ == "__main__":
    unittest.main()
