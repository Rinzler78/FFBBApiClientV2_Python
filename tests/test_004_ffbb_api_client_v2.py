import os
import unittest
from typing import Any

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


class Test004FfbbApiClientV2(unittest.TestCase):
    # List of 10 largest French cities
    LARGEST_FRENCH_CITIES = [
        "Paris",
        "Marseille",
        "Lyon",
        "Toulouse",
        "Nice",
        "Nantes",
        "Strasbourg",
        "Montpellier",
        "Bordeaux",
        "Lille",
    ]

    def setUp(self):
        api_token = os.getenv("API_FFBB_APP_BEARER_TOKEN")

        if not api_token:
            self.skipTest("API_FFBB_APP_BEARER_TOKEN environment variable not set")

        mls_token = os.getenv("MEILISEARCH_BEARER_TOKEN")

        if not mls_token:
            self.skipTest("MEILISEARCH_BEARER_TOKEN environment variable not set")

        # NOTE: Set debug=True for detailed logging if needed during debugging
        self.api_client = FFBBAPIClientV2.create(
            meilisearch_bearer_token=mls_token,
            api_bearer_token=api_token,
            debug=False,
        )

    def setup_method(self, method):
        self.setUp()

    def test_get_lives(self):
        lives = self.api_client.get_lives()
        self.assertIsNotNone(lives)

    def __validate_test_search(
        self,
        search_result: Any,
        result_type: type,
        facet_distribution_type: type,
        facet_stats_type: type,
        hit_type: type,
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
        result_type: type,
        facet_distribution_type: type,
        facet_stats_type: type,
        hit_type: type,
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

    def test_search_organismes_with_largest_cities(self):
        """Test search_multiple_organismes with 10 largest French cities."""
        search_organismes_result = self.api_client.search_multiple_organismes(
            self.LARGEST_FRENCH_CITIES
        )
        self.__validate_test_search_multi(
            search_organismes_result,
            OrganismesMultiSearchResult,
            OrganismesFacetDistribution,
            OrganismesFacetStats,
            OrganismesHit,
        )

    def test_search_organismes_single_city(self):
        """Test search_organismes with each of the 10 largest French cities."""
        for city in self.LARGEST_FRENCH_CITIES:
            with self.subTest(city=city):
                search_organismes_result = self.api_client.search_organismes(city)
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

    def test_search_rencontres_with_largest_cities(self):
        """Test search_multiple_rencontres with 10 largest French cities."""
        search_rencontres_result = self.api_client.search_multiple_rencontres(
            self.LARGEST_FRENCH_CITIES
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

    def test_search_terrains_with_largest_cities(self):
        """Test search_multiple_terrains with 10 largest French cities."""
        search_terrains_result = self.api_client.search_multiple_terrains(
            self.LARGEST_FRENCH_CITIES
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

    def test_search_competitions_with_largest_cities(self):
        """Test search_multiple_competitions with 10 largest French cities."""
        search_competitions_result = self.api_client.search_multiple_competitions(
            self.LARGEST_FRENCH_CITIES
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

    def test_search_salles_with_largest_cities(self):
        """Test search_multiple_salles with 10 largest French cities."""
        search_salles_result = self.api_client.search_multiple_salles(
            self.LARGEST_FRENCH_CITIES
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

    def test_search_tournois_with_largest_cities(self):
        """Test search_multiple_tournois with 10 largest French cities."""
        search_tournois_result = self.api_client.search_multiple_tournois(
            self.LARGEST_FRENCH_CITIES
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

    def test_search_pratiques_with_largest_cities(self):
        """Test search_multiple_pratiques with 10 largest French cities."""
        search_pratiques_result = self.api_client.search_multiple_pratiques(
            self.LARGEST_FRENCH_CITIES
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
