from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

from requests_cache import CachedSession

from ..config import (
    API_FFBB_BASE_URL,
    DEFAULT_USER_AGENT,
    ENDPOINT_COMMUNES,
    ENDPOINT_COMPETITIONS,
    ENDPOINT_CONFIGURATION,
    ENDPOINT_ENGAGEMENTS,
    ENDPOINT_ENTRAINEURS,
    ENDPOINT_FORMATIONS,
    ENDPOINT_LIVES,
    ENDPOINT_OFFICIELS,
    ENDPOINT_ORGANISMES,
    ENDPOINT_POULES,
    ENDPOINT_PRATIQUES,
    ENDPOINT_RENCONTRES,
    ENDPOINT_SAISONS,
    ENDPOINT_SALLES,
    ENDPOINT_TERRAINS,
    ENDPOINT_TOURNOIS,
)
from ..helpers.http_requests_helper import catch_result
from ..helpers.http_requests_utils import http_get_json, url_with_params
from ..models.configuration_models import GetConfigurationResponse
from ..models.field_set import FieldSet
from ..models.get_communes_response import GetCommunesResponse
from ..models.get_competition_response import GetCompetitionResponse
from ..models.get_engagements_response import GetEngagementsResponse
from ..models.get_entraineurs_response import GetEntraineursResponse
from ..models.get_formations_response import GetFormationsResponse
from ..models.get_officiels_response import GetOfficielsResponse
from ..models.get_organisme_response import GetOrganismeResponse
from ..models.get_pratiques_response import GetPratiquesResponse
from ..models.get_rencontres_response import GetRencontresResponse
from ..models.get_salles_response import GetSallesResponse
from ..models.get_terrains_response import GetTerrainsResponse
from ..models.get_tournois_response import GetTournoisResponse
from ..models.lives import Live, lives_from_dict
from ..models.poules_models import GetPouleResponse
from ..models.query_fields_manager import QueryFieldsManager
from ..models.saisons_models import GetSaisonsResponse
from ..utils.cache_manager import CacheConfig, CacheManager
from ..utils.retry_utils import (
    RetryConfig,
    TimeoutConfig,
    get_default_retry_config,
    get_default_timeout_config,
)
from ..utils.secure_logging import get_secure_logger, mask_token

T = TypeVar("T")


