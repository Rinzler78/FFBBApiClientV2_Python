from dataclasses import dataclass
from typing import Any, Optional

from .converters import from_none, from_str, from_union


@dataclass
class Salle:
    libelle: Optional[str] = None
    libelle2: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Salle":
        """
        Convert a dictionary object to a Salle instance.

        Args:
            obj (Any): The dictionary object to convert.

        Returns:
            Salle: The converted Salle instance.
        """
        assert isinstance(obj, dict)
        libelle = from_union([from_str, from_none], obj.get("libelle"))
        libelle2 = from_union([from_str, from_none], obj.get("libelle2"))
        return Salle(libelle, libelle2)

    def to_dict(self) -> dict:
        """
        Convert the Salle instance to a dictionary object.

        Returns:
            dict: The converted dictionary object.
        """
        result: dict = {}
        if self.libelle is not None:
            result["libelle"] = from_union([from_str, from_none], self.libelle)
        if self.libelle2 is not None:
            result["libelle2"] = from_union([from_str, from_none], self.libelle2)
        return result
