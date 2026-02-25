"""Unit tests for FacetDistribution abstract base class."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.meilisearch.models.facet_distribution import (
    FacetDistribution,
)


class ConcreteFacetDistribution(FacetDistribution):
    """Minimal concrete subclass for testing."""

    def to_dict(self) -> dict[str, Any]:
        return super().to_dict()


class TestFacetDistributionAbstract(unittest.TestCase):
    def test_base_to_dict_returns_empty(self) -> None:
        concrete = ConcreteFacetDistribution()
        self.assertEqual(concrete.to_dict(), {})

    def test_from_dict_raises(self) -> None:
        with self.assertRaises(AssertionError):
            FacetDistribution.from_dict({"key": "value"})

    def test_cannot_instantiate_abstract(self) -> None:
        with self.assertRaises(TypeError):
            FacetDistribution()  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
