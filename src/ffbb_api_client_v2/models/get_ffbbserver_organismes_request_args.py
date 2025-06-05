from typing import Any

from .converters import from_int, to_class


class GetFfbbserverOrganismesRequestArgs:
    id: int

    def __init__(self, id: int) -> None:
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> "GetFfbbserverOrganismesRequestArgs":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        return GetFfbbserverOrganismesRequestArgs(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        return result


def get_ffbbserver_organismes_request_args_from_dict(
    s: Any,
) -> GetFfbbserverOrganismesRequestArgs:
    return GetFfbbserverOrganismesRequestArgs.from_dict(s)


def get_ffbbserver_organismes_request_args_to_dict(
    x: GetFfbbserverOrganismesRequestArgs,
) -> Any:
    return to_class(GetFfbbserverOrganismesRequestArgs, x)
