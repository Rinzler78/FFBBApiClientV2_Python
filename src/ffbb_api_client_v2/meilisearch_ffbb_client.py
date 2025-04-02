from typing import List

from requests_cache import CachedSession

from .http_requests_helper import default_cached_session
from .meilisearch_client_extension import MeilisearchClientExtension
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


class MeilisearchFFBBClient(MeilisearchClientExtension):
    def __init__(
        self,
        bearer_token: str,
        url: str = "https://meilisearch-prod.ffbb.app/",
        debug: bool = False,
        cached_session: CachedSession = default_cached_session,
    ):
        super().__init__(bearer_token, url, debug, cached_session)

    def search_multiple_organismes(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[OrganismesMultiSearchResult]:
        if not names:
            return None

        queries = [OrganismesMultiSearchQuery(name) for name in names]
        results = self.recursive_multi_search(queries, cached_session)

        return results.results if results else None

    def search_organismes(
        self, name: str = None, cached_session: CachedSession = None
    ) -> OrganismesMultiSearchResult:
        return self.search_multiple_organismes([name], cached_session)[0]

    def search_multiple_rencontres(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[RencontresMultiSearchResult]:
        if not names:
            return None

        queries = [RencontresMultiSearchQuery(name) for name in names]
        results = self.recursive_multi_search(queries, cached_session)

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
        results = self.recursive_multi_search(queries, cached_session)

        return results.results if results else None

    def search_terrains(
        self, name: str = None, cached_session: CachedSession = None
    ) -> TerrainsMultiSearchResult:
        return self.search_multiple_terrains([name], cached_session)[0]

    def search_multiple_competitions(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[CompetitionsMultiSearchResult]:
        if not names:
            return None

        queries = [CompetitionsMultiSearchQuery(name) for name in names]
        results = self.recursive_multi_search(queries, cached_session)

        return results.results if results else None

    def search_competitions(
        self, name: str = None, cached_session: CachedSession = None
    ) -> CompetitionsMultiSearchResult:
        return self.search_multiple_competitions([name], cached_session)[0]

    def search_multiple_salles(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[SallesMultiSearchResult]:
        if not names:
            return None

        queries = [SallesMultiSearchQuery(name) for name in names]
        results = self.recursive_multi_search(queries, cached_session)

        return results.results if results else None

    def search_salles(
        self, name: str = None, cached_session: CachedSession = None
    ) -> SallesMultiSearchResult:
        return self.search_multiple_salles([name], cached_session)[0]

    def search_multiple_tournois(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[TournoisMultiSearchResult]:
        if not names:
            return None

        queries = [TournoisMultiSearchQuery(name) for name in names]
        results = self.recursive_multi_search(queries, cached_session)

        return results.results if results else None

    def search_tournois(
        self, name: str = None, cached_session: CachedSession = None
    ) -> TournoisMultiSearchResult:
        return self.search_multiple_tournois([name], cached_session)[0]

    def search_multiple_pratiques(
        self, names: List[str] = None, cached_session: CachedSession = None
    ) -> List[PratiquesMultiSearchResult]:
        if not names:
            return None

        queries = [PratiquesMultiSearchQuery(name) for name in names]
        results = self.recursive_multi_search(queries, cached_session)

        return results.results if results else None

    def search_pratiques(
        self, name: str = None, cached_session: CachedSession = None
    ) -> PratiquesMultiSearchResult:
        return self.search_multiple_pratiques([name], cached_session)[0]
