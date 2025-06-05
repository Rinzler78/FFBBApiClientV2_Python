from typing import Any, Optional

from .converters import from_float, from_none, from_union, to_float


class Geo:
    lat: Optional[float] = None
    lng: Optional[float] = None

    def __init__(self, lat: Optional[float], lng: Optional[float]):
        self.lat = lat
        self.lng = lng

    @staticmethod
    def from_dict(obj: Any) -> "Geo":
        assert isinstance(obj, dict)
        lat = from_union([from_float, from_none], obj.get("lat"))
        lng = from_union([from_float, from_none], obj.get("lng"))
        return Geo(lat, lng)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.lat is not None:
            result["lat"] = from_union([to_float, from_none], self.lat)
        if self.lng is not None:
            result["lng"] = from_union([to_float, from_none], self.lng)
        return result
