"""FFBB-specific Directus API client."""

from __future__ import annotations

from typing import Any

from requests_cache import CachedSession

from .._http.helper import HttpHelper
from ..directus.client import DirectusClient
from ..directus.models.field_set import FieldSet
from ..utils.cache_manager import CacheConfig
from ..utils.retry_utils import RetryConfig, TimeoutConfig
from .config import (
    API_FFBB_BASE_URL,
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
from .models.configuration_models import GetConfigurationResponse
from .models.get_communes_response import GetCommunesResponse
from .models.get_competition_response import GetCompetitionResponse
from .models.get_engagements_response import GetEngagementsResponse
from .models.get_entraineurs_response import GetEntraineursResponse
from .models.get_formations_response import GetFormationsResponse
from .models.get_officiels_response import GetOfficielsResponse
from .models.get_organisme_response import GetOrganismeResponse
from .models.get_pratiques_response import GetPratiquesResponse
from .models.get_rencontres_response import GetRencontresResponse
from .models.get_salles_response import GetSallesResponse
from .models.get_terrains_response import GetTerrainsResponse
from .models.get_tournois_response import GetTournoisResponse
from .models.lives import Live, lives_from_dict
from .models.poules_models import GetPouleResponse
from .models.query_fields_manager import QueryFieldsManager
from .models.saisons_models import GetSaisonsResponse


class ApiFFBBAppClient(DirectusClient):
    """FFBB-specific Directus API client.

    Extends DirectusClient with FFBB business endpoints:
    competitions, organismes, rencontres, salles, terrains, etc.
    """

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
        super().__init__(
            bearer_token=bearer_token,
            url=url,
            debug=debug,
            cached_session=cached_session,
            retry_config=retry_config,
            timeout_config=timeout_config,
            cache_config=cache_config,
        )

    # --- Single-item endpoints ---

    def get_lives(
        self, cached_session: CachedSession | None = None
    ) -> list[Live] | None:
        """Retrieves a list of live events."""
        url = f"{self.url}{ENDPOINT_LIVES}"
        return HttpHelper.catch_result(
            lambda: lives_from_dict(self._get_json(url, cached_session))
        )

    def get_competition(
        self,
        competition_id: int,
        deep_rencontres_limit: int | None = 1000,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetCompetitionResponse | None:
        """Retrieves detailed information about a competition."""
        params: dict[str, Any] = {}
        if deep_rencontres_limit is not None:
            params["deep[phases][poules][rencontres][_limit]"] = str(
                deep_rencontres_limit
            )
        data = self._get_item(
            f"{ENDPOINT_COMPETITIONS}/{competition_id}",
            fields=QueryFieldsManager.get_competition_fields(field_set),
            params=params,
            cached_session=cached_session,
        )
        return GetCompetitionResponse.from_dict(data) if data else None

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
        """Retrieves detailed information about a poule."""
        params: dict[str, Any] = {}
        if deep_rencontres_limit is not None:
            params["deep[rencontres][_limit]"] = str(deep_rencontres_limit)
        if deep_rencontres_filter_saison_actif:
            params["deep[rencontres][_filter][saison][actif]"] = "true"
        if deep_rencontres_sort:
            params["deep[rencontres][_sort][]"] = deep_rencontres_sort
        if deep_classements_limit is not None:
            params["deep[classements][_limit]"] = str(deep_classements_limit)
        data = self._get_item(
            f"{ENDPOINT_POULES}/{poule_id}",
            fields=QueryFieldsManager.get_poule_fields(field_set),
            params=params,
            cached_session=cached_session,
        )
        return GetPouleResponse.from_dict(data) if data else None

    def get_saisons(
        self,
        filter_criteria: str | None = '{"actif":{"_eq":true}}',
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> list[GetSaisonsResponse]:
        """Retrieves list of seasons."""
        params: dict[str, Any] = {}
        if filter_criteria:
            params["filter"] = filter_criteria
        data = self._list_items(
            ENDPOINT_SAISONS,
            fields=QueryFieldsManager.get_saison_fields(field_set),
            params=params,
            limit=100,
            cached_session=cached_session,
        )
        return GetSaisonsResponse.from_list(data) if data else []

    def get_organisme(
        self,
        organisme_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetOrganismeResponse | None:
        """Retrieves detailed information about an organisme."""
        data = self._get_item(
            f"{ENDPOINT_ORGANISMES}/{organisme_id}",
            fields=QueryFieldsManager.get_organisme_fields(field_set),
            cached_session=cached_session,
        )
        return GetOrganismeResponse.from_dict(data) if data else None

    def get_configuration(
        self,
        cached_session: CachedSession | None = None,
    ) -> GetConfigurationResponse | None:
        """Retrieves the API configuration including bearer tokens."""
        data = self._get_item(
            ENDPOINT_CONFIGURATION,
            cached_session=cached_session,
        )
        return GetConfigurationResponse.from_dict(data) if data else None

    def get_rencontre(
        self,
        rencontre_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetRencontresResponse | None:
        """Retrieves a rencontre by ID."""
        data = self._get_item(
            f"{ENDPOINT_RENCONTRES}/{rencontre_id}",
            fields=QueryFieldsManager.get_rencontres_fields(field_set),
            cached_session=cached_session,
        )
        return GetRencontresResponse.from_dict(data) if data else None

    def get_salle(
        self,
        salle_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetSallesResponse | None:
        """Retrieves a salle by ID."""
        data = self._get_item(
            f"{ENDPOINT_SALLES}/{salle_id}",
            fields=QueryFieldsManager.get_salles_fields(field_set),
            cached_session=cached_session,
        )
        return GetSallesResponse.from_dict(data) if data else None

    def get_terrain(
        self,
        terrain_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetTerrainsResponse | None:
        """Retrieves a terrain by ID."""
        data = self._get_item(
            f"{ENDPOINT_TERRAINS}/{terrain_id}",
            fields=QueryFieldsManager.get_terrains_fields(field_set),
            cached_session=cached_session,
        )
        return GetTerrainsResponse.from_dict(data) if data else None

    def get_tournoi(
        self,
        tournoi_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetTournoisResponse | None:
        """Retrieves a tournoi by ID."""
        data = self._get_item(
            f"{ENDPOINT_TOURNOIS}/{tournoi_id}",
            fields=QueryFieldsManager.get_tournois_fields(field_set),
            cached_session=cached_session,
        )
        return GetTournoisResponse.from_dict(data) if data else None

    def get_engagement(
        self,
        engagement_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetEngagementsResponse | None:
        """Retrieves an engagement by ID."""
        data = self._get_item(
            f"{ENDPOINT_ENGAGEMENTS}/{engagement_id}",
            fields=QueryFieldsManager.get_engagements_fields(field_set),
            cached_session=cached_session,
        )
        return GetEngagementsResponse.from_dict(data) if data else None

    def get_formation(
        self,
        formation_id: str,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetFormationsResponse | None:
        """Retrieves a formation by ID."""
        data = self._get_item(
            f"{ENDPOINT_FORMATIONS}/{formation_id}",
            fields=QueryFieldsManager.get_formations_fields(field_set),
            cached_session=cached_session,
        )
        return GetFormationsResponse.from_dict(data) if data else None

    def get_entraineur(
        self,
        entraineur_id: int,
        field_set: FieldSet = FieldSet.DETAILED,
        cached_session: CachedSession | None = None,
    ) -> GetEntraineursResponse | None:
        """Retrieves an entraineur by ID."""
        data = self._get_item(
            f"{ENDPOINT_ENTRAINEURS}/{entraineur_id}",
            fields=QueryFieldsManager.get_entraineurs_fields(field_set),
            cached_session=cached_session,
        )
        return GetEntraineursResponse.from_dict(data) if data else None

    # --- List endpoints ---

    def _build_list_params(
        self,
        filter_criteria: str | None = None,
        sort: list[str] | None = None,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Build common list params (filter, sort, search)."""
        params: dict[str, Any] = {}
        if filter_criteria:
            params["filter"] = filter_criteria
        if sort:
            params["sort[]"] = sort
        if search:
            params["search"] = search
        return params

    def list_competitions(
        self,
        limit: int = 10,
        field_set: FieldSet = FieldSet.BASIC,
        cached_session: CachedSession | None = None,
    ) -> list[GetCompetitionResponse | None]:
        """Lists competitions."""
        data = self._list_items(
            ENDPOINT_COMPETITIONS,
            fields=QueryFieldsManager.get_competition_fields(field_set),
            limit=limit,
            cached_session=cached_session,
        )
        return [GetCompetitionResponse.from_dict(item) for item in data] if data else []

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
        data = self._list_items(
            ENDPOINT_RENCONTRES,
            fields=QueryFieldsManager.get_rencontres_fields(field_set),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetRencontresResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_SALLES,
            fields=QueryFieldsManager.get_salles_fields(field_set),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetSallesResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_TERRAINS,
            fields=QueryFieldsManager.get_terrains_fields(field_set),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetTerrainsResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_TOURNOIS,
            fields=QueryFieldsManager.get_tournois_fields(field_set),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetTournoisResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_ENGAGEMENTS,
            fields=QueryFieldsManager.get_engagements_fields(field_set),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetEngagementsResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_FORMATIONS,
            fields=QueryFieldsManager.get_formations_fields(field_set),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetFormationsResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_ENTRAINEURS,
            fields=QueryFieldsManager.get_entraineurs_fields(field_set),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetEntraineursResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_COMMUNES,
            fields=QueryFieldsManager.get_communes_fields(field_set),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetCommunesResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_OFFICIELS,
            fields=QueryFieldsManager.get_officiels_fields(field_set),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetOfficielsResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_PRATIQUES,
            fields=QueryFieldsManager.get_pratiques_fields(field_set),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetPratiquesResponse.from_list(data) if data else []

    # --- Automatic pagination endpoints ---

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
