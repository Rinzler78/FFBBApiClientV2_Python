from abc import ABC, abstractmethod
from typing import Any


class FacetStats(ABC):
    @staticmethod
    def from_dict(obj: Any) -> "FacetStats":
        # This should be implemented by concrete subclasses
        assert False, "FacetStats is abstract and cannot be instantiated"

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        return {}
