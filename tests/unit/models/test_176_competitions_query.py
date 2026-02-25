"""Unit tests for CompetitionsQuery dataclass."""

from __future__ import annotations

import unittest

from ffbb_api_client_v2.directus_ffbb.models.competitions_query import (
    CompetitionsQuery,
)


class TestCompetitionsQuery(unittest.TestCase):
    def test_defaults(self) -> None:
        q = CompetitionsQuery()
        self.assertEqual(q.deep_phases_poules_rencontres__limit, "1000")
        self.assertIsNone(q.fields_)

    def test_custom_values(self) -> None:
        q = CompetitionsQuery(
            deep_phases_poules_rencontres__limit="500",
            fields_=["id", "nom"],
        )
        self.assertEqual(q.deep_phases_poules_rencontres__limit, "500")
        self.assertEqual(q.fields_, ["id", "nom"])


if __name__ == "__main__":
    unittest.main()
