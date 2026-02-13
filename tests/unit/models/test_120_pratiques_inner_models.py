"""Round-trip tests for inner models in multi_search_result_pratiques.py."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_pratiques import (
    PratiquesMultiSearchResult,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.pratiques_facet_distribution import (
    PratiquesFacetDistribution,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.pratiques_hit import PratiquesHit
from ffbb_api_client_v2.meilisearch_ffbb.models.pratiques_type_class import (
    PratiquesTypeClass as TypeClass,
)
from ffbb_api_client_v2.models.affiche import Affiche
from ffbb_api_client_v2.models.cartographie import Cartographie
from ffbb_api_client_v2.models.coordonnees import Coordonnees
from ffbb_api_client_v2.models.geo import Geo


class Test042PratiquesInnerModels(unittest.TestCase):
    def _assert_stable(self, model_class: type, input_data: dict[str, Any]) -> None:
        obj1 = model_class.from_dict(input_data)
        dict1 = obj1.to_dict()
        obj2 = model_class.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2, f"{model_class.__name__} round-trip not stable")

    def test_000_type_class_full(self) -> None:
        self._assert_stable(
            TypeClass,
            {
                "Basket Inclusif": 3,
                "Basket Santé": 10,
                "Basket Tonik": 5,
                "Centre Génération Basket": 2,
                "Micro Basket": 8,
            },
        )

    def test_001_pratiques_facet_distribution_full(self) -> None:
        self._assert_stable(
            PratiquesFacetDistribution,
            {
                "label": {"Basket Santé Découverte": 15, "BaskeTonik": 8},
                "type": {
                    "Basket Inclusif": 3,
                    "Basket Santé": 10,
                    "Basket Tonik": 5,
                    "Centre Génération Basket": 2,
                    "Micro Basket": 8,
                },
            },
        )

    def test_002_affiche_full(self) -> None:
        self._assert_stable(
            Affiche,
            {
                "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "gradient_color": "#FF5733",
                "width": 800,
                "height": 600,
            },
        )

    def test_003_coordonnees_full(self) -> None:
        self._assert_stable(
            Coordonnees,
            {"type": "Point", "coordinates": [2.3522, 48.8566]},
        )

    def test_004_cartographie_full(self) -> None:
        self._assert_stable(
            Cartographie,
            {
                "adresse": "12 rue du Sport",
                "codePostal": "75001",
                "coordonnees": {"type": "Point", "coordinates": [2.3522, 48.8566]},
                "date_created": None,
                "date_updated": None,
                "id": "carto-001",
                "latitude": 48.8566,
                "longitude": 2.3522,
                "title": "Gymnase Central",
                "ville": "Paris",
                "status": "draft",
            },
        )

    def test_005_geo_full(self) -> None:
        self._assert_stable(Geo, {"lat": 48.8566, "lng": 2.3522})

    def test_006_pratiques_hit_with_all_fields(self) -> None:
        """PratiquesHit with cartographie, affiche, geo, and enums populated."""
        self._assert_stable(
            PratiquesHit,
            {
                "titre": "Basket Sante Decouverte",
                "type": "Basket Santé",
                "adresse": "10 rue des Sports",
                "description": "Seances adaptees",
                "id": "777",
                "date_created": "2024-01-01T00:00:00",
                "date_debut": "2024-09-01T00:00:00",
                "date_demande": None,
                "date_fin": "2025-06-30T00:00:00",
                "date_updated": "2024-06-01T00:00:00",
                "facebook": None,
                "site_web": "https://club.fr",
                "twitter": None,
                "action": "Decouverte",
                "adresse_salle": "Gymnase A",
                "adresse_structure": "10 avenue B",
                "assurance": "Assurance X",
                "code": "BS-001",
                "cp_salle": "75015",
                "date_inscription": None,
                "email": "bs@club.fr",
                "engagement": "Engagement 1",
                "horaires_seances": "Mercredi 14h-16h",
                "inscriptions": "Ouvertes",
                "jours": ["mercredi", "samedi"],
                "label": "Basket Santé Découverte",
                "latitude": None,
                "longitude": None,
                "mail_demandeur": "user@test.fr",
                "mail_structure": "structure@test.fr",
                "nom_demandeur": "Dupont",
                "nom_salle": "Gymnase A",
                "nom_structure": "Club Sante",
                "nombre_personnes": "20",
                "nombre_seances": "30",
                "objectif": "Préventif",
                "prenom_demandeur": "Jean",
                "public": "Adultes",
                "telephone": "0100000003",
                "ville_salle": "Paris",
                "cartographie": {
                    "adresse": "10 rue des Sports",
                    "codePostal": "75015",
                    "coordonnees": {"type": "Point", "coordinates": [2.30, 48.84]},
                    "date_created": None,
                    "date_updated": None,
                    "id": "carto-002",
                    "latitude": 48.84,
                    "longitude": 2.30,
                    "title": None,
                    "ville": "Paris",
                },
                "affiche": {
                    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                    "gradient_color": "#003366",
                    "width": 400,
                    "height": 300,
                },
                "_geo": {"lat": 48.84, "lng": 2.30},
                "date_debut_timestamp": 1725148800,
                "date_fin_timestamp": 1751241600,
                "thumbnail": "https://img.ffbb.fr/thumb.jpg",
            },
        )

    def test_007_pratiques_result_with_facets(self) -> None:
        """PratiquesMultiSearchResult with facets and type."""
        self._assert_stable(
            PratiquesMultiSearchResult,
            {
                "indexUid": "ffbbnational_pratiques",
                "hits": [
                    {
                        "id": "999",
                        "titre": "Basket Sante",
                        "facebook": None,
                        "twitter": None,
                        "latitude": None,
                        "longitude": None,
                    }
                ],
                "query": "basket",
                "processingTimeMs": 3,
                "limit": 20,
                "offset": 0,
                "estimatedTotalHits": 50,
                "facetDistribution": {
                    "label": {"Basket Santé Découverte": 10},
                    "type": {"Basket Santé": 20, "Micro Basket": 5},
                },
            },
        )


if __name__ == "__main__":
    unittest.main()
