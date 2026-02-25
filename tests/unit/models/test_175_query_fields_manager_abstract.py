"""Unit tests for QueryFieldsManager abstract base class."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.directus_ffbb.models.query_fields_manager import (
    QueryFieldsManager,
)


class ConcreteFieldsManager(QueryFieldsManager):
    """Minimal concrete subclass for testing."""

    @classmethod
    def get_fields(cls) -> list[str]:
        return ["id", "nom"]


class TestQueryFieldsManagerAbstract(unittest.TestCase):
    def test_concrete_get_fields(self) -> None:
        fields = ConcreteFieldsManager.get_fields()
        self.assertEqual(fields, ["id", "nom"])

    def test_cannot_instantiate_abstract(self) -> None:
        with self.assertRaises(TypeError):
            QueryFieldsManager()  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
