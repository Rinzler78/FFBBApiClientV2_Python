from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_none, from_str, from_union


class Saison:
    code: str | None = None

    def __init__(self, code: str | None) -> None:
        self.code = code

    @staticmethod
    def from_dict(obj: Any) -> Saison:
        assert isinstance(obj, dict)
        code = from_union([from_str, from_none], obj.get("code"))
        return Saison(code)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        return result
