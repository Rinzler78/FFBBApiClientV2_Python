from __future__ import annotations

from ..models.multi_search_query import (
    CompetitionsMultiSearchQuery,
    OrganismesMultiSearchQuery,
    PratiquesMultiSearchQuery,
    RencontresMultiSearchQuery,
    SallesMultiSearchQuery,
    TerrainsMultiSearchQuery,
    TournoisMultiSearchQuery,
)


def generate_queries(search_name: str = None, limit: int | None = 1):
    return [
        OrganismesMultiSearchQuery(search_name, limit=limit),
        RencontresMultiSearchQuery(search_name, limit=limit),
        TerrainsMultiSearchQuery(search_name, limit=limit),
        CompetitionsMultiSearchQuery(search_name, limit=limit),
        SallesMultiSearchQuery(search_name, limit=limit),
        TournoisMultiSearchQuery(search_name, limit=limit),
        PratiquesMultiSearchQuery(search_name, limit=limit),
    ]
