from __future__ import annotations

from requests_cache import CachedSession

from ..helpers.http_requests_helper import catch_result, default_cached_session
from ..helpers.http_requests_utils import http_get_json, url_with_params
from ..models.competitions_models import GetCompetitionResponse
from ..models.lives import Live, lives_from_dict
from ..models.organismes_models import GetOrganismeResponse
from ..models.poules_models import GetPouleResponse
from ..models.query_fields import (
    FieldSet,
    QueryFieldsManager,
)
from ..models.saisons_models import GetSaisonsResponse


class ApiFFBBAppClient:
    def __init__(
        self,
        bearer_token: str,
        url: str = "https://api.ffbb.app/",
        debug: bool = False,
        cached_session: CachedSession = default_cached_session,
    ):
        """
        Initializes an instance of the ApiFFBBAppClient class.

        Args:
            bearer_token (str): The bearer token used for authentication.
            url (str, optional): The base URL. Defaults to "https://api.ffbb.app/".
            debug (bool, optional): Whether to enable debug mode. Defaults to False.
            cached_session (CachedSession, optional): The cached session to use.
        """
        if not bearer_token:
            raise ValueError("bearer_token cannot be None or empty")
        self.bearer_token = bearer_token
        self.url = url
        self.debug = debug
        self.cached_session = cached_session
        self.headers = {"Authorization": f"Bearer {self.bearer_token}"}

    def get_lives(self, cached_session: CachedSession = None) -> list[Live]:
        """
        Retrieves a list of live events.

        Args:
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            List[Live]: A list of Live objects representing the live events.
        """
        url = f"{self.url}json/lives.json"
        return catch_result(
            lambda: lives_from_dict(
                http_get_json(
                    url,
                    self.headers,
                    debug=self.debug,
                    cached_session=cached_session or self.cached_session,
                )
            )
        )

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
            fields (List[str], optional): List of fields to retrieve.
                If None, uses default fields.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            GetCompetitionResponse: Competition data with nested phases,
                poules, and rencontres
        """
        url = f"{self.url}items/ffbbserver_competitions/{competition_id}"

        params = {}
        if deep_limit:
            params["deep[phases][poules][rencontres][_limit]"] = deep_limit

        if fields:
            for field in fields:
                if "fields[]" not in params:
                    params["fields[]"] = []
                params["fields[]"].append(field)
        else:
            # Use default fields from descriptor when no fields are specified
            params["fields[]"] = QueryFieldsManager.get_competition_fields(
                FieldSet.DEFAULT
            )

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
            fields (List[str], optional): List of fields to retrieve.
                If None, uses default fields.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            GetPouleResponse: Poule data with rencontres
        """
        url = f"{self.url}items/ffbbserver_poules/{poule_id}"

        params = {}
        if deep_limit:
            params["deep[rencontres][_limit]"] = deep_limit

        if fields:
            params["fields[]"] = fields
        else:
            # Use default fields from descriptor when no fields are specified
            params["fields[]"] = QueryFieldsManager.get_poule_fields(FieldSet.DEFAULT)

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
        fields: list[str] | None = None,
        filter_criteria: str | None = '{"actif":{"_eq":true}}',
        cached_session: CachedSession = None,
    ) -> list[GetSaisonsResponse]:
        """
        Retrieves list of seasons.

        Args:
            fields (List[str], optional): List of fields to retrieve.
                If None, uses default fields.
            filter_criteria (str, optional): JSON filter criteria.
                Defaults to active seasons.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            List[GetSaisonsResponse]: List of season data
        """
        url = f"{self.url}items/ffbbserver_saisons"

        params = {}
        if fields:
            params["fields[]"] = fields
        else:
            # Use default fields from descriptor when no fields are specified
            params["fields[]"] = QueryFieldsManager.get_saison_fields(FieldSet.DEFAULT)

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
        return GetSaisonsResponse.from_list(actual_data) if actual_data else []

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
            fields (List[str], optional): List of fields to retrieve.
                If None, uses default fields.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            GetOrganismeResponse: Organisme data with members, competitions, etc.
        """
        url = f"{self.url}items/ffbbserver_organismes/{organisme_id}"

        params = {}
        if fields:
            params["fields[]"] = fields
        else:
            # Use default fields from descriptor when no fields are specified
            params["fields[]"] = QueryFieldsManager.get_organisme_fields(
                FieldSet.DEFAULT
            )

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
