import os
import unittest

from dotenv import load_dotenv

from ffbb_api_client_v2.meilisearch_ffbb_app_client import (
    MeilisearchFFBBAPPClientHelper,
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
    MultiSearchResultCompetitions,
)
from ffbb_api_client_v2.MultiSearchResultOrganismes import MultiSearchResultOrganismes
from ffbb_api_client_v2.MultiSearchResultRencontres import MultiSearchResultRencontres
from ffbb_api_client_v2.MultiSearchResultSalles import MultiSearchResultSalles
from ffbb_api_client_v2.MultiSearchResultTerrains import MultiSearchResultTerrains
from ffbb_api_client_v2.MultiSearchResultTournois import MultiSearchResultTournois

load_dotenv()

MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN = os.getenv(
    "MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN"
)


class TestMeilisearchFFBBAPPClientHelper(unittest.TestCase):

    def setUp(self):
        self.api_client: MeilisearchFFBBAPPClientHelper = (
            MeilisearchFFBBAPPClientHelper(
                MEILISEARCH_PROD_FFBB_APP_BEARER_TOKEN,
                debug=True,
            )
        )

    def setup_method(self, method):
        self.setUp()

    def test_multi_search_with_empty_queries(self):
        result = self.api_client.multi_search()
        self.assertIsNotNone(result)

    def __validate_test_search_organismes(self, search_organismes_result):
        self.assertIsNotNone(search_organismes_result)
        self.assertIsNotNone(search_organismes_result.results)
        self.assertGreater(len(search_organismes_result.results), 0)

        for result in search_organismes_result.results:
            self.assertEqual(type(result), MultiSearchResultOrganismes)

            if result.facet_distribution:
                self.assertEqual(
                    type(result.facet_distribution), OrganismesFacetDistribution
                )

            if result.facet_stats:
                self.assertEqual(type(result.facet_stats), OrganismesFacetStats)

            for hit in result.hits:
                self.assertEqual(type(hit), OrganismesHit)

    def test_search_organismes_with_empty_name(self):
        search_organismes_result = self.api_client.search_organismes()
        self.__validate_test_search_organismes(search_organismes_result)

    def test_search_organismes_with_most_used_letters(self):
        search_organismes_result = self.api_client.search_multiple_organismes(
            ["a", "e", "i", "o", "u", "y", "b", "l", "m", "s"]
        )

        self.__validate_test_search_organismes(search_organismes_result)

    def test_search_organismes_with_known_names(self):
        search_organismes_result = self.api_client.search_multiple_organismes(
            ["Paris", "Senas", "Reims"]
        )
        self.assertIsNotNone(search_organismes_result)
        self.assertIsNotNone(search_organismes_result.results)
        self.assertGreater(len(search_organismes_result.results), 0)

        self.__validate_test_search_organismes(search_organismes_result)

    def __validate_test_search_rencontres(self, search_rencontres_result):
        self.assertIsNotNone(search_rencontres_result)
        self.assertIsNotNone(search_rencontres_result.results)
        self.assertGreater(len(search_rencontres_result.results), 0)

        for result in search_rencontres_result.results:
            self.assertEqual(type(result), MultiSearchResultRencontres)

            if result.facet_distribution:
                self.assertEqual(
                    type(result.facet_distribution), RencontresFacetDistribution
                )

            if result.facet_stats:
                self.assertEqual(type(result.facet_stats), RencontresFacetStats)

            for hit in result.hits:
                self.assertEqual(type(hit), RencontresHit)

    def test_search_rencontres_with_empty_names(self):
        search_rencontres_result = self.api_client.search_rencontres()
        self.__validate_test_search_rencontres(search_rencontres_result)

    def test_search_rencontres_with_most_used_letters(self):
        search_rencontres_result = self.api_client.search_multiple_rencontres(
            ["a", "e", "i", "o", "u", "y", "b", "l", "m", "s"]
        )
        self.__validate_test_search_rencontres(search_rencontres_result)

    def test_search_rencontres_with_known_names(self):
        search_rencontres_result = self.api_client.search_multiple_rencontres(
            ["Paris", "Senas", "Reims"]
        )
        self.__validate_test_search_rencontres(search_rencontres_result)

    def __validate_test_search_terrains(self, search_terrains_result):
        self.assertIsNotNone(search_terrains_result)
        self.assertIsNotNone(search_terrains_result.results)
        self.assertGreater(len(search_terrains_result.results), 0)

        for result in search_terrains_result.results:
            self.assertEqual(type(result), MultiSearchResultTerrains)

            if result.facet_distribution:
                self.assertEqual(
                    type(result.facet_distribution), TerrainsFacetDistribution
                )

            if result.facet_stats:
                self.assertEqual(type(result.facet_stats), TerrainsFacetStats)

            for hit in result.hits:
                self.assertEqual(type(hit), TerrainsHit)

    def test_search_terrains_with_empty_names(self):
        search_terrains_result = self.api_client.search_terrains()

        self.__validate_test_search_terrains(search_terrains_result)

    def test_search_terrains_with_most_used_letters(self):
        search_terrains_result = self.api_client.search_multiple_terrains(
            ["a", "e", "i", "o", "u", "y", "b", "l", "m", "s"]
        )

        self.__validate_test_search_terrains(search_terrains_result)

    def test_search_terrains_with_known_names(self):
        search_terrains_result = self.api_client.search_multiple_terrains(
            ["Paris", "Senas", "Reims"]
        )
        self.__validate_test_search_terrains(search_terrains_result)

    def __validate_test_search_competitions(self, search_competitions_result):
        self.assertIsNotNone(search_competitions_result)
        self.assertIsNotNone(search_competitions_result.results)
        self.assertGreater(len(search_competitions_result.results), 0)

        for result in search_competitions_result.results:
            self.assertEqual(type(result), MultiSearchResultCompetitions)

            if result.facet_distribution:
                self.assertEqual(
                    type(result.facet_distribution), CompetitionsFacetDistribution
                )

            if result.facet_stats:
                self.assertEqual(type(result.facet_stats), CompetitionsFacetStats)

            for hit in result.hits:
                self.assertEqual(type(hit), CompetitionsHit)

    def test_search_competitions_with_empty_names(self):
        search_competitions_result = self.api_client.search_competitions()
        self.__validate_test_search_competitions(search_competitions_result)

    def test_search_competitions_with_most_used_letters(self):
        search_competitions_result = self.api_client.search_multiple_competitions(
            ["a", "e", "i", "o", "u", "y", "b", "l", "m", "s"]
        )
        self.__validate_test_search_competitions(search_competitions_result)

    def test_search_competitions_with_known_names(self):
        search_competitions_result = self.api_client.search_multiple_competitions(
            ["Paris", "Senas", "Reims"]
        )
        self.__validate_test_search_competitions(search_competitions_result)

    def __validate_test_search_salles(self, search_salles_result):
        self.assertIsNotNone(search_salles_result)
        self.assertIsNotNone(search_salles_result.results)
        self.assertGreater(len(search_salles_result.results), 0)

        for result in search_salles_result.results:
            self.assertEqual(type(result), MultiSearchResultSalles)

            if result.facet_distribution:
                self.assertEqual(
                    type(result.facet_distribution), SallesFacetDistribution
                )

            if result.facet_stats:
                self.assertEqual(type(result.facet_stats), SallesFacetStats)

            for hit in result.hits:
                self.assertEqual(type(hit), SallesHit)

    def test_search_salles_with_empty_names(self):
        search_salles_result = self.api_client.search_salles()
        self.__validate_test_search_salles(search_salles_result)

    def test_search_salles_with_most_used_letters(self):
        search_salles_result = self.api_client.search_multiple_salles(
            ["a", "e", "i", "o", "u", "y", "b", "l", "m", "s"]
        )
        self.__validate_test_search_salles(search_salles_result)

    def test_search_salles_with_known_names(self):
        search_salles_result = self.api_client.search_multiple_salles(
            ["Paris", "Senas", "Reims"]
        )
        self.__validate_test_search_salles(search_salles_result)

    def __validate_test_search_tournois(self, search_tournois_result):
        self.assertIsNotNone(search_tournois_result)
        self.assertIsNotNone(search_tournois_result.results)
        self.assertGreater(len(search_tournois_result.results), 0)

        for result in search_tournois_result.results:
            self.assertEqual(type(result), MultiSearchResultTournois)

            if result.facet_distribution:
                self.assertEqual(
                    type(result.facet_distribution), TournoisFacetDistribution
                )

            if result.facet_stats:
                self.assertEqual(type(result.facet_stats), TournoisFacetStats)

            for hit in result.hits:
                self.assertEqual(type(hit), TournoisHit)

    def test_search_tournois_with_empty_names(self):
        search_tournois_result = self.api_client.search_tournois()
        self.__validate_test_search_tournois(search_tournois_result)

    def test_search_tournois_with_most_used_letters(self):
        search_tournois_result = self.api_client.search_multiple_tournois(
            ["a", "e", "i", "o", "u", "y", "b", "l", "m", "s"]
        )
        self.__validate_test_search_tournois(search_tournois_result)

    def test_search_tournois_with_known_names(self):
        search_tournois_result = self.api_client.search_multiple_tournois(
            ["Paris", "Senas", "Reims"]
        )
        self.__validate_test_search_tournois(search_tournois_result)
