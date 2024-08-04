import os
import unittest
from typing import Any, List, Optional, Type

from dotenv import load_dotenv

from ffbb_api_client_v2.meilisearch_ffbb_client import MeilisearchFFBBClient
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
from ffbb_api_client_v2.multi_search_result_competitions import (
    CompetitionsFacetDistribution,
    CompetitionsFacetStats,
    CompetitionsHit,
)
from ffbb_api_client_v2.multi_search_result_organismes import (
    OrganismesFacetDistribution,
    OrganismesFacetStats,
    OrganismesHit,
)
from ffbb_api_client_v2.multi_search_result_pratiques import (
    PratiquesFacetDistribution,
    PratiquesFacetStats,
    PratiquesHit,
)
from ffbb_api_client_v2.multi_search_result_rencontres import (
    RencontresFacetDistribution,
    RencontresFacetStats,
    RencontresHit,
)
from ffbb_api_client_v2.multi_search_result_salles import (
    SallesFacetDistribution,
    SallesFacetStats,
    SallesHit,
)
from ffbb_api_client_v2.multi_search_result_terrains import (
    TerrainsFacetDistribution,
    TerrainsFacetStats,
    TerrainsHit,
)
from ffbb_api_client_v2.multi_search_result_tournois import (
    TournoisFacetDistribution,
    TournoisFacetStats,
    TournoisHit,
)
from ffbb_api_client_v2.MultiSearchResultCompetitions import (
    CompetitionsMultiSearchResult,
)
from ffbb_api_client_v2.MultiSearchResultOrganismes import OrganismesMultiSearchResult
from ffbb_api_client_v2.MultiSearchResultPratiques import PratiquesMultiSearchResult
from ffbb_api_client_v2.MultiSearchResultRencontres import RencontresMultiSearchResult
from ffbb_api_client_v2.MultiSearchResultSalles import SallesMultiSearchResult
from ffbb_api_client_v2.MultiSearchResultTerrains import TerrainsMultiSearchResult
from ffbb_api_client_v2.MultiSearchResultTournois import TournoisMultiSearchResult

load_dotenv()

meilisearch_ffbb_app_token = os.getenv("MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN")


