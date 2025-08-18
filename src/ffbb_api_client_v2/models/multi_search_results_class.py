from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_list, from_none, from_union, to_class
from .multi_search_result_competitions import CompetitionsMultiSearchResult
from .multi_search_result_organismes import OrganismesMultiSearchResult
from .multi_search_result_pratiques import PratiquesMultiSearchResult
from .multi_search_result_rencontres import RencontresMultiSearchResult
from .multi_search_result_salles import SallesMultiSearchResult
from .multi_search_result_terrains import TerrainsMultiSearchResult
from .multi_search_result_tournois import TournoisMultiSearchResult
from .multi_search_results import MultiSearchResult

index_uids = [
    "ffbbserver_organismes",
    "ffbbserver_rencontres",
    "ffbbserver_terrains",
    "ffbbserver_salles",
    "ffbbserver_tournois",
    "ffbbserver_competitions",
    "ffbbnational_pratiques",
]

index_uids_converters = {
    index_uids[0]: lambda x: OrganismesMultiSearchResult.from_dict(x),
    index_uids[1]: lambda x: RencontresMultiSearchResult.from_dict(x),
    index_uids[2]: lambda x: TerrainsMultiSearchResult.from_dict(x),
    index_uids[3]: lambda x: SallesMultiSearchResult.from_dict(x),
    index_uids[4]: lambda x: TournoisMultiSearchResult.from_dict(x),
    index_uids[5]: lambda x: CompetitionsMultiSearchResult.from_dict(x),
    index_uids[6]: lambda x: PratiquesMultiSearchResult.from_dict(x),
}


def result_from_list(s: list[Any]) -> list[MultiSearchResult]:
    results = []

    if s:
        for element in s:
            try:
                index_uid = element["indexUid"]
                from_dict_func = index_uids_converters[index_uid]
                result = from_dict_func(element)
                results.append(result)
            except Exception:
                # Skip invalid or unsupported index results
                pass

    return results


class MultiSearchResults:
    results: list[MultiSearchResult] | None = None

    def __init__(self, results: list[MultiSearchResult] | None) -> None:
        self.results = results

    @staticmethod
    def from_dict(obj: Any) -> MultiSearchResults:
        assert isinstance(obj, dict)
        results = from_union([result_from_list, from_none], obj.get("results"))
        return MultiSearchResults(results)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.results is not None:
            result["results"] = from_union(
                [
                    lambda x: from_list(lambda x: to_class(MultiSearchResult, x), x),
                    from_none,
                ],
                self.results,
            )
        return result


def multi_search_results_from_dict(s: Any) -> MultiSearchResults:
    return MultiSearchResults.from_dict(s)


def multi_search_results_to_dict(x: MultiSearchResults) -> Any:
    return to_class(MultiSearchResults, x)
