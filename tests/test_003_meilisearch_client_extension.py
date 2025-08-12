import os
import unittest

from ffbb_api_client_v2 import (
    MeilisearchClientExtension,
    MultiSearchQuery,
    generate_queries,
)


class Test003MeilisearchClientExtension(unittest.TestCase):
    def setUp(self):
        mls_token = os.getenv("MEILISEARCH_BEARER_TOKEN")

        if not mls_token:
            raise Exception("MEILISEARCH_TOKEN environment variable not set")

        # NOTE: Set debug=True for detailed logging if needed during debugging
        self.api_client: MeilisearchClientExtension = MeilisearchClientExtension(
            bearer_token=mls_token,
            url="https://meilisearch-prod.ffbb.app/",
            debug=False,
        )

    def setup_method(self, method):
        self.setUp()

    def test_smart_multi_search_with_empty_queries(self):
        result = self.api_client.smart_multi_search()
        self.assertIsNotNone(result)

    def __validate_test(self, queries: list[MultiSearchQuery], search_result):
        self.assertIsNotNone(search_result)
        self.assertIsNotNone(search_result.results)
        self.assertGreater(len(search_result.results), 0)

        for i in range(0, len(search_result.results)):
            result = search_result.results[i]
            query = queries[i]

            self.assertTrue(query.is_valid_result(result))

    def test_smart_multi_search_with_all_possible_empty_queries(self):
        queries = generate_queries()
        result = self.api_client.smart_multi_search(queries)
        self.__validate_test(queries, result)

    def test_recursive_smart_multi_search_with_empty_queries(self):
        result = self.api_client.recursive_smart_multi_search()
        self.assertIsNotNone(result)

    def __validate_multi_search_with_all_possible_queries(
        self, queries: list[MultiSearchQuery], search_result
    ):
        self.assertIsNotNone(search_result)
        self.assertIsNotNone(search_result.results)
        self.assertGreater(len(search_result.results), 0)

        for i in range(0, len(search_result.results)):
            result = search_result.results[i]
            query = queries[i]

            self.assertTrue(query.is_valid_result(result))

    def test_recursive_smart_multi_search_with_all_possible_empty_queries(self):
        queries = generate_queries()
        result = self.api_client.recursive_smart_multi_search(queries)
        self.__validate_multi_search_with_all_possible_queries(queries, result)

    def test_recursive_smart_multi_search_with_known_query(self):
        queries = generate_queries("Senas")
        result = self.api_client.recursive_smart_multi_search(queries)
        self.__validate_multi_search_with_all_possible_queries(queries, result)


if __name__ == "__main__":
    unittest.main()
