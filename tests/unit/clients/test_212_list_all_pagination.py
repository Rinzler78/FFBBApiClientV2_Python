"""Unit tests for automatic pagination via list_all_xxx() methods."""

import unittest
from unittest.mock import Mock, patch

from requests_cache import CachedSession

from ffbb_api_client_v2.directus_ffbb.client import ApiFFBBAppClient


class Test212ListAllPaginationRencontres(unittest.TestCase):
    """Tests for list_all_rencontres pagination."""

    def setUp(self):
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_008_single_page(self, mock_http):
        """Test single page when total < page_size."""
        mock_http.return_value = {
            "data": [{"id": "1"}, {"id": "2"}],
            "meta": {"total_count": 2, "filter_count": 2},
        }
        result = self.client.list_all_rencontres(page_size=100)
        self.assertEqual(len(result), 2)
        self.assertEqual(mock_http.call_count, 1)

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_006_multi_page(self, mock_http):
        """Test multi-page pagination with meta total_count."""
        page1 = [{"id": str(i)} for i in range(100)]
        page2 = [{"id": str(i)} for i in range(100, 200)]
        page3 = [{"id": str(i)} for i in range(200, 250)]

        mock_http.side_effect = [
            {"data": page1, "meta": {"total_count": 250, "filter_count": 250}},
            {"data": page2, "meta": {"total_count": 250, "filter_count": 250}},
            {"data": page3, "meta": {"total_count": 250, "filter_count": 250}},
        ]
        result = self.client.list_all_rencontres(page_size=100)
        self.assertEqual(len(result), 250)
        self.assertEqual(mock_http.call_count, 3)

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_002_max_items_guard(self, mock_http):
        """Test max_items stops pagination."""
        page1 = [{"id": str(i)} for i in range(100)]

        mock_http.return_value = {
            "data": page1,
            "meta": {"total_count": 10000, "filter_count": 10000},
        }
        result = self.client.list_all_rencontres(page_size=100, max_items=50)
        # First page returns 100 items, which exceeds max_items=50
        self.assertEqual(len(result), 100)
        self.assertEqual(mock_http.call_count, 1)

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_003_empty_response(self, mock_http):
        """Test empty data returns empty list."""
        mock_http.return_value = {"data": [], "meta": {"total_count": 0}}
        result = self.client.list_all_rencontres()
        self.assertEqual(result, [])

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_004_with_filter_and_sort(self, mock_http):
        """Test filter and sort params are passed."""
        mock_http.return_value = {
            "data": [{"id": "1"}],
            "meta": {"total_count": 1, "filter_count": 1},
        }
        self.client.list_all_rencontres(
            filter_criteria='{"actif":{"_eq":true}}',
            sort=["date_rencontre"],
        )
        url = mock_http.call_args[0][0]
        self.assertIn("filter=", url)
        self.assertIn("sort%5B%5D=", url)
        self.assertIn("meta=", url)


class Test212ListAllPaginationSalles(unittest.TestCase):
    """Tests for list_all_salles pagination."""

    def setUp(self):
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_008_single_page(self, mock_http):
        """Test single page when total < page_size."""
        mock_http.return_value = {
            "data": [{"id": "1", "libelle": "Salle A"}],
            "meta": {"total_count": 1, "filter_count": 1},
        }
        result = self.client.list_all_salles(page_size=100)
        self.assertEqual(len(result), 1)
        self.assertEqual(mock_http.call_count, 1)

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_006_multi_page(self, mock_http):
        """Test multi-page pagination."""
        page1 = [{"id": str(i), "libelle": f"Salle {i}"} for i in range(50)]
        page2 = [{"id": str(i), "libelle": f"Salle {i}"} for i in range(50, 80)]

        mock_http.side_effect = [
            {"data": page1, "meta": {"total_count": 80, "filter_count": 80}},
            {"data": page2, "meta": {"total_count": 80, "filter_count": 80}},
        ]
        result = self.client.list_all_salles(page_size=50)
        self.assertEqual(len(result), 80)
        self.assertEqual(mock_http.call_count, 2)

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_007_none_response(self, mock_http):
        """Test None response breaks pagination."""
        mock_http.return_value = None
        result = self.client.list_all_salles()
        self.assertEqual(result, [])


class Test212ListAllPaginationCommunes(unittest.TestCase):
    """Tests for list_all_communes pagination."""

    def setUp(self):
        self.client = ApiFFBBAppClient(
            bearer_token="test_token_for_unit_tests",
            cached_session=Mock(spec=CachedSession),
        )

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_008_single_page(self, mock_http):
        """Test single page."""
        mock_http.return_value = {
            "data": [{"id": "1", "codeInsee": "75056", "libelle": "Paris"}],
            "meta": {"total_count": 1, "filter_count": 1},
        }
        result = self.client.list_all_communes(page_size=100)
        self.assertEqual(len(result), 1)

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_009_with_search(self, mock_http):
        """Test search param is passed."""
        mock_http.return_value = {
            "data": [{"id": "1", "codeInsee": "75056", "libelle": "Paris"}],
            "meta": {"total_count": 1, "filter_count": 1},
        }
        self.client.list_all_communes(search="paris")
        url = mock_http.call_args[0][0]
        self.assertIn("search=", url)

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_010_partial_last_page(self, mock_http):
        """Test stops when last page is smaller than page_size."""
        page1 = [{"id": str(i)} for i in range(10)]
        page2 = [{"id": str(i)} for i in range(10, 15)]

        mock_http.side_effect = [
            {"data": page1, "meta": {"total_count": 15, "filter_count": 15}},
            {"data": page2, "meta": {"total_count": 15, "filter_count": 15}},
        ]
        result = self.client.list_all_communes(page_size=10)
        self.assertEqual(len(result), 15)
        self.assertEqual(mock_http.call_count, 2)

    @patch("ffbb_api_client_v2._http.client.HttpClient.http_get_json")
    def test_011_no_meta_stops_after_short_page(self, mock_http):
        """Test stops when no meta and page is short."""
        mock_http.return_value = {
            "data": [{"id": "1"}],
            "meta": {},
        }
        result = self.client.list_all_communes(page_size=100)
        self.assertEqual(len(result), 1)
        self.assertEqual(mock_http.call_count, 1)


if __name__ == "__main__":
    unittest.main()
