"""Tests for ContactInfo dataclass."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.models.contact_info import ContactInfo
from ffbb_api_client_v2.models.contact_role import ContactRole


class Test160ContactInfo(unittest.TestCase):
    """Tests for ContactInfo."""

    def test_000_create_contact_info(self) -> None:
        contact = ContactInfo(
            titre=ContactRole.ENTRAINEUR,
            nom="Dupont",
            prenom="Jean",
            telephone="0612345678",
            email="jean@example.com",
            source="directus:get_entraineur",
        )
        self.assertEqual(contact.titre, ContactRole.ENTRAINEUR)
        self.assertEqual(contact.nom, "Dupont")
        self.assertEqual(contact.prenom, "Jean")
        self.assertEqual(contact.telephone, "0612345678")
        self.assertEqual(contact.email, "jean@example.com")
        self.assertEqual(contact.source, "directus:get_entraineur")

    def test_001_contact_info_with_empty_fields(self) -> None:
        contact = ContactInfo(
            titre=ContactRole.CLUB,
            nom="",
            prenom="",
            telephone="",
            email="",
            source="directus:get_organisme",
        )
        self.assertEqual(contact.nom, "")
        self.assertEqual(contact.email, "")

    def test_002_contact_info_equality(self) -> None:
        c1 = ContactInfo(ContactRole.CLUB, "B", "C", "D", "E", "F")
        c2 = ContactInfo(ContactRole.CLUB, "B", "C", "D", "E", "F")
        self.assertEqual(c1, c2)

    def test_003_contact_info_inequality(self) -> None:
        c1 = ContactInfo(ContactRole.CLUB, "B", "C", "D", "E", "F")
        c2 = ContactInfo(ContactRole.ENTRAINEUR, "B", "C", "D", "E", "F")
        self.assertNotEqual(c1, c2)


if __name__ == "__main__":
    unittest.main()
