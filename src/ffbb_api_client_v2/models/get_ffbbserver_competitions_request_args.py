from typing import Any, Type, cast

from .converters import from_int, to_class


class GetFfbbserverCompetitionsRequestArgs:
    id: int

    def __init__(self, id: int) -> None:
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> "GetFfbbserverCompetitionsRequestArgs":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        return GetFfbbserverCompetitionsRequestArgs(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        return result


def get_ffbbserver_competitions_request_args_from_dict(
    s: Any,
) -> GetFfbbserverCompetitionsRequestArgs:
    return GetFfbbserverCompetitionsRequestArgs.from_dict(s)


def get_ffbbserver_competitions_request_args_to_dict(
    x: GetFfbbserverCompetitionsRequestArgs,
) -> Any:
    return to_class(GetFfbbserverCompetitionsRequestArgs, x)
