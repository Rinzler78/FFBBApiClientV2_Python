from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_bool, from_obj, from_str
from .competition_base import CompetitionBase
from .competition_origine import CompetitionOrigine


@dataclass
class Competition(CompetitionBase):
    """Competition as returned by Meilisearch search results."""

    creation_en_cours: bool | None = None
    live_stat: bool | None = None
    publication_internet: str | None = None
    pro: bool | None = None
    competition_origine: CompetitionOrigine | None = None
    nom_extended: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> Competition:
        try:
            assert isinstance(obj, dict)
            base = CompetitionBase._parse_base(obj)
            return Competition(
                **base,
                creation_en_cours=from_bool(obj, "creationEnCours"),
                live_stat=from_bool(obj, "liveStat"),
                publication_internet=from_str(obj, "publicationInternet"),
                pro=from_bool(obj, "pro"),
                competition_origine=from_obj(
                    CompetitionOrigine.from_dict, obj, "competition_origine"
                ),
                nom_extended=from_str(obj, "nomExtended"),
            )
        except Exception as e:
            raise ValueError("Invalid Competition object") from e

    def to_dict(self) -> dict:
        result = self._base_to_dict()
        if self.creation_en_cours is not None:
            result["creationEnCours"] = self.creation_en_cours
        if self.live_stat is not None:
            result["liveStat"] = self.live_stat
        if self.publication_internet is not None:
            result["publicationInternet"] = self.publication_internet
        if self.pro is not None:
            result["pro"] = self.pro
        if self.competition_origine is not None:
            result["competition_origine"] = self.competition_origine.to_dict()
        if self.nom_extended is not None:
            result["nomExtended"] = self.nom_extended
        return result
