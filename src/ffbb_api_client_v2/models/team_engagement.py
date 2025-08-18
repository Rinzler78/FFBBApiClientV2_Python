from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_none, from_str, from_union, to_class
from .logo import Logo


@dataclass
class TeamEngagement:
    nom_officiel: str | None = None
    nom_usuel: str | None = None
    code_abrege: str | None = None
    logo: Logo | None = None

    def __init__(
        self,
        nom_officiel: str | None,
        nom_usuel: str | None,
        code_abrege: str | None,
        logo: Logo | None,
    ) -> None:
        self.nom_officiel = nom_officiel
        self.nom_usuel = nom_usuel
        self.code_abrege = code_abrege
        self.logo = logo

    @staticmethod
    def from_dict(obj: Any) -> TeamEngagement:
        """
        Convert a dictionary object to a TeamEngagement instance.

        Args:
            obj (Any): The dictionary object to convert.

        Returns:
            TeamEngagement: The converted TeamEngagement instance.
        """
        assert isinstance(obj, dict)
        nom_officiel = from_union([from_str, from_none], obj.get("nomOfficiel"))
        nom_usuel = from_union([from_str, from_none], obj.get("nomUsuel"))
        code_abrege = from_union([from_str, from_none], obj.get("codeAbrege"))
        logo = from_union([Logo.from_dict, from_none], obj.get("logo"))
        return TeamEngagement(nom_officiel, nom_usuel, code_abrege, logo)

    def to_dict(self) -> dict:
        """
        Convert the TeamEngagement instance to a dictionary object.

        Returns:
            dict: The converted dictionary object.
        """
        result: dict = {}
        if self.nom_officiel is not None:
            result["nomOfficiel"] = from_union([from_str, from_none], self.nom_officiel)
        if self.nom_usuel is not None:
            result["nomUsuel"] = from_union([from_str, from_none], self.nom_usuel)
        if self.code_abrege is not None:
            result["codeAbrege"] = from_union([from_str, from_none], self.code_abrege)
        if self.logo is not None:
            result["logo"] = from_union(
                [lambda x: to_class(Logo, x), from_none], self.logo
            )
        return result
