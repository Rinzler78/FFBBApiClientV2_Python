from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class GameStatsModel:
    """Model for live game statistics from gsId field."""

    match_id: str | None = None
    current_status: str | None = None
    current_period: str | None = None

    # Score domicile (home team)
    score_q1_home: int | None = None
    score_q2_home: int | None = None
    score_q3_home: int | None = None
    score_q4_home: int | None = None
    score_ot1_home: int | None = None
    score_ot2_home: int | None = None

    # Score extérieur (away team)
    score_q1_out: int | None = None
    score_q2_out: int | None = None
    score_q3_out: int | None = None
    score_q4_out: int | None = None
    score_ot1_out: int | None = None
    score_ot2_out: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GameStatsModel | None:
        """Convert dictionary to GameStatsModel instance."""
        if not data:
            return None

        # Handle case where data is not a dictionary
        if not isinstance(data, dict):
            return None

        return cls(
            match_id=data.get("matchId"),
            current_status=data.get("currentStatus"),
            current_period=data.get("currentPeriod"),
            score_q1_home=data.get("score_q1_home"),
            score_q2_home=data.get("score_q2_home"),
            score_q3_home=data.get("score_q3_home"),
            score_q4_home=data.get("score_q4_home"),
            score_ot1_home=data.get("score_ot1_home"),
            score_ot2_home=data.get("score_ot2_home"),
            score_q1_out=data.get("score_q1_out"),
            score_q2_out=data.get("score_q2_out"),
            score_q3_out=data.get("score_q3_out"),
            score_q4_out=data.get("score_q4_out"),
            score_ot1_out=data.get("score_ot1_out"),
            score_ot2_out=data.get("score_ot2_out"),
        )
