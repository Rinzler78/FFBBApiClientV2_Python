import os
import unittest
from typing import List, Optional

from dotenv import load_dotenv

from ffbb_api_client_v2.meilisearch_client import MeilisearchClient
from ffbb_api_client_v2.multi_search_query import (
    CompetitionsMultiSearchQuery,
    MultiSearchQuery,
    OrganismesMultiSearchQuery,
    PratiquesMultiSearchQuery,
    RencontresMultiSearchQuery,
    SallesMultiSearchQuery,
    TerrainsMultiSearchQuery,
    TournoisMultiSearchQuery,
)

load_dotenv()

meilisearch_ffbb_app_token = os.getenv("MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN")


class TestMeilisearchClient(unittest.TestCase):

    def setUp(self):
        self.api_client: MeilisearchClient = MeilisearchClient(
            meilisearch_ffbb_app_token,
            debug=True,
        )

    def setup_method(self, method):
        self.setUp()

    def test_multi_search_with_empty_queries(self):
        result = self.api_client.multi_search()
        self.assertIsNotNone(result)

    def __generate_queries(self, search_name: str = None, limit: Optional[int] = 10000):
        return [
            OrganismesMultiSearchQuery(search_name, limit=limit),
            RencontresMultiSearchQuery(search_name, limit=limit),
            TerrainsMultiSearchQuery(search_name, limit=limit),
            CompetitionsMultiSearchQuery(search_name, limit=limit),
            SallesMultiSearchQuery(search_name, limit=limit),
            TournoisMultiSearchQuery(search_name, limit=limit),
            PratiquesMultiSearchQuery(search_name, limit=limit),
        ]

    def __validate_test_recursive_multi_search_with_all_possible_queries(
        self, queries: List[MultiSearchQuery], search_result
    ):
        self.assertIsNotNone(search_result)
        self.assertIsNotNone(search_result.results)
        self.assertGreater(len(search_result.results), 0)

        for i in range(0, len(search_result.results)):
            result = search_result.results[i]
            query = queries[i]

            self.assertTrue(query.is_valid_result(result))

    def test_multi_search_with_all_possible_empty_queries(self):
        queries = self.__generate_queries()
        result = self.api_client.multi_search(queries)
        self.__validate_test_recursive_multi_search_with_all_possible_queries(
            queries, result
        )


if __name__ == "__main__":
    unittest.main()
