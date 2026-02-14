from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_str


@dataclass
class LabellisationProgramme:
    id: str | None = None
    libelle: str | None = None
    labellisation_label: str | None = None
    logo_vertical: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> LabellisationProgramme:
        assert isinstance(obj, dict)
        return LabellisationProgramme(
            id=from_str(obj, "id"),
            libelle=from_str(obj, "libelle"),
            labellisation_label=from_str(obj, "labellisationLabel"),
            logo_vertical=from_str(obj, "logo_vertical"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.libelle is not None:
            result["libelle"] = self.libelle
        if self.labellisation_label is not None:
            result["labellisationLabel"] = self.labellisation_label
        if self.logo_vertical is not None:
            result["logo_vertical"] = self.logo_vertical
        return result
