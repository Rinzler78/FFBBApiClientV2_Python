"""Tests for facade contact methods (get_engagement_contacts, get_club_contacts)."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from ffbb_api_client_v2.directus_ffbb.models.get_engagements_response import (
    GetEngagementsResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_entraineurs_response import (
    GetEntraineursResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_organisme_response import (
    GetOrganismeResponse,
)
from ffbb_api_client_v2.facade.client import FFBBAPIClientV2
from ffbb_api_client_v2.models.code_fonction import CodeFonction
from ffbb_api_client_v2.models.contact_role import ContactRole
from ffbb_api_client_v2.models.membre import Membre


def _make_client() -> FFBBAPIClientV2:
    api = MagicMock()
    ms = MagicMock()
    return FFBBAPIClientV2(api, ms)


class Test214GetEngagementContacts(unittest.TestCase):
    """Tests for FFBBAPIClientV2.get_engagement_contacts."""

    def test_000_returns_none_when_engagement_not_found(self) -> None:
        client = _make_client()
        client.api_ffbb_client.get_engagement.return_value = None

        result = client.get_engagement_contacts(999)
        self.assertIsNone(result)

    def test_001_returns_correspondant_contact(self) -> None:
        client = _make_client()
        eng = GetEngagementsResponse(
            id="100",
            telephonePortableCorrespondantEquipe="0612345678",
            nomCorrespondantEquipe="Dupont",
            emailCorrespondantEquipe="dupont@test.com",
        )
        client.api_ffbb_client.get_engagement.return_value = eng

        result = client.get_engagement_contacts(100)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.engagement, eng)
        self.assertIsNotNone(result.correspondant)
        assert result.correspondant is not None
        self.assertEqual(result.correspondant.nom, "Dupont")
        self.assertEqual(result.correspondant.email, "dupont@test.com")
        self.assertIsNone(result.entraineur)
        self.assertIsNone(result.entraineur_adjoint)

    def test_002_returns_entraineur_contact(self) -> None:
        client = _make_client()
        eng = GetEngagementsResponse(id="101", entraineur=42)
        ent = GetEntraineursResponse(
            idLicence="LIC42",
            nom="Coach",
            prenom="Pierre",
            telephonePortable="0698765432",
            email="coach@test.com",
        )
        client.api_ffbb_client.get_engagement.return_value = eng
        client.api_ffbb_client.get_entraineur.return_value = ent

        result = client.get_engagement_contacts(101)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertIsNotNone(result.entraineur)
        assert result.entraineur is not None
        self.assertEqual(result.entraineur.titre, ContactRole.ENTRAINEUR)
        self.assertEqual(result.entraineur.nom, "Coach")

    def test_003_returns_entraineur_adjoint_contact(self) -> None:
        client = _make_client()
        eng = GetEngagementsResponse(id="102", entraineurAdjoint=43)
        adj = GetEntraineursResponse(
            idLicence="LIC43",
            nom="Adjoint",
            prenom="Marie",
            email="adjoint@test.com",
        )
        client.api_ffbb_client.get_engagement.return_value = eng
        client.api_ffbb_client.get_entraineur.return_value = adj

        result = client.get_engagement_contacts(102)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertIsNotNone(result.entraineur_adjoint)
        assert result.entraineur_adjoint is not None
        self.assertEqual(
            result.entraineur_adjoint.titre, ContactRole.ENTRAINEUR_ADJOINT
        )

    def test_004_all_contacts_populated(self) -> None:
        client = _make_client()
        eng = GetEngagementsResponse(
            id="103",
            telephonePortableCorrespondantEquipe="0600000000",
            nomCorrespondantEquipe="Corresp",
            entraineur=10,
            entraineurAdjoint=11,
        )
        ent1 = GetEntraineursResponse(
            idLicence="L10",
            nom="Coach1",
            telephonePortable="0610000000",
        )
        ent2 = GetEntraineursResponse(
            idLicence="L11",
            nom="Coach2",
            telephonePortable="0620000000",
        )
        client.api_ffbb_client.get_engagement.return_value = eng
        client.api_ffbb_client.get_entraineur.side_effect = [ent1, ent2]

        result = client.get_engagement_contacts(103)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertIsNotNone(result.correspondant)
        self.assertIsNotNone(result.entraineur)
        self.assertIsNotNone(result.entraineur_adjoint)

    def test_005_no_entraineur_when_id_is_none(self) -> None:
        client = _make_client()
        eng = GetEngagementsResponse(id="104", entraineur=None)
        client.api_ffbb_client.get_engagement.return_value = eng

        result = client.get_engagement_contacts(104)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertIsNone(result.entraineur)
        client.api_ffbb_client.get_entraineur.assert_not_called()


class Test214GetClubContacts(unittest.TestCase):
    """Tests for FFBBAPIClientV2.get_club_contacts."""

    def test_000_returns_none_when_organisme_not_found(self) -> None:
        client = _make_client()
        client.api_ffbb_client.get_organisme.return_value = None

        result = client.get_club_contacts(999)
        self.assertIsNone(result)

    def test_001_returns_club_contact(self) -> None:
        client = _make_client()
        org = GetOrganismeResponse(
            id="200",
            nom="BC Lille",
            telephone="0320123456",
            mail="contact@bclille.fr",
        )
        client.api_ffbb_client.get_organisme.return_value = org

        result = client.get_club_contacts(200)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.organisme, org)
        self.assertIsNotNone(result.club_contact)
        assert result.club_contact is not None
        self.assertEqual(result.club_contact.titre, ContactRole.CLUB)
        self.assertEqual(result.club_contact.email, "contact@bclille.fr")
        self.assertEqual(result.membres, [])

    def test_002_returns_membres_contacts(self) -> None:
        client = _make_client()
        org = GetOrganismeResponse(
            id="201",
            nom="Club B",
            membres=[
                Membre(
                    id="M1",
                    nom="president",
                    prenom="jean",
                    telephone_portable="0612345678",
                    mail="pres@club.fr",
                    code_fonction=CodeFonction.PRESIDENT,
                ),
            ],
        )
        client.api_ffbb_client.get_organisme.return_value = org

        result = client.get_club_contacts(201)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(len(result.membres), 1)
        self.assertEqual(result.membres[0].titre, ContactRole.PRESIDENT)
        self.assertEqual(result.membres[0].nom, "President")

    def test_003_no_club_contact_when_no_info(self) -> None:
        client = _make_client()
        org = GetOrganismeResponse(id="202", nom="Club C")
        client.api_ffbb_client.get_organisme.return_value = org

        result = client.get_club_contacts(202)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertIsNone(result.club_contact)
        self.assertEqual(result.membres, [])

    def test_004_club_with_all_contacts(self) -> None:
        client = _make_client()
        org = GetOrganismeResponse(
            id="203",
            nom="Club D",
            telephone="0100000000",
            mail="info@clubd.fr",
            membres=[
                Membre(
                    id="M1",
                    nom="a",
                    mail="a@test.com",
                    code_fonction=CodeFonction.PRESIDENT,
                ),
                Membre(
                    id="M2",
                    nom="b",
                    mail="b@test.com",
                    code_fonction=CodeFonction.CORRESPONDANT,
                ),
            ],
        )
        client.api_ffbb_client.get_organisme.return_value = org

        result = client.get_club_contacts(203)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertIsNotNone(result.club_contact)
        self.assertEqual(len(result.membres), 2)


if __name__ == "__main__":
    unittest.main()
