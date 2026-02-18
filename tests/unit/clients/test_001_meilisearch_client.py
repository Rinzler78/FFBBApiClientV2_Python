import os
import unittest

from dotenv import load_dotenv

from ffbb_api_client_v2 import MeilisearchClient, MultiSearchQuery, generate_queries


class Test002MeilisearchClient(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        mls_token = os.getenv("MEILISEARCH_BEARER_TOKEN")

        if not mls_token:
            self.skipTest("MEILISEARCH_BEARER_TOKEN environment variable not set")

        # NOTE: Set debug=True for detailed logging if needed during debugging
        self.api_client: MeilisearchClient = MeilisearchClient(
            bearer_token=mls_token,
            url="https://meilisearch-prod.ffbb.app/",
            debug=False,
        )

    def setup_method(self, method):
        self.setUp()

    def test_000_multi_search_with_empty_queries(self):
        if not hasattr(self, "api_client") or self.api_client is None:
            self.skipTest("Meilisearch client not initialized - missing token")
        result = self.api_client.multi_search()
        self.assertIsNotNone(result)

    def __validate_result(self, queries: list[MultiSearchQuery], search_result):
        self.assertIsNotNone(search_result)
        self.assertIsNotNone(search_result.results)
        self.assertGreater(len(search_result.results), 0)

        # Create a mapping of index_uid to query for proper validation
        queries_by_index = {q.index_uid: q for q in queries}

        for result in search_result.results:
            # Find the matching query by index_uid
            query = queries_by_index.get(result.index_uid)
            self.assertIsNotNone(
                query, f"No query found for result index_uid: {result.index_uid}"
            )
            self.assertTrue(query.is_valid_result(result))

    def test_001_multi_search_with_all_possible_empty_queries(self):
        if not hasattr(self, "api_client") or self.api_client is None:
            self.skipTest("Meilisearch client not initialized - missing token")
        queries = generate_queries()
        result = self.api_client.multi_search(queries)
        self.__validate_result(queries, result)


if __name__ == "__main__":
    unittest.main()
