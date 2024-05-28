from dataclasses import dataclass
from typing import Any, Optional

from .converters import from_none, from_str, from_union


@dataclass
class IDPoule:
    nom: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "IDPoule":
        """
        Convert a dictionary object to an instance of IDPoule.

        Args:
            obj (Any): The dictionary object to convert.

        Returns:
            IDPoule: An instance of IDPoule.

        """
        assert isinstance(obj, dict)
        nom = from_union([from_str, from_none], obj.get("nom"))
        return IDPoule(nom)

    def to_dict(self) -> dict:
        """
        Convert the IDPoule instance to a dictionary object.

        Returns:
            dict: The dictionary representation of the IDPoule instance.

        """
        result: dict = {}
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        return result
