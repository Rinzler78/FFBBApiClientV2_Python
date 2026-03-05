from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_str


@dataclass
class Saison:
    code: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> Saison:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        code = from_str(obj, "code")
        return Saison(code=code)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = self.code
        return result
