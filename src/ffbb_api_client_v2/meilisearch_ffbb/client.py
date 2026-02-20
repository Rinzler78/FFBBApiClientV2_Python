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
        """Get settings for all known FFBB Meilisearch indexes."""
        from .config import MEILISEARCH_INDEX_UIDS

        result: dict[str, MeilisearchIndexSettings] = {}
        for uid in MEILISEARCH_INDEX_UIDS:
            settings = self.get_index_settings(uid, cached_session)
            if settings:
                result[uid] = settings
        return result
