from typing import Any

from .multi_search_result_terrains import (
    TerrainsFacetDistribution,
    TerrainsFacetStats,
    TerrainsHit,
)
from .multi_search_results import MultiSearchResult


class TerrainsMultiSearchResult(
    MultiSearchResult[TerrainsHit, TerrainsFacetDistribution, TerrainsFacetStats]
):
    @staticmethod
    def from_dict(obj: Any) -> "TerrainsMultiSearchResult":
        return MultiSearchResult.from_dict(
            obj,
            TerrainsHit,
            TerrainsFacetDistribution,
            TerrainsFacetStats,
            TerrainsMultiSearchResult,
        )
