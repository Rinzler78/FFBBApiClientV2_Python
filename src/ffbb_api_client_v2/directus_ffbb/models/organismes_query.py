from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class OrganismesQuery:
    fields_: list[str] | None = field(default=None)  # Original: fields[]
