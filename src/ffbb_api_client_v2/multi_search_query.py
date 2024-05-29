from dataclasses import dataclass
from typing import Any, List, Optional

from ffbb_api_client_v2.converters import (
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
)


@dataclass
class MultiSearchQuery:
    index_uid: Optional[str] = None
    q: Optional[str] = None
    facets: Optional[List[str]] = None
    limit: Optional[int] = None
    filter: Optional[List[Any]] = None
    sort: Optional[List[Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> "MultiSearchQuery":
        assert isinstance(obj, dict)
        index_uid = from_union([from_str, from_none], obj.get("indexUid"))
        q = from_union([from_str, from_none], obj.get("q"))
        facets = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("facets")
        )
        limit = from_union([from_int, from_none], obj.get("limit"))
        filter = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], obj.get("filter")
        )
        sort = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], obj.get("sort")
        )
        return MultiSearchQuery(index_uid, q, facets, limit, filter, sort)

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
        if self.filter is not None:
            result["filter"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.filter
            )
        if self.sort is not None:
            result["sort"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.sort
            )
        return result
