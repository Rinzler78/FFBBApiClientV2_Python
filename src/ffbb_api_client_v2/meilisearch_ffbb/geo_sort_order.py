from __future__ import annotations

from enum import Enum


class GeoSortOrder(str, Enum):
    """Sort order for geographic proximity searches."""

    NEAREST_FIRST = "asc"
    FARTHEST_FIRST = "desc"
