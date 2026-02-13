from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SaisonsQuery:
    fields_: list[str] | None = field(default=None)  # Original: fields[]
    filter: str | None = '{"actif":{"_eq":true}}'  # Original: filter
