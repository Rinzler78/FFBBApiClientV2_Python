"""Unit tests for OrganismesQuery and QueryFieldsManager ABC."""

from __future__ import annotations

import unittest


class TestOrganismesQuery(unittest.TestCase):
    """Tests for OrganismesQuery dataclass."""

    def test_organismes_query_default(self) -> None:
        from ffbb_api_client_v2.directus_ffbb.models.organismes_query import (
            OrganismesQuery,
        )

        query = OrganismesQuery()
        self.assertIsNone(query.fields_)

    def test_organismes_query_with_fields(self) -> None:
        from ffbb_api_client_v2.directus_ffbb.models.organismes_query import (
            OrganismesQuery,
        )

        query = OrganismesQuery(fields_=["id", "nom", "adresse"])
        self.assertEqual(query.fields_, ["id", "nom", "adresse"])


class TestQueryFieldsManagerABC(unittest.TestCase):
    """Tests for QueryFieldsManager abstract base class."""

    def test_query_fields_manager_is_abstract(self) -> None:
        from ffbb_api_client_v2.directus_ffbb.models.query_fields_manager import (
            QueryFieldsManager,
        )

        with self.assertRaises(TypeError):
            QueryFieldsManager()  # type: ignore[abstract]

    def test_query_fields_manager_concrete_subclass(self) -> None:
        from ffbb_api_client_v2.directus_ffbb.models.query_fields_manager import (
            QueryFieldsManager,
        )

        class ConcreteManager(QueryFieldsManager):
            @classmethod
            def get_fields(cls) -> list[str]:
                return ["id", "name", "status"]

        result = ConcreteManager.get_fields()
        self.assertEqual(result, ["id", "name", "status"])


if __name__ == "__main__":
    unittest.main()
