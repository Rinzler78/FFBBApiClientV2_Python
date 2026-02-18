"""Tests de conversion JSON brute pour les modeles FFBB API.

Section A: Integration tests - appels HTTP directs + from_dict sur JSON brut
Section B: Meilisearch - multi-search brute + from_dict sur resultats
Section C: Edge-case tests unitaires - from_dict avec donnees limites
"""

from __future__ import annotations

import os
import time
import unittest
from typing import Any

import requests

from ffbb_api_client_v2.config import (
    MEILISEARCH_BASE_URL,
    MEILISEARCH_ENDPOINT_MULTI_SEARCH,
)
from ffbb_api_client_v2.directus.client import DEFAULT_USER_AGENT
from ffbb_api_client_v2.directus_ffbb.config import (
    API_FFBB_BASE_URL,
    ENDPOINT_COMPETITIONS,
    ENDPOINT_CONFIGURATION,
    ENDPOINT_LIVES,
    ENDPOINT_ORGANISMES,
    ENDPOINT_POULES,
    ENDPOINT_SAISONS,
)
from ffbb_api_client_v2.directus_ffbb.models.configuration_models import (
    GetConfigurationResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_competition_response import (
    GetCompetitionResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_organisme_response import (
    GetOrganismeResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.lives import Clock, Live, lives_from_dict
from ffbb_api_client_v2.directus_ffbb.models.poules_models import GetPouleResponse
from ffbb_api_client_v2.directus_ffbb.models.rankings_models import (
    RankingEngagement,
    TeamRanking,
)
from ffbb_api_client_v2.directus_ffbb.models.saisons_models import GetSaisonsResponse
from ffbb_api_client_v2.meilisearch.models.multi_search_results_class import (
    MultiSearchResults,
    multi_search_results_from_dict,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.competitions_facet_distribution import (
    CompetitionsFacetDistribution,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_competitions import (
    CompetitionsMultiSearchResult,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_organismes import (
    OrganismesMultiSearchResult,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_pratiques import (
    PratiquesMultiSearchResult,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_rencontres import (
    RencontresMultiSearchResult,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_salles import (
    SallesMultiSearchResult,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_terrains import (
    TerrainsMultiSearchResult,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_tournois import (
    TournoisMultiSearchResult,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.organismes_facet_distribution import (
    OrganismesFacetDistribution,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.pratiques_facet_distribution import (
    PratiquesFacetDistribution,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.salles_facet_distribution import (
    SallesFacetDistribution,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.terrains_facet_distribution import (
    TerrainsFacetDistribution,
)
from ffbb_api_client_v2.models.game_stats_model import GameStatsModel
from ffbb_api_client_v2.models.niveau_models import (
    CategorieType,
    NiveauExtractor,
    NiveauInfo,
    NiveauType,
)

# ---------------------------------------------------------------------------
# Section A: Integration tests - API REST (api.ffbb.com)
# ---------------------------------------------------------------------------


@unittest.skipUnless(
    os.getenv("API_FFBB_APP_BEARER_TOKEN"),
    "API_FFBB_APP_BEARER_TOKEN not set",
)
class Test021RawApiRestConversion(unittest.TestCase):
    """Integration tests: raw HTTP calls to api.ffbb.com + from_dict conversion."""

    @classmethod
    def setUpClass(cls) -> None:
        api_token = os.environ["API_FFBB_APP_BEARER_TOKEN"]
        mls_token = os.getenv("MEILISEARCH_BEARER_TOKEN", "")

        cls.api_headers = {
            "Authorization": f"Bearer {api_token}",
            "user-agent": DEFAULT_USER_AGENT,
        }
        cls.mls_headers = {
            "Authorization": f"Bearer {mls_token}",
            "Content-Type": "application/json",
            "user-agent": DEFAULT_USER_AGENT,
        }

        # Discover dynamic IDs via Meilisearch searches
        cls.discovered_competition_id: int | None = None
        cls.discovered_organisme_id: int | None = None
        cls.discovered_poule_id: int | None = None

        if mls_token:
            cls._discover_ids()

    @classmethod
    def _discover_ids(cls) -> None:
        """Discover valid IDs by searching Meilisearch for 'Paris'."""
        url = f"{MEILISEARCH_BASE_URL}{MEILISEARCH_ENDPOINT_MULTI_SEARCH}"
        payload: dict[str, Any] = {
            "queries": [
                {
                    "indexUid": "ffbbserver_organismes",
                    "q": "Paris",
                    "limit": 1,
                },
                {
                    "indexUid": "ffbbserver_competitions",
                    "q": "Paris",
                    "limit": 1,
                },
            ]
        }

        try:
            resp = requests.post(url, headers=cls.mls_headers, json=payload, timeout=15)
            resp.raise_for_status()
            data = resp.json()

            results = data.get("results", [])
            for result in results:
                index_uid = result.get("indexUid", "")
                hits = result.get("hits", [])
                if not hits:
                    continue

                if index_uid == "ffbbserver_organismes" and hits:
                    cls.discovered_organisme_id = int(hits[0]["id"])

                if index_uid == "ffbbserver_competitions" and hits:
                    comp_id = hits[0].get("id")
                    if comp_id:
                        cls.discovered_competition_id = int(comp_id)
        except Exception:
            pass

        # Discover a poule ID from the competition if found
        if cls.discovered_competition_id:
            try:
                time.sleep(0.3)
                comp_url = (
                    f"{API_FFBB_BASE_URL}{ENDPOINT_COMPETITIONS}"
                    f"/{cls.discovered_competition_id}"
                    "?fields[]=id&fields[]=phases.poules.id"
                    "&deep[phases][poules][rencontres][_limit]=1"
                )
                resp = requests.get(comp_url, headers=cls.api_headers, timeout=15)
                if resp.ok:
                    comp_data = resp.json().get("data", {})
                    phases = comp_data.get("phases", [])
                    for phase in phases:
                        poules = phase.get("poules", [])
                        if poules:
                            cls.discovered_poule_id = int(poules[0]["id"])
                            break
            except Exception:
                pass

    def setUp(self) -> None:
        time.sleep(0.3)

    # -- test_001: Saisons --------------------------------------------------

    @unittest.skipUnless(os.getenv("API_FFBB_APP_BEARER_TOKEN"), "token required")
    def test_001_raw_saisons_conversion(self) -> None:
        """GET /items/ffbbserver_saisons -> GetSaisonsResponse.from_list."""
        url = f"{API_FFBB_BASE_URL}{ENDPOINT_SAISONS}"
        resp = requests.get(url, headers=self.api_headers, timeout=15)
        resp.raise_for_status()
        raw = resp.json()

        self.assertIn("data", raw)
        data_list = raw["data"]
        self.assertIsInstance(data_list, list)
        self.assertGreater(len(data_list), 0)

        saisons = GetSaisonsResponse.from_list(data_list)
        self.assertIsInstance(saisons, list)
        self.assertGreater(len(saisons), 0)

        for s in saisons:
            self.assertIsInstance(s, GetSaisonsResponse)
            self.assertIsInstance(s.id, str)
            self.assertTrue(len(s.id) > 0)
            if s.actif is not None:
                self.assertIsInstance(s.actif, bool)

    # -- test_002: Competition detail ---------------------------------------

    def test_002_raw_competition_conversion(self) -> None:
        """GET /items/ffbbserver_competitions/{id} -> GetCompetitionResponse.from_dict."""
        if not self.discovered_competition_id:
            self.skipTest("No competition ID discovered")

        url = (
            f"{API_FFBB_BASE_URL}{ENDPOINT_COMPETITIONS}"
            f"/{self.discovered_competition_id}"
            "?fields[]=id&fields[]=nom&fields[]=sexe&fields[]=saison"
            "&fields[]=code&fields[]=typeCompetition&fields[]=liveStat"
            "&fields[]=competition_origine&fields[]=competition_origine_nom"
            "&fields[]=publicationInternet&fields[]=categorie.code"
            "&fields[]=categorie.ordre"
            "&fields[]=typeCompetitionGenerique.id"
            "&fields[]=typeCompetitionGenerique.logo.id"
            "&fields[]=typeCompetitionGenerique.logo.gradient_color"
            "&fields[]=poules.id&fields[]=poules.nom"
            "&fields[]=phases.id&fields[]=phases.poules.id"
            "&fields[]=phases.poules.nom"
            "&deep[phases][poules][rencontres][_limit]=5"
        )
        resp = requests.get(url, headers=self.api_headers, timeout=20)
        resp.raise_for_status()
        raw = resp.json()

        actual_data = raw.get("data", raw)
        self.assertIsInstance(actual_data, dict)

        result = GetCompetitionResponse.from_dict(actual_data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, GetCompetitionResponse)
        self.assertIsInstance(result.id, str)
        self.assertTrue(len(result.id) > 0)

        # Validate top-level string fields
        if result.nom is not None:
            self.assertIsInstance(result.nom, str)
        if result.sexe is not None:
            self.assertIsInstance(result.sexe, str)
        if result.code is not None:
            self.assertIsInstance(result.code, str)

    # -- test_003: Organisme detail ----------------------------------------

    def test_003_raw_organisme_conversion(self) -> None:
        """GET /items/ffbbserver_organismes/{id} -> GetOrganismeResponse.from_dict."""
        if not self.discovered_organisme_id:
            self.skipTest("No organisme ID discovered")

        url = (
            f"{API_FFBB_BASE_URL}{ENDPOINT_ORGANISMES}"
            f"/{self.discovered_organisme_id}"
            "?fields[]=id&fields[]=nom&fields[]=code&fields[]=telephone"
            "&fields[]=adresse&fields[]=mail&fields[]=type"
            "&fields[]=urlSiteWeb&fields[]=nomClubPro"
            "&fields[]=commune.codePostal&fields[]=commune.libelle"
            "&fields[]=cartographie.latitude&fields[]=cartographie.longitude"
            "&fields[]=logo.id&fields[]=logo.gradient_color"
            "&fields[]=salle.libelle&fields[]=salle.adresse"
        )
        resp = requests.get(url, headers=self.api_headers, timeout=15)
        resp.raise_for_status()
        raw = resp.json()

        actual_data = raw.get("data", raw)
        self.assertIsInstance(actual_data, dict)

        result = GetOrganismeResponse.from_dict(actual_data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, GetOrganismeResponse)
        self.assertIsInstance(result.id, str)
        self.assertTrue(len(result.id) > 0)
        self.assertIsInstance(result.nom, str)

        # Nested commune check
        if result.commune is not None:
            if result.commune.code_postal is not None:
                self.assertIsInstance(result.commune.code_postal, str)
            if result.commune.libelle is not None:
                self.assertIsInstance(result.commune.libelle, str)

    # -- test_004: Poule detail --------------------------------------------

    def test_004_raw_poule_conversion(self) -> None:
        """GET /items/ffbbserver_poules/{id} -> GetPouleResponse.from_dict."""
        if not self.discovered_poule_id:
            self.skipTest("No poule ID discovered")

        url = (
            f"{API_FFBB_BASE_URL}{ENDPOINT_POULES}"
            f"/{self.discovered_poule_id}"
            "?fields[]=id&fields[]=rencontres.id&fields[]=rencontres.numero"
            "&fields[]=rencontres.numeroJournee&fields[]=rencontres.idPoule"
            "&fields[]=rencontres.competitionId"
            "&fields[]=rencontres.resultatEquipe1"
            "&fields[]=rencontres.resultatEquipe2&fields[]=rencontres.joue"
            "&fields[]=rencontres.nomEquipe1&fields[]=rencontres.nomEquipe2"
            "&fields[]=rencontres.date_rencontre"
            "&fields[]=classements.*"
            "&deep[rencontres][_limit]=10"
            "&deep[classements][_limit]=100"
        )
        resp = requests.get(url, headers=self.api_headers, timeout=15)
        resp.raise_for_status()
        raw = resp.json()

        actual_data = raw.get("data", raw)
        self.assertIsInstance(actual_data, dict)

        result = GetPouleResponse.from_dict(actual_data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, GetPouleResponse)
        self.assertIsInstance(result.id, str)
        self.assertIsInstance(result.rencontres, list)

        for r in result.rencontres[:3]:
            self.assertIsInstance(r.id, str)
            self.assertIsInstance(r.nomEquipe1, str)
            self.assertIsInstance(r.nomEquipe2, str)
            self.assertIsInstance(r.joue, int)

        # Validate classements if present
        if result.classements:
            for c in result.classements[:3]:
                self.assertIsInstance(c, TeamRanking)
                self.assertIsInstance(c.id, str)
                self.assertIsInstance(c.position, int)
                self.assertIsInstance(c.points, int)
                self.assertIsInstance(c.match_joues, int)
                self.assertIsInstance(c.quotient, float)

    # -- test_005: Lives ---------------------------------------------------

    def test_005_raw_lives_conversion(self) -> None:
        """GET /json/lives.json -> lives_from_dict conversion."""
        url = f"{API_FFBB_BASE_URL}{ENDPOINT_LIVES}"
        resp = requests.get(url, headers=self.api_headers, timeout=15)
        resp.raise_for_status()
        raw = resp.json()

        # lives endpoint returns a list directly
        self.assertIsInstance(raw, list)

        lives = lives_from_dict(raw)
        self.assertIsInstance(lives, list)

        for live in lives[:5]:
            self.assertIsInstance(live, Live)
            if live.clock is not None:
                self.assertIsInstance(live.clock, Clock)
                self.assertIsInstance(live.clock.minutes, int)
                self.assertIsInstance(live.clock.seconds, int)
                self.assertIsInstance(live.clock.milliseconds, int)
            if live.match_id is not None:
                self.assertIsInstance(live.match_id, int)
            if live.score_home is not None:
                self.assertIsInstance(live.score_home, int)
            if live.score_out is not None:
                self.assertIsInstance(live.score_out, int)

    # -- test_006: Configuration -------------------------------------------

    def test_006_raw_configuration_conversion(self) -> None:
        """GET /items/configuration -> GetConfigurationResponse.from_dict."""
        url = f"{API_FFBB_BASE_URL}{ENDPOINT_CONFIGURATION}"
        resp = requests.get(url, headers=self.api_headers, timeout=15)
        resp.raise_for_status()
        raw = resp.json()

        actual_data = raw.get("data", raw)
        self.assertIsInstance(actual_data, dict)

        result = GetConfigurationResponse.from_dict(actual_data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, GetConfigurationResponse)
        self.assertIsInstance(result.id, int)
        self.assertIsInstance(result.key_dh, str)
        self.assertTrue(len(result.key_dh) > 0)
        self.assertIsInstance(result.key_ms, str)
        self.assertTrue(len(result.key_ms) > 0)

        # Property aliases
        self.assertEqual(result.api_bearer_token, result.key_dh)
        self.assertEqual(result.meilisearch_token, result.key_ms)

    # -- test_007: GameStatsModel ------------------------------------------

    def test_007_raw_game_stats_conversion(self) -> None:
        """GameStatsModel.from_dict with realistic data dict."""
        data: dict[str, Any] = {
            "matchId": "12345",
            "currentStatus": "LIVE",
            "currentPeriod": "Q3",
            "score_q1_home": 22,
            "score_q2_home": 18,
            "score_q3_home": 15,
            "score_q4_home": None,
            "score_ot1_home": None,
            "score_ot2_home": None,
            "score_q1_out": 20,
            "score_q2_out": 16,
            "score_q3_out": 12,
            "score_q4_out": None,
            "score_ot1_out": None,
            "score_ot2_out": None,
        }
        result = GameStatsModel.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.match_id, "12345")
        self.assertEqual(result.current_status, "LIVE")
        self.assertEqual(result.current_period, "Q3")
        self.assertEqual(result.score_q1_home, 22)
        self.assertEqual(result.score_q2_home, 18)
        self.assertEqual(result.score_q3_home, 15)
        self.assertIsNone(result.score_q4_home)
        self.assertEqual(result.score_q1_out, 20)
        self.assertEqual(result.score_q2_out, 16)
        self.assertEqual(result.score_q3_out, 12)
        self.assertIsNone(result.score_q4_out)


# ---------------------------------------------------------------------------
# Section B: Integration tests - Meilisearch (meilisearch-prod.ffbb.app)
# ---------------------------------------------------------------------------


@unittest.skipUnless(
    os.getenv("MEILISEARCH_BEARER_TOKEN"),
    "MEILISEARCH_BEARER_TOKEN not set",
)
class Test021RawMeilisearchConversion(unittest.TestCase):
    """Integration tests: raw HTTP calls to Meilisearch + from_dict conversion."""

    @classmethod
    def setUpClass(cls) -> None:
        mls_token = os.environ["MEILISEARCH_BEARER_TOKEN"]
        cls.headers = {
            "Authorization": f"Bearer {mls_token}",
            "Content-Type": "application/json",
            "user-agent": DEFAULT_USER_AGENT,
        }
        cls.url = f"{MEILISEARCH_BASE_URL}{MEILISEARCH_ENDPOINT_MULTI_SEARCH}"

    def setUp(self) -> None:
        time.sleep(0.3)

    def _raw_multi_search(
        self,
        index_uid: str,
        query: str = "Paris",
        facets: list[str] | None = None,
        limit: int = 3,
    ) -> dict[str, Any]:
        """Helper: performs raw multi-search and returns the first result dict."""
        q: dict[str, Any] = {
            "indexUid": index_uid,
            "q": query,
            "limit": limit,
        }
        if facets:
            q["facets"] = facets
        payload = {"queries": [q]}
        resp = requests.post(self.url, headers=self.headers, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        self.assertGreater(len(results), 0, f"No results for {index_uid}")
        return results[0]

    # -- test_010: competitions search ------------------------------------

    def test_010_raw_search_competitions(self) -> None:
        """Meilisearch competitions -> CompetitionsMultiSearchResult.from_dict."""
        raw_result = self._raw_multi_search("ffbbserver_competitions")
        result = CompetitionsMultiSearchResult.from_dict(raw_result)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, CompetitionsMultiSearchResult)
        self.assertEqual(result.index_uid, "ffbbserver_competitions")
        self.assertIsNotNone(result.hits)
        self.assertIsInstance(result.hits, list)
        if result.processing_time_ms is not None:
            self.assertIsInstance(result.processing_time_ms, int)

    # -- test_011: organismes search --------------------------------------

    def test_011_raw_search_organismes(self) -> None:
        """Meilisearch organismes -> OrganismesMultiSearchResult.from_dict."""
        raw_result = self._raw_multi_search(
            "ffbbserver_organismes",
            facets=[
                "type_association.libelle",
                "type",
                "labellisation",
                "offresPratiques",
            ],
        )
        result = OrganismesMultiSearchResult.from_dict(raw_result)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, OrganismesMultiSearchResult)
        self.assertEqual(result.index_uid, "ffbbserver_organismes")
        self.assertIsNotNone(result.hits)
        self.assertIsInstance(result.hits, list)

        if result.facet_distribution is not None:
            self.assertIsInstance(
                result.facet_distribution, OrganismesFacetDistribution
            )

    # -- test_012: salles search ------------------------------------------

    def test_012_raw_search_salles(self) -> None:
        """Meilisearch salles -> SallesMultiSearchResult.from_dict."""
        raw_result = self._raw_multi_search("ffbbserver_salles")
        result = SallesMultiSearchResult.from_dict(raw_result)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, SallesMultiSearchResult)
        self.assertEqual(result.index_uid, "ffbbserver_salles")
        self.assertIsNotNone(result.hits)

        if result.facet_distribution is not None:
            self.assertIsInstance(result.facet_distribution, SallesFacetDistribution)

    # -- test_013: terrains search ----------------------------------------

    def test_013_raw_search_terrains(self) -> None:
        """Meilisearch terrains -> TerrainsMultiSearchResult.from_dict."""
        raw_result = self._raw_multi_search("ffbbserver_terrains")
        result = TerrainsMultiSearchResult.from_dict(raw_result)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, TerrainsMultiSearchResult)
        self.assertEqual(result.index_uid, "ffbbserver_terrains")
        self.assertIsNotNone(result.hits)

        if result.facet_distribution is not None:
            self.assertIsInstance(result.facet_distribution, TerrainsFacetDistribution)

    # -- test_014: rencontres search --------------------------------------

    def test_014_raw_search_rencontres(self) -> None:
        """Meilisearch rencontres -> RencontresMultiSearchResult.from_dict."""
        raw_result = self._raw_multi_search(
            "ffbbserver_rencontres",
            facets=[
                "competitionId.categorie.code",
                "competitionId.typeCompetition",
                "niveau",
                "competitionId.sexe",
            ],
        )
        result = RencontresMultiSearchResult.from_dict(raw_result)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, RencontresMultiSearchResult)
        self.assertEqual(result.index_uid, "ffbbserver_rencontres")
        self.assertIsNotNone(result.hits)

        if result.facet_distribution is not None:
            self.assertIsInstance(
                result.facet_distribution, CompetitionsFacetDistribution
            )

    # -- test_015: pratiques search ---------------------------------------

    def test_015_raw_search_pratiques(self) -> None:
        """Meilisearch pratiques -> PratiquesMultiSearchResult.from_dict."""
        raw_result = self._raw_multi_search(
            "ffbbnational_pratiques",
            query="basket",
            facets=["label", "type"],
        )
        result = PratiquesMultiSearchResult.from_dict(raw_result)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, PratiquesMultiSearchResult)
        self.assertEqual(result.index_uid, "ffbbnational_pratiques")
        self.assertIsNotNone(result.hits)

        if result.facet_distribution is not None:
            self.assertIsInstance(result.facet_distribution, PratiquesFacetDistribution)

    # -- test_016: tournois search ----------------------------------------

    def test_016_raw_search_tournois(self) -> None:
        """Meilisearch tournois -> TournoisMultiSearchResult.from_dict."""
        raw_result = self._raw_multi_search(
            "ffbbserver_tournois",
            facets=["sexe", "tournoiTypes3x3.libelle", "tournoiType"],
        )
        result = TournoisMultiSearchResult.from_dict(raw_result)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, TournoisMultiSearchResult)
        self.assertEqual(result.index_uid, "ffbbserver_tournois")
        self.assertIsNotNone(result.hits)

        if result.facet_distribution is not None:
            self.assertIsInstance(result.facet_distribution, TerrainsFacetDistribution)

    # -- test_017: full multi-search results wrapper ----------------------

    def test_017_raw_multi_search_results_wrapper(self) -> None:
        """Full multi-search across all indexes -> MultiSearchResults.from_dict."""
        payload: dict[str, Any] = {
            "queries": [
                {"indexUid": "ffbbserver_organismes", "q": "Paris", "limit": 1},
                {"indexUid": "ffbbserver_rencontres", "q": "Paris", "limit": 1},
                {"indexUid": "ffbbserver_competitions", "q": "Paris", "limit": 1},
                {"indexUid": "ffbbserver_salles", "q": "Paris", "limit": 1},
                {"indexUid": "ffbbserver_terrains", "q": "Paris", "limit": 1},
                {"indexUid": "ffbbserver_tournois", "q": "Paris", "limit": 1},
                {"indexUid": "ffbbnational_pratiques", "q": "basket", "limit": 1},
            ]
        }
        resp = requests.post(self.url, headers=self.headers, json=payload, timeout=20)
        resp.raise_for_status()
        raw = resp.json()

        result = multi_search_results_from_dict(raw)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, MultiSearchResults)
        self.assertIsNotNone(result.results)
        self.assertGreater(len(result.results), 0)


# ---------------------------------------------------------------------------
# Section C: Edge-case / unit tests
# ---------------------------------------------------------------------------


class Test021FromDictEdgeCases(unittest.TestCase):
    """Unit tests for from_dict with edge-case data."""

    # -- test_020: from_dict(None) -----------------------------------------

    def test_020_from_dict_with_none(self) -> None:
        """All models with None-safety should return None for from_dict(None)."""
        self.assertIsNone(GetSaisonsResponse.from_dict(None))  # type: ignore[arg-type]
        self.assertIsNone(GetCompetitionResponse.from_dict(None))  # type: ignore[arg-type]
        self.assertIsNone(GetOrganismeResponse.from_dict(None))  # type: ignore[arg-type]
        self.assertIsNone(GetPouleResponse.from_dict(None))  # type: ignore[arg-type]
        self.assertIsNone(GameStatsModel.from_dict(None))  # type: ignore[arg-type]
        self.assertIsNone(TeamRanking.from_dict(None))  # type: ignore[arg-type]
        self.assertIsNone(RankingEngagement.from_dict(None))  # type: ignore[arg-type]

    # -- test_021: from_dict({}) -------------------------------------------

    def test_021_from_dict_with_empty_dict(self) -> None:
        """from_dict({}) should not crash - may return None or default."""
        self.assertIsNone(GetSaisonsResponse.from_dict({}))
        self.assertIsNone(GetCompetitionResponse.from_dict({}))
        self.assertIsNone(GetOrganismeResponse.from_dict({}))
        self.assertIsNone(GetPouleResponse.from_dict({}))
        self.assertIsNone(GameStatsModel.from_dict({}))
        self.assertIsNone(TeamRanking.from_dict({}))
        self.assertIsNone(RankingEngagement.from_dict({}))

    # -- test_022: from_dict with errors key -------------------------------

    def test_022_from_dict_with_errors_key(self) -> None:
        """from_dict with 'errors' key should return None (API error response)."""
        error_data: dict[str, Any] = {"errors": [{"message": "Not found"}]}
        self.assertIsNone(GetSaisonsResponse.from_dict(error_data))
        self.assertIsNone(GetCompetitionResponse.from_dict(error_data))
        self.assertIsNone(GetOrganismeResponse.from_dict(error_data))
        self.assertIsNone(GetPouleResponse.from_dict(error_data))

    # -- test_023: from_dict with non-dict ---------------------------------

    def test_023_from_dict_with_non_dict(self) -> None:
        """from_dict with non-dict input should return None."""
        self.assertIsNone(GetSaisonsResponse.from_dict("string"))  # type: ignore[arg-type]
        self.assertIsNone(GetCompetitionResponse.from_dict("string"))  # type: ignore[arg-type]
        self.assertIsNone(GetOrganismeResponse.from_dict("string"))  # type: ignore[arg-type]
        self.assertIsNone(GetPouleResponse.from_dict("string"))  # type: ignore[arg-type]
        self.assertIsNone(GameStatsModel.from_dict("string"))  # type: ignore[arg-type]
        self.assertIsNone(TeamRanking.from_dict("string"))  # type: ignore[arg-type]

    # -- test_024: from_dict with minimal fields ---------------------------

    def test_024_from_dict_minimal_fields(self) -> None:
        """from_dict with only minimal required fields should produce valid objects."""
        # Saison with just id
        s = GetSaisonsResponse.from_dict({"id": "42"})
        self.assertIsNotNone(s)
        self.assertEqual(s.id, "42")
        self.assertIsNone(s.actif)

        # Configuration with just required fields
        c = GetConfigurationResponse.from_dict(
            {"id": 1, "key_dh": "tok1", "key_ms": "tok2"}
        )
        self.assertIsNotNone(c)
        self.assertEqual(c.id, 1)
        self.assertEqual(c.key_dh, "tok1")
        self.assertEqual(c.key_ms, "tok2")
        self.assertIsNone(c.ios_version)
        self.assertIsNone(c.android_version)

        # GameStatsModel with just matchId
        g = GameStatsModel.from_dict({"matchId": "99"})
        self.assertIsNotNone(g)
        self.assertEqual(g.match_id, "99")
        self.assertIsNone(g.current_status)
        self.assertIsNone(g.score_q1_home)

    # -- test_025: Clock.from_str ------------------------------------------

    def test_025_clock_from_str(self) -> None:
        """Clock.from_str parses minutes:seconds:milliseconds."""
        clock = Clock.from_str("10:30:500")
        self.assertEqual(clock.minutes, 10)
        self.assertEqual(clock.seconds, 30)
        self.assertEqual(clock.milliseconds, 500)

        # Round-trip
        self.assertEqual(clock.to_str(), "10:30:500")

        # Zero values
        clock_zero = Clock.from_str("0:0:0")
        self.assertEqual(clock_zero.minutes, 0)
        self.assertEqual(clock_zero.seconds, 0)
        self.assertEqual(clock_zero.milliseconds, 0)

        # Empty string (fallback)
        clock_empty = Clock.from_str("")
        self.assertEqual(clock_empty.minutes, 0)
        self.assertEqual(clock_empty.seconds, 0)
        self.assertEqual(clock_empty.milliseconds, 0)

    # -- test_026: NiveauExtractor -----------------------------------------

    def test_026_niveau_extraction(self) -> None:
        """NiveauExtractor.extract_niveau with various patterns."""
        # Departemental
        n = NiveauExtractor.extract_niveau("D1 masculine seniors")
        self.assertIsNotNone(n)
        self.assertIsInstance(n, NiveauInfo)
        self.assertEqual(n.type, NiveauType.DEPARTEMENTAL)
        self.assertEqual(n.division, 1)

        # Regional
        n = NiveauExtractor.extract_niveau("R2 feminine U17")
        self.assertIsNotNone(n)
        self.assertEqual(n.type, NiveauType.REGIONAL)
        self.assertEqual(n.division, 2)
        self.assertEqual(n.categorie, CategorieType.U17)

        # Elite
        n = NiveauExtractor.extract_niveau("ELITE masculine seniors")
        self.assertIsNotNone(n)
        self.assertEqual(n.type, NiveauType.ELITE)
        self.assertTrue(n.is_elite)
        self.assertEqual(n.zone_effective, "regional")
        self.assertEqual(n.zone_geographique, "regional")

        # National
        n = NiveauExtractor.extract_niveau("NATIONAL 1 masculine")
        self.assertIsNotNone(n)
        self.assertEqual(n.type, NiveauType.NATIONAL)

        # None for unrecognized
        n = NiveauExtractor.extract_niveau("random text")
        self.assertIsNone(n)

        # None for empty
        n = NiveauExtractor.extract_niveau("")
        self.assertIsNone(n)

    # -- test_027: RankingEngagement.from_dict -----------------------------

    def test_027_ranking_engagement_from_dict(self) -> None:
        """RankingEngagement.from_dict with logo parsing and optional fields."""
        data: dict[str, Any] = {
            "id": "eng-001",
            "nom": "Club Paris BC",
            "nomUsuel": "Paris BC",
            "codeAbrege": "PBC",
            "numeroEqu": "1",
            "numeroEquipe": "001",
            "logo": {"id": "logo-123", "gradient_color": "#FF0000"},
        }
        eng = RankingEngagement.from_dict(data)
        self.assertIsNotNone(eng)
        self.assertEqual(eng.id, "eng-001")
        self.assertEqual(eng.nom, "Club Paris BC")
        self.assertEqual(eng.nom_usuel, "Paris BC")
        self.assertEqual(eng.code_abrege, "PBC")
        self.assertEqual(eng.numero_equ, "1")
        self.assertEqual(eng.numero_equipe, "001")
        self.assertEqual(eng.logo_id, "logo-123")
        self.assertEqual(eng.logo_gradient, "#FF0000")

        # Without logo
        eng_no_logo = RankingEngagement.from_dict({"id": "eng-002", "nom": "Club Lyon"})
        self.assertIsNotNone(eng_no_logo)
        self.assertIsNone(eng_no_logo.logo_id)
        self.assertIsNone(eng_no_logo.logo_gradient)

    # -- test_028: TeamRanking.from_dict -----------------------------------

    def test_028_team_ranking_from_dict(self) -> None:
        """TeamRanking.from_dict with all numeric fields and nested organisme."""
        data: dict[str, Any] = {
            "id": "rank-001",
            "position": 1,
            "points": 30,
            "matchJoues": 15,
            "gagnes": 14,
            "perdus": 1,
            "nuls": 0,
            "nombreForfaits": 0,
            "nombreDefauts": 0,
            "paniersMarques": 1200,
            "paniersEncaisses": 900,
            "difference": 300,
            "quotient": 1.333,
            "pointInitiaux": 0,
            "penalitesArbitrage": 0,
            "penalitesEntraineur": 0,
            "penalitesDiverses": 0,
            "horsClassement": False,
            "idEngagement": {
                "id": "eng-001",
                "nom": "Paris BC",
                "logo": {"id": "logo-1", "gradient_color": "#00F"},
            },
            "organisme": {
                "id": "org-001",
                "nom": "Organisme Paris",
                "nom_simple": "Paris",
                "logo": {"id": "org-logo-1"},
            },
            "idPoule": {"id": "poule-001"},
            "idCompetition": "comp-001",
        }
        tr = TeamRanking.from_dict(data)
        self.assertIsNotNone(tr)
        self.assertEqual(tr.id, "rank-001")
        self.assertEqual(tr.position, 1)
        self.assertEqual(tr.points, 30)
        self.assertEqual(tr.match_joues, 15)
        self.assertEqual(tr.gagnes, 14)
        self.assertEqual(tr.perdus, 1)
        self.assertEqual(tr.nuls, 0)
        self.assertEqual(tr.nombre_forfaits, 0)
        self.assertEqual(tr.nombre_defauts, 0)
        self.assertEqual(tr.paniers_marques, 1200)
        self.assertEqual(tr.paniers_encaisses, 900)
        self.assertEqual(tr.difference, 300)
        self.assertAlmostEqual(tr.quotient, 1.333, places=2)
        self.assertEqual(tr.point_initiaux, 0)
        self.assertEqual(tr.penalites_arbitrage, 0)
        self.assertEqual(tr.penalites_entraineur, 0)
        self.assertEqual(tr.penalites_diverses, 0)
        self.assertFalse(tr.hors_classement)

        # Nested idEngagement
        self.assertIsNotNone(tr.id_engagement)
        self.assertEqual(tr.id_engagement.id, "eng-001")
        self.assertEqual(tr.id_engagement.nom, "Paris BC")
        self.assertEqual(tr.id_engagement.logo_id, "logo-1")

        # Nested organisme
        self.assertEqual(tr.organisme_id, "org-001")
        self.assertEqual(tr.organisme_nom, "Organisme Paris")
        self.assertEqual(tr.organisme_nom_simple, "Paris")
        self.assertEqual(tr.organisme_logo_id, "org-logo-1")

        # Nested idPoule
        self.assertEqual(tr.id_poule_id, "poule-001")

        # idCompetition
        self.assertEqual(tr.id_competition, "comp-001")

    # -- test_029: Live.from_dict with full data ---------------------------

    def test_029_live_from_dict(self) -> None:
        """Live.from_dict with complete data dict."""
        data: dict[str, Any] = {
            "matchId": "99999",
            "matchTime": "2025-03-15T20:00:00",
            "competitionAbgName": "LNB Pro A",
            "score_q1_home": 22,
            "score_q2_home": 18,
            "score_q3_home": 20,
            "score_q4_home": 25,
            "score_q1_out": 19,
            "score_q2_out": 21,
            "score_q3_out": 17,
            "score_q4_out": 23,
            "score_ot1_home": None,
            "score_ot2_home": None,
            "score_ot1_out": None,
            "score_ot2_out": None,
            "score_home": 85,
            "score_out": 80,
            "clock": "5:30:0",
            "competitionName": "LNB Pro A 2024-2025",
            "currentStatus": "FINISHED",
            "currentPeriod": "Q4",
            "matchStatus": "COMPLETED",
            "teamName_home": "Paris Basketball",
            "teamName_out": "AS Monaco",
            "externalId": None,
            "teamEngagement_home": None,
            "teamEngagement_out": None,
        }
        live = Live.from_dict(data)
        self.assertIsInstance(live, Live)
        self.assertEqual(live.match_id, 99999)
        self.assertEqual(live.competition_abg_name, "LNB Pro A")
        self.assertEqual(live.score_q1_home, 22)
        self.assertEqual(live.score_q4_home, 25)
        self.assertEqual(live.score_home, 85)
        self.assertEqual(live.score_out, 80)
        self.assertIsNotNone(live.clock)
        self.assertEqual(live.clock.minutes, 5)
        self.assertEqual(live.clock.seconds, 30)
        self.assertEqual(live.clock.milliseconds, 0)
        self.assertEqual(live.team_name_home, "Paris Basketball")
        self.assertEqual(live.team_name_out, "AS Monaco")

    # -- test_030: from_list edge cases -----------------------------------

    def test_030_saisons_from_list_edge_cases(self) -> None:
        """GetSaisonsResponse.from_list with edge-case data."""
        # Empty list
        self.assertEqual(GetSaisonsResponse.from_list([]), [])

        # None list
        self.assertEqual(GetSaisonsResponse.from_list(None), [])  # type: ignore[arg-type]

        # Mixed valid / invalid items
        mixed = [
            {"id": "1", "nom": "Saison 2024"},
            None,
            {"errors": [{"message": "error"}]},
            {"id": "2", "nom": "Saison 2025", "actif": True},
        ]
        result = GetSaisonsResponse.from_list(mixed)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[1].id, "2")
        self.assertTrue(result[1].actif)

    # -- test_031: NiveauInfo methods -------------------------------------

    def test_031_niveau_info_methods(self) -> None:
        """NiveauInfo.matches_filter and properties."""
        info = NiveauInfo(
            type=NiveauType.DEPARTEMENTAL,
            division=1,
            categorie=CategorieType.SENIOR,
            raw_text="D1",
        )
        self.assertFalse(info.is_elite)
        self.assertEqual(info.zone_effective, "departemental")
        self.assertTrue(info.matches_filter("departemental", 1))
        self.assertFalse(info.matches_filter("departemental", 2))
        self.assertFalse(info.matches_filter("regional"))

        # Elite info
        elite = NiveauInfo(
            type=NiveauType.ELITE,
            raw_text="ELITE",
            zone_geographique="regional",
        )
        self.assertTrue(elite.is_elite)
        self.assertEqual(elite.zone_effective, "regional")
        self.assertTrue(elite.matches_filter("regional"))

    # -- test_032: NiveauExtractor.extract_from_competition_data ----------

    def test_032_extract_from_competition_data(self) -> None:
        """NiveauExtractor.extract_from_competition_data fallback to code."""
        # With nom
        result = NiveauExtractor.extract_from_competition_data(
            {"nom": "D2 masculine seniors", "code": "XXX"}
        )
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.DEPARTEMENTAL)
        self.assertEqual(result.division, 2)

        # Fallback to code when nom doesn't match
        result = NiveauExtractor.extract_from_competition_data(
            {"nom": "something unknown", "code": "R1 feminine"}
        )
        self.assertIsNotNone(result)
        self.assertEqual(result.type, NiveauType.REGIONAL)

        # Neither matches
        result = NiveauExtractor.extract_from_competition_data(
            {"nom": "unknown", "code": "unknown"}
        )
        self.assertIsNone(result)

        # Empty dict
        result = NiveauExtractor.extract_from_competition_data({})
        self.assertIsNone(result)

    # -- test_033: Poule with classements ---------------------------------

    def test_033_poule_from_dict_with_classements(self) -> None:
        """GetPouleResponse.from_dict with classements data."""
        data: dict[str, Any] = {
            "id": "poule-1",
            "rencontres": [
                {
                    "id": "r-1",
                    "numero": "1",
                    "numeroJournee": "1",
                    "idPoule": "poule-1",
                    "competitionId": "comp-1",
                    "resultatEquipe1": "85",
                    "resultatEquipe2": "72",
                    "joue": True,
                    "nomEquipe1": "Team A",
                    "nomEquipe2": "Team B",
                    "date_rencontre": "2025-01-15",
                },
            ],
            "classements": [
                {
                    "id": "c-1",
                    "position": 1,
                    "points": 10,
                    "matchJoues": 5,
                    "gagnes": 5,
                    "perdus": 0,
                    "nombreForfaits": 0,
                    "paniersMarques": 400,
                    "paniersEncaisses": 300,
                    "difference": 100,
                    "quotient": 1.333,
                },
            ],
        }
        result = GetPouleResponse.from_dict(data)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "poule-1")
        self.assertEqual(len(result.rencontres), 1)
        self.assertEqual(result.rencontres[0].nomEquipe1, "Team A")
        self.assertEqual(result.rencontres[0].joue, 1)

        self.assertIsNotNone(result.classements)
        self.assertEqual(len(result.classements), 1)
        self.assertEqual(result.classements[0].position, 1)
        self.assertEqual(result.classements[0].points, 10)

    # -- test_034: Configuration complete ---------------------------------

    def test_034_configuration_all_fields(self) -> None:
        """GetConfigurationResponse.from_dict with all optional fields."""
        data: dict[str, Any] = {
            "id": 1,
            "key_dh": "api_token_val",
            "key_ms": "mls_token_val",
            "key_directus_website": "web_key",
            "key_directus_competitions": "comp_key",
            "ios_version": "3.0.1",
            "android_version": "3.0.2",
            "date_created": "2024-01-01T00:00:00Z",
            "date_updated": "2025-06-01T12:00:00Z",
        }
        result = GetConfigurationResponse.from_dict(data)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.key_dh, "api_token_val")
        self.assertEqual(result.key_ms, "mls_token_val")
        self.assertEqual(result.key_directus_website, "web_key")
        self.assertEqual(result.key_directus_competitions, "comp_key")
        self.assertEqual(result.ios_version, "3.0.1")
        self.assertEqual(result.android_version, "3.0.2")
        self.assertEqual(result.date_created, "2024-01-01T00:00:00Z")
        self.assertEqual(result.date_updated, "2025-06-01T12:00:00Z")
        self.assertEqual(result.api_bearer_token, "api_token_val")
        self.assertEqual(result.meilisearch_token, "mls_token_val")

    # -- test_035: Live.from_dict with TeamEngagement ----------------------

    def test_035_live_with_team_engagement(self) -> None:
        """Live.from_dict with nested teamEngagement data."""
        data: dict[str, Any] = {
            "matchId": "100",
            "clock": "10:0:0",
            "teamEngagement_home": {
                "nomOfficiel": "Paris BC Officiel",
                "nomUsuel": "Paris BC",
                "codeAbrege": "PBC",
                "logo": None,
            },
            "teamEngagement_out": {
                "nomOfficiel": "Lyon BC Officiel",
                "nomUsuel": "Lyon BC",
                "codeAbrege": "LBC",
                "logo": None,
            },
        }
        live = Live.from_dict(data)
        self.assertIsNotNone(live.team_engagement_home)
        self.assertEqual(live.team_engagement_home.nom_officiel, "Paris BC Officiel")
        self.assertEqual(live.team_engagement_home.nom_usuel, "Paris BC")
        self.assertEqual(live.team_engagement_home.code_abrege, "PBC")

        self.assertIsNotNone(live.team_engagement_out)
        self.assertEqual(live.team_engagement_out.nom_officiel, "Lyon BC Officiel")

    # -- test_036: Live.from_dict with ExternalID --------------------------

    def test_036_live_with_external_id(self) -> None:
        """Live.from_dict with nested externalId data."""
        data: dict[str, Any] = {
            "matchId": "200",
            "clock": "0:0:0",
            "externalId": {
                "nomEquipe1": "Team A",
                "nomEquipe2": "Team B",
                "numeroJournee": "5",
                "competitionId": {
                    "code": "C001",
                    "nom": "Championnat",
                    "sexe": "M",
                    "typeCompetition": "CHAMP",
                },
                "idOrganismeEquipe1": None,
                "idOrganismeEquipe2": None,
                "salle": None,
                "idPoule": None,
            },
        }
        live = Live.from_dict(data)
        self.assertIsNotNone(live.external_id)
        self.assertEqual(live.external_id.nom_equipe1, "Team A")
        self.assertEqual(live.external_id.nom_equipe2, "Team B")
        self.assertEqual(live.external_id.numero_journee, 5)
        self.assertIsNotNone(live.external_id.competition_id)
        self.assertEqual(live.external_id.competition_id.code, "C001")
        self.assertEqual(live.external_id.competition_id.sexe, "M")


if __name__ == "__main__":
    unittest.main()
