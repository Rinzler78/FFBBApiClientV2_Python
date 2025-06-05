from typing import Any, Type, cast

from .converters import from_int, to_class


class GetFfbbserverPoulesRequestArgs:
    id: int

    def __init__(self, id: int) -> None:
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> "GetFfbbserverPoulesRequestArgs":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        return GetFfbbserverPoulesRequestArgs(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        return result


def get_ffbbserver_poules_request_args_from_dict(
    s: Any,
) -> GetFfbbserverPoulesRequestArgs:
    return GetFfbbserverPoulesRequestArgs.from_dict(s)


def get_ffbbserver_poules_request_args_to_dict(
    x: GetFfbbserverPoulesRequestArgs,
) -> Any:
    return to_class(GetFfbbserverPoulesRequestArgs, x)
