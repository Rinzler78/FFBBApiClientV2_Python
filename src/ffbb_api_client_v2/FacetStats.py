from dataclasses import dataclass
from typing import Any


@dataclass
class FacetStats:
    pass

    @staticmethod
    def from_dict(obj: Any) -> "FacetStats":
        assert isinstance(obj, dict)
        return FacetStats()

    def to_dict(self) -> dict:
        result: dict = {}
        return result
