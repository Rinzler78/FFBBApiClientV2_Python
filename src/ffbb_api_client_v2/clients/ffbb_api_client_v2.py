from __future__ import annotations

from requests_cache import CachedSession

from ..helpers.http_requests_helper import default_cached_session
from ..helpers.multi_search_query_helper import generate_queries
from ..models.competitions_models import GetCompetitionResponse
from ..models.lives import Live
from ..models.multi_search_query import (
    CompetitionsMultiSearchQuery,
    OrganismesMultiSearchQuery,
    PratiquesMultiSearchQuery,
    RencontresMultiSearchQuery,
    SallesMultiSearchQuery,
    TerrainsMultiSearchQuery,
    TournoisMultiSearchQuery,
)
from ..models.multi_search_results import MultiSearchResult
from ..models.MultiSearchResultCompetitions import CompetitionsMultiSearchResult
from ..models.MultiSearchResultOrganismes import OrganismesMultiSearchResult
from ..models.MultiSearchResultPratiques import PratiquesMultiSearchResult
from ..models.MultiSearchResultRencontres import RencontresMultiSearchResult
from ..models.MultiSearchResultSalles import SallesMultiSearchResult
from ..models.MultiSearchResultTerrains import TerrainsMultiSearchResult
from ..models.MultiSearchResultTournois import TournoisMultiSearchResult
from ..models.organismes_models import GetOrganismeResponse
from ..models.poules_models import GetPouleResponse
from ..models.saisons_models import GetSaisonsResponse
from .api_ffbb_app_client import ApiFFBBAppClient
from .meilisearch_ffbb_client import MeilisearchFFBBClient


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
    ) -> FFBBAPIClientV2:
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

    def get_competition(
        self,
        competition_id: int,
        deep_limit: str | None = "1000",
        fields: list[str] | None = None,
        cached_session: CachedSession = None,
    ) -> GetCompetitionResponse:
        """
        Retrieves detailed information about a competition.

        Args:
            competition_id (int): The ID of the competition
            deep_limit (str, optional): Limit for nested rencontres.
                Defaults to "1000".
            fields (List[str], optional): List of fields to retrieve
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            GetCompetitionResponse: Competition data with nested phases,
                poules, and rencontres
        """
        return self.api_ffbb_client.get_competition(
            competition_id=competition_id,
            deep_limit=deep_limit,
            fields=fields,
            cached_session=cached_session,
        )

    def get_lives(self, cached_session: CachedSession = None) -> list[Live]:
        """
        Retrieves a list of live events.

        Args:
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            list[Live]: A list of Live objects representing the live events.
        """
        return self.api_ffbb_client.get_lives(cached_session)

    def get_organisme(
        self,
        organisme_id: int,
        fields: list[str] | None = None,
        cached_session: CachedSession = None,
    ) -> GetOrganismeResponse:
        """
        Retrieves detailed information about an organisme.

        Args:
            organisme_id (int): The ID of the organisme
            fields (List[str], optional): List of fields to retrieve
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            GetOrganismeResponse: Organisme data with members, competitions, etc.
        """
        return self.api_ffbb_client.get_organisme(
            organisme_id=organisme_id,
            fields=fields,
            cached_session=cached_session,
        )

    def get_poule(
        self,
        poule_id: int,
        deep_limit: str | None = "1000",
        fields: list[str] | None = None,
        cached_session: CachedSession = None,
    ) -> GetPouleResponse:
        """
        Retrieves detailed information about a poule.

        Args:
            poule_id (int): The ID of the poule
            deep_limit (str, optional): Limit for nested rencontres.
                Defaults to "1000".
            fields (List[str], optional): List of fields to retrieve
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            GetPouleResponse: Poule data with rencontres
        """
        return self.api_ffbb_client.get_poule(
            poule_id=poule_id,
            deep_limit=deep_limit,
            fields=fields,
            cached_session=cached_session,
        )

    def get_saisons(
        self,
        fields: list[str] | None = None,
        filter_criteria: str | None = '{"actif":{"_eq":true}}',
        cached_session: CachedSession = None,
    ) -> list[GetSaisonsResponse]:
        """
        Retrieves list of seasons.

        Args:
            fields (List[str], optional): List of fields to retrieve.
                Defaults to ["id"].
            filter_criteria (str, optional): JSON filter criteria.
                Defaults to active seasons.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            List[GetSaisonsResponse]: List of season data
        """
        return self.api_ffbb_client.get_saisons(
            fields=fields,
            filter_criteria=filter_criteria,
            cached_session=cached_session,
        )

    def multi_search(
        self, name: str = None, cached_session: CachedSession = None
    ) -> list[MultiSearchResult]:
        queries = generate_queries(name)
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session=cached_session
        )

        return results.results if results else None

    def search_competitions(
        self, name: str = None, cached_session: CachedSession = None
    ) -> CompetitionsMultiSearchResult:
        results = self.search_multiple_competitions([name], cached_session)
        return results[0] if results else None

    def search_multiple_competitions(
        self, names: list[str] = None, cached_session: CachedSession = None
    ) -> list[CompetitionsMultiSearchResult]:
        if not names:
            return None

        queries = [CompetitionsMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return results.results if results else None

    def search_multiple_organismes(
        self, names: list[str] = None, cached_session: CachedSession = None
    ) -> list[OrganismesMultiSearchResult]:
        if not names:
            return None

        queries = [OrganismesMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return results.results if results else None

    def search_multiple_pratiques(
        self, names: list[str] = None, cached_session: CachedSession = None
    ) -> list[PratiquesMultiSearchResult]:
        if not names:
            return None

        queries = [PratiquesMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return results.results if results else None

    def search_multiple_rencontres(
        self, names: list[str] = None, cached_session: CachedSession = None
    ) -> list[RencontresMultiSearchResult]:
        if not names:
            return None

        queries = [RencontresMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return results.results if results else None

    def search_multiple_salles(
        self, names: list[str] = None, cached_session: CachedSession = None
    ) -> list[SallesMultiSearchResult]:
        if not names:
            return None

        queries = [SallesMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return results.results if results else None

    def search_multiple_terrains(
        self, names: list[str] = None, cached_session: CachedSession = None
    ) -> list[TerrainsMultiSearchResult]:
        if not names:
            return None

        queries = [TerrainsMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return results.results if results else None

    def search_multiple_tournois(
        self, names: list[str] = None, cached_session: CachedSession = None
    ) -> list[TournoisMultiSearchResult]:
        if not names:
            return None

        queries = [TournoisMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return results.results if results else None

    def search_organismes(
        self, name: str = None, cached_session: CachedSession = None
    ) -> OrganismesMultiSearchResult:
        results = self.search_multiple_organismes([name], cached_session)
        return results[0] if results else OrganismesMultiSearchResult()

    def search_pratiques(
        self, name: str = None, cached_session: CachedSession = None
    ) -> PratiquesMultiSearchResult:
        results = self.search_multiple_pratiques([name], cached_session)
        return results[0] if results else None

    def search_rencontres(
        self, name: str = None, cached_session: CachedSession = None
    ) -> RencontresMultiSearchResult:
        results = self.search_multiple_rencontres([name], cached_session)
        return results[0] if results else None

    def search_salles(
        self, name: str = None, cached_session: CachedSession = None
    ) -> SallesMultiSearchResult:
        results = self.search_multiple_salles([name], cached_session)
        return results[0] if results else None

    def search_terrains(
        self, name: str = None, cached_session: CachedSession = None
    ) -> TerrainsMultiSearchResult:
        results = self.search_multiple_terrains([name], cached_session)
        return results[0] if results else None

    def search_tournois(
        self, name: str = None, cached_session: CachedSession = None
    ) -> TournoisMultiSearchResult:
        results = self.search_multiple_tournois([name], cached_session)
        return results[0] if results else None
