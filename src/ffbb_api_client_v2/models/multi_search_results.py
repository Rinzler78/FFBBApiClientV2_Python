from typing import Any, List, Optional

from ..utils.converters import from_list, from_none, from_union, to_class
from .competitions_multi_search_result import CompetitionsMultiSearchResult
from .multi_search_result import MultiSearchResult
from .organismes_multi_search_result import OrganismesMultiSearchResult
from .pratiques_multi_search_result import PratiquesMultiSearchResult
from .rencontres_multi_search_result import RencontresMultiSearchResult
from .salles_multi_search_result import SallesMultiSearchResult
from .terrains_multi_search_result import TerrainsMultiSearchResult
from .tournois_multi_search_result import TournoisMultiSearchResult

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


def result_from_list(s: List[Any]) -> List[MultiSearchResult]:
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
    results: Optional[List[MultiSearchResult]] = None

    def __init__(self, results: Optional[List[MultiSearchResult]]) -> None:
        self.results = results

    @staticmethod
    def from_dict(obj: Any) -> "MultiSearchResults":
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
