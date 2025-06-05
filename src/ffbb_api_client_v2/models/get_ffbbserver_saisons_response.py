from typing import Any, Callable, List, Type, cast

from .converters import from_list, from_str, to_class



class Datum:
    id: int

    def __init__(self, id: int) -> None:
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> "Datum":
        assert isinstance(obj, dict)
        id = int(from_str(obj.get("id")))
        return Datum(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(str(self.id))
        return result


class GetFfbbserverSaisonsResponse:
    data: List[Datum]

    def __init__(self, data: List[Datum]) -> None:
        self.data = data

    @staticmethod
    def from_dict(obj: Any) -> "GetFfbbserverSaisonsResponse":
        assert isinstance(obj, dict)
        data = from_list(Datum.from_dict, obj.get("data"))
        return GetFfbbserverSaisonsResponse(data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_list(lambda x: to_class(Datum, x), self.data)
        return result


def get_ffbbserver_saisons_response_from_dict(s: Any) -> GetFfbbserverSaisonsResponse:
    return GetFfbbserverSaisonsResponse.from_dict(s)


def get_ffbbserver_saisons_response_to_dict(x: GetFfbbserverSaisonsResponse) -> Any:
    return to_class(GetFfbbserverSaisonsResponse, x)
