"""FFBB-specific Directus API client."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from requests_cache import CachedSession

from .._http.helper import HttpHelper
from ..directus.client import DirectusClient
from ..utils.cache_manager import CacheConfig
from ..utils.retry_utils import RetryConfig, TimeoutConfig
from .config import (
    API_FFBB_BASE_URL,
    DEFAULT_DIRECTUS_RETRY_CONFIG,
    DEFAULT_DIRECTUS_TIMEOUT_CONFIG,
    ENDPOINT_ASSETS,
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
from .models.communes_fields import CommunesFields
from .models.competition_fields import CompetitionFields
from .models.configuration_models import GetConfigurationResponse
from .models.engagements_fields import EngagementsFields
from .models.entraineurs_fields import EntraineursFields
from .models.formations_fields import FormationsFields
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
from .models.officiels_fields import OfficielsFields
from .models.organisme_fields import OrganismeFields
from .models.poule_fields import PouleFields
from .models.poules_models import GetPouleResponse
from .models.pratiques_fields import PratiquesFields
from .models.rencontres_fields import RencontresFields
from .models.saison_fields import SaisonFields
from .models.saisons_models import GetSaisonsResponse
from .models.salles_fields import SallesFields
from .models.terrains_fields import TerrainsFields
from .models.tournois_fields import TournoisFields


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
            retry_config=retry_config or DEFAULT_DIRECTUS_RETRY_CONFIG,
            timeout_config=timeout_config or DEFAULT_DIRECTUS_TIMEOUT_CONFIG,
            cache_config=cache_config,
        )

    # --- Asset URLs ---

    def get_asset_url(self, file_id: str | UUID) -> str:
        """Build the URL for a Directus file asset."""
        return f"{self.url}{ENDPOINT_ASSETS}{file_id}"

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
            fields=CompetitionFields.get_fields(),
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
            fields=PouleFields.get_fields(),
            params=params,
            cached_session=cached_session,
        )
        return GetPouleResponse.from_dict(data) if data else None

    def get_saisons(
        self,
        filter_criteria: str | None = '{"actif":{"_eq":true}}',
        cached_session: CachedSession | None = None,
    ) -> list[GetSaisonsResponse]:
        """Retrieves list of seasons."""
        params: dict[str, Any] = {}
        if filter_criteria:
            params["filter"] = filter_criteria
        data = self._list_items(
            ENDPOINT_SAISONS,
            fields=SaisonFields.get_fields(),
            params=params,
            limit=100,
            cached_session=cached_session,
        )
        return GetSaisonsResponse.from_list(data) if data else []

    def get_organisme(
        self,
        organisme_id: int,
        cached_session: CachedSession | None = None,
    ) -> GetOrganismeResponse | None:
        """Retrieves detailed information about an organisme."""
        data = self._get_item(
            f"{ENDPOINT_ORGANISMES}/{organisme_id}",
            fields=OrganismeFields.get_fields(),
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
        cached_session: CachedSession | None = None,
    ) -> GetRencontresResponse | None:
        """Retrieves a rencontre by ID."""
        data = self._get_item(
            f"{ENDPOINT_RENCONTRES}/{rencontre_id}",
            fields=RencontresFields.get_fields(),
            cached_session=cached_session,
        )
        return GetRencontresResponse.from_dict(data) if data else None

    def get_salle(
        self,
        salle_id: int,
        cached_session: CachedSession | None = None,
    ) -> GetSallesResponse | None:
        """Retrieves a salle by ID."""
        data = self._get_item(
            f"{ENDPOINT_SALLES}/{salle_id}",
            fields=SallesFields.get_fields(),
            cached_session=cached_session,
        )
        return GetSallesResponse.from_dict(data) if data else None

    def get_terrain(
        self,
        terrain_id: int,
        cached_session: CachedSession | None = None,
    ) -> GetTerrainsResponse | None:
        """Retrieves a terrain by ID."""
        data = self._get_item(
            f"{ENDPOINT_TERRAINS}/{terrain_id}",
            fields=TerrainsFields.get_fields(),
            cached_session=cached_session,
        )
        return GetTerrainsResponse.from_dict(data) if data else None

    def get_tournoi(
        self,
        tournoi_id: int,
        cached_session: CachedSession | None = None,
    ) -> GetTournoisResponse | None:
        """Retrieves a tournoi by ID."""
        data = self._get_item(
            f"{ENDPOINT_TOURNOIS}/{tournoi_id}",
            fields=TournoisFields.get_fields(),
            cached_session=cached_session,
        )
        return GetTournoisResponse.from_dict(data) if data else None

    def get_engagement(
        self,
        engagement_id: int,
        cached_session: CachedSession | None = None,
    ) -> GetEngagementsResponse | None:
        """Retrieves an engagement by ID."""
        data = self._get_item(
            f"{ENDPOINT_ENGAGEMENTS}/{engagement_id}",
            fields=EngagementsFields.get_fields(),
            cached_session=cached_session,
        )
        return GetEngagementsResponse.from_dict(data) if data else None

    def get_formation(
        self,
        formation_id: str,
        cached_session: CachedSession | None = None,
    ) -> GetFormationsResponse | None:
        """Retrieves a formation by ID."""
        data = self._get_item(
            f"{ENDPOINT_FORMATIONS}/{formation_id}",
            fields=FormationsFields.get_fields(),
            cached_session=cached_session,
        )
        return GetFormationsResponse.from_dict(data) if data else None

    def get_entraineur(
        self,
        entraineur_id: int,
        cached_session: CachedSession | None = None,
    ) -> GetEntraineursResponse | None:
        """Retrieves an entraineur by ID."""
        data = self._get_item(
            f"{ENDPOINT_ENTRAINEURS}/{entraineur_id}",
            fields=EntraineursFields.get_fields(),
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
        cached_session: CachedSession | None = None,
    ) -> list[GetCompetitionResponse | None]:
        """Lists competitions."""
        data = self._list_items(
            ENDPOINT_COMPETITIONS,
            fields=CompetitionFields.get_fields(),
            limit=limit,
            cached_session=cached_session,
        )
        return [GetCompetitionResponse.from_dict(item) for item in data] if data else []

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
        data = self._list_items(
            ENDPOINT_RENCONTRES,
            fields=RencontresFields.get_fields(),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetRencontresResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_SALLES,
            fields=SallesFields.get_fields(),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetSallesResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_TERRAINS,
            fields=TerrainsFields.get_fields(),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetTerrainsResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_TOURNOIS,
            fields=TournoisFields.get_fields(),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetTournoisResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_ENGAGEMENTS,
            fields=EngagementsFields.get_fields(),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetEngagementsResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_FORMATIONS,
            fields=FormationsFields.get_fields(),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetFormationsResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_ENTRAINEURS,
            fields=EntraineursFields.get_fields(),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetEntraineursResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_COMMUNES,
            fields=CommunesFields.get_fields(),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetCommunesResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_OFFICIELS,
            fields=OfficielsFields.get_fields(),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetOfficielsResponse.from_list(data) if data else []

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
        data = self._list_items(
            ENDPOINT_PRATIQUES,
            fields=PratiquesFields.get_fields(),
            params=self._build_list_params(filter_criteria, sort, search),
            limit=limit,
            offset=offset,
            cached_session=cached_session,
        )
        return GetPratiquesResponse.from_list(data) if data else []

    # --- Automatic pagination endpoints ---

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
        return self._fetch_all_pages(
            endpoint=ENDPOINT_RENCONTRES,
            fields=RencontresFields.get_fields(),
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
            fields=SallesFields.get_fields(),
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
            fields=TerrainsFields.get_fields(),
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
            fields=TournoisFields.get_fields(),
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
            fields=EngagementsFields.get_fields(),
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
            fields=FormationsFields.get_fields(),
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
            fields=EntraineursFields.get_fields(),
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
            fields=CommunesFields.get_fields(),
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
            fields=OfficielsFields.get_fields(),
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
            fields=PratiquesFields.get_fields(),
            from_list_fn=GetPratiquesResponse.from_list,
            filter_criteria=filter_criteria,
            sort=sort,
            search=search,
            page_size=page_size,
            max_items=max_items,
            cached_session=cached_session,
        )
