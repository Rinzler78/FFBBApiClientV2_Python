from abc import ABC, abstractmethod
from typing import Any


class FacetStats(ABC):
    @staticmethod
    def from_dict(obj: Any) -> "FacetStats":
        FacetStats()

    @abstractmethod
    def to_dict(self) -> dict:
        return {}
