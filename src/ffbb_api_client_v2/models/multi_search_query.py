from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_int, from_list, from_none, from_str, from_union
from .FacetDistribution import FacetDistribution
from .FacetStats import FacetStats
from .Hit import Hit
from .MultiSearchResultCompetitions import (
    CompetitionsFacetDistribution,
    CompetitionsFacetStats,
    CompetitionsMultiSearchResult,
)
from .MultiSearchResultOrganismes import (
    OrganismesFacetDistribution,
    OrganismesFacetStats,
    OrganismesMultiSearchResult,
)
from .MultiSearchResultPratiques import (
    PratiquesFacetDistribution,
    PratiquesFacetStats,
    PratiquesMultiSearchResult,
)
from .MultiSearchResultRencontres import (
    RencontresFacetDistribution,
    RencontresFacetStats,
    RencontresMultiSearchResult,
)
from .MultiSearchResults import MultiSearchResult
from .MultiSearchResultSalles import (
    SallesFacetDistribution,
    SallesFacetStats,
    SallesMultiSearchResult,
)
from .MultiSearchResultTerrains import (
    TerrainsFacetDistribution,
    TerrainsFacetStats,
    TerrainsMultiSearchResult,
)
from .MultiSearchResultTournois import (
    TournoisFacetDistribution,
    TournoisFacetStats,
    TournoisMultiSearchResult,
)


class MultiSearchQuery:
    index_uid: str | None = None
    q: str | None = None
    facets: list[str] | None = None
    limit: int | None = None
    offset: int | None = None
    filter: list[Any] | None = None
    sort: list[Any] | None = None

    def __init__(
        self,
        index_uid: str | None,
        q: str | None,
        facets: list[str] | None = None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] = None,
        sort: list[str] = None,
    ):
        self.index_uid = index_uid
        self.q = q
        self.lower_q = q.lower() if q else None

        self.facets = facets
        self.limit = limit
        self.offset = offset
        self.filter = filter
        self.sort = sort

    @staticmethod
    def from_dict(obj: Any) -> MultiSearchQuery:
        assert isinstance(obj, dict)
        index_uid = from_union([from_str, from_none], obj.get("indexUid"))
        q = from_union([from_str, from_none], obj.get("q"))
        facets = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("facets")
        )
        limit = from_union([from_int, from_none], obj.get("limit"))
        offset = from_union([from_int, from_none], obj.get("offset"))
        filter = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], obj.get("filter")
        )
        sort = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], obj.get("sort")
        )
        return MultiSearchQuery(index_uid, q, facets, limit, filter, offset, sort)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.index_uid is not None:
            result["indexUid"] = from_union([from_str, from_none], self.index_uid)
        if self.q is not None:
            result["q"] = from_union([from_str, from_none], self.q)
        if self.facets is not None:
            result["facets"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.facets
            )
        if self.limit is not None:
            result["limit"] = from_union([from_int, from_none], self.limit)
        if self.offset is not None:
            result["offset"] = from_union([from_int, from_none], self.offset)
        if self.filter is not None:
            result["filter"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.filter
            )
        if self.sort is not None:
            result["sort"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.sort
            )
        return result

    def is_valid_result(self, result: MultiSearchResult):
        return result and (
            isinstance(result, MultiSearchResult)
            and (
                result.facet_distribution is None
                or isinstance(result.facet_distribution, FacetDistribution)
            )
            and (
                result.facet_stats is None or isinstance(result.facet_stats, FacetStats)
            )
        )

    def is_valid_hit(self, hit: Hit):
        return True

    def filter_result(self, result: MultiSearchResult) -> MultiSearchResult:
        if self.lower_q and result.hits:
            invalid_hits = [
                hit for hit in result.hits if not hit.is_valid_for_query(self.lower_q)
            ]

            if invalid_hits:
                result.estimated_total_hits -= len(invalid_hits)

                for hit in invalid_hits:
                    result.hits.remove(hit)
        return result


class OrganismesMultiSearchQuery(MultiSearchQuery):
    def __init__(
        self,
        q: str | None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] = None,
        sort: list[str] = None,
    ):
        super().__init__(
            index_uid="ffbbserver_organismes",
            q=q,
            facets=[
                "type_association.libelle",
                "type",
                "labellisation",
                "offresPratiques",
            ],
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
        )

    def is_valid_result(self, result: MultiSearchResult):
        return result and (
            isinstance(result, OrganismesMultiSearchResult)
            and (
                result.facet_distribution is None
                or isinstance(result.facet_distribution, OrganismesFacetDistribution)
            )
            and (
                result.facet_stats is None
                or isinstance(result.facet_stats, OrganismesFacetStats)
            )
        )


