from typing import Any, Callable, List, Optional, Type, cast

from .converters import (
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    to_class,
)



class Query:
    facets: Optional[List[str]]
    filter: List[Any]
    index_uid: str
    limit: int
    q: str
    sort: List[Any]

    def __init__(
        self,
        facets: Optional[List[str]],
        filter: List[Any],
        index_uid: str,
        limit: int,
        q: str,
        sort: List[Any],
    ) -> None:
        self.facets = facets
        self.filter = filter
        self.index_uid = index_uid
        self.limit = limit
        self.q = q
        self.sort = sort

    @staticmethod
    def from_dict(obj: Any) -> "Query":
        assert isinstance(obj, dict)
        facets = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("facets")
        )
        filter = from_list(lambda x: x, obj.get("filter"))
        index_uid = from_str(obj.get("indexUid"))
        limit = from_int(obj.get("limit"))
        q = from_str(obj.get("q"))
        sort = from_list(lambda x: x, obj.get("sort"))
        return Query(facets, filter, index_uid, limit, q, sort)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.facets is not None:
            result["facets"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.facets
            )
        result["filter"] = from_list(lambda x: x, self.filter)
        result["indexUid"] = from_str(self.index_uid)
        result["limit"] = from_int(self.limit)
        result["q"] = from_str(self.q)
        result["sort"] = from_list(lambda x: x, self.sort)
        return result


class PostMultiSearchRequest:
    queries: List[Query]

    def __init__(self, queries: List[Query]) -> None:
        self.queries = queries

    @staticmethod
    def from_dict(obj: Any) -> "PostMultiSearchRequest":
        assert isinstance(obj, dict)
        queries = from_list(Query.from_dict, obj.get("queries"))
        return PostMultiSearchRequest(queries)

    def to_dict(self) -> dict:
        result: dict = {}
        result["queries"] = from_list(lambda x: to_class(Query, x), self.queries)
        return result


def post_multi_search_request_from_dict(s: Any) -> PostMultiSearchRequest:
    return PostMultiSearchRequest.from_dict(s)


def post_multi_search_request_to_dict(x: PostMultiSearchRequest) -> Any:
    return to_class(PostMultiSearchRequest, x)
