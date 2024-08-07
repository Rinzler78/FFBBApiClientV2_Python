import os
import unittest
from typing import Any, Type

from dotenv import load_dotenv

from ffbb_api_client_v2 import (
    CompetitionsFacetDistribution,
    CompetitionsFacetStats,
    CompetitionsHit,
    CompetitionsMultiSearchResult,
    FFBBAPIClientV2,
    OrganismesFacetDistribution,
    OrganismesFacetStats,
    OrganismesHit,
    OrganismesMultiSearchResult,
    PratiquesFacetDistribution,
    PratiquesFacetStats,
    PratiquesHit,
    PratiquesMultiSearchResult,
    RencontresFacetDistribution,
    RencontresFacetStats,
    RencontresHit,
    RencontresMultiSearchResult,
    SallesFacetDistribution,
    SallesFacetStats,
    SallesHit,
    SallesMultiSearchResult,
    TerrainsFacetDistribution,
    TerrainsFacetStats,
    TerrainsHit,
    TerrainsMultiSearchResult,
    TournoisFacetDistribution,
    TournoisFacetStats,
    TournoisHit,
    TournoisMultiSearchResult,
)

load_dotenv()

MEILISEARCH_BEARER_TOKEN = os.getenv("MEILISEARCH_BEARER_TOKEN")
API_FFBB_APP_BEARER_TOKEN = os.getenv("API_FFBB_APP_BEARER_TOKEN")


class Test_04_FFBBAPIClientV2(unittest.TestCase):
    def setUp(self):
        self.api_client = FFBBAPIClientV2.create(
            MEILISEARCH_BEARER_TOKEN, API_FFBB_APP_BEARER_TOKEN, debug=True
        )

    def setup_method(self, method):
        self.setUp()

    def test_get_lives(self):
        lives = self.api_client.get_lives()
        self.assertIsNotNone(lives)

    def __validate_test_search(
        self,
        search_result: Any,
        result_type: Type,
        facet_distribution_type: Type,
        facet_stats_type: Type,
        hit_type: Type,
    ):
        self.assertIsNotNone(search_result)
        self.assertEqual(type(search_result), result_type)

        if search_result.facet_distribution:
            self.assertEqual(
                type(search_result.facet_distribution), facet_distribution_type
            )

        if search_result.facet_stats:
            self.assertEqual(type(search_result.facet_stats), facet_stats_type)

        for hit in search_result.hits:
            self.assertEqual(type(hit), hit_type)

    def __validate_test_search_multi(
        self,
        search_result: Any,
        result_type: Type,
        facet_distribution_type: Type,
        facet_stats_type: Type,
        hit_type: Type,
    ):
        self.assertIsNotNone(search_result)
        self.assertEqual(type(search_result), list)

        for result in search_result:
            self.__validate_test_search(
                result, result_type, facet_distribution_type, facet_stats_type, hit_type
            )

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
        self.__validate_test_search_multi(
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
        self.__validate_test_search_multi(
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
        self.__validate_test_search_multi(
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
        self.__validate_test_search_multi(
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
        self.__validate_test_search_multi(
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
        self.__validate_test_search_multi(
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
        self.__validate_test_search_multi(
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
        self.__validate_test_search_multi(
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
        self.__validate_test_search_multi(
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
        self.__validate_test_search_multi(
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
        self.__validate_test_search_multi(
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
        self.__validate_test_search_multi(
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
        self.__validate_test_search_multi(
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
        self.__validate_test_search_multi(
            search_pratiques_result,
            PratiquesMultiSearchResult,
            PratiquesFacetDistribution,
            PratiquesFacetStats,
            PratiquesHit,
        )


if __name__ == "__main__":
    unittest.main()
