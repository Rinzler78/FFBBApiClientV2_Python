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
    """Client REST Directus pour l'API FFBB.

    Accede aux collections Directus via des endpoints REST parametres par des
    ``fields[]`` qui controlent la morphologie de la reponse :

    - **FK-only** (int brut) : necessite un appel supplementaire pour resoudre
    - **Embedded** (dot notation) : objets expandus inline par Directus

    Collections : organismes, competitions, poules, engagements, rencontres,
    salles, terrains, tournois, entraineurs, formations, communes, officiels,
    pratiques, saisons, lives.

    Methodes :
        - 12x ``get_*`` : recuperation par ID (single item)
        - 10x ``list_*`` : liste paginee avec filter/sort/search
        - 10x ``list_all_*`` : pagination automatique exhaustive
        - ``get_lives()``, ``get_saisons()``, ``get_asset_url()``
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
        """Construit l'URL de telechargement d'un fichier Directus.

        Utilise pour resoudre les FK de type UUID (logo, photo, image).

        Args:
            file_id: UUID du fichier (str ou UUID).

        Returns:
            URL complete de l'asset Directus.
        """
        return f"{self.url}{ENDPOINT_ASSETS}{file_id}"

    # --- Single-item endpoints ---

    def get_lives(
        self, cached_session: CachedSession | None = None
    ) -> list[Live] | None:
        """Recupere les matchs en direct.

        FK a resoudre dans chaque Live : match_id (int) → ``get_rencontre()``.
        Embedded : clock, external_id, team_engagement_home/out.

        Args:
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de Live ou None si aucun match en cours.
        """
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
        """Recupere une competition par son ID Directus.

        Utilise CompetitionFields. Le parametre ``deep`` controle la limite
        des rencontres nestees dans phases.poules.rencontres.

        FK a resoudre : saison (int), competition_origine (int),
        idCompetitionPere (int), organisateur (int), logo (UUID), poules (list[int]).
        Embedded : categorie, typeCompetitionGenerique, phases (hybride).

        Args:
            competition_id: ID numerique de la competition.
            deep_rencontres_limit: Limite Directus pour les rencontres nestees.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            GetCompetitionResponse ou None si non trouve.
        """
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
        """Recupere une poule par son ID Directus.

        Utilise PouleFields. Parametres ``deep`` pour rencontres et classements.

        FK a resoudre : id_competition (int), rencontres (list[int]),
        engagements (list[int]).
        Embedded hybride : classements (list[TeamRanking]) contient des FK
        implicites (organisme_id, id_engagement).

        Args:
            poule_id: ID numerique de la poule.
            deep_rencontres_limit: Limite pour rencontres nestees.
            deep_rencontres_filter_saison_actif: Filtre saison active.
            deep_rencontres_sort: Champ de tri des rencontres.
            deep_classements_limit: Limite pour classements nestes.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            GetPouleResponse ou None si non trouve.
        """
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
        """Recupere la liste des saisons.

        Feuille terminale — aucune FK a resoudre.

        Args:
            filter_criteria: Filtre JSON Directus. Defaut : saisons actives.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de GetSaisonsResponse (vide si aucun resultat).
        """
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
        """Recupere un organisme par son ID Directus.

        Utilise OrganismeFields.

        FK a resoudre : commune (int), salle (int), saison (int),
        organisme_id_pere (int), engagements (list[int]),
        competitions (list[int]), organismes_fils (list[int]), logo (UUID).
        Embedded : cartographie, membres, offres_pratiques, labellisation.

        Args:
            organisme_id: ID numerique de l'organisme.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            GetOrganismeResponse ou None si non trouve.
        """
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
        """Recupere une rencontre par son ID Directus.

        Utilise RencontresFields. 100% FK-only : competitionId, idEngagementEquipe1/2,
        idOrganismeEquipe1/2, idPoule, saison, salle (tous int).

        Args:
            rencontre_id: ID numerique de la rencontre.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            GetRencontresResponse ou None si non trouve.
        """
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
        """Recupere une salle par son ID Directus.

        FK a resoudre : commune (int).
        Embedded : cartographie (Cartographie).

        Args:
            salle_id: ID numerique de la salle.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            GetSallesResponse ou None si non trouve.
        """
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
        """Recupere un terrain par son ID Directus.

        FK a resoudre : commune (int).
        Embedded : natureSol (NatureSol), cartographie (Cartographie).

        Args:
            terrain_id: ID numerique du terrain.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            GetTerrainsResponse ou None si non trouve.
        """
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
        """Recupere un tournoi par son ID Directus.

        FK a resoudre : commune (int).
        Embedded : cartographie (Cartographie), document_flyer (DocumentFlyer).

        Args:
            tournoi_id: ID numerique du tournoi.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            GetTournoisResponse ou None si non trouve.
        """
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
        """Recupere un engagement par son ID Directus.

        Utilise EngagementsFields.

        FK a resoudre : idCompetition (int), idOrganisme (int),
        idOrganismeCtc (int), idPoule (int), entraineur (int),
        entraineurAdjoint (int), logo/photo/logo_genius (UUID),
        rencontres_domiciles (list[int]), rencontres_exterieur (list[int]).
        Embedded : niveau (Categorie), positions (list[EngagementPosition]).

        Args:
            engagement_id: ID numerique de l'engagement.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            GetEngagementsResponse ou None si non trouve.
        """
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
        """Recupere une formation par son ID Directus (str, pas int).

        FK a resoudre : image (UUID).
        Embedded : domain (Folder), theme (Folder).

        Args:
            formation_id: ID string (UUID) de la formation.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            GetFormationsResponse ou None si non trouve.
        """
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
        """Recupere un entraineur par son ID Directus (idLicence).

        FK a resoudre : commune (int).
        Feuille terminale — pas d'embedded complexe.

        Args:
            entraineur_id: ID numerique (licence) de l'entraineur.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            GetEntraineursResponse ou None si non trouve.
        """
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
        """Liste les competitions (paginee).

        Args:
            limit: Nombre max d'items (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de GetCompetitionResponse.
        """
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
        """Liste les rencontres (paginee) avec filtres optionnels.

        Args:
            limit: Nombre max d'items (defaut: 10).
            filter_criteria: Filtre JSON Directus (ex: ``'{"joue":{"_eq":true}}'``).
            sort: Champs de tri (ex: ``["date_rencontre"]``).
            offset: Offset pour la pagination.
            search: Recherche plein-texte Directus.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de GetRencontresResponse.
        """
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
        """Liste les salles (paginee) avec filtres optionnels.

        Args:
            limit: Nombre max d'items.
            filter_criteria: Filtre JSON Directus.
            sort: Champs de tri.
            offset: Offset pagination.
            search: Recherche plein-texte.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de GetSallesResponse.
        """
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
        """Liste les terrains (paginee) avec filtres optionnels.

        Args:
            limit: Nombre max d'items.
            filter_criteria: Filtre JSON Directus.
            sort: Champs de tri.
            offset: Offset pagination.
            search: Recherche plein-texte.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de GetTerrainsResponse.
        """
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
        """Liste les tournois (paginee) avec filtres optionnels.

        Args:
            limit: Nombre max d'items.
            filter_criteria: Filtre JSON Directus.
            sort: Champs de tri.
            offset: Offset pagination.
            search: Recherche plein-texte.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de GetTournoisResponse.
        """
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
        """Liste les engagements (paginee) avec filtres optionnels.

        Args:
            limit: Nombre max d'items.
            filter_criteria: Filtre JSON Directus (ex: ``'{"idPoule":{"_eq":123}}'``).
            sort: Champs de tri.
            offset: Offset pagination.
            search: Recherche plein-texte.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de GetEngagementsResponse.
        """
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
        """Liste les formations (paginee) avec filtres optionnels.

        Args:
            limit: Nombre max d'items.
            filter_criteria: Filtre JSON Directus.
            sort: Champs de tri.
            offset: Offset pagination.
            search: Recherche plein-texte.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de GetFormationsResponse.
        """
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
        """Liste les entraineurs (paginee) avec filtres optionnels.

        Args:
            limit: Nombre max d'items.
            filter_criteria: Filtre JSON Directus.
            sort: Champs de tri.
            offset: Offset pagination.
            search: Recherche plein-texte.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de GetEntraineursResponse.
        """
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
        """Liste les communes (paginee) avec filtres optionnels.

        Feuille terminale — pas de FK a resoudre dans les items.
        Utilisee pour resoudre les FK commune des autres entites :
        ``list_communes(filter_criteria='{"id":{"_eq":N}}')``.

        Args:
            limit: Nombre max d'items.
            filter_criteria: Filtre JSON Directus (ex: ``'{"id":{"_eq":42}}'``).
            sort: Champs de tri.
            offset: Offset pagination.
            search: Recherche plein-texte (ex: ``"Paris"``).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de GetCommunesResponse.
        """
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
        """Liste les officiels (paginee) avec filtres optionnels.

        Feuille terminale — pas de FK a resoudre.

        Args:
            limit: Nombre max d'items.
            filter_criteria: Filtre JSON Directus.
            sort: Champs de tri.
            offset: Offset pagination.
            search: Recherche plein-texte.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de GetOfficielsResponse.
        """
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
        """Liste les pratiques (paginee) avec filtres optionnels.

        Feuille terminale — pas de FK a resoudre.

        Args:
            limit: Nombre max d'items.
            filter_criteria: Filtre JSON Directus.
            sort: Champs de tri.
            offset: Offset pagination.
            search: Recherche plein-texte.
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de GetPratiquesResponse.
        """
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
        """Recupere toutes les rencontres avec pagination automatique.

        Args:
            filter_criteria: Filtre JSON Directus.
            sort: Champs de tri.
            search: Recherche plein-texte.
            page_size: Taille de page (defaut: 100).
            max_items: Nombre max total d'items (defaut: 10000).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste complete de GetRencontresResponse.
        """
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
