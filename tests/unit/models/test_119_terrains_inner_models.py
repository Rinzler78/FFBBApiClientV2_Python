"""Round-trip tests for inner models in multi_search_result_terrains.py."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.multi_search_result_terrains import (
    TerrainsMultiSearchResult,
)
from ffbb_api_client_v2.models.sexe_class import SexeClass
from ffbb_api_client_v2.models.terrains_facet_distribution import (
    TerrainsFacetDistribution,
)
from ffbb_api_client_v2.models.terrains_hit import TerrainsHit
from ffbb_api_client_v2.models.tournoi_types_3x3 import TournoiTypes3X3
from ffbb_api_client_v2.models.tournoi_types_3x3_libelle import TournoiTypes3X3Libelle


class Test041TerrainsInnerModels(unittest.TestCase):
    def _assert_stable(self, model_class: type, input_data: dict[str, Any]) -> None:
        obj1 = model_class.from_dict(input_data)
        dict1 = obj1.to_dict()
        obj2 = model_class.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2, f"{model_class.__name__} round-trip not stable")

    def test_001_sexe_class_full(self) -> None:
        self._assert_stable(
            SexeClass,
            {"Féminin": 5, "Masculin": 10, "Mixte": 2},
        )

    def test_002_tournoi_types3x3_libelle_full(self) -> None:
        self._assert_stable(
            TournoiTypes3X3Libelle,
            {
                "Open Plus - Junior league 3x3": 3,
                "Open Plus - Super league 3x3": 2,
                "Open Plus Access - Junior league 3x3": 1,
                "Open Plus Access - Super league 3x3": 4,
                "Open Start - Junior league 3x3": 5,
                "Open Start - Super league 3x3": 6,
            },
        )

    def test_003_terrains_facet_distribution_full(self) -> None:
        self._assert_stable(
            TerrainsFacetDistribution,
            {
                "sexe": {"Féminin": 5, "Masculin": 10, "Mixte": 2},
                "tournoiType": {"Open Plus": 3, "Open Plus Access": 1, "Open Start": 5},
                "tournoiTypes3x3.libelle": {
                    "Open Plus - Junior league 3x3": 3,
                    "Open Plus - Super league 3x3": 2,
                    "Open Plus Access - Junior league 3x3": 1,
                    "Open Plus Access - Super league 3x3": 4,
                    "Open Start - Junior league 3x3": 5,
                    "Open Start - Super league 3x3": 6,
                },
            },
        )

    def test_004_tournoi_types3x3_full(self) -> None:
        self._assert_stable(
            TournoiTypes3X3,
            {
                "libelle": "Open Plus - Junior league 3x3",
                "logo": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "type_league": "junior",
                "type_tournois": "1",
            },
        )

    def test_005_terrains_hit_with_full_data(self) -> None:
        """TerrainsHit with all fields populated for to_dict coverage."""
        self._assert_stable(
            TerrainsHit,
            {
                "nom": "Terrain Paris",
                "rue": "Quai de Bercy",
                "id": "555",
                "accesLibre": True,
                "date_created": "2024-03-01T00:00:00",
                "date_updated": "2024-06-01T00:00:00",
                "largeur": 15,
                "longueur": 28,
                "numero": 1,
                "cartographie": {
                    "adresse": "Parc de Bercy",
                    "codePostal": "75012",
                    "coordonnees": None,
                    "date_created": None,
                    "date_updated": None,
                    "id": "carto-001",
                    "latitude": 48.834,
                    "longitude": 2.386,
                    "title": None,
                    "ville": "Paris",
                },
                "commune": {
                    "codeInsee": None,
                    "codePostal": "75012",
                    "date_created": None,
                    "date_updated": None,
                    "id": "12012",
                    "libelle": "Paris 12e",
                    "departement": "Paris",
                },
                "natureSol": {
                    "code": "BIT",
                    "date_created": "2024-01-01T00:00:00",
                    "date_updated": None,
                    "id": "ns-1",
                    "libelle": "Bitume",
                    "terrain": "true",
                },
                "_geo": {"lat": 48.834, "lng": 2.386},
                "thumbnail": None,
                "type": "Terrain",
            },
        )

    def test_006_terrains_result_with_facets(self) -> None:
        """TerrainsMultiSearchResult with facet distribution."""
        self._assert_stable(
            TerrainsMultiSearchResult,
            {
                "indexUid": "ffbbserver_terrains",
                "hits": [
                    {
                        "id": "111",
                        "nom": "Terrain Y",
                        "thumbnail": None,
                    }
                ],
                "query": "test",
                "processingTimeMs": 5,
                "limit": 20,
                "offset": 0,
                "estimatedTotalHits": 1,
                "facetDistribution": {
                    "sexe": {"Féminin": 3, "Masculin": 7, "Mixte": 1},
                    "tournoiType": {"Open Plus": 3},
                    "tournoiTypes3x3.libelle": {
                        "Open Plus - Junior league 3x3": 2,
                    },
                },
            },
        )


if __name__ == "__main__":
    unittest.main()