class TestMeilisearchFFBBAPPClientHelper(unittest.TestCase):

    def setUp(self):
        self.api_client: MeilisearchFFBBClient = MeilisearchFFBBClient(
            meilisearch_ffbb_app_token,
            debug=True,
        )

    def setup_method(self, method):
        self.setUp()

    def __generate_queries(self, search_name: str = None, limit: Optional[int] = 1):
        return [
            OrganismesMultiSearchQuery(search_name, limit=limit),
            RencontresMultiSearchQuery(search_name, limit=limit),
            TerrainsMultiSearchQuery(search_name, limit=limit),
            CompetitionsMultiSearchQuery(search_name, limit=limit),
            SallesMultiSearchQuery(search_name, limit=limit),
            TournoisMultiSearchQuery(search_name, limit=limit),
            PratiquesMultiSearchQuery(search_name, limit=limit),
        ]

    def __validate_multi_search_with_all_possible_queries(
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
        self.__validate_multi_search_with_all_possible_queries(queries, result)

    def test_multi_search_with_all_possible_queries(self):
        queries = self.__generate_queries("Senas")
        result = self.api_client.multi_search(queries)
        self.__validate_multi_search_with_all_possible_queries(queries, result)

    def __validate_test_search(
        self,
        search_result: Any,
        result_type: Type,
        facet_distribution_type: Type,
        facet_stats_type: Type,
        hit_type: Type,
    ):
        self.assertIsNotNone(search_result)
        self.assertIsNotNone(search_result.results)
        self.assertGreater(len(search_result.results), 0)

        for result in search_result.results:
            self.assertEqual(type(result), result_type)

            if result.facet_distribution:
                self.assertEqual(
                    type(result.facet_distribution), facet_distribution_type
                )

            if result.facet_stats:
                self.assertEqual(type(result.facet_stats), facet_stats_type)

            for hit in result.hits:
                self.assertEqual(type(hit), hit_type)

    def test_search_organismes_with_empty_name(self):
        search_organismes_result = self.api_client.search_organismes()
        self.__validate_test_search(
            search_organismes_result,
            OrganismesMultiSearchResult,
            OrganismesFacetDistribution,
            OrganismesFacetStats,
            OrganismesHit,
        )

    def test_search_organismes_with_most_used_letters(self):
        search_organismes_result = self.api_client.search_multiple_organismes(
            ["a", "e", "i", "o", "u", "y", "b", "l", "m", "s"]
        )
        self.__validate_test_search(
            search_organismes_result,
            OrganismesMultiSearchResult,
            OrganismesFacetDistribution,
            OrganismesFacetStats,
            OrganismesHit,
        )

    def test_search_organismes_with_known_names(self):
        search_organismes_result = self.api_client.search_multiple_organismes(
            ["Paris", "Senas", "Reims"]
        )
        self.__validate_test_search(
            search_organismes_result,
            OrganismesMultiSearchResult,
            OrganismesFacetDistribution,
            OrganismesFacetStats,
            OrganismesHit,
        )

    def test_search_rencontres_with_empty_names(self):
        search_rencontres_result = self.api_client.search_rencontres()
        self.__validate_test_search(
            search_rencontres_result,
            RencontresMultiSearchResult,
            RencontresFacetDistribution,
            RencontresFacetStats,
            RencontresHit,
        )

    def test_search_rencontres_with_most_used_letters(self):
        search_rencontres_result = self.api_client.search_multiple_rencontres(
            ["a", "e", "i", "o", "u", "y", "b", "l", "m", "s"]
        )
        self.__validate_test_search(
            search_rencontres_result,
            RencontresMultiSearchResult,
            RencontresFacetDistribution,
            RencontresFacetStats,
            RencontresHit,
        )

    def test_search_rencontres_with_known_names(self):
        search_rencontres_result = self.api_client.search_multiple_rencontres(
            ["Paris", "Senas", "Reims"]
        )
        self.__validate_test_search(
            search_rencontres_result,
            RencontresMultiSearchResult,
            RencontresFacetDistribution,
            RencontresFacetStats,
            RencontresHit,
        )

    def test_search_terrains_with_empty_names(self):
        search_terrains_result = self.api_client.search_terrains()
        self.__validate_test_search(
            search_terrains_result,
            TerrainsMultiSearchResult,
            TerrainsFacetDistribution,
            TerrainsFacetStats,
            TerrainsHit,
        )

    def test_search_terrains_with_most_used_letters(self):
        search_terrains_result = self.api_client.search_multiple_terrains(
            ["a", "e", "i", "o", "u", "y", "b", "l", "m", "s"]
        )
        self.__validate_test_search(
            search_terrains_result,
            TerrainsMultiSearchResult,
            TerrainsFacetDistribution,
            TerrainsFacetStats,
            TerrainsHit,
        )

    def test_search_terrains_with_known_names(self):
        search_terrains_result = self.api_client.search_multiple_terrains(
            ["Paris", "Senas", "Reims"]
        )
        self.__validate_test_search(
            search_terrains_result,
            TerrainsMultiSearchResult,
            TerrainsFacetDistribution,
            TerrainsFacetStats,
            TerrainsHit,
        )

    def test_search_competitions_with_empty_names(self):
        search_competitions_result = self.api_client.search_competitions()
        self.__validate_test_search(
            search_competitions_result,
            CompetitionsMultiSearchResult,
            CompetitionsFacetDistribution,
            CompetitionsFacetStats,
            CompetitionsHit,
        )

    def test_search_competitions_with_most_used_letters(self):
        search_competitions_result = self.api_client.search_multiple_competitions(
            ["a", "e", "i", "o", "u", "y", "b", "l", "m", "s"]
        )
        self.__validate_test_search(
            search_competitions_result,
            CompetitionsMultiSearchResult,
            CompetitionsFacetDistribution,
            CompetitionsFacetStats,
            CompetitionsHit,
        )

    def test_search_competitions_with_known_names(self):
        search_competitions_result = self.api_client.search_multiple_competitions(
            ["Paris", "Senas", "Reims"]
        )
        self.__validate_test_search(
            search_competitions_result,
            CompetitionsMultiSearchResult,
            CompetitionsFacetDistribution,
            CompetitionsFacetStats,
            CompetitionsHit,
        )

    def test_search_salles_with_empty_names(self):
        search_salles_result = self.api_client.search_salles()
        self.__validate_test_search(
            search_salles_result,
            SallesMultiSearchResult,
            SallesFacetDistribution,
            SallesFacetStats,
            SallesHit,
        )

    def test_search_salles_with_most_used_letters(self):
        search_salles_result = self.api_client.search_multiple_salles(
            ["a", "e", "i", "o", "u", "y", "b", "l", "m", "s"]
        )
        self.__validate_test_search(
            search_salles_result,
            SallesMultiSearchResult,
            SallesFacetDistribution,
            SallesFacetStats,
            SallesHit,
        )

    def test_search_salles_with_known_names(self):
        search_salles_result = self.api_client.search_multiple_salles(
            ["Paris", "Senas", "Reims"]
        )
        self.__validate_test_search(
            search_salles_result,
            SallesMultiSearchResult,
            SallesFacetDistribution,
            SallesFacetStats,
            SallesHit,
        )

    def test_search_tournois_with_empty_names(self):
        search_tournois_result = self.api_client.search_tournois()
        self.__validate_test_search(
            search_tournois_result,
            TournoisMultiSearchResult,
            TournoisFacetDistribution,
            TournoisFacetStats,
            TournoisHit,
        )

    def test_search_tournois_with_most_used_letters(self):
        search_tournois_result = self.api_client.search_multiple_tournois(
            ["a", "e", "i", "o", "u", "y", "b", "l", "m", "s"]
        )
        self.__validate_test_search(
            search_tournois_result,
            TournoisMultiSearchResult,
            TournoisFacetDistribution,
            TournoisFacetStats,
            TournoisHit,
        )

    def test_search_tournois_with_known_names(self):
        search_tournois_result = self.api_client.search_multiple_tournois(
            ["Paris", "Senas", "Reims"]
        )
        self.__validate_test_search(
            search_tournois_result,
            TournoisMultiSearchResult,
            TournoisFacetDistribution,
            TournoisFacetStats,
            TournoisHit,
        )

    def test_search_pratiques_with_empty_names(self):
        search_pratiques_result = self.api_client.search_pratiques()
        self.__validate_test_search(
            search_pratiques_result,
            PratiquesMultiSearchResult,
            PratiquesFacetDistribution,
            PratiquesFacetStats,
            PratiquesHit,
        )

    def test_search_pratiques_with_most_used_letters(self):
        search_pratiques_result = self.api_client.search_multiple_pratiques(
            ["a", "e", "i", "o", "u", "y", "b", "l", "m", "s"]
        )
        self.__validate_test_search(
            search_pratiques_result,
            PratiquesMultiSearchResult,
            PratiquesFacetDistribution,
            PratiquesFacetStats,
            PratiquesHit,
        )

    def test_search_pratiques_with_known_names(self):
        search_pratiques_result = self.api_client.search_multiple_pratiques(
            ["Paris", "Senas", "Reims"]
        )
        self.__validate_test_search(
            search_pratiques_result,
            PratiquesMultiSearchResult,
            PratiquesFacetDistribution,
            PratiquesFacetStats,
            PratiquesHit,
        )
