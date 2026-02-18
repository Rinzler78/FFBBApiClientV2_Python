"""Integration tests for DirectusClient with real FFBB Directus API.

Tests use the real Directus API at https://api.ffbb.app/ to validate
_get_json, _get_item, _list_items, _fetch_all_pages on data endpoints,
and error enrichment on restricted schema endpoints.

Note: FFBB Directus collections use the 'ffbbserver_' prefix
(e.g. items/ffbbserver_saisons, items/ffbbserver_competitions).
"""

from __future__ import annotations

import os
import time
import unittest

from ffbb_api_client_v2.directus.client import DirectusClient
from ffbb_api_client_v2.directus.exceptions import DirectusAuthError


class Test001DirectusClientIntegration(unittest.TestCase):
    """Integration tests for DirectusClient against the real FFBB Directus API."""

    @classmethod
    def setUpClass(cls) -> None:
        api_token = os.getenv("API_FFBB_APP_BEARER_TOKEN")
        if not api_token:
            raise Exception("API_FFBB_APP_BEARER_TOKEN environment variable not set")
        cls.client = DirectusClient(
            bearer_token=api_token,
            url="https://api.ffbb.app/",
            debug=False,
        )

    def setUp(self) -> None:
        time.sleep(0.5)

    def test_001_get_json_success(self) -> None:
        """_get_json returns a dict with 'data' key for a valid endpoint."""
        result = self.client._get_json(
            "https://api.ffbb.app/items/ffbbserver_saisons?limit=1"
        )
        self.assertIsInstance(result, dict)
        self.assertIn("data", result)

    def test_002_get_item_real(self) -> None:
        """_get_item retrieves a single item by ID."""
        # First, get a valid saison ID via _list_items
        items = self.client._list_items(
            "items/ffbbserver_saisons", fields=["id"], limit=1
        )
        self.assertGreater(len(items), 0, "Need at least one saison to test _get_item")
        saison_id = items[0]["id"]

        result = self.client._get_item(
            f"items/ffbbserver_saisons/{saison_id}",
            fields=["id", "libelle"],
        )
        self.assertIsNotNone(result)
        assert result is not None  # narrow type for subsequent assertions
        self.assertIsInstance(result, dict)
        self.assertIn("id", result)
        self.assertEqual(result["id"], saison_id)

    def test_003_list_items_real(self) -> None:
        """_list_items retrieves a bounded list of items."""
        result = self.client._list_items("items/ffbbserver_saisons", limit=3)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertLessEqual(len(result), 3)

    def test_004_list_items_with_fields_and_offset(self) -> None:
        """_list_items respects fields and offset parameters."""
        result = self.client._list_items(
            "items/ffbbserver_saisons",
            fields=["id", "libelle"],
            limit=2,
            offset=1,
        )
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 2)
        if result:
            self.assertIn("id", result[0])

    def test_005_fetch_all_pages_real(self) -> None:
        """_fetch_all_pages paginates through saisons collection."""
        result = self.client._fetch_all_pages(
            "items/ffbbserver_saisons",
            fields=["id", "libelle"],
            from_list_fn=lambda items: items,
            page_size=5,
            max_items=20,
        )
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_006_get_collections_raises_auth_error(self) -> None:
        """get_collections raises DirectusAuthError on restricted schema endpoint."""
        with self.assertRaises(DirectusAuthError):
            self.client.get_collections()

    def test_007_get_fields_raises_auth_error(self) -> None:
        """get_fields raises DirectusAuthError on restricted schema endpoint."""
        with self.assertRaises(DirectusAuthError):
            self.client.get_fields()


if __name__ == "__main__":
    unittest.main()
