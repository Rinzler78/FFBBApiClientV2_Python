"""Tests for new fields in Directus response models."""

from __future__ import annotations

import unittest
from datetime import datetime
from uuid import UUID

from ffbb_api_client_v2.directus_ffbb.models.get_competition_response import (
    GetCompetitionResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_configuration_response import (
    GetConfigurationResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_organisme_response import (
    GetOrganismeResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_rencontres_response import (
    GetRencontresResponse,
)


class TestGetCompetitionResponseNewFields(unittest.TestCase):
    """Test date_created and date_updated fields."""

    def test_from_dict_with_dates(self) -> None:
        data = {
            "id": "comp-1",
            "nom": "Championnat",
            "date_created": "2025-07-31T07:34:57.704Z",
            "date_updated": "2026-02-20T11:21:17.517Z",
        }
        resp = GetCompetitionResponse.from_dict(data)
        self.assertIsNotNone(resp)
        assert resp is not None
        self.assertIsInstance(resp.date_created, datetime)
        self.assertIsInstance(resp.date_updated, datetime)

    def test_from_dict_without_dates(self) -> None:
        data = {"id": "comp-1", "nom": "Test"}
        resp = GetCompetitionResponse.from_dict(data)
        self.assertIsNotNone(resp)
        assert resp is not None
        self.assertIsNone(resp.date_created)
        self.assertIsNone(resp.date_updated)


class TestGetConfigurationResponseNewFields(unittest.TestCase):
    """Test user_created and user_updated UUID fields."""

    def test_from_dict_with_user_fields(self) -> None:
        data = {
            "id": 1,
            "key_dh": "token1",
            "key_ms": "token2",
            "user_created": "ec250a4a-e5dd-480e-87b8-e2ecbbd13da5",
            "user_updated": None,
        }
        resp = GetConfigurationResponse.from_dict(data)
        self.assertEqual(
            resp.user_created, UUID("ec250a4a-e5dd-480e-87b8-e2ecbbd13da5")
        )
        self.assertIsNone(resp.user_updated)

    def test_from_dict_without_user_fields(self) -> None:
        data = {"id": 1, "key_dh": "t1", "key_ms": "t2"}
        resp = GetConfigurationResponse.from_dict(data)
        self.assertIsNone(resp.user_created)
        self.assertIsNone(resp.user_updated)


class TestGetRencontresResponseNewFields(unittest.TestCase):
    """Test gsId field."""

    def test_from_dict_with_gs_id(self) -> None:
        data = {"id": "r-1", "gsId": "gs-12345"}
        resp = GetRencontresResponse.from_dict(data)
        self.assertIsNotNone(resp)
        assert resp is not None
        self.assertEqual(resp.gsId, "gs-12345")

    def test_from_dict_with_null_gs_id(self) -> None:
        data = {"id": "r-1", "gsId": None}
        resp = GetRencontresResponse.from_dict(data)
        self.assertIsNotNone(resp)
        assert resp is not None
        self.assertIsNone(resp.gsId)

    def test_from_dict_without_gs_id(self) -> None:
        data = {"id": "r-1"}
        resp = GetRencontresResponse.from_dict(data)
        self.assertIsNotNone(resp)
        assert resp is not None
        self.assertIsNone(resp.gsId)


class TestGetOrganismeResponseNewFields(unittest.TestCase):
    """Test 8 new fields in GetOrganismeResponse."""

    FULL_DATA: dict = {
        "id": "org-1",
        "nom": "Club Test",
        "dateAffiliation": None,
        "entreprise": False,
        "handibasket": False,
        "horsAssociation": False,
        "logo_base64": "c4b146f5-141f-40a5-a01a-e218a9808e69",
        "omnisport": False,
        "saison_en_cours": True,
        "url_competition": "/ligues/cvl/comites/0045/clubs/cvl0045063",
    }

    def test_from_dict_with_all_new_fields(self) -> None:
        resp = GetOrganismeResponse.from_dict(self.FULL_DATA)
        self.assertIsNotNone(resp)
        assert resp is not None
        self.assertIsNone(resp.date_affiliation)
        self.assertIs(resp.entreprise, False)
        self.assertIs(resp.handibasket, False)
        self.assertIs(resp.hors_association, False)
        self.assertEqual(resp.logo_base64, UUID("c4b146f5-141f-40a5-a01a-e218a9808e69"))
        self.assertIs(resp.omnisport, False)
        self.assertIs(resp.saison_en_cours, True)
        self.assertEqual(
            resp.url_competition, "/ligues/cvl/comites/0045/clubs/cvl0045063"
        )

    def test_from_dict_without_new_fields(self) -> None:
        data = {"id": "org-1", "nom": "Test"}
        resp = GetOrganismeResponse.from_dict(data)
        self.assertIsNotNone(resp)
        assert resp is not None
        self.assertIsNone(resp.date_affiliation)
        self.assertIsNone(resp.entreprise)
        self.assertIsNone(resp.handibasket)
        self.assertIsNone(resp.hors_association)
        self.assertIsNone(resp.logo_base64)
        self.assertIsNone(resp.omnisport)
        self.assertIsNone(resp.saison_en_cours)
        self.assertIsNone(resp.url_competition)


if __name__ == "__main__":
    unittest.main()
