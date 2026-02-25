"""Unit tests for game_stats_models backward-compatibility re-export."""

from __future__ import annotations

import unittest


class TestGameStatsModelsReExport(unittest.TestCase):
    def test_import_from_shim(self) -> None:
        from ffbb_api_client_v2.directus_ffbb.models.game_stats_models import (
            GameStatsModel,
        )
        from ffbb_api_client_v2.models.game_stats_model import (
            GameStatsModel as Original,
        )

        self.assertIs(GameStatsModel, Original)

    def test_all_export(self) -> None:
        from ffbb_api_client_v2.directus_ffbb.models import game_stats_models

        self.assertIn("GameStatsModel", game_stats_models.__all__)


if __name__ == "__main__":
    unittest.main()
