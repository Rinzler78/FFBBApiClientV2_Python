from __future__ import annotations

from typing import Any

from requests_cache import CachedSession

from ..config import (
    API_FFBB_BASE_URL,
    DEFAULT_USER_AGENT,
    ENDPOINT_COMPETITIONS,
    ENDPOINT_CONFIGURATION,
    ENDPOINT_LIVES,
    ENDPOINT_ORGANISMES,
    ENDPOINT_POULES,
    ENDPOINT_SAISONS,
)
from ..helpers.http_requests_helper import catch_result
from ..helpers.http_requests_utils import http_get_json, url_with_params
from ..models.configuration_models import GetConfigurationResponse
from ..models.field_set import FieldSet
from ..models.get_competition_response import GetCompetitionResponse
from ..models.get_organisme_response import GetOrganismeResponse
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
