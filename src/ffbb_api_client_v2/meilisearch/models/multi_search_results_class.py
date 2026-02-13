from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from ...meilisearch_ffbb.config import (
    MEILISEARCH_INDEX_COMPETITIONS,
    MEILISEARCH_INDEX_ENGAGEMENTS,
    MEILISEARCH_INDEX_FORMATIONS,
    MEILISEARCH_INDEX_ORGANISMES,
    MEILISEARCH_INDEX_PRATIQUES,
    MEILISEARCH_INDEX_RENCONTRES,
    MEILISEARCH_INDEX_SALLES,
    MEILISEARCH_INDEX_TERRAINS,
    MEILISEARCH_INDEX_TOURNOIS,
    MEILISEARCH_INDEX_UIDS,
)
from ...meilisearch_ffbb.models.multi_search_result_competitions import (
    CompetitionsMultiSearchResult,
)
from ...meilisearch_ffbb.models.multi_search_result_engagements import (
    EngagementsMultiSearchResult,
)
from ...meilisearch_ffbb.models.multi_search_result_formations import (
    FormationsMultiSearchResult,
)
from ...meilisearch_ffbb.models.multi_search_result_organismes import (
    OrganismesMultiSearchResult,
)
from ...meilisearch_ffbb.models.multi_search_result_pratiques import (
    PratiquesMultiSearchResult,
)
from ...meilisearch_ffbb.models.multi_search_result_rencontres import (
    RencontresMultiSearchResult,
)
from ...meilisearch_ffbb.models.multi_search_result_salles import (
    SallesMultiSearchResult,
)
from ...meilisearch_ffbb.models.multi_search_result_terrains import (
    TerrainsMultiSearchResult,
)
from ...meilisearch_ffbb.models.multi_search_result_tournois import (
    TournoisMultiSearchResult,
)
from .multi_search_results import MultiSearchResult

# Re-export for backward compatibility
index_uids = MEILISEARCH_INDEX_UIDS

index_uids_converters: dict[str, Callable[[Any], MultiSearchResult[Any, Any, Any]]] = {
    MEILISEARCH_INDEX_ORGANISMES: OrganismesMultiSearchResult.from_dict,
    MEILISEARCH_INDEX_RENCONTRES: RencontresMultiSearchResult.from_dict,
    MEILISEARCH_INDEX_TERRAINS: TerrainsMultiSearchResult.from_dict,
    MEILISEARCH_INDEX_SALLES: SallesMultiSearchResult.from_dict,
    MEILISEARCH_INDEX_TOURNOIS: TournoisMultiSearchResult.from_dict,
    MEILISEARCH_INDEX_COMPETITIONS: CompetitionsMultiSearchResult.from_dict,
    MEILISEARCH_INDEX_ENGAGEMENTS: EngagementsMultiSearchResult.from_dict,
    MEILISEARCH_INDEX_FORMATIONS: FormationsMultiSearchResult.from_dict,
    MEILISEARCH_INDEX_PRATIQUES: PratiquesMultiSearchResult.from_dict,
}


def result_from_list(s: list[Any]) -> list[MultiSearchResult[Any, Any, Any]]:
    results: list[MultiSearchResult[Any, Any, Any]] = []

    if s:
        for element in s:
            try:
                index_uid = element["indexUid"]
                from_dict_func = index_uids_converters[index_uid]
                result = from_dict_func(element)
                results.append(result)
            except (KeyError, TypeError, ValueError, AssertionError):
                # Skip invalid or unsupported index results
                pass

    return results


@dataclass
class MultiSearchResults:
    results: list[MultiSearchResult[Any, Any, Any]] | None = None

    @staticmethod
    def from_dict(obj: Any) -> MultiSearchResults:
        assert isinstance(obj, dict)
        results_raw = obj.get("results")
        results = result_from_list(results_raw) if results_raw is not None else None
        return MultiSearchResults(results=results)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.results is not None:
            result["results"] = [r.to_dict() for r in self.results]
        return result


def multi_search_results_from_dict(s: Any) -> MultiSearchResults:
    return MultiSearchResults.from_dict(s)
