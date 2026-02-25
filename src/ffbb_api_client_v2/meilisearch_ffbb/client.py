from __future__ import annotations

from typing import Any, cast

from requests_cache import CachedSession

from ..config import MEILISEARCH_BASE_URL
from ..meilisearch.client_extension import MeilisearchClientExtension
from ..meilisearch.models.federated_search_result import FederatedSearchResult
from ..meilisearch.models.meilisearch_index_settings import MeilisearchIndexSettings
from ..utils.retry_utils import RetryConfig, TimeoutConfig
from .geo_sort_order import GeoSortOrder
from .models.competitions_multi_search_query import CompetitionsMultiSearchQuery
from .models.engagements_multi_search_query import EngagementsMultiSearchQuery
from .models.formations_multi_search_query import FormationsMultiSearchQuery
from .models.multi_search_result_competitions import CompetitionsMultiSearchResult
from .models.multi_search_result_engagements import EngagementsMultiSearchResult
from .models.multi_search_result_formations import FormationsMultiSearchResult
from .models.multi_search_result_organismes import OrganismesMultiSearchResult
from .models.multi_search_result_pratiques import PratiquesMultiSearchResult
from .models.multi_search_result_rencontres import RencontresMultiSearchResult
from .models.multi_search_result_salles import SallesMultiSearchResult
from .models.multi_search_result_terrains import TerrainsMultiSearchResult
from .models.multi_search_result_tournois import TournoisMultiSearchResult
from .models.organismes_multi_search_query import OrganismesMultiSearchQuery
from .models.pratiques_multi_search_query import PratiquesMultiSearchQuery
from .models.rencontres_multi_search_query import RencontresMultiSearchQuery
from .models.salles_multi_search_query import SallesMultiSearchQuery
from .models.terrains_multi_search_query import TerrainsMultiSearchQuery
from .models.tournois_multi_search_query import TournoisMultiSearchQuery


