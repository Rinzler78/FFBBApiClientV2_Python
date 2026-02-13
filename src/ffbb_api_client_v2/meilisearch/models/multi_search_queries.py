from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...utils.converter_utils import from_list
from .multi_search_query import MultiSearchQuery


@dataclass
class MultiSearchQueries:
    queries: list[MultiSearchQuery] | None = None

    @staticmethod
    def from_dict(obj: Any) -> MultiSearchQueries:
        assert isinstance(obj, dict)
        queries = from_list(MultiSearchQuery.from_dict, obj, "queries")
        return MultiSearchQueries(queries=queries)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.queries is not None:
            result["queries"] = [q.to_dict() for q in self.queries]
        return result
