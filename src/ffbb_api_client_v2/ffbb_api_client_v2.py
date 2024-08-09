from typing import List

from requests_cache import CachedSession

from ffbb_api_client_v2.meilisearch_ffbb_client import MeilisearchFFBBClient

from .api_ffbb_app_client import ApiFFBBAppClient
from .http_requests_helper import default_cached_session
from .lives import Live
from .multi_search_query import (
    CompetitionsMultiSearchQuery,
    OrganismesMultiSearchQuery,
    PratiquesMultiSearchQuery,
    RencontresMultiSearchQuery,
    SallesMultiSearchQuery,
    TerrainsMultiSearchQuery,
    TournoisMultiSearchQuery,
)
from .MultiSearchResultCompetitions import CompetitionsMultiSearchResult
from .MultiSearchResultOrganismes import OrganismesMultiSearchResult
from .MultiSearchResultPratiques import PratiquesMultiSearchResult
from .MultiSearchResultRencontres import RencontresMultiSearchResult
from .MultiSearchResultSalles import SallesMultiSearchResult
from .MultiSearchResultTerrains import TerrainsMultiSearchResult
from .MultiSearchResultTournois import TournoisMultiSearchResult


class FFBBAPIClientV2:
    def __init__(
        self,
        api_ffbb_client: ApiFFBBAppClient,
        meilisearch_ffbb_client: MeilisearchFFBBClient,
    ):
        self.api_ffbb_client = api_ffbb_client
        self.meilisearch_ffbb_client = meilisearch_ffbb_client

    @staticmethod
    def create(
        meilisearch_bearer_token: str,
        api_bearer_token: str,
        debug: bool = False,
        cached_session: CachedSession = default_cached_session,
    ) -> "FFBBAPIClientV2":
        if not api_bearer_token:
            raise ValueError("Api Bearer token cannot be None or empty.")

        api_ffbb_client = ApiFFBBAppClient(
            api_bearer_token, debug=debug, cached_session=cached_session
        )

        if not meilisearch_bearer_token:
            raise ValueError("Meilisearch Bearer token cannot be None or empty.")

        meilisearch_ffbb_client: MeilisearchFFBBClient = MeilisearchFFBBClient(
            meilisearch_bearer_token, debug=debug, cached_session=cached_session
        )

        return FFBBAPIClientV2(api_ffbb_client, meilisearch_ffbb_client)

    def get_lives(self, cached_session: CachedSession = None) -> List[Live]:
        return self.api_ffbb_client.get_lives(cached_session)

    def search_multiple_organismes(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[OrganismesMultiSearchResult]:
        if not names:
            return None

        queries = [OrganismesMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return results.results if results else None

    def search_organismes(
        self, name: str = None, cached_session: CachedSession = None
    ) -> OrganismesMultiSearchResult:
        results = self.search_multiple_organismes([name], cached_session)
        return results[0] if results else None

    def search_multiple_rencontres(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[RencontresMultiSearchResult]:
        if not names:
            return None

        queries = [RencontresMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return results.results if results else None

    def search_rencontres(
        self, name: str = None, cached_session: CachedSession = None
    ) -> RencontresMultiSearchResult:
        results = self.search_multiple_rencontres([name], cached_session)
        return results[0] if results else None

    def search_multiple_terrains(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[TerrainsMultiSearchResult]:
        if not names:
            return None

        queries = [TerrainsMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return results.results if results else None

    def search_terrains(
        self, name: str = None, cached_session: CachedSession = None
    ) -> TerrainsMultiSearchResult:
        results = self.search_multiple_terrains([name], cached_session)
        return results[0] if results else None

    def search_multiple_competitions(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[CompetitionsMultiSearchResult]:
        if not names:
            return None

        queries = [CompetitionsMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return results.results if results else None

    def search_competitions(
        self, name: str = None, cached_session: CachedSession = None
    ) -> CompetitionsMultiSearchResult:
        results = self.search_multiple_competitions([name], cached_session)
        return results[0] if results else None

    def search_multiple_salles(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[SallesMultiSearchResult]:
        if not names:
            return None

        queries = [SallesMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return results.results if results else None

    def search_salles(
        self, name: str = None, cached_session: CachedSession = None
    ) -> SallesMultiSearchResult:
        results = self.search_multiple_salles([name], cached_session)
        return results[0] if results else None

    def search_multiple_tournois(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[TournoisMultiSearchResult]:
        if not names:
            return None

        queries = [TournoisMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return results.results if results else None

    def search_tournois(
        self, name: str = None, cached_session: CachedSession = None
    ) -> TournoisMultiSearchResult:
        results = self.search_multiple_tournois([name], cached_session)
        return results[0] if results else None

    def search_multiple_pratiques(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[PratiquesMultiSearchResult]:
        if not names:
            return None

        queries = [PratiquesMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return results.results if results else None

    def search_pratiques(
        self, name: str = None, cached_session: CachedSession = None
    ) -> PratiquesMultiSearchResult:
        results = self.search_multiple_pratiques([name], cached_session)
        return results[0] if results else None
