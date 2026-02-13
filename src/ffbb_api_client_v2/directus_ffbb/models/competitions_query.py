from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CompetitionsQuery:
    deep_phases_poules_rencontres__limit: str | None = (
        "1000"  # Original: deep[phases][poules][rencontres][_limit]
    )
    fields_: list[str] | None = field(default=None)  # Original: fields[]
