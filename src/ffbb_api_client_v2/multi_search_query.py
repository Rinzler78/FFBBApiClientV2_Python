from typing import Any, List, Optional

from .converters import from_int, from_list, from_none, from_str, from_union
from .FacetDistribution import FacetDistribution
from .FacetStats import FacetStats
from .Hit import Hit
from .multi_search_result_competitions import (
    CompetitionsFacetDistribution,
    CompetitionsFacetStats,
)
from .multi_search_result_organismes import (
    OrganismesFacetDistribution,
    OrganismesFacetStats,
)
from .multi_search_result_pratiques import (
    PratiquesFacetDistribution,
    PratiquesFacetStats,
)
from .multi_search_result_rencontres import (
    RencontresFacetDistribution,
    RencontresFacetStats,
)
from .multi_search_result_salles import SallesFacetDistribution, SallesFacetStats
from .multi_search_result_terrains import TerrainsFacetDistribution, TerrainsFacetStats
from .multi_search_result_tournois import TournoisFacetDistribution, TournoisFacetStats
from .multi_search_results import MultiSearchResult
from .MultiSearchResultCompetitions import CompetitionsMultiSearchResult
from .MultiSearchResultOrganismes import OrganismesMultiSearchResult
from .MultiSearchResultPratiques import PratiquesMultiSearchResult
from .MultiSearchResultRencontres import RencontresMultiSearchResult
from .MultiSearchResultSalles import SallesMultiSearchResult
from .MultiSearchResultTerrains import TerrainsMultiSearchResult
from .MultiSearchResultTournois import TournoisMultiSearchResult


class MultiSearchQuery:
    index_uid: Optional[str] = None
    q: Optional[str] = None
    facets: Optional[List[str]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    filter: Optional[List[Any]] = None
    sort: Optional[List[Any]] = None

    def __init__(
        self,
        index_uid: Optional[str],
        q: Optional[str],
        facets: Optional[List[str]] = None,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        filter: List[str] = None,
        sort: List[str] = None,
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
    def from_dict(obj: Any) -> "MultiSearchQuery":
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
        q: Optional[str],
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        filter: List[str] = None,
        sort: List[str] = None,
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
        q: Optional[str],
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        filter: List[str] = None,
        sort: List[str] = None,
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
        q: Optional[str],
        facets: Optional[List[str]] = None,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        filter: List[str] = None,
        sort: List[str] = None,
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
        q: Optional[str],
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        filter: List[str] = None,
        sort: List[str] = None,
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
        q: Optional[str],
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        filter: List[str] = None,
        sort: List[str] = None,
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
        q: Optional[str],
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        filter: List[str] = None,
        sort: List[str] = None,
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
        q: Optional[str],
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        filter: List[str] = None,
        sort: List[str] = None,
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
