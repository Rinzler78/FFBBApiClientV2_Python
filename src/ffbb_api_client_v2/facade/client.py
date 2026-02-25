from __future__ import annotations

import json
from typing import cast
from uuid import UUID

from requests_cache import CachedSession

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
from ..meilisearch_ffbb.geo_sort_order import GeoSortOrder
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
from ..models.club_contacts import (
    ClubContacts,
    extract_club_info,
    extract_membres_contacts,
)
from ..models.contact_role import ContactRole
from ..models.engagement_contacts import (
    EngagementContacts,
    extract_correspondant,
    extract_entraineur_contact,
)
from ..utils.cache_manager import CacheManager
from ..utils.input_validation import (
    validate_boolean,
    validate_filter_criteria,
    validate_offset,
    validate_search_query,
    validate_string_list,
    validate_token,
)
from ..utils.retry_utils import RetryConfig, TimeoutConfig


class FFBBAPIClientV2:
    """Facade unifiee pour les APIs FFBB v2.

    Compose deux clients backend :

    - **ApiFFBBAppClient** (Directus REST) : get/list avec FK bruts (int IDs)
    - **MeilisearchFFBBClient** (Meilisearch) : search avec objets denormalises

    Pattern d'utilisation recommande :

    1. Meilisearch pour la decouverte (recherche textuelle, geo)
    2. Directus pour l'approfondissement (resolution FK en profondeur)
    3. ``int(hit.id)`` pour passer d'un hit Meilisearch a un get Directus

    69 methodes publiques : get (13), list (10), list_all (10), search (9),
    search_multiple (9), search_geo (4), composite (2), batch (5),
    settings (4), create (1), asset (1).
    """

    def __init__(
        self,
        api_ffbb_client: ApiFFBBAppClient,
        meilisearch_ffbb_client: MeilisearchFFBBClient,
    ):
        """Initialise la facade avec les deux clients backend.

        Preferer ``FFBBAPIClientV2.create()`` pour la construction standard.

        Args:
            api_ffbb_client: Client Directus REST configure.
            meilisearch_ffbb_client: Client Meilisearch configure.
        """
        self.api_ffbb_client = api_ffbb_client
        self.meilisearch_ffbb_client = meilisearch_ffbb_client

    @staticmethod
    def create(
        meilisearch_bearer_token: str,
        api_bearer_token: str,
        debug: bool = False,
        cached_session: CachedSession | None = None,
        directus_retry_config: RetryConfig | None = None,
        directus_timeout_config: TimeoutConfig | None = None,
        meilisearch_retry_config: RetryConfig | None = None,
        meilisearch_timeout_config: TimeoutConfig | None = None,
    ) -> FFBBAPIClientV2:
        """
        Create a new FFBB API Client V2 instance with comprehensive input validation.

        Args:
            meilisearch_bearer_token (str): Bearer token for Meilisearch API
            api_bearer_token (str): Bearer token for FFBB API
            debug (bool, optional): Enable debug logging. Defaults to False.
            cached_session (CachedSession, optional): HTTP cache session
            directus_retry_config (RetryConfig, optional): Retry config for Directus client.
                Defaults to 1 attempt (deep wildcard queries are expensive).
            directus_timeout_config (TimeoutConfig, optional): Timeout config for Directus.
                Defaults to 120s read timeout for deep wildcard field queries.
            meilisearch_retry_config (RetryConfig, optional): Retry config for Meilisearch.
                Defaults to 3 attempts.
            meilisearch_timeout_config (TimeoutConfig, optional): Timeout config for Meilisearch.
                Defaults to 30s read timeout.

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
            validated_api_token,
            debug=validated_debug,
            cached_session=cached_session,
            retry_config=directus_retry_config,
            timeout_config=directus_timeout_config,
        )

        meilisearch_ffbb_client: MeilisearchFFBBClient = MeilisearchFFBBClient(
            validated_meilisearch_token,
            debug=validated_debug,
            cached_session=cached_session,
            retry_config=meilisearch_retry_config,
            timeout_config=meilisearch_timeout_config,
        )

        return FFBBAPIClientV2(api_ffbb_client, meilisearch_ffbb_client)

    # --- Asset URLs ---

    def get_asset_url(self, file_id: str | UUID) -> str:
        """Build the download URL for a Directus file asset."""
        return self.api_ffbb_client.get_asset_url(file_id)

    # --- Directus REST API ---

    def get_competition(
        self,
        competition_id: int,
        deep_rencontres_limit: int | None = 1000,
        cached_session: CachedSession | None = None,
    ) -> GetCompetitionResponse | None:
        """
        Retrieves detailed information about a competition.

        Args:
            competition_id (int): The ID of the competition
            deep_rencontres_limit (int, optional): Limit for nested rencontres.
                Defaults to 1000.

            cached_session (CachedSession, optional): The cached session to use

        Returns:
            GetCompetitionResponse: Competition data with nested phases,
                poules, and rencontres
        """
        return self.api_ffbb_client.get_competition(
            competition_id=competition_id,
            deep_rencontres_limit=deep_rencontres_limit,
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
        cached_session: CachedSession | None = None,
    ) -> GetOrganismeResponse | None:
        """
        Retrieves detailed information about an organisme.

        Args:
            organisme_id (int): The ID of the organisme

            cached_session (CachedSession, optional): The cached session to use

        Returns:
            GetOrganismeResponse: Organisme data with members, competitions, etc.
        """
        return self.api_ffbb_client.get_organisme(
            organisme_id=organisme_id,
            cached_session=cached_session,
        )

    def get_poule(
        self,
        poule_id: int,
        deep_rencontres_limit: int | None = 1000,
        deep_rencontres_filter_saison_actif: bool | None = True,
        deep_rencontres_sort: str | None = "date_rencontre",
        deep_classements_limit: int | None = 100000,
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
            cached_session=cached_session,
        )

    def get_saisons(
        self,
        filter_criteria: str | None = '{"actif":{"_eq":true}}',
        cached_session: CachedSession | None = None,
    ) -> list[GetSaisonsResponse] | None:
        """
        Retrieves list of seasons with comprehensive input validation.

        Args:
            filter_criteria (str, optional): JSON filter criteria.
                 Defaults to active seasons.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            List[GetSaisonsResponse]: List of season data

        Raises:
            ValidationError: If input parameters are invalid
        """
        validated_filter = validate_filter_criteria(filter_criteria, "filter_criteria")

        return self.api_ffbb_client.get_saisons(
            filter_criteria=validated_filter,
            cached_session=cached_session,
        )

    # --- Directus: Rencontres ---

    def get_rencontre(
        self,
        rencontre_id: int,
        cached_session: CachedSession | None = None,
    ) -> GetRencontresResponse | None:
        """Retrieves a rencontre by ID."""
        return self.api_ffbb_client.get_rencontre(
            rencontre_id=rencontre_id,
            cached_session=cached_session,
        )

    def list_rencontres(
        self,
        limit: int = 10,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetRencontresResponse]:
        """Lists rencontres."""
        return self.api_ffbb_client.list_rencontres(
            limit=limit,
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
        cached_session: CachedSession | None = None,
    ) -> GetSallesResponse | None:
        """Retrieves a salle by ID."""
        return self.api_ffbb_client.get_salle(
            salle_id=salle_id,
            cached_session=cached_session,
        )

    def list_salles(
        self,
        limit: int = 10,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetSallesResponse]:
        """Lists salles."""
        return self.api_ffbb_client.list_salles(
            limit=limit,
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
        cached_session: CachedSession | None = None,
    ) -> GetTerrainsResponse | None:
        """Retrieves a terrain by ID."""
        return self.api_ffbb_client.get_terrain(
            terrain_id=terrain_id,
            cached_session=cached_session,
        )

    def list_terrains(
        self,
        limit: int = 10,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetTerrainsResponse]:
        """Lists terrains."""
        return self.api_ffbb_client.list_terrains(
            limit=limit,
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
        cached_session: CachedSession | None = None,
    ) -> GetTournoisResponse | None:
        """Retrieves a tournoi by ID."""
        return self.api_ffbb_client.get_tournoi(
            tournoi_id=tournoi_id,
            cached_session=cached_session,
        )

    def list_tournois(
        self,
        limit: int = 10,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetTournoisResponse]:
        """Lists tournois."""
        return self.api_ffbb_client.list_tournois(
            limit=limit,
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
        cached_session: CachedSession | None = None,
    ) -> GetEngagementsResponse | None:
        """Retrieves an engagement by ID."""
        return self.api_ffbb_client.get_engagement(
            engagement_id=engagement_id,
            cached_session=cached_session,
        )

    def list_engagements(
        self,
        limit: int = 10,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetEngagementsResponse]:
        """Lists engagements."""
        return self.api_ffbb_client.list_engagements(
            limit=limit,
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
        cached_session: CachedSession | None = None,
    ) -> GetFormationsResponse | None:
        """Retrieves a formation by ID."""
        return self.api_ffbb_client.get_formation(
            formation_id=formation_id,
            cached_session=cached_session,
        )

    def list_formations(
        self,
        limit: int = 10,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetFormationsResponse]:
        """Lists formations."""
        return self.api_ffbb_client.list_formations(
            limit=limit,
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
        cached_session: CachedSession | None = None,
    ) -> GetEntraineursResponse | None:
        """Retrieves an entraineur by ID."""
        return self.api_ffbb_client.get_entraineur(
            entraineur_id=entraineur_id,
            cached_session=cached_session,
        )

    def list_entraineurs(
        self,
        limit: int = 10,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetEntraineursResponse]:
        """Lists entraineurs."""
        return self.api_ffbb_client.list_entraineurs(
            limit=limit,
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
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetCommunesResponse]:
        """Lists communes."""
        return self.api_ffbb_client.list_communes(
            limit=limit,
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
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetOfficielsResponse]:
        """Lists officiels."""
        return self.api_ffbb_client.list_officiels(
            limit=limit,
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
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        offset: int | None = None,
        search: str | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetPratiquesResponse]:
        """Lists pratiques."""
        return self.api_ffbb_client.list_pratiques(
            limit=limit,
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            offset=validate_offset(offset),
            search=validate_search_query(search, "search"),
            cached_session=cached_session,
        )

    # --- Directus: Automatic Pagination ---

    def list_all_rencontres(
        self,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetRencontresResponse]:
        """Retrieves all rencontres with automatic pagination."""
        return self.api_ffbb_client.list_all_rencontres(
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_salles(
        self,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetSallesResponse]:
        """Retrieves all salles with automatic pagination."""
        return self.api_ffbb_client.list_all_salles(
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_terrains(
        self,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetTerrainsResponse]:
        """Retrieves all terrains with automatic pagination."""
        return self.api_ffbb_client.list_all_terrains(
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_tournois(
        self,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetTournoisResponse]:
        """Retrieves all tournois with automatic pagination."""
        return self.api_ffbb_client.list_all_tournois(
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_engagements(
        self,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetEngagementsResponse]:
        """Retrieves all engagements with automatic pagination."""
        return self.api_ffbb_client.list_all_engagements(
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_formations(
        self,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetFormationsResponse]:
        """Retrieves all formations with automatic pagination."""
        return self.api_ffbb_client.list_all_formations(
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_entraineurs(
        self,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetEntraineursResponse]:
        """Retrieves all entraineurs with automatic pagination."""
        return self.api_ffbb_client.list_all_entraineurs(
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_communes(
        self,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetCommunesResponse]:
        """Retrieves all communes with automatic pagination."""
        return self.api_ffbb_client.list_all_communes(
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_officiels(
        self,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetOfficielsResponse]:
        """Retrieves all officiels with automatic pagination."""
        return self.api_ffbb_client.list_all_officiels(
            filter_criteria=validate_filter_criteria(filter_criteria),
            sort=validate_string_list(sort, "sort"),
            search=validate_search_query(search, "search"),
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )

    def list_all_pratiques(
        self,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[GetPratiquesResponse]:
        """Retrieves all pratiques with automatic pagination."""
        return self.api_ffbb_client.list_all_pratiques(
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
        """Recherche textuelle dans ffbbserver_competitions.

        ``int(hit.id)`` → ``get_competition()``.
        """
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
        """Recherche batch dans ffbbserver_competitions (une query par name)."""
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
        """Recherche batch dans ffbbserver_organismes (une query par name)."""
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
        """Recherche batch dans ffbbnational_pratiques (une query par name)."""
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
        """Recherche batch dans ffbbserver_rencontres (une query par name)."""
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
        """Recherche batch dans ffbbserver_salles (une query par name)."""
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
        """Recherche batch dans ffbbserver_terrains (une query par name)."""
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
        """Recherche batch dans ffbbserver_engagements (une query par name)."""
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
        """Recherche batch dans ffbbserver_formations (une query par name)."""
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
        """Recherche batch dans ffbbserver_tournois (une query par name)."""
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
        """Recherche textuelle dans ffbbserver_organismes.

        ``int(hit.id)`` → ``get_organisme()``. Hits denormalises avec commune, salle, geo.
        """
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
        """Recherche textuelle dans ffbbnational_pratiques."""
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
        """Recherche textuelle dans ffbbserver_rencontres.

        ``int(hit.id)`` → ``get_rencontre()``.
        """
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
        """Recherche textuelle dans ffbbserver_salles.

        ``int(hit.id)`` → ``get_salle()``.
        """
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
        """Recherche textuelle dans ffbbserver_terrains.

        ``int(hit.id)`` → ``get_terrain()``.
        """
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
        """Recherche textuelle dans ffbbserver_engagements.

        ``int(hit.id)`` → ``get_engagement()``.
        """
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
        """Recherche textuelle dans ffbbserver_formations.

        ``hit.id`` est un str (UUID) → ``get_formation(hit.id)``.
        """
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
        """Recherche textuelle dans ffbbserver_tournois.

        ``int(hit.id)`` → ``get_tournoi()``.
        """
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

    # --- Geo-search proxies ---

    def search_organismes_by_geo(
        self,
        lat: float,
        lng: float,
        radius_km: float = 10.0,
        q: str = "",
        limit: int | None = 20,
        geo_sort: GeoSortOrder = GeoSortOrder.NEAREST_FIRST,
        cached_session: CachedSession | None = None,
    ) -> OrganismesMultiSearchResult | None:
        """Search organismes by geographic proximity."""
        return self.meilisearch_ffbb_client.search_organismes_by_geo(
            lat, lng, radius_km, q, limit, geo_sort, cached_session
        )

    # --- City-search proxies ---

    def search_organismes_by_city(
        self,
        city_name: str,
        q: str = "",
        limit: int | None = 200,
        cached_session: CachedSession | None = None,
    ) -> OrganismesMultiSearchResult | None:
        """Search organismes located in a specific city."""
        return self.meilisearch_ffbb_client.search_organismes_by_city(
            city_name, q, limit, cached_session
        )

    def search_salles_by_geo(
        self,
        lat: float,
        lng: float,
        radius_km: float = 10.0,
        q: str = "",
        limit: int | None = 20,
        geo_sort: GeoSortOrder = GeoSortOrder.NEAREST_FIRST,
        cached_session: CachedSession | None = None,
    ) -> SallesMultiSearchResult | None:
        """Search salles by geographic proximity."""
        return self.meilisearch_ffbb_client.search_salles_by_geo(
            lat, lng, radius_km, q, limit, geo_sort, cached_session
        )

    def search_engagements_by_geo(
        self,
        lat: float,
        lng: float,
        radius_km: float = 10.0,
        q: str = "",
        limit: int | None = 20,
        geo_sort: GeoSortOrder = GeoSortOrder.NEAREST_FIRST,
        cached_session: CachedSession | None = None,
    ) -> EngagementsMultiSearchResult | None:
        """Search engagements by geographic proximity."""
        return self.meilisearch_ffbb_client.search_engagements_by_geo(
            lat, lng, radius_km, q, limit, geo_sort, cached_session
        )

    def search_engagements_filtered(
        self,
        lat: float,
        lng: float,
        radius_km: float = 10.0,
        q: str = "",
        limit: int | None = 5000,
        geo_sort: GeoSortOrder = GeoSortOrder.NEAREST_FIRST,
        sexes: list[str] | None = None,
        niveau_codes: list[str] | None = None,
        cached_session: CachedSession | None = None,
    ) -> EngagementsMultiSearchResult | None:
        """Search engagements with geo + sexe + niveau.code filters."""
        return self.meilisearch_ffbb_client.search_engagements_filtered(
            lat,
            lng,
            radius_km,
            q,
            limit,
            geo_sort,
            sexes,
            niveau_codes,
            cached_session,
        )

    # --- Composite contact methods ---

    def get_engagement_contacts(
        self,
        engagement_id: int,
        cached_session: CachedSession | None = None,
    ) -> EngagementContacts | None:
        """Recupere les contacts d'un engagement : correspondant + entraineurs.

        Methode composite qui appelle ``get_engagement()`` puis
        ``get_entraineur()`` pour le coach principal et adjoint.

        Args:
            engagement_id: ID numerique de l'engagement.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            EngagementContacts (engagement, correspondant, entraineur,
            entraineur_adjoint) ou None.
        """
        engagement = self.get_engagement(engagement_id, cached_session=cached_session)
        if not engagement:
            return None

        correspondant = extract_correspondant(engagement)

        entraineur = None
        if engagement.entraineur:
            ent = self.get_entraineur(
                engagement.entraineur, cached_session=cached_session
            )
            entraineur = extract_entraineur_contact(ent, ContactRole.ENTRAINEUR)

        entraineur_adj = None
        if engagement.entraineurAdjoint:
            adj = self.get_entraineur(
                engagement.entraineurAdjoint, cached_session=cached_session
            )
            entraineur_adj = extract_entraineur_contact(
                adj, ContactRole.ENTRAINEUR_ADJOINT
            )

        return EngagementContacts(engagement, correspondant, entraineur, entraineur_adj)

    def get_club_contacts(
        self,
        organisme_id: int,
        cached_session: CachedSession | None = None,
    ) -> ClubContacts | None:
        """Recupere les contacts d'un club : info club + membres/dirigeants.

        Methode composite qui appelle ``get_organisme()`` puis extrait
        les contacts du club et des membres.

        Args:
            organisme_id: ID numerique de l'organisme (club).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            ClubContacts (organisme, club_contact, membres) ou None.
        """
        organisme = self.get_organisme(organisme_id, cached_session=cached_session)
        if not organisme:
            return None

        club_contact = extract_club_info(organisme)
        membres = extract_membres_contacts(organisme)

        return ClubContacts(organisme, club_contact, membres)

    # --- Batch helpers (Directus _in filters) ---
    #
    # The ``_in`` filter JSON must stay under the 1000-char validation
    # limit.  With a ~30-char overhead (``{"field":{"_in":[...]}}``),
    # that leaves ~970 chars for the comma-separated IDs.  Using 50 IDs
    # per chunk keeps us safely within bounds for IDs up to ~18 digits.

    _BATCH_CHUNK_SIZE = 50

    @staticmethod
    def _chunked(items: list[int], size: int) -> list[list[int]]:
        """Split *items* into sublists of at most *size* elements."""
        return [items[i : i + size] for i in range(0, len(items), size)]

    def list_engagements_by_ids(
        self,
        ids: list[int],
        cached_session: CachedSession | None = None,
    ) -> list[GetEngagementsResponse]:
        """Fetch multiple engagements using ``_in`` filter (auto-chunked)."""
        if not ids:
            return []
        results: list[GetEngagementsResponse] = []
        for chunk in self._chunked(ids, self._BATCH_CHUNK_SIZE):
            results.extend(
                self.list_engagements(
                    limit=len(chunk),
                    filter_criteria=json.dumps({"id": {"_in": chunk}}),
                    cached_session=cached_session,
                )
            )
        return results

    def list_engagements_by_poule(
        self,
        poule_id: int,
        limit: int = 250,
        cached_session: CachedSession | None = None,
    ) -> list[GetEngagementsResponse]:
        """List engagements belonging to a single poule."""
        return self.list_engagements(
            limit=limit,
            filter_criteria=json.dumps({"idPoule": {"_eq": poule_id}}),
            cached_session=cached_session,
        )

    def list_engagements_by_poules(
        self,
        poule_ids: list[int],
        limit: int = 2000,
        cached_session: CachedSession | None = None,
    ) -> list[GetEngagementsResponse]:
        """Fetch engagements for multiple poules using ``_in`` (auto-chunked)."""
        if not poule_ids:
            return []
        results: list[GetEngagementsResponse] = []
        for chunk in self._chunked(poule_ids, self._BATCH_CHUNK_SIZE):
            results.extend(
                self.list_engagements(
                    limit=limit,
                    filter_criteria=json.dumps({"idPoule": {"_in": chunk}}),
                    cached_session=cached_session,
                )
            )
        return results

    def list_rencontres_by_poule(
        self,
        poule_id: int,
        limit: int = 500,
        sort: list[str] | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetRencontresResponse]:
        """List rencontres belonging to a single poule."""
        return self.list_rencontres(
            limit=limit,
            filter_criteria=json.dumps({"idPoule": {"_eq": poule_id}}),
            sort=sort,
            cached_session=cached_session,
        )

    def list_rencontres_by_poules(
        self,
        poule_ids: list[int],
        limit: int = 5000,
        sort: list[str] | None = None,
        cached_session: CachedSession | None = None,
    ) -> list[GetRencontresResponse]:
        """Fetch rencontres for multiple poules using ``_in`` (auto-chunked)."""
        if not poule_ids:
            return []
        results: list[GetRencontresResponse] = []
        for chunk in self._chunked(poule_ids, self._BATCH_CHUNK_SIZE):
            results.extend(
                self.list_rencontres(
                    limit=limit,
                    filter_criteria=json.dumps({"idPoule": {"_in": chunk}}),
                    sort=sort,
                    cached_session=cached_session,
                )
            )
        return results

    def list_entraineurs_by_ids(
        self,
        ids: list[int],
        cached_session: CachedSession | None = None,
    ) -> list[GetEntraineursResponse]:
        """Fetch multiple entraineurs by licence ID using ``_in`` (auto-chunked).

        The ``ids`` are the numeric values stored in
        ``engagement.entraineur`` / ``engagement.entraineurAdjoint``
        which correspond to the ``idLicence`` primary key.
        """
        if not ids:
            return []
        results: list[GetEntraineursResponse] = []
        for chunk in self._chunked(ids, self._BATCH_CHUNK_SIZE):
            str_ids = [str(i) for i in chunk]
            results.extend(
                self.list_entraineurs(
                    limit=len(chunk),
                    filter_criteria=json.dumps({"idLicence": {"_in": str_ids}}),
                    cached_session=cached_session,
                )
            )
        return results
