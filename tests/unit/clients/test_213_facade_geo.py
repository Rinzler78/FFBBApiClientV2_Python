"""Tests for facade geo-search proxy methods."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from ffbb_api_client_v2.facade.client import FFBBAPIClientV2
from ffbb_api_client_v2.meilisearch_ffbb.geo_sort_order import GeoSortOrder
from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_engagements import (
    EngagementsMultiSearchResult,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_organismes import (
    OrganismesMultiSearchResult,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_salles import (
    SallesMultiSearchResult,
)


def _make_client() -> FFBBAPIClientV2:
    api = MagicMock()
    ms = MagicMock()
    return FFBBAPIClientV2(api, ms)


class Test213FacadeGeoOrganismes(unittest.TestCase):
    """Tests for facade search_organismes_by_geo proxy."""

    def test_000_delegates_to_meilisearch_client(self) -> None:
        client = _make_client()
        mock_result = MagicMock(spec=OrganismesMultiSearchResult)
        client.meilisearch_ffbb_client.search_organismes_by_geo.return_value = (
            mock_result
        )

        result = client.search_organismes_by_geo(lat=48.8, lng=2.3, radius_km=10)

        client.meilisearch_ffbb_client.search_organismes_by_geo.assert_called_once_with(
            48.8, 2.3, 10, "", 20, GeoSortOrder.NEAREST_FIRST, None
        )
        self.assertEqual(result, mock_result)

    def test_001_passes_all_params(self) -> None:
        client = _make_client()
        client.meilisearch_ffbb_client.search_organismes_by_geo.return_value = None

        result = client.search_organismes_by_geo(
            lat=1.0,
            lng=2.0,
            radius_km=50.0,
            q="test",
            limit=100,
            geo_sort=GeoSortOrder.FARTHEST_FIRST,
        )

        client.meilisearch_ffbb_client.search_organismes_by_geo.assert_called_once_with(
            1.0, 2.0, 50.0, "test", 100, GeoSortOrder.FARTHEST_FIRST, None
        )
        self.assertIsNone(result)


class Test213FacadeGeoSalles(unittest.TestCase):
    """Tests for facade search_salles_by_geo proxy."""

    def test_000_delegates_to_meilisearch_client(self) -> None:
        client = _make_client()
        mock_result = MagicMock(spec=SallesMultiSearchResult)
        client.meilisearch_ffbb_client.search_salles_by_geo.return_value = mock_result

        result = client.search_salles_by_geo(lat=43.3, lng=5.4)

        client.meilisearch_ffbb_client.search_salles_by_geo.assert_called_once()
        self.assertEqual(result, mock_result)


class Test213FacadeGeoEngagements(unittest.TestCase):
    """Tests for facade search_engagements_by_geo proxy."""

    def test_000_delegates_to_meilisearch_client(self) -> None:
        client = _make_client()
        mock_result = MagicMock(spec=EngagementsMultiSearchResult)
        client.meilisearch_ffbb_client.search_engagements_by_geo.return_value = (
            mock_result
        )

        result = client.search_engagements_by_geo(
            lat=50.6, lng=3.1, radius_km=100, limit=500
        )

        client.meilisearch_ffbb_client.search_engagements_by_geo.assert_called_once_with(
            50.6, 3.1, 100, "", 500, GeoSortOrder.NEAREST_FIRST, None
        )
        self.assertEqual(result, mock_result)

    def test_001_returns_none_when_no_results(self) -> None:
        client = _make_client()
        client.meilisearch_ffbb_client.search_engagements_by_geo.return_value = None

        result = client.search_engagements_by_geo(lat=0, lng=0)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