class ApiFFBBAppClient:
    def __init__(
        self,
        bearer_token: str,
        url: str = API_FFBB_BASE_URL,
        debug: bool = False,
        cached_session: CachedSession | None = None,
        retry_config: RetryConfig | None = None,
        timeout_config: TimeoutConfig | None = None,
        cache_config: CacheConfig | None = None,
    ):
        """
        Initializes an instance of the ApiFFBBAppClient class.

        Args:
            bearer_token (str): The bearer token used for authentication.
            url (str, optional): The base URL. Defaults to "https://api.ffbb.app/".
            debug (bool, optional): Whether to enable debug mode. Defaults to False.
            cached_session (CachedSession, optional): The cached session to use.
            retry_config (RetryConfig, optional): Retry configuration. Defaults to None.
            timeout_config (TimeoutConfig, optional): Timeout configuration.
                Defaults to None.
            cache_config (CacheConfig, optional): Cache configuration. Defaults to None.
        """
        if not bearer_token or not bearer_token.strip():
            raise ValueError("bearer_token cannot be None, empty, or whitespace-only")

        # Store token securely (private attribute)
        self._bearer_token = bearer_token
        self.url = url
        self.debug = debug
        self.cached_session = cached_session
        self.headers = {
            "Authorization": f"Bearer {self._bearer_token}",
            "user-agent": DEFAULT_USER_AGENT,
        }

        # Configure retry and timeout settings
        self.retry_config = retry_config or get_default_retry_config()
        self.timeout_config = timeout_config or get_default_timeout_config()

        # Configure cache manager
        self.cache_manager = CacheManager(cache_config)
        if cached_session is None:
            self.cached_session = self.cache_manager.session
        else:
            self.cached_session = cached_session

        # Initialize secure logger
        self.logger = get_secure_logger(f"{self.__class__.__name__}")

        # Log initialization with masked token
        masked_token = mask_token(self._bearer_token)
        if self.debug:
            self.logger.info(f"ApiFFBBAppClient initialized with token: {masked_token}")
            self.logger.info(
                f"Retry config: {self.retry_config.max_attempts} attempts, "
                f"timeout: {self.timeout_config.total_timeout}s"
            )
        else:
            self.logger.info("ApiFFBBAppClient initialized successfully")

    @property
    def bearer_token(self) -> str:
        """Get the bearer token."""
        return self._bearer_token

    def get_lives(
        self, cached_session: CachedSession | None = None
    ) -> list[Live] | None:
        """
        Retrieves a list of live events with retry logic.

        Args:
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            List[Live]: A list of Live objects representing the live events.
        """
        url = f"{self.url}{ENDPOINT_LIVES}"
        return catch_result(
            lambda: lives_from_dict(
                http_get_json(
                    url,
                    self.headers,
                    debug=self.debug,
                    cached_session=cached_session or self.cached_session,
                    retry_config=self.retry_config,
                    timeout_config=self.timeout_config,
                )
            )
        )

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
        url = f"{self.url}{ENDPOINT_COMPETITIONS}/{competition_id}"

        params: dict[str, Any] = {}
        if deep_rencontres_limit is not None:
            params["deep[phases][poules][rencontres][_limit]"] = str(
                deep_rencontres_limit
            )

        params["fields[]"] = QueryFieldsManager.get_competition_fields(field_set)

        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )

        # Extract the actual data from the response wrapper
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetCompetitionResponse.from_dict(actual_data) if actual_data else None

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
        url = f"{self.url}{ENDPOINT_POULES}/{poule_id}"

        params: dict[str, Any] = {}
        if deep_rencontres_limit is not None:
            params["deep[rencontres][_limit]"] = str(deep_rencontres_limit)
        if deep_rencontres_filter_saison_actif:
            params["deep[rencontres][_filter][saison][actif]"] = "true"
        if deep_rencontres_sort:
            params["deep[rencontres][_sort][]"] = deep_rencontres_sort
        if deep_classements_limit is not None:
            params["deep[classements][_limit]"] = str(deep_classements_limit)

        params["fields[]"] = QueryFieldsManager.get_poule_fields(field_set)

        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )

        # Extract the actual data from the response wrapper
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetPouleResponse.from_dict(actual_data) if actual_data else None

    def get_saisons(
        self,
        filter_criteria: str | None = '{"actif":{"_eq":true}}',
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> list[GetSaisonsResponse]:
        """
        Retrieves list of seasons.

        Args:
            filter_criteria (str, optional): JSON filter criteria.
                Defaults to active seasons.
            field_set (FieldSet): Predefined field set to use.
                Defaults to FieldSet.DETAILED.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            List[GetSaisonsResponse]: List of season data
        """
        url = f"{self.url}{ENDPOINT_SAISONS}"

        params: dict[str, Any] = {}
        params["fields[]"] = QueryFieldsManager.get_saison_fields(field_set)

        if filter_criteria:
            params["filter"] = filter_criteria

        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )

        # Extract the actual data from the response wrapper
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data and isinstance(actual_data, list):
            return GetSaisonsResponse.from_list(actual_data)
        return []

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
        url = f"{self.url}{ENDPOINT_ORGANISMES}/{organisme_id}"

        params: dict[str, Any] = {}
        params["fields[]"] = QueryFieldsManager.get_organisme_fields(field_set)

        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )

        # Extract the actual data from the response wrapper
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetOrganismeResponse.from_dict(actual_data) if actual_data else None

    def list_competitions(
        self,
        limit: int = 10,
        field_set: FieldSet = FieldSet.BASIC,
        cached_session: CachedSession | None = None,
    ) -> list[GetCompetitionResponse | None]:
        """
        Lists competitions with optional field selection.

        Args:
            limit (int): Maximum number of competitions to return. Defaults to 10.
            field_set (FieldSet): Predefined field set to use.
                Defaults to FieldSet.BASIC.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            list[GetCompetitionResponse]: List of competition data
        """
        url = f"{self.url}{ENDPOINT_COMPETITIONS}"

        params: dict[str, Any] = {"limit": str(limit)}
        params["fields[]"] = QueryFieldsManager.get_competition_fields(field_set)

        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )

        # Extract the actual data from the response wrapper
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data and isinstance(actual_data, list):
            return [GetCompetitionResponse.from_dict(item) for item in actual_data]
        return []

    def get_configuration(
        self,
        cached_session: CachedSession | None = None,
    ) -> GetConfigurationResponse | None:
        """
        Retrieves the API configuration including bearer tokens.

        This endpoint returns configuration data including:
        - key_dh: The API bearer token for api.ffbb.app
        - key_ms: The Meilisearch bearer token for meilisearch-prod.ffbb.app

        Args:
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            GetConfigurationResponse: Configuration data with tokens
        """
        url = f"{self.url}{ENDPOINT_CONFIGURATION}"
        data = catch_result(
            lambda: http_get_json(
                url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
                retry_config=self.retry_config,
                timeout_config=self.timeout_config,
            )
        )

        # Extract the actual data from the response wrapper
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetConfigurationResponse.from_dict(actual_data) if actual_data else None

    # --- New Directus collection endpoints ---

    def get_rencontre(
        self,
        rencontre_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetRencontresResponse | None:
        """Retrieves a rencontre by ID."""
        url = f"{self.url}{ENDPOINT_RENCONTRES}/{rencontre_id}"
        params: dict[str, Any] = {}
        params["fields[]"] = QueryFieldsManager.get_rencontres_fields(field_set)
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetRencontresResponse.from_dict(actual_data) if actual_data else None

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
        """Lists rencontres with optional filtering."""
        url = f"{self.url}{ENDPOINT_RENCONTRES}"
        params: dict[str, Any] = {"limit": str(limit)}
        params["fields[]"] = QueryFieldsManager.get_rencontres_fields(field_set)
        if filter_criteria:
            params["filter"] = filter_criteria
        if sort:
            params["sort[]"] = sort
        if offset is not None:
            params["offset"] = str(offset)
        if search:
            params["search"] = search
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data and isinstance(actual_data, list):
            return GetRencontresResponse.from_list(actual_data)
        return []

    def get_salle(
        self,
        salle_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetSallesResponse | None:
        """Retrieves a salle by ID."""
        url = f"{self.url}{ENDPOINT_SALLES}/{salle_id}"
        params: dict[str, Any] = {}
        params["fields[]"] = QueryFieldsManager.get_salles_fields(field_set)
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetSallesResponse.from_dict(actual_data) if actual_data else None

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
        url = f"{self.url}{ENDPOINT_SALLES}"
        params: dict[str, Any] = {"limit": str(limit)}
        params["fields[]"] = QueryFieldsManager.get_salles_fields(field_set)
        if filter_criteria:
            params["filter"] = filter_criteria
        if sort:
            params["sort[]"] = sort
        if offset is not None:
            params["offset"] = str(offset)
        if search:
            params["search"] = search
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data and isinstance(actual_data, list):
            return GetSallesResponse.from_list(actual_data)
        return []

    def get_terrain(
        self,
        terrain_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetTerrainsResponse | None:
        """Retrieves a terrain by ID."""
        url = f"{self.url}{ENDPOINT_TERRAINS}/{terrain_id}"
        params: dict[str, Any] = {}
        params["fields[]"] = QueryFieldsManager.get_terrains_fields(field_set)
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetTerrainsResponse.from_dict(actual_data) if actual_data else None

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
        url = f"{self.url}{ENDPOINT_TERRAINS}"
        params: dict[str, Any] = {"limit": str(limit)}
        params["fields[]"] = QueryFieldsManager.get_terrains_fields(field_set)
        if filter_criteria:
            params["filter"] = filter_criteria
        if sort:
            params["sort[]"] = sort
        if offset is not None:
            params["offset"] = str(offset)
        if search:
            params["search"] = search
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data and isinstance(actual_data, list):
            return GetTerrainsResponse.from_list(actual_data)
        return []

    def get_tournoi(
        self,
        tournoi_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetTournoisResponse | None:
        """Retrieves a tournoi by ID."""
        url = f"{self.url}{ENDPOINT_TOURNOIS}/{tournoi_id}"
        params: dict[str, Any] = {}
        params["fields[]"] = QueryFieldsManager.get_tournois_fields(field_set)
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetTournoisResponse.from_dict(actual_data) if actual_data else None

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
        url = f"{self.url}{ENDPOINT_TOURNOIS}"
        params: dict[str, Any] = {"limit": str(limit)}
        params["fields[]"] = QueryFieldsManager.get_tournois_fields(field_set)
        if filter_criteria:
            params["filter"] = filter_criteria
        if sort:
            params["sort[]"] = sort
        if offset is not None:
            params["offset"] = str(offset)
        if search:
            params["search"] = search
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data and isinstance(actual_data, list):
            return GetTournoisResponse.from_list(actual_data)
        return []

    def get_engagement(
        self,
        engagement_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetEngagementsResponse | None:
        """Retrieves an engagement by ID."""
        url = f"{self.url}{ENDPOINT_ENGAGEMENTS}/{engagement_id}"
        params: dict[str, Any] = {}
        params["fields[]"] = QueryFieldsManager.get_engagements_fields(field_set)
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetEngagementsResponse.from_dict(actual_data) if actual_data else None

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
        url = f"{self.url}{ENDPOINT_ENGAGEMENTS}"
        params: dict[str, Any] = {"limit": str(limit)}
        params["fields[]"] = QueryFieldsManager.get_engagements_fields(field_set)
        if filter_criteria:
            params["filter"] = filter_criteria
        if sort:
            params["sort[]"] = sort
        if offset is not None:
            params["offset"] = str(offset)
        if search:
            params["search"] = search
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data and isinstance(actual_data, list):
            return GetEngagementsResponse.from_list(actual_data)
        return []

    def get_formation(
        self,
        formation_id: str,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetFormationsResponse | None:
        """Retrieves a formation by ID."""
        url = f"{self.url}{ENDPOINT_FORMATIONS}/{formation_id}"
        params: dict[str, Any] = {}
        params["fields[]"] = QueryFieldsManager.get_formations_fields(field_set)
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetFormationsResponse.from_dict(actual_data) if actual_data else None

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
        url = f"{self.url}{ENDPOINT_FORMATIONS}"
        params: dict[str, Any] = {"limit": str(limit)}
        params["fields[]"] = QueryFieldsManager.get_formations_fields(field_set)
        if filter_criteria:
            params["filter"] = filter_criteria
        if sort:
            params["sort[]"] = sort
        if offset is not None:
            params["offset"] = str(offset)
        if search:
            params["search"] = search
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data and isinstance(actual_data, list):
            return GetFormationsResponse.from_list(actual_data)
        return []

    def get_entraineur(
        self,
        entraineur_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetEntraineursResponse | None:
        """Retrieves an entraineur by ID."""
        url = f"{self.url}{ENDPOINT_ENTRAINEURS}/{entraineur_id}"
        params: dict[str, Any] = {}
        params["fields[]"] = QueryFieldsManager.get_entraineurs_fields(field_set)
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetEntraineursResponse.from_dict(actual_data) if actual_data else None

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
        url = f"{self.url}{ENDPOINT_ENTRAINEURS}"
        params: dict[str, Any] = {"limit": str(limit)}
        params["fields[]"] = QueryFieldsManager.get_entraineurs_fields(field_set)
        if filter_criteria:
            params["filter"] = filter_criteria
        if sort:
            params["sort[]"] = sort
        if offset is not None:
            params["offset"] = str(offset)
        if search:
            params["search"] = search
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data and isinstance(actual_data, list):
            return GetEntraineursResponse.from_list(actual_data)
        return []

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
        url = f"{self.url}{ENDPOINT_COMMUNES}"
        params: dict[str, Any] = {"limit": str(limit)}
        params["fields[]"] = QueryFieldsManager.get_communes_fields(field_set)
        if filter_criteria:
            params["filter"] = filter_criteria
        if sort:
            params["sort[]"] = sort
        if offset is not None:
            params["offset"] = str(offset)
        if search:
            params["search"] = search
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data and isinstance(actual_data, list):
            return GetCommunesResponse.from_list(actual_data)
        return []

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
        url = f"{self.url}{ENDPOINT_OFFICIELS}"
        params: dict[str, Any] = {"limit": str(limit)}
        params["fields[]"] = QueryFieldsManager.get_officiels_fields(field_set)
        if filter_criteria:
            params["filter"] = filter_criteria
        if sort:
            params["sort[]"] = sort
        if offset is not None:
            params["offset"] = str(offset)
        if search:
            params["search"] = search
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data and isinstance(actual_data, list):
            return GetOfficielsResponse.from_list(actual_data)
        return []

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
        url = f"{self.url}{ENDPOINT_PRATIQUES}"
        params: dict[str, Any] = {"limit": str(limit)}
        params["fields[]"] = QueryFieldsManager.get_pratiques_fields(field_set)
        if filter_criteria:
            params["filter"] = filter_criteria
        if sort:
            params["sort[]"] = sort
        if offset is not None:
            params["offset"] = str(offset)
        if search:
            params["search"] = search
        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data and isinstance(actual_data, list):
            return GetPratiquesResponse.from_list(actual_data)
        return []

    # --- Automatic pagination ---

    def _fetch_all_pages(
        self,
        endpoint: str,
        fields: list[str],
        from_list_fn: Callable[[list[dict[str, Any]]], list[T]],
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
        page_size: int = 100,
        max_items: int = 10000,
        cached_session: CachedSession | None = None,
    ) -> list[T]:
        """Paginate automatically via meta=total_count until all items are fetched."""
        all_items: list[T] = []
        offset = 0

        while True:
            params: dict[str, Any] = {
                "limit": str(page_size),
                "offset": str(offset),
                "meta": "total_count,filter_count",
            }
            params["fields[]"] = fields
            if filter_criteria:
                params["filter"] = filter_criteria
            if sort:
                params["sort[]"] = sort
            if search:
                params["search"] = search

            url = f"{self.url}{endpoint}"
            final_url = url_with_params(url, params)
            data = catch_result(
                lambda: http_get_json(
                    final_url,
                    self.headers,
                    debug=self.debug,
                    cached_session=cached_session or self.cached_session,
                )
            )

            if not data or not isinstance(data, dict):
                break

            actual_data = data.get("data")
            if not actual_data or not isinstance(actual_data, list):
                break

            items = from_list_fn(actual_data)
            all_items.extend(items)

            meta = data.get("meta", {})
            total = meta.get("filter_count") or meta.get("total_count") or 0

            if len(all_items) >= total:
                break

            if len(all_items) >= max_items:
                break

            if len(actual_data) < page_size:
                break

            offset += page_size

        return all_items

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
        return self._fetch_all_pages(
            endpoint=ENDPOINT_RENCONTRES,
            fields=QueryFieldsManager.get_rencontres_fields(field_set),
            from_list_fn=GetRencontresResponse.from_list,
            filter_criteria=filter_criteria,
            sort=sort,
            search=search,
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
        return self._fetch_all_pages(
            endpoint=ENDPOINT_SALLES,
            fields=QueryFieldsManager.get_salles_fields(field_set),
            from_list_fn=GetSallesResponse.from_list,
            filter_criteria=filter_criteria,
            sort=sort,
            search=search,
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
        return self._fetch_all_pages(
            endpoint=ENDPOINT_TERRAINS,
            fields=QueryFieldsManager.get_terrains_fields(field_set),
            from_list_fn=GetTerrainsResponse.from_list,
            filter_criteria=filter_criteria,
            sort=sort,
            search=search,
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
        return self._fetch_all_pages(
            endpoint=ENDPOINT_TOURNOIS,
            fields=QueryFieldsManager.get_tournois_fields(field_set),
            from_list_fn=GetTournoisResponse.from_list,
            filter_criteria=filter_criteria,
            sort=sort,
            search=search,
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
        return self._fetch_all_pages(
            endpoint=ENDPOINT_ENGAGEMENTS,
            fields=QueryFieldsManager.get_engagements_fields(field_set),
            from_list_fn=GetEngagementsResponse.from_list,
            filter_criteria=filter_criteria,
            sort=sort,
            search=search,
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
        return self._fetch_all_pages(
            endpoint=ENDPOINT_FORMATIONS,
            fields=QueryFieldsManager.get_formations_fields(field_set),
            from_list_fn=GetFormationsResponse.from_list,
            filter_criteria=filter_criteria,
            sort=sort,
            search=search,
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
        return self._fetch_all_pages(
            endpoint=ENDPOINT_ENTRAINEURS,
            fields=QueryFieldsManager.get_entraineurs_fields(field_set),
            from_list_fn=GetEntraineursResponse.from_list,
            filter_criteria=filter_criteria,
            sort=sort,
            search=search,
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
        return self._fetch_all_pages(
            endpoint=ENDPOINT_COMMUNES,
            fields=QueryFieldsManager.get_communes_fields(field_set),
            from_list_fn=GetCommunesResponse.from_list,
            filter_criteria=filter_criteria,
            sort=sort,
            search=search,
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
        return self._fetch_all_pages(
            endpoint=ENDPOINT_OFFICIELS,
            fields=QueryFieldsManager.get_officiels_fields(field_set),
            from_list_fn=GetOfficielsResponse.from_list,
            filter_criteria=filter_criteria,
            sort=sort,
            search=search,
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
        return self._fetch_all_pages(
            endpoint=ENDPOINT_PRATIQUES,
            fields=QueryFieldsManager.get_pratiques_fields(field_set),
            from_list_fn=GetPratiquesResponse.from_list,
            filter_criteria=filter_criteria,
            sort=sort,
            search=search,
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )
