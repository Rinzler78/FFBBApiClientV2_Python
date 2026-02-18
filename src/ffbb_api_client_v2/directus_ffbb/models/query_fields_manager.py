from abc import ABC, abstractmethod


class QueryFieldsManager(ABC):
    """Abstract base class for endpoint field definitions."""

    @classmethod
    @abstractmethod
    def get_fields(cls) -> list[str]:
        """Return the complete list of fields for this endpoint."""
        ...
