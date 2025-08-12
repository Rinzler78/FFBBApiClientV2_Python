from __future__ import annotations

from dataclasses import dataclass


# Query Parameters Model
@dataclass
class SaisonsQuery:
    fields_: list[str] = None  # Original: fields[]
    filter: str | None = '{"actif":{"_eq":true}}'  # Original: filter


# Response Model
@dataclass
class GetSaisonsResponse:
    id: str
    nom: str | None = None
    actif: bool | None = None

    @classmethod
    def from_dict(cls, data: dict) -> GetSaisonsResponse:
        """Convert dictionary to GetSaisonsResponse instance."""
        if not data:
            return None

        # Handle case where data is not a dictionary
        if not isinstance(data, dict):
            return None

        # Handle API error responses
        if "errors" in data:
            return None

        return cls(
            id=str(data.get("id", "")),
            nom=str(data.get("nom", "")) if data.get("nom") else None,
            actif=bool(data.get("actif", False)) if "actif" in data else None,
        )

    @classmethod
    def from_list(cls, data_list: list) -> list[GetSaisonsResponse]:
        """Convert list of dictionaries to list of SaisonsModel instances."""
        if not data_list:
            return []

        # Filter out None results from from_dict (invalid items)
        return [
            result
            for item in data_list
            if item
            for result in [cls.from_dict(item)]
            if result is not None
        ]


# ResponseType = List[SaisonsModel]
