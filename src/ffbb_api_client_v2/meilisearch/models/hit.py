from abc import ABC, abstractmethod
from typing import Any


class Hit(ABC):
    @staticmethod
    def from_dict(obj: Any) -> "Hit":
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def is_valid_for_query(self, query: str) -> bool:
        raise NotImplementedError
