from dataclasses import dataclass
from typing import Any, Optional

from ffbb_api_client_v2.converters import from_none, from_str, from_union


@dataclass
class Saison:
    code: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Saison":
        assert isinstance(obj, dict)
        code = from_union([from_str, from_none], obj.get("code"))
        return Saison(code)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        return result
