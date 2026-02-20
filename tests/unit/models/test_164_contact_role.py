"""Tests for ContactRole enum."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.models.contact_role import ContactRole


class Test164ContactRole(unittest.TestCase):
    """Tests for ContactRole enum."""

    def test_000_values(self) -> None:
        self.assertEqual(ContactRole.CLUB.value, "Club")
        self.assertEqual(ContactRole.CORRESPONDANT_EQUIPE.value, "Correspondant")
        self.assertEqual(ContactRole.ENTRAINEUR.value, "Entraîneur")
        self.assertEqual(ContactRole.ENTRAINEUR_ADJOINT.value, "Entraîneur adjoint")
        self.assertEqual(ContactRole.PRESIDENT.value, "Président")
        self.assertEqual(ContactRole.CORRESPONDANT_CLUB.value, "Correspondant club")
        self.assertEqual(ContactRole.REFERENT_SECURITE.value, "Référent sécurité")
        self.assertEqual(ContactRole.MEMBRE.value, "Membre")

    def test_001_str_subclass(self) -> None:
        self.assertIsInstance(ContactRole.CLUB, str)
        self.assertEqual(ContactRole.CLUB, "Club")

    def test_002_member_count(self) -> None:
        self.assertEqual(len(ContactRole), 8)

    def test_003_human_readable(self) -> None:
        for role in ContactRole:
            self.assertTrue(len(role.value) > 0)
            self.assertFalse(role.value.startswith("_"))


if __name__ == "__main__":
    unittest.main()
