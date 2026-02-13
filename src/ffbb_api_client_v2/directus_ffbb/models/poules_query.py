from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PoulesQuery:
    deep_rencontres__limit: str | None = "1000"  # Original: deep[rencontres][_limit]
    fields_: list[str] | None = field(default=None)  # Original: fields[]
