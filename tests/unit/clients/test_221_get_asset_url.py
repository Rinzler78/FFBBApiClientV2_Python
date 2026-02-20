"""Unit tests for get_asset_url on ApiFFBBAppClient and facade."""

from __future__ import annotations

import unittest
from unittest.mock import Mock, patch
from uuid import UUID

from requests_cache import CachedSession

from ffbb_api_client_v2.directus_ffbb.client import ApiFFBBAppClient
from ffbb_api_client_v2.facade.client import FFBBAPIClientV2


class TestApiFFBBAppClientGetAssetUrl(unittest.TestCase):
    """Tests for ApiFFBBAppClient.get_asset_url."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v2.directus.client.CacheManager"):
            self.client = ApiFFBBAppClient(
                bearer_token="test-token",
                cached_session=Mock(spec=CachedSession),
            )

    def test_get_asset_url_with_uuid(self) -> None:
        uid = UUID("12345678-1234-5678-1234-567812345678")
        url = self.client.get_asset_url(uid)
        self.assertEqual(
            url, "https://api.ffbb.app/assets/12345678-1234-5678-1234-567812345678"
        )

    def test_get_asset_url_with_string(self) -> None:
        url = self.client.get_asset_url("abc-def-123")
        self.assertEqual(url, "https://api.ffbb.app/assets/abc-def-123")


class TestFacadeGetAssetUrl(unittest.TestCase):
    """Tests for FFBBAPIClientV2.get_asset_url (facade delegation)."""

    def setUp(self) -> None:
        self.mock_api = Mock(spec=ApiFFBBAppClient)
        self.mock_meili = Mock()
        self.facade = FFBBAPIClientV2(self.mock_api, self.mock_meili)

    def test_facade_delegates_to_api_client(self) -> None:
        uid = UUID("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")
        self.mock_api.get_asset_url.return_value = (
            "https://api.ffbb.app/assets/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        )
        url = self.facade.get_asset_url(uid)
        self.mock_api.get_asset_url.assert_called_once_with(uid)
        self.assertEqual(
            url, "https://api.ffbb.app/assets/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        )


if __name__ == "__main__":
    unittest.main()
