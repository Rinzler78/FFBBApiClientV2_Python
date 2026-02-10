from __future__ import annotations

from ..models.competitions_multi_search_query import CompetitionsMultiSearchQuery
from ..models.engagements_multi_search_query import EngagementsMultiSearchQuery
from ..models.formations_multi_search_query import FormationsMultiSearchQuery
from ..models.organismes_multi_search_query import OrganismesMultiSearchQuery
from ..models.pratiques_multi_search_query import PratiquesMultiSearchQuery
from ..models.rencontres_multi_search_query import RencontresMultiSearchQuery
from ..models.salles_multi_search_query import SallesMultiSearchQuery
from ..models.terrains_multi_search_query import TerrainsMultiSearchQuery
from ..models.tournois_multi_search_query import TournoisMultiSearchQuery


def generate_queries(search_name: str | None = None, limit: int | None = 1):
    return [
        OrganismesMultiSearchQuery(search_name, limit=limit),
        RencontresMultiSearchQuery(search_name, limit=limit),
        TerrainsMultiSearchQuery(search_name, limit=limit),
        CompetitionsMultiSearchQuery(search_name, limit=limit),
        SallesMultiSearchQuery(search_name, limit=limit),
        TournoisMultiSearchQuery(search_name, limit=limit),
        PratiquesMultiSearchQuery(search_name, limit=limit),
        EngagementsMultiSearchQuery(search_name, limit=limit),
        FormationsMultiSearchQuery(search_name, limit=limit),
    ]
