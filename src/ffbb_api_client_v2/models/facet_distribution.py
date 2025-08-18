from abc import ABC, abstractmethod
from typing import Any


class FacetDistribution(ABC):
    @staticmethod
    def from_dict(obj: Any) -> "FacetDistribution":
        # Cannot instantiate abstract class - should be implemented by subclasses
        raise NotImplementedError(
            "FacetDistribution is abstract and cannot be instantiated"
        )

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        return {}
