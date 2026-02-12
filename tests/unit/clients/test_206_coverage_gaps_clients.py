"""Coverage gap tests for client modules.

Extracted from test_122_coverage_gaps.py:
- FFBBAPIClientV2 search_multiple_* and delegation tests
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock


class TestFFBBAPIClientV2Coverage(unittest.TestCase):
    """ffbb_api_client_v2.py -- cover search_multiple_* with None names."""

    def test_000_search_multiple_with_none_names_returns_none(self) -> None:
        from ffbb_api_client_v2.clients.ffbb_api_client_v2 import FFBBAPIClientV2

        api_client = MagicMock()
        meili_client = MagicMock()
        client = FFBBAPIClientV2(api_client, meili_client)

        self.assertIsNone(client.search_multiple_competitions(None))
        self.assertIsNone(client.search_multiple_organismes(None))
        self.assertIsNone(client.search_multiple_pratiques(None))
        self.assertIsNone(client.search_multiple_rencontres(None))
        self.assertIsNone(client.search_multiple_salles(None))
        self.assertIsNone(client.search_multiple_terrains(None))
        self.assertIsNone(client.search_multiple_tournois(None))

    def test_001_search_multiple_with_empty_list_returns_none(self) -> None:
        from ffbb_api_client_v2.clients.ffbb_api_client_v2 import FFBBAPIClientV2

        api_client = MagicMock()
        meili_client = MagicMock()
        client = FFBBAPIClientV2(api_client, meili_client)

        self.assertIsNone(client.search_multiple_competitions([]))
        self.assertIsNone(client.search_multiple_organismes([]))

    def test_002_get_competition_delegates(self) -> None:
        from ffbb_api_client_v2.clients.ffbb_api_client_v2 import FFBBAPIClientV2

        api_client = MagicMock()
        api_client.get_competition.return_value = "result"
        meili_client = MagicMock()
        client = FFBBAPIClientV2(api_client, meili_client)

        result = client.get_competition(competition_id=123)
        self.assertEqual(result, "result")
        api_client.get_competition.assert_called_once()

    def test_003_get_organisme_delegates(self) -> None:
        from ffbb_api_client_v2.clients.ffbb_api_client_v2 import FFBBAPIClientV2

        api_client = MagicMock()
        api_client.get_organisme.return_value = "org_result"
        meili_client = MagicMock()
        client = FFBBAPIClientV2(api_client, meili_client)

        result = client.get_organisme(organisme_id=456)
        self.assertEqual(result, "org_result")

    def test_004_get_poule_delegates(self) -> None:
        from ffbb_api_client_v2.clients.ffbb_api_client_v2 import FFBBAPIClientV2

        api_client = MagicMock()
        api_client.get_poule.return_value = "poule_result"
        meili_client = MagicMock()
        client = FFBBAPIClientV2(api_client, meili_client)

        result = client.get_poule(poule_id=789)
        self.assertEqual(result, "poule_result")


if __name__ == "__main__":
    unittest.main()
