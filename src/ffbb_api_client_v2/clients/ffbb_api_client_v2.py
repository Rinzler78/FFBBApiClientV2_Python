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
from ..models.multi_search_result_competitions import CompetitionsMultiSearchResult
from ..models.multi_search_result_organismes import OrganismesMultiSearchResult
from ..models.multi_search_result_pratiques import PratiquesMultiSearchResult
from ..models.multi_search_result_rencontres import RencontresMultiSearchResult
from ..models.multi_search_result_salles import SallesMultiSearchResult
from ..models.multi_search_result_terrains import TerrainsMultiSearchResult
from ..models.multi_search_result_tournois import TournoisMultiSearchResult
from ..models.multi_search_results import MultiSearchResult
from ..models.organismes_models import GetOrganismeResponse
from ..models.poules_models import GetPouleResponse
from ..models.saisons_models import GetSaisonsResponse
from ..utils.input_validation import (
    validate_boolean,
    validate_filter_criteria,
    validate_search_query,
    validate_string_list,
    validate_token,
)
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
        """
        Create a new FFBB API Client V2 instance with comprehensive input validation.

        Args:
            meilisearch_bearer_token (str): Bearer token for Meilisearch API
            api_bearer_token (str): Bearer token for FFBB API
            debug (bool, optional): Enable debug logging. Defaults to False.
            cached_session (CachedSession, optional): HTTP cache session

        Returns:
            FFBBAPIClientV2: Configured API client instance

        Raises:
            ValidationError: If any input parameter is invalid
        """
        # Validate inputs with comprehensive checks
        validated_meilisearch_token = validate_token(
            meilisearch_bearer_token, "meilisearch_bearer_token"
        )
        validated_api_token = validate_token(api_bearer_token, "api_bearer_token")
        validated_debug = validate_boolean(debug, "debug")

        # Create API clients with validated parameters
        api_ffbb_client = ApiFFBBAppClient(
            validated_api_token, debug=validated_debug, cached_session=cached_session
        )

        meilisearch_ffbb_client: MeilisearchFFBBClient = MeilisearchFFBBClient(
            validated_meilisearch_token,
            debug=validated_debug,
            cached_session=cached_session,
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
        Retrieves list of seasons with comprehensive input validation.

        Args:
            fields (List[str], optional): List of fields to retrieve.
                 Defaults to ["id"].
            filter_criteria (str, optional): JSON filter criteria.
                 Defaults to active seasons.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            List[GetSaisonsResponse]: List of season data

        Raises:
            ValidationError: If input parameters are invalid
        """
        validated_fields = validate_string_list(fields, "fields")
        validated_filter = validate_filter_criteria(filter_criteria, "filter_criteria")

        return self.api_ffbb_client.get_saisons(
            fields=validated_fields,
            filter_criteria=validated_filter,
            cached_session=cached_session,
        )

    def multi_search(
        self, name: str = None, cached_session: CachedSession = None
    ) -> list[MultiSearchResult]:
        """
        Perform multi-search across all resource types with input validation.

        Args:
            name (str, optional): Search query string
            cached_session (CachedSession, optional): HTTP cache session

        Returns:
            list[MultiSearchResult]: Search results across all resource types

        Raises:
            ValidationError: If search query is invalid
        """
        validated_name = validate_search_query(name, "name")
        queries = generate_queries(validated_name)
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
