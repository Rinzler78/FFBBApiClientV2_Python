from abc import ABC, abstractmethod
from typing import Any


class FacetDistribution(ABC):
    @staticmethod
    def from_dict(obj: Any) -> "FacetDistribution":
        return FacetDistribution()

    @abstractmethod
    def to_dict(self) -> dict:
        return {}
