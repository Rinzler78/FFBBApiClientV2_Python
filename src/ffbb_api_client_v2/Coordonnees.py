from typing import Any, List, Optional

from .converters import from_float, from_list, from_none, from_str, from_union, to_float


class Coordonnees:
    type: Optional[str] = None
    coordinates: Optional[List[float]] = None

    def __init__(self, type: Optional[str], coordinates: Optional[List[float]]):
        self.type = type
        self.coordinates = coordinates

    @staticmethod
    def from_dict(obj: Any) -> "Coordonnees":
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        coordinates = from_union(
            [lambda x: from_list(from_float, x), from_none], obj.get("coordinates")
        )
        return Coordonnees(type, coordinates)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        if self.coordinates is not None:
            result["coordinates"] = from_union(
                [lambda x: from_list(to_float, x), from_none], self.coordinates
            )
        return result
