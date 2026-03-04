"""Tests for ClubContacts and helper functions."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.directus_ffbb.models.get_organisme_response import (
    GetOrganismeResponse,
)
from ffbb_api_client_v2.models.club_contacts import (
    ClubContacts,
    extract_club_info,
    extract_membres_contacts,
)
from ffbb_api_client_v2.models.code_fonction_enum import CodeFonctionEnum
from ffbb_api_client_v2.models.contact_role_enum import ContactRoleEnum
from ffbb_api_client_v2.models.membre import Membre


class Test162ExtractClubInfo(unittest.TestCase):
    """Tests for extract_club_info."""

    def test_000_extract_club_with_phone_and_email(self) -> None:
        org = GetOrganismeResponse(
            id="1",
            nom="BC Lille",
            telephone="03 20 12 34 56",
            mail="contact@bclille.fr",
        )
        contact = extract_club_info(org)
        self.assertIsNotNone(contact)
        assert contact is not None
        self.assertEqual(contact.titre, ContactRoleEnum.CLUB)
        self.assertEqual(contact.nom, "BC Lille")
        self.assertEqual(contact.telephone, "0320123456")
        self.assertEqual(contact.email, "contact@bclille.fr")
        self.assertEqual(contact.source, "directus:get_organisme")

    def test_001_extract_club_email_only(self) -> None:
        org = GetOrganismeResponse(
            id="2",
            nom="Test Club",
            mail="info@test.fr",
        )
        contact = extract_club_info(org)
        self.assertIsNotNone(contact)
        assert contact is not None
        self.assertEqual(contact.email, "info@test.fr")
        self.assertEqual(contact.telephone, "")

    def test_002_extract_club_no_contact(self) -> None:
        org = GetOrganismeResponse(id="3", nom="Empty Club")
        contact = extract_club_info(org)
        self.assertIsNone(contact)

    def test_003_extract_club_phone_only(self) -> None:
        org = GetOrganismeResponse(
            id="4",
            nom="Phone Club",
            telephone="01 23 45 67 89",
        )
        contact = extract_club_info(org)
        self.assertIsNotNone(contact)
        assert contact is not None
        self.assertEqual(contact.telephone, "0123456789")


class Test162ExtractMembresContacts(unittest.TestCase):
    """Tests for extract_membres_contacts."""

    def test_000_extract_membres_with_contacts(self) -> None:
        org = GetOrganismeResponse(
            id="1",
            nom="Club A",
            membres=[
                Membre(
                    id="M1",
                    nom="dupont",
                    prenom="jean",
                    telephone_portable="06 12 34 56 78",
                    mail="jean@example.com",
                    code_fonction=CodeFonctionEnum.PRESIDENT,
                ),
                Membre(
                    id="M2",
                    nom="martin",
                    prenom="paul",
                    telephone_fixe="03 20 00 00 00",
                    code_fonction=CodeFonctionEnum.CORRESPONDANT,
                ),
            ],
        )
        contacts = extract_membres_contacts(org)
        self.assertEqual(len(contacts), 2)
        self.assertEqual(contacts[0].titre, ContactRoleEnum.PRESIDENT)
        self.assertEqual(contacts[0].nom, "Dupont")
        self.assertEqual(contacts[0].prenom, "Jean")
        self.assertEqual(contacts[0].telephone, "0612345678")
        self.assertEqual(contacts[0].email, "jean@example.com")
        self.assertEqual(contacts[0].source, "directus:get_organisme:membre")
        self.assertEqual(contacts[1].titre, ContactRoleEnum.CORRESPONDANT_CLUB)
        self.assertEqual(contacts[1].nom, "Martin")

    def test_001_extract_membres_no_contact_info(self) -> None:
        org = GetOrganismeResponse(
            id="2",
            nom="Club B",
            membres=[Membre(id="M3", nom="test")],
        )
        contacts = extract_membres_contacts(org)
        self.assertEqual(len(contacts), 0)

    def test_002_extract_membres_empty_list(self) -> None:
        org = GetOrganismeResponse(id="3", nom="Club C", membres=[])
        contacts = extract_membres_contacts(org)
        self.assertEqual(len(contacts), 0)

    def test_003_extract_membres_default_titre(self) -> None:
        org = GetOrganismeResponse(
            id="4",
            nom="Club D",
            membres=[
                Membre(
                    id="M4",
                    nom="test",
                    mail="test@test.com",
                ),
            ],
        )
        contacts = extract_membres_contacts(org)
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0].titre, ContactRoleEnum.MEMBRE)

    def test_004_extract_membres_email_only(self) -> None:
        org = GetOrganismeResponse(
            id="5",
            nom="Club E",
            membres=[
                Membre(
                    id="M5",
                    nom="email_only",
                    mail="only@example.com",
                    code_fonction=CodeFonctionEnum.REFERENT_SECURITE,
                ),
            ],
        )
        contacts = extract_membres_contacts(org)
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0].email, "only@example.com")
        self.assertEqual(contacts[0].telephone, "")


class Test162ClubContacts(unittest.TestCase):
    """Tests for ClubContacts dataclass."""

    def test_000_create_club_contacts(self) -> None:
        org = GetOrganismeResponse(id="1", nom="Club")
        cc = ClubContacts(organisme=org, club_contact=None, membres=[])
        self.assertEqual(cc.organisme, org)
        self.assertIsNone(cc.club_contact)
        self.assertEqual(cc.membres, [])

    def test_001_club_contacts_default_membres(self) -> None:
        org = GetOrganismeResponse(id="1")
        cc = ClubContacts(organisme=org, club_contact=None)
        self.assertEqual(cc.membres, [])


if __name__ == "__main__":
    unittest.main()
