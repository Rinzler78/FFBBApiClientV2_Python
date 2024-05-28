from dataclasses import dataclass
from typing import Any, Optional
from uuid import UUID

from .converters import from_none, from_union


@dataclass
class Logo:
    id: Optional[UUID] = None

    @staticmethod
    def from_dict(obj: Any) -> "Logo":
        """
        Convert a dictionary object to a Logo object.

        Args:
            obj (Any): The dictionary object to convert.

        Returns:
            Logo: The converted Logo object.
        """
        assert isinstance(obj, dict)
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        return Logo(id)

    def to_dict(self) -> dict:
        """
        Convert the Logo object to a dictionary.

        Returns:
            dict: The converted dictionary object.
        """
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([lambda x: str(x), from_none], self.id)
        return result
