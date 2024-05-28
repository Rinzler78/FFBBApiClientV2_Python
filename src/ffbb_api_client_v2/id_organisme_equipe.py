from dataclasses import dataclass
from typing import Any

from .converters import from_none


@dataclass
class IDOrganismeEquipe:
    logo: None

    @staticmethod
    def from_dict(obj: Any) -> "IDOrganismeEquipe":
        """
        Construct a IDOrganismeEquipe object from a dictionary.

        Args:
            obj (Any): The dictionary containing the object data.

        Returns:
            IDOrganismeEquipe: The constructed IDOrganismeEquipe object.
        """
        assert isinstance(obj, dict)
        logo = from_none(obj.get("logo"))
        return IDOrganismeEquipe(logo)

    def to_dict(self) -> dict:
        """
        Convert the IDOrganismeEquipe object to a dictionary.

        Returns:
            dict: The dictionary representation of the IDOrganismeEquipe object.
        """
        result: dict = {}
        if self.logo is not None:
            result["logo"] = from_none(self.logo)
        return result