class MeilisearchFFBBClient(MeilisearchClientExtension):
    """Client Meilisearch pour les index FFBB.

    Fournit des methodes de recherche textuelle, geo-spatiale et multi-index
    sur les 9 index Meilisearch FFBB. Les hits contiennent des objets denormalises
    (commune, salle, geo, saison embarques) contrairement au client Directus
    qui retourne des FK bruts.

    Index disponibles (9) :
        ffbbserver_organismes, ffbbserver_competitions, ffbbserver_rencontres,
        ffbbserver_salles, ffbbserver_terrains, ffbbserver_tournois,
        ffbbnational_pratiques, ffbbserver_engagements, ffbbserver_formations

    Methodes (30+) :
        - 9x ``search_*`` : recherche textuelle sur un index
        - 9x ``search_multiple_*`` : recherche batch multi-requetes
        - 4x ``search_*_by_geo`` : recherche geo-spatiale (_geoRadius)
        - ``search_organismes_by_city`` : filtre par commune.libelle
        - ``search_engagements_filtered`` : geo + sexe + niveau.code
        - ``federated_search_all`` : recherche federee multi-index
        - ``get_index_settings``, ``get_all_index_settings``
        - ``get_filterable_attributes``, ``get_sortable_attributes``
    """

    def __init__(
        self,
        bearer_token: str,
        url: str = MEILISEARCH_BASE_URL,
        debug: bool = False,
        cached_session: CachedSession | None = None,
        retry_config: RetryConfig | None = None,
        timeout_config: TimeoutConfig | None = None,
    ):
        super().__init__(
            bearer_token, url, debug, cached_session, retry_config, timeout_config
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
        """Recherche batch dans l'index ffbbserver_organismes.

        Envoie une requete multi-search avec une query par element de *names*.
        Les hits contiennent commune (Commune), salle (Salle), geo (Geo) embarques.

        Args:
            names: Liste de termes de recherche (None pour tout lister).
            filter: Filtres Meilisearch (ex: ``['type = "ASS"']``).
            sort: Tri (ex: ``['nom:asc']``). Voir ``get_sortable_attributes()``.
            limit: Nombre max de resultats par query (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de OrganismesMultiSearchResult (un par query) ou None.
        """
        if not names:
            return None

        queries = [
            OrganismesMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[OrganismesMultiSearchResult], results.results)
            if results
            else None
        )

    def search_organismes(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> OrganismesMultiSearchResult | None:
        """Recherche textuelle dans l'index ffbbserver_organismes.

        Les hits contiennent des objets denormalises : commune (Commune),
        salle (Salle), geo (Geo), saison (Saison) sont embarques.
        L'id du hit correspond au PK Directus : ``int(hit.id)`` pour ``get_organisme()``.

        Args:
            name: Terme de recherche textuel (None pour tout lister).
            filter: Filtre Meilisearch (ex: ``['type = "ASS"']``).
            sort: Tri (ex: ``['nom:asc']``).
            limit: Nombre max de resultats (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            OrganismesMultiSearchResult avec .hits et .estimated_total_hits, ou None.
        """
        results = self.search_multiple_organismes(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    # --- Rencontres ---

    def search_multiple_rencontres(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[RencontresMultiSearchResult] | None:
        """Recherche batch dans l'index ffbbserver_rencontres.

        Args:
            names: Liste de termes de recherche.
            filter: Filtres Meilisearch (ex: ``['joue = true']``).
            sort: Tri (ex: ``['date_rencontre_timestamp:desc']``).
            limit: Nombre max de resultats par query (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de RencontresMultiSearchResult (un par query) ou None.
        """
        if not names:
            return None

        queries = [
            RencontresMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[RencontresMultiSearchResult], results.results)
            if results
            else None
        )

    def search_rencontres(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> RencontresMultiSearchResult | None:
        """Recherche textuelle dans l'index ffbbserver_rencontres.

        Les hits contiennent competitionId, idOrganismeEquipe1/2, salle
        en objets denormalises. ``int(hit.id)`` → ``get_rencontre()``.

        Args:
            name: Terme de recherche (None pour tout lister).
            filter: Filtre Meilisearch (ex: ``['joue = true']``).
            sort: Tri. Voir ``get_sortable_attributes()``.
            limit: Nombre max de resultats (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            RencontresMultiSearchResult ou None.
        """
        results = self.search_multiple_rencontres(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    # --- Terrains ---

    def search_multiple_terrains(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[TerrainsMultiSearchResult] | None:
        """Recherche batch dans l'index ffbbserver_terrains.

        Args:
            names: Liste de termes de recherche.
            filter: Filtres Meilisearch (ex: ``['natureSol.code = "PARQ"']``).
            sort: Tri.
            limit: Nombre max de resultats par query (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de TerrainsMultiSearchResult (un par query) ou None.
        """
        if not names:
            return None

        queries = [
            TerrainsMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[TerrainsMultiSearchResult], results.results) if results else None
        )

    def search_terrains(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> TerrainsMultiSearchResult | None:
        """Recherche textuelle dans l'index ffbbserver_terrains.

        Les hits contiennent commune, natureSol, geo en objets denormalises.
        ``int(hit.id)`` → ``get_terrain()``.

        Args:
            name: Terme de recherche (None pour tout lister).
            filter: Filtre Meilisearch.
            sort: Tri.
            limit: Nombre max de resultats (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            TerrainsMultiSearchResult ou None.
        """
        results = self.search_multiple_terrains(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    # --- Competitions ---

    def search_multiple_competitions(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[CompetitionsMultiSearchResult] | None:
        """Recherche batch dans l'index ffbbserver_competitions.

        Args:
            names: Liste de termes de recherche.
            filter: Filtres Meilisearch (ex: ``['sexe = "Masculin"']``).
            sort: Tri.
            limit: Nombre max de resultats par query (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de CompetitionsMultiSearchResult (un par query) ou None.
        """
        if not names:
            return None

        queries = [
            CompetitionsMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[CompetitionsMultiSearchResult], results.results)
            if results
            else None
        )

    def search_competitions(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> CompetitionsMultiSearchResult | None:
        """Recherche textuelle dans l'index ffbbserver_competitions.

        Les hits contiennent categorie, organisateur, saison en objets denormalises.
        ``int(hit.id)`` → ``get_competition()``.

        Args:
            name: Terme de recherche (None pour tout lister).
            filter: Filtre Meilisearch (ex: ``['sexe = "Masculin"']``).
            sort: Tri.
            limit: Nombre max de resultats (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            CompetitionsMultiSearchResult ou None.
        """
        results = self.search_multiple_competitions(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    # --- Salles ---

    def search_multiple_salles(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[SallesMultiSearchResult] | None:
        """Recherche batch dans l'index ffbbserver_salles.

        Args:
            names: Liste de termes de recherche.
            filter: Filtres Meilisearch (ex: ``['commune.departement = "75"']``).
            sort: Tri.
            limit: Nombre max de resultats par query (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de SallesMultiSearchResult (un par query) ou None.
        """
        if not names:
            return None

        queries = [
            SallesMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return cast(list[SallesMultiSearchResult], results.results) if results else None

    def search_salles(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> SallesMultiSearchResult | None:
        """Recherche textuelle dans l'index ffbbserver_salles.

        Les hits contiennent commune (Commune), geo (Geo) embarques.
        ``int(hit.id)`` → ``get_salle()``.

        Args:
            name: Terme de recherche (None pour tout lister).
            filter: Filtre Meilisearch.
            sort: Tri.
            limit: Nombre max de resultats (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            SallesMultiSearchResult ou None.
        """
        results = self.search_multiple_salles(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    # --- Tournois ---

    def search_multiple_tournois(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[TournoisMultiSearchResult] | None:
        """Recherche batch dans l'index ffbbserver_tournois.

        Args:
            names: Liste de termes de recherche.
            filter: Filtres Meilisearch (ex: ``['sexe = "Masculin"']``).
            sort: Tri.
            limit: Nombre max de resultats par query (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de TournoisMultiSearchResult (un par query) ou None.
        """
        if not names:
            return None

        queries = [
            TournoisMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[TournoisMultiSearchResult], results.results) if results else None
        )

    def search_tournois(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> TournoisMultiSearchResult | None:
        """Recherche textuelle dans l'index ffbbserver_tournois.

        Les hits contiennent commune, geo, sexe embarques.
        ``int(hit.id)`` → ``get_tournoi()``.

        Args:
            name: Terme de recherche (None pour tout lister).
            filter: Filtre Meilisearch.
            sort: Tri.
            limit: Nombre max de resultats (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            TournoisMultiSearchResult ou None.
        """
        results = self.search_multiple_tournois(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    # --- Pratiques ---

    def search_multiple_pratiques(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[PratiquesMultiSearchResult] | None:
        """Recherche batch dans l'index ffbbnational_pratiques.

        Args:
            names: Liste de termes de recherche.
            filter: Filtres Meilisearch (ex: ``['type = "basket"']``).
            sort: Tri.
            limit: Nombre max de resultats par query (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de PratiquesMultiSearchResult (un par query) ou None.
        """
        if not names:
            return None

        queries = [
            PratiquesMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[PratiquesMultiSearchResult], results.results) if results else None
        )

    def search_pratiques(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> PratiquesMultiSearchResult | None:
        """Recherche textuelle dans l'index ffbbnational_pratiques.

        ``int(hit.id)`` correspond au PK Directus pour ``list_pratiques()``.

        Args:
            name: Terme de recherche (None pour tout lister).
            filter: Filtre Meilisearch.
            sort: Tri.
            limit: Nombre max de resultats (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            PratiquesMultiSearchResult ou None.
        """
        results = self.search_multiple_pratiques(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    # --- Engagements ---

    def search_multiple_engagements(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[EngagementsMultiSearchResult] | None:
        """Recherche batch dans l'index ffbbserver_engagements (~105k hits).

        Args:
            names: Liste de termes de recherche.
            filter: Filtres Meilisearch (ex: ``['niveau.code = "SEN"']``).
            sort: Tri.
            limit: Nombre max de resultats par query (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de EngagementsMultiSearchResult (un par query) ou None.
        """
        if not names:
            return None

        queries = [
            EngagementsMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[EngagementsMultiSearchResult], results.results)
            if results
            else None
        )

    def search_engagements(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> EngagementsMultiSearchResult | None:
        """Recherche textuelle dans l'index ffbbserver_engagements.

        Les hits contiennent idCompetition, niveau, geo embarques.
        ``int(hit.id)`` → ``get_engagement()``.

        Args:
            name: Terme de recherche (None pour tout lister).
            filter: Filtre Meilisearch (ex: ``['niveau.code = "SEN"']``).
            sort: Tri.
            limit: Nombre max de resultats (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            EngagementsMultiSearchResult ou None.
        """
        results = self.search_multiple_engagements(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    # --- Formations ---

    def search_multiple_formations(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> list[FormationsMultiSearchResult] | None:
        """Recherche batch dans l'index ffbbserver_formations (~90 hits).

        Args:
            names: Liste de termes de recherche (None pour tout lister).
            filter: Filtres Meilisearch (ex: ``['mode = "presentiel"']``).
            sort: Tri.
            limit: Nombre max de resultats par query (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Liste de FormationsMultiSearchResult (un par query) ou None.
        """
        if not names:
            return None

        queries = [
            FormationsMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[FormationsMultiSearchResult], results.results)
            if results
            else None
        )

    def search_formations(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: CachedSession | None = None,
    ) -> FormationsMultiSearchResult | None:
        """Recherche textuelle dans l'index ffbbserver_formations.

        Petit index (~90 hits). ``hit.id`` est un str (UUID Directus)
        → ``get_formation(hit.id)`` (pas de conversion int).

        Args:
            name: Terme de recherche (None pour tout lister).
            filter: Filtre Meilisearch.
            sort: Tri.
            limit: Nombre max de resultats (defaut: 10).
            cached_session: Session HTTP cache optionnelle.

        Returns:
            FormationsMultiSearchResult ou None.
        """
        results = self.search_multiple_formations(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    # --- Geo-search ---

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
        """Search organismes by geographic proximity.

        Uses Meilisearch _geoRadius() filter to find organismes near a location.

        Args:
            lat: Latitude of the center point.
            lng: Longitude of the center point.
            radius_km: Radius in kilometers. Defaults to 10.
            q: Optional search query to combine with geo filter.
            limit: Maximum results to return. Defaults to 20.
            geo_sort: Sort order for distance. Defaults to NEAREST_FIRST.
            cached_session: Optional cached session.

        Returns:
            OrganismesMultiSearchResult or None.
        """
        radius_meters = int(radius_km * 1000)
        geo_filter = f"_geoRadius({lat}, {lng}, {radius_meters})"
        sort = [f"_geoPoint({lat}, {lng}):{geo_sort.value}"]

        query = OrganismesMultiSearchQuery(
            q, limit=limit, filter=[geo_filter], sort=sort
        )
        results = self.smart_multi_search([query], cached_session)
        if results and results.results:
            return cast(OrganismesMultiSearchResult, results.results[0])
        return None

    def search_organismes_by_city(
        self,
        city_name: str,
        q: str = "",
        limit: int | None = 200,
        cached_session: CachedSession | None = None,
    ) -> OrganismesMultiSearchResult | None:
        """Search organismes located in a specific city.

        Uses the ``commune.libelle`` Meilisearch filterable facet
        to return only organismes whose commune matches *city_name*.

        Args:
            city_name: Exact city name (e.g. ``"Lille"``).
            q: Optional text query to combine with the city filter.
            limit: Maximum results to return. Defaults to 200.
            cached_session: Optional cached session.

        Returns:
            OrganismesMultiSearchResult or None.
        """
        city_filter = f'commune.libelle = "{city_name}"'
        query = OrganismesMultiSearchQuery(
            q,
            limit=limit,
            filter=[city_filter],
        )
        results = self.smart_multi_search([query], cached_session)
        if results and results.results:
            return cast(OrganismesMultiSearchResult, results.results[0])
        return None

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
        """Search salles by geographic proximity.

        Args:
            lat: Latitude of the center point.
            lng: Longitude of the center point.
            radius_km: Radius in kilometers. Defaults to 10.
            q: Optional search query to combine with geo filter.
            limit: Maximum results to return. Defaults to 20.
            geo_sort: Sort order for distance. Defaults to NEAREST_FIRST.
            cached_session: Optional cached session.

        Returns:
            SallesMultiSearchResult or None.
        """
        radius_meters = int(radius_km * 1000)
        geo_filter = f"_geoRadius({lat}, {lng}, {radius_meters})"
        sort = [f"_geoPoint({lat}, {lng}):{geo_sort.value}"]

        query = SallesMultiSearchQuery(q, limit=limit, filter=[geo_filter], sort=sort)
        results = self.smart_multi_search([query], cached_session)
        if results and results.results:
            return cast(SallesMultiSearchResult, results.results[0])
        return None

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
        """Search engagements by geographic proximity.

        Args:
            lat: Latitude of the center point.
            lng: Longitude of the center point.
            radius_km: Radius in kilometers. Defaults to 10.
            q: Optional search query to combine with geo filter.
            limit: Maximum results to return. Defaults to 20.
            geo_sort: Sort order for distance. Defaults to NEAREST_FIRST.
            cached_session: Optional cached session.

        Returns:
            EngagementsMultiSearchResult or None.
        """
        radius_meters = int(radius_km * 1000)
        geo_filter = f"_geoRadius({lat}, {lng}, {radius_meters})"
        sort = [f"_geoPoint({lat}, {lng}):{geo_sort.value}"]

        query = EngagementsMultiSearchQuery(
            q, limit=limit, filter=[geo_filter], sort=sort
        )
        results = self.smart_multi_search([query], cached_session)
        if results and results.results:
            return cast(EngagementsMultiSearchResult, results.results[0])
        return None

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
        """Search engagements with geo + sexe + niveau.code filters.

        Builds a combined Meilisearch filter from:
        - ``_geoRadius(lat, lng, radius_meters)``
        - ``idCompetition.sexe IN [...]`` (when *sexes* provided)
        - ``niveau.code IN [...]`` (when *niveau_codes* provided)

        Args:
            lat: Latitude of the center point.
            lng: Longitude of the center point.
            radius_km: Radius in kilometers. Defaults to 10.
            q: Optional text query.
            limit: Max results. Defaults to 5000.
            geo_sort: Sort order for distance. Defaults to NEAREST_FIRST.
            sexes: Sexe values (e.g. ``["Masculin", "Féminin"]``).
            niveau_codes: Niveau codes (e.g. ``["NM1", "SED1M"]``).
            cached_session: Optional cached session.

        Returns:
            EngagementsMultiSearchResult or None.
        """
        radius_meters = int(radius_km * 1000)
        filters: list[str] = [f"_geoRadius({lat}, {lng}, {radius_meters})"]
        sort = [f"_geoPoint({lat}, {lng}):{geo_sort.value}"]

        if sexes:
            quoted = ", ".join(f'"{s}"' for s in sexes)
            filters.append(f"idCompetition.sexe IN [{quoted}]")

        if niveau_codes:
            quoted = ", ".join(f'"{c}"' for c in niveau_codes)
            filters.append(f"niveau.code IN [{quoted}]")

        query = EngagementsMultiSearchQuery(q, limit=limit, filter=filters, sort=sort)
        results = self.smart_multi_search([query], cached_session)
        if results and results.results:
            return cast(EngagementsMultiSearchResult, results.results[0])
        return None

    # --- Federated search (FFBB-specific) ---

    def federated_search_all(
        self,
        q: str = "",
        limit: int = 20,
        federation_options: dict[str, Any] | None = None,
        cached_session: CachedSession | None = None,
    ) -> FederatedSearchResult | None:
        """Search across all FFBB indexes with federated results.

        Returns a single merged list of hits ranked by global relevance,
        instead of separate results per index.

        Args:
            q: Search query.
            limit: Maximum total hits in merged results. Defaults to 20.
            federation_options: Optional federation config (weights, etc.).
            cached_session: Optional cached session.

        Returns:
            FederatedSearchResult with merged hits, or None.
        """
        queries = [
            OrganismesMultiSearchQuery(q),
            RencontresMultiSearchQuery(q),
            CompetitionsMultiSearchQuery(q),
            SallesMultiSearchQuery(q),
            TerrainsMultiSearchQuery(q),
            TournoisMultiSearchQuery(q),
            PratiquesMultiSearchQuery(q),
            EngagementsMultiSearchQuery(q),
            FormationsMultiSearchQuery(q),
        ]
        options = federation_options or {}
        if "limit" not in options:
            options["limit"] = limit
        return self.federated_multi_search(
            queries=queries,
            federation_options=options,
            cached_session=cached_session,
        )

    # --- Index Settings ---

    def get_all_index_settings(
        self,
        cached_session: CachedSession | None = None,
    ) -> dict[str, MeilisearchIndexSettings]:
        """Recupere les settings de tous les index FFBB connus (9 index).

        Itere sur ``MEILISEARCH_INDEX_UIDS`` et appelle ``get_index_settings()``
        pour chacun. Les settings incluent filterableAttributes, sortableAttributes,
        searchableAttributes, etc.

        Args:
            cached_session: Session HTTP cache optionnelle.

        Returns:
            Dict {index_uid: MeilisearchIndexSettings} pour chaque index accessible.
        """
        from .config import MEILISEARCH_INDEX_UIDS

        result: dict[str, MeilisearchIndexSettings] = {}
        for uid in MEILISEARCH_INDEX_UIDS:
            settings = self.get_index_settings(uid, cached_session)
            if settings:
                result[uid] = settings
        return result
