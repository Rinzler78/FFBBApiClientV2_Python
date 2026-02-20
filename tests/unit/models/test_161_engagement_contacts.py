"""Tests for EngagementContacts and helper functions."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.directus_ffbb.models.get_engagements_response import (
    GetEngagementsResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_entraineurs_response import (
    GetEntraineursResponse,
)
from ffbb_api_client_v2.models.contact_role import ContactRole
from ffbb_api_client_v2.models.engagement_contacts import (
    EngagementContacts,
    extract_correspondant,
    extract_entraineur_contact,
)


class Test161ExtractCorrespondant(unittest.TestCase):
    """Tests for extract_correspondant."""

    def test_000_extract_correspondant_with_phone(self) -> None:
        eng = GetEngagementsResponse(
            id="1",
            telephonePortableCorrespondantEquipe="06 12 34 56 78",
            nomCorrespondantEquipe="dupont",
            emailCorrespondantEquipe="dupont@example.com",
        )
        contact = extract_correspondant(eng)
        self.assertIsNotNone(contact)
        assert contact is not None
        self.assertEqual(contact.titre, ContactRole.CORRESPONDANT_EQUIPE)
        self.assertEqual(contact.nom, "Dupont")
        self.assertEqual(contact.telephone, "0612345678")
        self.assertEqual(contact.email, "dupont@example.com")
        self.assertEqual(contact.source, "directus:get_engagement")

    def test_001_extract_correspondant_with_email_only(self) -> None:
        eng = GetEngagementsResponse(
            id="2",
            emailCorrespondantEquipe="test@example.com",
        )
        contact = extract_correspondant(eng)
        self.assertIsNotNone(contact)
        assert contact is not None
        self.assertEqual(contact.email, "test@example.com")
        self.assertEqual(contact.telephone, "")

    def test_002_extract_correspondant_no_contact(self) -> None:
        eng = GetEngagementsResponse(id="3")
        contact = extract_correspondant(eng)
        self.assertIsNone(contact)

    def test_003_extract_correspondant_fixe_phone(self) -> None:
        eng = GetEngagementsResponse(
            id="4",
            telephoneFixeCorrespondantEquipe="03 20 12 34 56",
            nomCorrespondantEquipe="martin",
        )
        contact = extract_correspondant(eng)
        self.assertIsNotNone(contact)
        assert contact is not None
        self.assertEqual(contact.telephone, "0320123456")

    def test_004_extract_correspondant_travail_phone(self) -> None:
        eng = GetEngagementsResponse(
            id="5",
            telephoneTravailCorrespondantEquipe="01 23 45 67 89",
        )
        contact = extract_correspondant(eng)
        self.assertIsNotNone(contact)
        assert contact is not None
        self.assertEqual(contact.telephone, "0123456789")

    def test_005_extract_correspondant_name_sanitized(self) -> None:
        eng = GetEngagementsResponse(
            id="6",
            telephonePortableCorrespondantEquipe="0600000000",
            nomCorrespondantEquipe="  JEAN-PIERRE  ",
        )
        contact = extract_correspondant(eng)
        self.assertIsNotNone(contact)
        assert contact is not None
        self.assertEqual(contact.nom, "Jean-Pierre")


class Test161ExtractEntraineurContact(unittest.TestCase):
    """Tests for extract_entraineur_contact."""

    def test_000_extract_entraineur_with_phone(self) -> None:
        ent = GetEntraineursResponse(
            idLicence="LIC001",
            nom="martin",
            prenom="paul",
            telephonePortable="06 98 76 54 32",
            email="paul@example.com",
        )
        contact = extract_entraineur_contact(ent, ContactRole.ENTRAINEUR)
        self.assertIsNotNone(contact)
        assert contact is not None
        self.assertEqual(contact.titre, ContactRole.ENTRAINEUR)
        self.assertEqual(contact.nom, "Martin")
        self.assertEqual(contact.prenom, "Paul")
        self.assertEqual(contact.telephone, "0698765432")
        self.assertEqual(contact.email, "paul@example.com")

    def test_001_extract_entraineur_none(self) -> None:
        contact = extract_entraineur_contact(None, ContactRole.ENTRAINEUR)
        self.assertIsNone(contact)

    def test_002_extract_entraineur_no_contact(self) -> None:
        ent = GetEntraineursResponse(idLicence="LIC002", nom="Test")
        contact = extract_entraineur_contact(ent, ContactRole.ENTRAINEUR_ADJOINT)
        self.assertIsNone(contact)

    def test_003_extract_entraineur_domicile_phone(self) -> None:
        ent = GetEntraineursResponse(
            idLicence="LIC003",
            telephoneDomicile="03 20 00 00 00",
        )
        contact = extract_entraineur_contact(ent, ContactRole.ENTRAINEUR)
        self.assertIsNotNone(contact)
        assert contact is not None
        self.assertEqual(contact.telephone, "0320000000")

    def test_004_extract_entraineur_travail_phone(self) -> None:
        ent = GetEntraineursResponse(
            idLicence="LIC004",
            telephoneTravail="01 00 00 00 00",
        )
        contact = extract_entraineur_contact(ent, ContactRole.ENTRAINEUR)
        self.assertIsNotNone(contact)
        assert contact is not None
        self.assertEqual(contact.telephone, "0100000000")

    def test_005_extract_entraineur_email_only(self) -> None:
        ent = GetEntraineursResponse(
            idLicence="LIC005",
            email="coach@example.com",
        )
        contact = extract_entraineur_contact(ent, ContactRole.ENTRAINEUR)
        self.assertIsNotNone(contact)
        assert contact is not None
        self.assertEqual(contact.email, "coach@example.com")
        self.assertEqual(contact.telephone, "")


class Test161EngagementContacts(unittest.TestCase):
    """Tests for EngagementContacts dataclass."""

    def test_000_create_engagement_contacts(self) -> None:
        eng = GetEngagementsResponse(id="1")
        ec = EngagementContacts(
            engagement=eng,
            correspondant=None,
            entraineur=None,
            entraineur_adjoint=None,
        )
        self.assertEqual(ec.engagement, eng)
        self.assertIsNone(ec.correspondant)
        self.assertIsNone(ec.entraineur)
        self.assertIsNone(ec.entraineur_adjoint)


if __name__ == "__main__":
    unittest.main()
