"""Unit tests for facade batch helpers and search delegation methods."""

from __future__ import annotations

import json
import unittest
from unittest.mock import Mock

from ffbb_api_client_v2.directus_ffbb.client import ApiFFBBAppClient
from ffbb_api_client_v2.directus_ffbb.models.get_engagements_response import (
    GetEngagementsResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_entraineurs_response import (
    GetEntraineursResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_rencontres_response import (
    GetRencontresResponse,
)
from ffbb_api_client_v2.facade.client import FFBBAPIClientV2
from ffbb_api_client_v2.meilisearch.models.meilisearch_index_settings import (
    MeilisearchIndexSettings,
)
from ffbb_api_client_v2.meilisearch.models.multi_search_results import (
    MultiSearchResult,
)
from ffbb_api_client_v2.meilisearch_ffbb.client import MeilisearchFFBBClient
from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_engagements import (
    EngagementsMultiSearchResult,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_formations import (
    FormationsMultiSearchResult,
)


class _FacadeTestBase(unittest.TestCase):
    """Shared setUp for facade delegation tests."""

    def setUp(self) -> None:
        self.mock_api = Mock(spec=ApiFFBBAppClient)
        self.mock_meili = Mock(spec=MeilisearchFFBBClient)
        self.facade = FFBBAPIClientV2(self.mock_api, self.mock_meili)


# ── search_multiple_engagements ──────────────────────────────────────


class TestSearchMultipleEngagements(_FacadeTestBase):
    def test_returns_none_when_names_is_none(self) -> None:
        result = self.facade.search_multiple_engagements(names=None)
        self.assertIsNone(result)

    def test_returns_none_when_names_is_empty(self) -> None:
        result = self.facade.search_multiple_engagements(names=[])
        self.assertIsNone(result)

    def test_delegates_to_recursive_smart_multi_search(self) -> None:
        mock_result = Mock(spec=MultiSearchResult)
        mock_inner = Mock(spec=EngagementsMultiSearchResult)
        mock_result.results = [mock_inner]
        self.mock_meili.recursive_smart_multi_search.return_value = mock_result

        result = self.facade.search_multiple_engagements(names=["Paris"])
        assert result is not None
        self.assertEqual(len(result), 1)
        self.mock_meili.recursive_smart_multi_search.assert_called_once()

    def test_returns_none_when_multi_search_returns_none(self) -> None:
        self.mock_meili.recursive_smart_multi_search.return_value = None
        result = self.facade.search_multiple_engagements(names=["Paris"])
        self.assertIsNone(result)


# ── search_multiple_formations ───────────────────────────────────────


class TestSearchMultipleFormations(_FacadeTestBase):
    def test_returns_none_when_names_is_none(self) -> None:
        result = self.facade.search_multiple_formations(names=None)
        self.assertIsNone(result)

    def test_returns_none_when_names_is_empty(self) -> None:
        result = self.facade.search_multiple_formations(names=[])
        self.assertIsNone(result)

    def test_delegates_to_recursive_smart_multi_search(self) -> None:
        mock_result = Mock(spec=MultiSearchResult)
        mock_inner = Mock(spec=FormationsMultiSearchResult)
        mock_result.results = [mock_inner]
        self.mock_meili.recursive_smart_multi_search.return_value = mock_result

        result = self.facade.search_multiple_formations(names=["Stage"])
        assert result is not None
        self.assertEqual(len(result), 1)
        self.mock_meili.recursive_smart_multi_search.assert_called_once()

    def test_returns_none_when_multi_search_returns_none(self) -> None:
        self.mock_meili.recursive_smart_multi_search.return_value = None
        result = self.facade.search_multiple_formations(names=["Stage"])
        self.assertIsNone(result)


# ── search_engagements (single-name wrapper) ─────────────────────────


class TestSearchEngagements(_FacadeTestBase):
    def test_returns_first_result(self) -> None:
        mock_result = Mock(spec=MultiSearchResult)
        mock_inner = Mock(spec=EngagementsMultiSearchResult)
        mock_result.results = [mock_inner]
        self.mock_meili.recursive_smart_multi_search.return_value = mock_result

        result = self.facade.search_engagements(name="Paris")
        self.assertEqual(result, mock_inner)

    def test_returns_none_when_no_results(self) -> None:
        self.mock_meili.recursive_smart_multi_search.return_value = None
        result = self.facade.search_engagements(name="Paris")
        self.assertIsNone(result)


# ── search_formations (single-name wrapper) ──────────────────────────


class TestSearchFormations(_FacadeTestBase):
    def test_returns_first_result(self) -> None:
        mock_result = Mock(spec=MultiSearchResult)
        mock_inner = Mock(spec=FormationsMultiSearchResult)
        mock_result.results = [mock_inner]
        self.mock_meili.recursive_smart_multi_search.return_value = mock_result

        result = self.facade.search_formations(name="Stage")
        self.assertEqual(result, mock_inner)

    def test_returns_none_when_no_results(self) -> None:
        self.mock_meili.recursive_smart_multi_search.return_value = None
        result = self.facade.search_formations(name="Stage")
        self.assertIsNone(result)


# ── Index settings delegation ────────────────────────────────────────


class TestIndexSettingsDelegation(_FacadeTestBase):
    def test_get_index_settings_delegates(self) -> None:
        expected = Mock(spec=MeilisearchIndexSettings)
        self.mock_meili.get_index_settings.return_value = expected
        result = self.facade.get_index_settings("organismes")
        self.mock_meili.get_index_settings.assert_called_once_with("organismes", None)
        self.assertEqual(result, expected)

    def test_get_all_index_settings_delegates(self) -> None:
        expected = {"organismes": Mock(spec=MeilisearchIndexSettings)}
        self.mock_meili.get_all_index_settings.return_value = expected
        result = self.facade.get_all_index_settings()
        self.mock_meili.get_all_index_settings.assert_called_once_with(None)
        self.assertEqual(result, expected)

    def test_get_filterable_attributes_delegates(self) -> None:
        self.mock_meili.get_filterable_attributes.return_value = ["id", "nom"]
        result = self.facade.get_filterable_attributes("organismes")
        self.mock_meili.get_filterable_attributes.assert_called_once_with(
            "organismes", None
        )
        self.assertEqual(result, ["id", "nom"])

    def test_get_sortable_attributes_delegates(self) -> None:
        self.mock_meili.get_sortable_attributes.return_value = ["nom"]
        result = self.facade.get_sortable_attributes("organismes")
        self.mock_meili.get_sortable_attributes.assert_called_once_with(
            "organismes", None
        )
        self.assertEqual(result, ["nom"])


# ── _chunked ─────────────────────────────────────────────────────────


class TestChunked(unittest.TestCase):
    def test_empty_list(self) -> None:
        self.assertEqual(FFBBAPIClientV2._chunked([], 10), [])

    def test_exact_split(self) -> None:
        self.assertEqual(FFBBAPIClientV2._chunked([1, 2, 3, 4], 2), [[1, 2], [3, 4]])

    def test_remainder(self) -> None:
        self.assertEqual(FFBBAPIClientV2._chunked([1, 2, 3], 2), [[1, 2], [3]])

    def test_single_chunk(self) -> None:
        self.assertEqual(FFBBAPIClientV2._chunked([1, 2], 5), [[1, 2]])


# ── list_engagements_by_ids ──────────────────────────────────────────


class TestListEngagementsByIds(_FacadeTestBase):
    def test_empty_ids_returns_empty(self) -> None:
        result = self.facade.list_engagements_by_ids([])
        self.assertEqual(result, [])
        self.mock_api.list_engagements.assert_not_called()

    def test_single_chunk(self) -> None:
        mock_eng = Mock(spec=GetEngagementsResponse)
        self.mock_api.list_engagements.return_value = [mock_eng]
        result = self.facade.list_engagements_by_ids([1, 2, 3])
        self.assertEqual(result, [mock_eng])
        self.mock_api.list_engagements.assert_called_once()
        call_kwargs = self.mock_api.list_engagements.call_args
        filter_arg = call_kwargs[1]["filter_criteria"]
        self.assertEqual(json.loads(filter_arg), {"id": {"_in": [1, 2, 3]}})

    def test_multiple_chunks(self) -> None:
        """IDs exceeding chunk size are split into multiple calls."""
        ids = list(range(1, 102))  # 101 IDs → 3 chunks (50+50+1)
        self.mock_api.list_engagements.return_value = []
        self.facade.list_engagements_by_ids(ids)
        self.assertEqual(self.mock_api.list_engagements.call_count, 3)


# ── list_engagements_by_poule ────────────────────────────────────────


class TestListEngagementsByPoule(_FacadeTestBase):
    def test_delegates_with_eq_filter(self) -> None:
        mock_eng = Mock(spec=GetEngagementsResponse)
        self.mock_api.list_engagements.return_value = [mock_eng]
        result = self.facade.list_engagements_by_poule(42)
        self.assertEqual(result, [mock_eng])
        call_kwargs = self.mock_api.list_engagements.call_args
        filter_arg = call_kwargs[1]["filter_criteria"]
        self.assertEqual(json.loads(filter_arg), {"idPoule": {"_eq": 42}})


# ── list_engagements_by_poules ───────────────────────────────────────


class TestListEngagementsByPoules(_FacadeTestBase):
    def test_empty_poule_ids_returns_empty(self) -> None:
        result = self.facade.list_engagements_by_poules([])
        self.assertEqual(result, [])
        self.mock_api.list_engagements.assert_not_called()

    def test_single_chunk(self) -> None:
        self.mock_api.list_engagements.return_value = []
        self.facade.list_engagements_by_poules([10, 20])
        self.mock_api.list_engagements.assert_called_once()
        call_kwargs = self.mock_api.list_engagements.call_args
        filter_arg = call_kwargs[1]["filter_criteria"]
        self.assertEqual(json.loads(filter_arg), {"idPoule": {"_in": [10, 20]}})

    def test_multiple_chunks(self) -> None:
        ids = list(range(1, 102))
        self.mock_api.list_engagements.return_value = []
        self.facade.list_engagements_by_poules(ids)
        self.assertEqual(self.mock_api.list_engagements.call_count, 3)


# ── list_rencontres_by_poule ─────────────────────────────────────────


class TestListRencontresByPoule(_FacadeTestBase):
    def test_delegates_with_eq_filter(self) -> None:
        mock_ren = Mock(spec=GetRencontresResponse)
        self.mock_api.list_rencontres.return_value = [mock_ren]
        result = self.facade.list_rencontres_by_poule(99)
        self.assertEqual(result, [mock_ren])
        call_kwargs = self.mock_api.list_rencontres.call_args
        filter_arg = call_kwargs[1]["filter_criteria"]
        self.assertEqual(json.loads(filter_arg), {"idPoule": {"_eq": 99}})


# ── list_rencontres_by_poules ────────────────────────────────────────


class TestListRencontresByPoules(_FacadeTestBase):
    def test_empty_poule_ids_returns_empty(self) -> None:
        result = self.facade.list_rencontres_by_poules([])
        self.assertEqual(result, [])
        self.mock_api.list_rencontres.assert_not_called()

    def test_single_chunk(self) -> None:
        self.mock_api.list_rencontres.return_value = []
        self.facade.list_rencontres_by_poules([5, 6])
        self.mock_api.list_rencontres.assert_called_once()

    def test_multiple_chunks(self) -> None:
        ids = list(range(1, 102))
        self.mock_api.list_rencontres.return_value = []
        self.facade.list_rencontres_by_poules(ids)
        self.assertEqual(self.mock_api.list_rencontres.call_count, 3)


# ── list_entraineurs_by_ids ──────────────────────────────────────────


class TestListEntraineursByIds(_FacadeTestBase):
    def test_empty_ids_returns_empty(self) -> None:
        result = self.facade.list_entraineurs_by_ids([])
        self.assertEqual(result, [])
        self.mock_api.list_entraineurs.assert_not_called()

    def test_single_chunk_converts_to_str_ids(self) -> None:
        mock_ent = Mock(spec=GetEntraineursResponse)
        self.mock_api.list_entraineurs.return_value = [mock_ent]
        result = self.facade.list_entraineurs_by_ids([100, 200])
        self.assertEqual(result, [mock_ent])
        call_kwargs = self.mock_api.list_entraineurs.call_args
        filter_arg = call_kwargs[1]["filter_criteria"]
        self.assertEqual(
            json.loads(filter_arg),
            {"idLicence": {"_in": ["100", "200"]}},
        )

    def test_multiple_chunks(self) -> None:
        ids = list(range(1, 102))
        self.mock_api.list_entraineurs.return_value = []
        self.facade.list_entraineurs_by_ids(ids)
        self.assertEqual(self.mock_api.list_entraineurs.call_count, 3)


if __name__ == "__main__":
    unittest.main()