class RencontresMultiSearchQuery(MultiSearchQuery):
    def __init__(
        self,
        q: str | None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] = None,
        sort: list[str] = None,
    ):
        super().__init__(
            index_uid="ffbbserver_rencontres",
            q=q,
            facets=[
                "competitionId.categorie.code",
                "competitionId.typeCompetition",
                "niveau",
                "competitionId.sexe",
                "organisateur.nom",
                "organisateur.id",
                "competitionId.nomExtended",
            ],
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
        )

    def is_valid_result(self, result: MultiSearchResult):
        return result and (
            isinstance(result, RencontresMultiSearchResult)
            and (
                result.facet_distribution is None
                or isinstance(result.facet_distribution, RencontresFacetDistribution)
            )
            and (
                result.facet_stats is None
                or isinstance(result.facet_stats, RencontresFacetStats)
            )
        )


class TerrainsMultiSearchQuery(MultiSearchQuery):
    def __init__(
        self,
        q: str | None,
        facets: list[str] | None = None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] = None,
        sort: list[str] = None,
    ):
        super().__init__(
            index_uid="ffbbserver_terrains",
            q=q,
            facets=facets,
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
        )

    def is_valid_result(self, result: MultiSearchResult):
        return result and (
            isinstance(result, TerrainsMultiSearchResult)
            and (
                result.facet_distribution is None
                or isinstance(result.facet_distribution, TerrainsFacetDistribution)
            )
            and (
                result.facet_stats is None
                or isinstance(result.facet_stats, TerrainsFacetStats)
            )
        )


class SallesMultiSearchQuery(MultiSearchQuery):
    def __init__(
        self,
        q: str | None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] = None,
        sort: list[str] = None,
    ):
        super().__init__(
            index_uid="ffbbserver_salles",
            q=q,
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
        )

    def is_valid_result(self, result: MultiSearchResult):
        return result and (
            isinstance(result, SallesMultiSearchResult)
            and (
                result.facet_distribution is None
                or isinstance(result.facet_distribution, SallesFacetDistribution)
            )
            and (
                result.facet_stats is None
                or isinstance(result.facet_stats, SallesFacetStats)
            )
        )


class TournoisMultiSearchQuery(MultiSearchQuery):
    def __init__(
        self,
        q: str | None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] = None,
        sort: list[str] = None,
    ):
        super().__init__(
            index_uid="ffbbserver_tournois",
            q=q,
            facets=["sexe", "tournoiTypes3x3.libelle", "tournoiType"],
            limit=limit,
            offset=offset,
            filter=filter,
        )

    def is_valid_result(self, result: MultiSearchResult):
        return result and (
            isinstance(result, TournoisMultiSearchResult)
            and (
                result.facet_distribution is None
                or isinstance(result.facet_distribution, TournoisFacetDistribution)
            )
            and (
                result.facet_stats is None
                or isinstance(result.facet_stats, TournoisFacetStats)
            )
        )


class CompetitionsMultiSearchQuery(MultiSearchQuery):
    def __init__(
        self,
        q: str | None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] = None,
        sort: list[str] = None,
    ):
        super().__init__(
            index_uid="ffbbserver_competitions",
            q=q,
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
        )

    def is_valid_result(self, result: MultiSearchResult):
        return result and (
            isinstance(result, CompetitionsMultiSearchResult)
            and (
                result.facet_distribution is None
                or isinstance(result.facet_distribution, CompetitionsFacetDistribution)
            )
            and (
                result.facet_stats is None
                or isinstance(result.facet_stats, CompetitionsFacetStats)
            )
        )


class PratiquesMultiSearchQuery(MultiSearchQuery):
    def __init__(
        self,
        q: str | None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] = None,
        sort: list[str] = None,
    ):
        super().__init__(
            index_uid="ffbbnational_pratiques",
            q=q,
            facets=["label", "type"],
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
        )

    def is_valid_result(self, result: MultiSearchResult):
        return result and (
            isinstance(result, PratiquesMultiSearchResult)
            and (
                result.facet_distribution is None
                or isinstance(result.facet_distribution, PratiquesFacetDistribution)
            )
            and (
                result.facet_stats is None
                or isinstance(result.facet_stats, PratiquesFacetStats)
            )
        )
