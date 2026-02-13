from __future__ import annotations

from typing import cast

from requests_cache import CachedSession

from ..directus.models.field_set import FieldSet
from ..directus_ffbb.client import ApiFFBBAppClient
from ..directus_ffbb.models.get_communes_response import GetCommunesResponse
from ..directus_ffbb.models.get_competition_response import GetCompetitionResponse
from ..directus_ffbb.models.get_engagements_response import GetEngagementsResponse
from ..directus_ffbb.models.get_entraineurs_response import GetEntraineursResponse
from ..directus_ffbb.models.get_formations_response import GetFormationsResponse
from ..directus_ffbb.models.get_officiels_response import GetOfficielsResponse
from ..directus_ffbb.models.get_organisme_response import GetOrganismeResponse
from ..directus_ffbb.models.get_pratiques_response import GetPratiquesResponse
from ..directus_ffbb.models.get_rencontres_response import GetRencontresResponse
from ..directus_ffbb.models.get_salles_response import GetSallesResponse
from ..directus_ffbb.models.get_terrains_response import GetTerrainsResponse
from ..directus_ffbb.models.get_tournois_response import GetTournoisResponse
from ..directus_ffbb.models.lives import Live
from ..directus_ffbb.models.poules_models import GetPouleResponse
from ..directus_ffbb.models.saisons_models import GetSaisonsResponse
from ..meilisearch.models.meilisearch_index_settings import MeilisearchIndexSettings
from ..meilisearch.models.multi_search_results import MultiSearchResult
from ..meilisearch_ffbb.client import MeilisearchFFBBClient
from ..meilisearch_ffbb.models.competitions_multi_search_query import (
    CompetitionsMultiSearchQuery,
)
from ..meilisearch_ffbb.models.engagements_multi_search_query import (
    EngagementsMultiSearchQuery,
)
from ..meilisearch_ffbb.models.formations_multi_search_query import (
    FormationsMultiSearchQuery,
)
from ..meilisearch_ffbb.models.multi_search_result_competitions import (
    CompetitionsMultiSearchResult,
)
from ..meilisearch_ffbb.models.multi_search_result_engagements import (
    EngagementsMultiSearchResult,
)
from ..meilisearch_ffbb.models.multi_search_result_formations import (
    FormationsMultiSearchResult,
)
from ..meilisearch_ffbb.models.multi_search_result_organismes import (
    OrganismesMultiSearchResult,
)
from ..meilisearch_ffbb.models.multi_search_result_pratiques import (
    PratiquesMultiSearchResult,
)
from ..meilisearch_ffbb.models.multi_search_result_rencontres import (
    RencontresMultiSearchResult,
)
from ..meilisearch_ffbb.models.multi_search_result_salles import SallesMultiSearchResult
from ..meilisearch_ffbb.models.multi_search_result_terrains import (
    TerrainsMultiSearchResult,
)
from ..meilisearch_ffbb.models.multi_search_result_tournois import (
    TournoisMultiSearchResult,
)
from ..meilisearch_ffbb.models.organismes_multi_search_query import (
    OrganismesMultiSearchQuery,
)
from ..meilisearch_ffbb.models.pratiques_multi_search_query import (
    PratiquesMultiSearchQuery,
)
from ..meilisearch_ffbb.models.rencontres_multi_search_query import (
    RencontresMultiSearchQuery,
)
from ..meilisearch_ffbb.models.salles_multi_search_query import SallesMultiSearchQuery
from ..meilisearch_ffbb.models.terrains_multi_search_query import (
    TerrainsMultiSearchQuery,
)
from ..meilisearch_ffbb.models.tournois_multi_search_query import (
    TournoisMultiSearchQuery,
)
from ..meilisearch_ffbb.query_helper import generate_queries
from ..utils.cache_manager import CacheManager
from ..utils.input_validation import (
    validate_boolean,
    validate_filter_criteria,
    validate_offset,
    validate_search_query,
    validate_string_list,
    validate_token,
)


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
        deep_rencontres_limit: int | None = 1000,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetCompetitionResponse | None:
        """
        Retrieves detailed information about a competition.

        Args:
            competition_id (int): The ID of the competition
            deep_rencontres_limit (int, optional): Limit for nested rencontres.
                Defaults to 1000.
            field_set (FieldSet): Predefined field set to use.
                Defaults to FieldSet.DETAILED.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            GetCompetitionResponse: Competition data with nested phases,
                poules, and rencontres
        """
        return self.api_ffbb_client.get_competition(
            competition_id=competition_id,
            deep_rencontres_limit=deep_rencontres_limit,
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
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetOrganismeResponse | None:
        """
        Retrieves detailed information about an organisme.

        Args:
            organisme_id (int): The ID of the organisme
            field_set (FieldSet): Predefined field set to use.
                Defaults to FieldSet.DETAILED.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            GetOrganismeResponse: Organisme data with members, competitions, etc.
        """
        return self.api_ffbb_client.get_organisme(
            organisme_id=organisme_id,
            field_set=field_set,
            cached_session=cached_session,
        )

    def get_poule(
        self,
        poule_id: int,
        deep_rencontres_limit: int | None = 1000,
        deep_rencontres_filter_saison_actif: bool | None = True,
        deep_rencontres_sort: str | None = "date_rencontre",
        deep_classements_limit: int | None = 100000,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetPouleResponse | None:
        """
        Retrieves detailed information about a poule.

        Args:
            poule_id (int): The ID of the poule
            deep_rencontres_limit (int, optional): Limit for nested rencontres.
                Defaults to 1000.
            deep_rencontres_filter_saison_actif (bool, optional): Filter
                rencontres by active season. Defaults to True.
            deep_rencontres_sort (str, optional): Sort field for rencontres.
                Defaults to "date_rencontre".
            deep_classements_limit (int, optional): Limit for nested
                classements. Defaults to 100000.
            field_set (FieldSet): Predefined field set to use.
                Defaults to FieldSet.DETAILED.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            GetPouleResponse: Poule data with rencontres
        """
        return self.api_ffbb_client.get_poule(
            poule_id=poule_id,
            deep_rencontres_limit=deep_rencontres_limit,
            deep_rencontres_filter_saison_actif=deep_rencontres_filter_saison_actif,
            deep_rencontres_sort=deep_rencontres_sort,
            deep_classements_limit=deep_classements_limit,
            field_set=field_set,
            cached_session=cached_session,
        )

    def get_saisons(
        self,
        filter_criteria: str | None = '{"actif":{"_eq":true}}',
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> list[GetSaisonsResponse] | None:
        """
        Retrieves list of seasons with comprehensive input validation.

        Args:
            filter_criteria (str, optional): JSON filter criteria.
                 Defaults to active seasons.
            field_set (FieldSet): Predefined field set to use.
                 Defaults to FieldSet.DETAILED.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            List[GetSaisonsResponse]: List of season data

        Raises:
            ValidationError: If input parameters are invalid
        """
        validated_filter = validate_filter_criteria(filter_criteria, "filter_criteria")

        return self.api_ffbb_client.get_saisons(
            filter_criteria=validated_filter,
            field_set=field_set,
            cached_session=cached_session,
        )

    # --- Directus: Rencontres ---

    def get_rencontre(
        self,
        rencontre_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetRencontresResponse | None:
        """Retrieves a rencontre by ID."""
        return self.api_ffbb_client.get_rencontre(
            rencontre_id=rencontre_id,
            field_set=field_set,
            cached_session=cached_session,
        )

    def list_rencontres(
        self,
        limit: int = 10,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetRencontresResponse]:
        """Lists rencontres."""
        return self.api_ffbb_client.list_rencontres(
            limit=limit,
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            offset=validate_offset(offset),
            search=validate_search_query(search, "search"),
            cached_session=cached_session,
        )

    # --- Directus: Salles ---

    def get_salle(
        self,
        salle_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetSallesResponse | None:
        """Retrieves a salle by ID."""
        return self.api_ffbb_client.get_salle(
            salle_id=salle_id,
            field_set=field_set,
            cached_session=cached_session,
        )

    def list_salles(
        self,
        limit: int = 10,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetSallesResponse]:
        """Lists salles."""
        return self.api_ffbb_client.list_salles(
            limit=limit,
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            offset=validate_offset(offset),
            search=validate_search_query(search, "search"),
            cached_session=cached_session,
        )

    # --- Directus: Terrains ---

    def get_terrain(
        self,
        terrain_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetTerrainsResponse | None:
        """Retrieves a terrain by ID."""
        return self.api_ffbb_client.get_terrain(
            terrain_id=terrain_id,
            field_set=field_set,
            cached_session=cached_session,
        )

    def list_terrains(
        self,
        limit: int = 10,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetTerrainsResponse]:
        """Lists terrains."""
        return self.api_ffbb_client.list_terrains(
            limit=limit,
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            offset=validate_offset(offset),
            search=validate_search_query(search, "search"),
            cached_session=cached_session,
        )

    # --- Directus: Tournois ---

    def get_tournoi(
        self,
        tournoi_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetTournoisResponse | None:
        """Retrieves a tournoi by ID."""
        return self.api_ffbb_client.get_tournoi(
            tournoi_id=tournoi_id,
            field_set=field_set,
            cached_session=cached_session,
        )

    def list_tournois(
        self,
        limit: int = 10,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetTournoisResponse]:
        """Lists tournois."""
        return self.api_ffbb_client.list_tournois(
            limit=limit,
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            offset=validate_offset(offset),
            search=validate_search_query(search, "search"),
            cached_session=cached_session,
        )

    # --- Directus: Engagements ---

    def get_engagement(
        self,
        engagement_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetEngagementsResponse | None:
        """Retrieves an engagement by ID."""
        return self.api_ffbb_client.get_engagement(
            engagement_id=engagement_id,
            field_set=field_set,
            cached_session=cached_session,
        )

    def list_engagements(
        self,
        limit: int = 10,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetEngagementsResponse]:
        """Lists engagements."""
        return self.api_ffbb_client.list_engagements(
            limit=limit,
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            offset=validate_offset(offset),
            search=validate_search_query(search, "search"),
            cached_session=cached_session,
        )

    # --- Directus: Formations ---

    def get_formation(
        self,
        formation_id: str,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetFormationsResponse | None:
        """Retrieves a formation by ID."""
        return self.api_ffbb_client.get_formation(
            formation_id=formation_id,
            field_set=field_set,
            cached_session=cached_session,
        )

    def list_formations(
        self,
        limit: int = 10,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetFormationsResponse]:
        """Lists formations."""
        return self.api_ffbb_client.list_formations(
            limit=limit,
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            offset=validate_offset(offset),
            search=validate_search_query(search, "search"),
            cached_session=cached_session,
        )

    # --- Directus: Entraineurs ---

    def get_entraineur(
        self,
        entraineur_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetEntraineursResponse | None:
        """Retrieves an entraineur by ID."""
        return self.api_ffbb_client.get_entraineur(
            entraineur_id=entraineur_id,
            field_set=field_set,
            cached_session=cached_session,
        )

    def list_entraineurs(
        self,
        limit: int = 10,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetEntraineursResponse]:
        """Lists entraineurs."""
        return self.api_ffbb_client.list_entraineurs(
            limit=limit,
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            offset=validate_offset(offset),
            search=validate_search_query(search, "search"),
            cached_session=cached_session,
        )

    # --- Directus: Communes ---

    def list_communes(
        self,
        limit: int = 10,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetCommunesResponse]:
        """Lists communes."""
        return self.api_ffbb_client.list_communes(
            limit=limit,
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            offset=validate_offset(offset),
            search=validate_search_query(search, "search"),
            cached_session=cached_session,
        )

    # --- Directus: Officiels ---

    def list_officiels(
        self,
        limit: int = 10,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetOfficielsResponse]:
        """Lists officiels."""
        return self.api_ffbb_client.list_officiels(
            limit=limit,
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            offset=validate_offset(offset),
            search=validate_search_query(search, "search"),
            cached_session=cached_session,
        )

    # --- Directus: Pratiques ---

    def list_pratiques(
        self,
        limit: int = 10,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetPratiquesResponse]:
        """Lists pratiques."""
        return self.api_ffbb_client.list_pratiques(
            limit=limit,
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            offset=validate_offset(offset),
            search=validate_search_query(search, "search"),
            cached_session=cached_session,
        )

    # --- Directus: Automatic Pagination ---

    def list_all_rencontres(
        self,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetRencontresResponse]:
        """Retrieves all rencontres with automatic pagination."""
        return self.api_ffbb_client.list_all_rencontres(
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_salles(
        self,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetSallesResponse]:
        """Retrieves all salles with automatic pagination."""
        return self.api_ffbb_client.list_all_salles(
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_terrains(
        self,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetTerrainsResponse]:
        """Retrieves all terrains with automatic pagination."""
        return self.api_ffbb_client.list_all_terrains(
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_tournois(
        self,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetTournoisResponse]:
        """Retrieves all tournois with automatic pagination."""
        return self.api_ffbb_client.list_all_tournois(
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_engagements(
        self,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetEngagementsResponse]:
        """Retrieves all engagements with automatic pagination."""
        return self.api_ffbb_client.list_all_engagements(
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_formations(
        self,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetFormationsResponse]:
        """Retrieves all formations with automatic pagination."""
        return self.api_ffbb_client.list_all_formations(
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_entraineurs(
        self,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetEntraineursResponse]:
        """Retrieves all entraineurs with automatic pagination."""
        return self.api_ffbb_client.list_all_entraineurs(
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_communes(
        self,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetCommunesResponse]:
        """Retrieves all communes with automatic pagination."""
        return self.api_ffbb_client.list_all_communes(
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_officiels(
        self,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetOfficielsResponse]:
        """Retrieves all officiels with automatic pagination."""
        return self.api_ffbb_client.list_all_officiels(
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_pratiques(
        self,
        field_set: FieldSet = FieldSet.DEFAULT,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetPratiquesResponse]:
        """Retrieves all pratiques with automatic pagination."""
        return self.api_ffbb_client.list_all_pratiques(
            field_set=field_set,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
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
