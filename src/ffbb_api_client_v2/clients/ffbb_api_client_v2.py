from __future__ import annotations

from typing import cast

from requests_cache import CachedSession

from ..helpers.multi_search_query_helper import generate_queries
from ..models.competitions_multi_search_query import CompetitionsMultiSearchQuery
from ..models.engagements_multi_search_query import EngagementsMultiSearchQuery
from ..models.field_set import FieldSet
from ..models.formations_multi_search_query import FormationsMultiSearchQuery
from ..models.get_competition_response import GetCompetitionResponse
from ..models.get_organisme_response import GetOrganismeResponse
from ..models.lives import Live
from ..models.meilisearch_index_settings import MeilisearchIndexSettings
from ..models.multi_search_result_competitions import CompetitionsMultiSearchResult
from ..models.multi_search_result_engagements import EngagementsMultiSearchResult
from ..models.multi_search_result_formations import FormationsMultiSearchResult
from ..models.multi_search_result_organismes import OrganismesMultiSearchResult
from ..models.multi_search_result_pratiques import PratiquesMultiSearchResult
from ..models.multi_search_result_rencontres import RencontresMultiSearchResult
from ..models.multi_search_result_salles import SallesMultiSearchResult
from ..models.multi_search_result_terrains import TerrainsMultiSearchResult
from ..models.multi_search_result_tournois import TournoisMultiSearchResult
from ..models.multi_search_results import MultiSearchResult
from ..models.organismes_multi_search_query import OrganismesMultiSearchQuery
from ..models.poules_models import GetPouleResponse
from ..models.pratiques_multi_search_query import PratiquesMultiSearchQuery
from ..models.rencontres_multi_search_query import RencontresMultiSearchQuery
from ..models.saisons_models import GetSaisonsResponse
from ..models.salles_multi_search_query import SallesMultiSearchQuery
from ..models.terrains_multi_search_query import TerrainsMultiSearchQuery
from ..models.tournois_multi_search_query import TournoisMultiSearchQuery
from ..utils.cache_manager import CacheManager
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
        cached_session: CachedSession | None = None,
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

        # Use singleton session if not provided
        if cached_session is None:
            cached_session = CacheManager().session

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

    # --- Directus REST API ---

    def get_competition(
        self,
        competition_id: int,
        deep_limit: str | None = "1000",
        fields: list[str] | None = None,
        field_set: FieldSet | None = None,
        cached_session: CachedSession | None = None,
    ) -> GetCompetitionResponse | None:
        """
        Retrieves detailed information about a competition.

        Args:
            competition_id (int): The ID of the competition
            deep_limit (str, optional): Limit for nested rencontres.
                Defaults to "1000".
            fields (List[str], optional): List of fields to retrieve
            field_set (FieldSet, optional): Predefined field set to use.
                Ignored if fields is provided.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            GetCompetitionResponse: Competition data with nested phases,
                poules, and rencontres
        """
        return self.api_ffbb_client.get_competition(
            competition_id=competition_id,
            deep_limit=deep_limit,
            fields=fields,
            field_set=field_set,
            cached_session=cached_session,
        )

    def get_lives(
        self, cached_session: CachedSession | None = None
    ) -> list[Live] | None:
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
        field_set: FieldSet | None = None,
        cached_session: CachedSession | None = None,
    ) -> GetOrganismeResponse | None:
        """
        Retrieves detailed information about an organisme.

        Args:
            organisme_id (int): The ID of the organisme
            fields (List[str], optional): List of fields to retrieve
            field_set (FieldSet, optional): Predefined field set to use.
                Ignored if fields is provided.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            GetOrganismeResponse: Organisme data with members, competitions, etc.
        """
        return self.api_ffbb_client.get_organisme(
            organisme_id=organisme_id,
            fields=fields,
            field_set=field_set,
            cached_session=cached_session,
        )

    def get_poule(
        self,
        poule_id: int,
        deep_limit: str | None = "1000",
        fields: list[str] | None = None,
        field_set: FieldSet | None = None,
        cached_session: CachedSession | None = None,
    ) -> GetPouleResponse | None:
        """
        Retrieves detailed information about a poule.

        Args:
            poule_id (int): The ID of the poule
            deep_limit (str, optional): Limit for nested rencontres.
                Defaults to "1000".
            fields (List[str], optional): List of fields to retrieve
            field_set (FieldSet, optional): Predefined field set to use.
                Ignored if fields is provided.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            GetPouleResponse: Poule data with rencontres
        """
        return self.api_ffbb_client.get_poule(
            poule_id=poule_id,
            deep_limit=deep_limit,
            fields=fields,
            field_set=field_set,
            cached_session=cached_session,
        )

    def get_saisons(
        self,
        fields: list[str] | None = None,
        filter_criteria: str | None = '{"actif":{"_eq":true}}',
        cached_session: CachedSession | None = None,
    ) -> list[GetSaisonsResponse] | None:
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

    # --- Meilisearch Multi-Search ---

    def multi_search(
        self, name: str | None = None, cached_session: CachedSession | None = None
    ) -> list[MultiSearchResult] | None:
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

    # --- Competitions ---

    def search_competitions(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> CompetitionsMultiSearchResult | None:
        results = self.search_multiple_competitions(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_multiple_competitions(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[CompetitionsMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            CompetitionsMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return (
            cast(list[CompetitionsMultiSearchResult], results.results)
            if results
            else None
        )

    # --- Organismes ---

    def search_multiple_organismes(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[OrganismesMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            OrganismesMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return (
            cast(list[OrganismesMultiSearchResult], results.results)
            if results
            else None
        )

    # --- Pratiques ---

    def search_multiple_pratiques(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[PratiquesMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            PratiquesMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return (
            cast(list[PratiquesMultiSearchResult], results.results) if results else None
        )

    # --- Rencontres ---

    def search_multiple_rencontres(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[RencontresMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            RencontresMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return (
            cast(list[RencontresMultiSearchResult], results.results)
            if results
            else None
        )

    # --- Salles ---

    def search_multiple_salles(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[SallesMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            SallesMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return cast(list[SallesMultiSearchResult], results.results) if results else None

    # --- Terrains ---

    def search_multiple_terrains(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[TerrainsMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            TerrainsMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return (
            cast(list[TerrainsMultiSearchResult], results.results) if results else None
        )

    # --- Engagements ---

    def search_multiple_engagements(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[EngagementsMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            EngagementsMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return (
            cast(list[EngagementsMultiSearchResult], results.results)
            if results
            else None
        )

    # --- Formations ---

    def search_multiple_formations(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[FormationsMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            FormationsMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return (
            cast(list[FormationsMultiSearchResult], results.results)
            if results
            else None
        )

    # --- Tournois ---

    def search_multiple_tournois(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[TournoisMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            TournoisMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return (
            cast(list[TournoisMultiSearchResult], results.results) if results else None
        )

    # --- Single search methods (delegate to search_multiple_*) ---

    def search_organismes(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> OrganismesMultiSearchResult | None:
        results = self.search_multiple_organismes(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_pratiques(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> PratiquesMultiSearchResult | None:
        results = self.search_multiple_pratiques(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_rencontres(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> RencontresMultiSearchResult | None:
        results = self.search_multiple_rencontres(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_salles(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> SallesMultiSearchResult | None:
        results = self.search_multiple_salles(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_terrains(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> TerrainsMultiSearchResult | None:
        results = self.search_multiple_terrains(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_engagements(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> EngagementsMultiSearchResult | None:
        results = self.search_multiple_engagements(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_formations(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> FormationsMultiSearchResult | None:
        results = self.search_multiple_formations(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_tournois(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> TournoisMultiSearchResult | None:
        results = self.search_multiple_tournois(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    # --- Meilisearch Index Settings ---

    def get_index_settings(
        self,
        index_uid: str,
        cached_session: CachedSession | None = None,
    ) -> MeilisearchIndexSettings | None:
        """Get settings for a specific Meilisearch index."""
        return self.meilisearch_ffbb_client.get_index_settings(
            index_uid, cached_session
        )

    def get_all_index_settings(
        self,
        cached_session: CachedSession | None = None,
    ) -> dict[str, MeilisearchIndexSettings]:
        """Get settings for all known FFBB Meilisearch indexes."""
        return self.meilisearch_ffbb_client.get_all_index_settings(cached_session)

    def get_filterable_attributes(
        self,
        index_uid: str,
        cached_session: CachedSession | None = None,
    ) -> list[str] | None:
        """Get filterable attributes for a Meilisearch index."""
        return self.meilisearch_ffbb_client.get_filterable_attributes(
            index_uid, cached_session
        )

    def get_sortable_attributes(
        self,
        index_uid: str,
        cached_session: CachedSession | None = None,
    ) -> list[str] | None:
        """Get sortable attributes for a Meilisearch index."""
        return self.meilisearch_ffbb_client.get_sortable_attributes(
            index_uid, cached_session
        )
