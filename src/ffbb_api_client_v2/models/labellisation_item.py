from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ..utils.converter_utils import from_datetime, from_obj, from_str
from .labellisation_programme import LabellisationProgramme


@dataclass
class LabellisationItem:
    id: str | None = None
    debut: datetime | None = None
    fin: datetime | None = None
    id_labellisation_programme: LabellisationProgramme | None = None

    @staticmethod
    def from_dict(obj: Any) -> LabellisationItem:
        assert isinstance(obj, dict)
        return LabellisationItem(
            id=from_str(obj, "id"),
            debut=from_datetime(obj, "debut"),
            fin=from_datetime(obj, "fin"),
            id_labellisation_programme=from_obj(
                LabellisationProgramme.from_dict, obj, "idLabellisationProgramme"
            ),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.debut is not None:
            result["debut"] = self.debut.isoformat()
        if self.fin is not None:
            result["fin"] = self.fin.isoformat()
        if self.id_labellisation_programme is not None:
            result["idLabellisationProgramme"] = (
                self.id_labellisation_programme.to_dict()
            )
        return result
