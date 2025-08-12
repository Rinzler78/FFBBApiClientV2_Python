from __future__ import annotations

from datetime import datetime
from typing import Any

from ..utils.converter_utils import (
    from_datetime,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
)
from .external_id import ExternalID
from .TeamEngagement import TeamEngagement


class Clock:
    minutes: int
    seconds: int
    milliseconds: int

    def __init__(self, minutes: int, seconds: int, milliseconds: int):
        self.minutes = minutes
        self.seconds = seconds
        self.milliseconds = milliseconds

    @staticmethod
    def from_str(obj: str) -> Clock:
        minutes, seconds, milliseconds = obj.split(":") if obj else ["0", "0", "0"]
        return Clock(int(minutes), int(seconds), int(milliseconds))

    def to_str(self) -> str:
        return f"{self.minutes}:{self.seconds}:{self.milliseconds}"


class Live:
    clock: Clock
    current_status: None
    current_period: None
    match_id: int | None = None
    match_time: datetime | None = None
    competition_abg_name: str | None = None
    score_q1_home: int | None = None
    score_q2_home: int | None = None
    score_q3_home: int | None = None
    score_q4_home: int | None = None
    score_q1_out: int | None = None
    score_q2_out: int | None = None
    score_q3_out: int | None = None
    score_q4_out: int | None = None
    score_ot1_home: int | None = None
    score_ot2_home: int | None = None
    score_ot1_out: int | None = None
    score_ot2_out: int | None = None
    score_home: int | None = None
    score_out: int | None = None

    competition_name: str | None = None

    match_status: str | None = None
    team_name_home: str | None = None
    team_name_out: str | None = None
    external_id: ExternalID | None = None
    team_engagement_home: TeamEngagement | None = None
    team_engagement_out: TeamEngagement | None = None

    def __init__(
        self,
        match_id: int | None,
        match_time: datetime | None,
        competition_abg_name: str | None,
        score_q1_home: int | None,
        score_q2_home: int | None,
        score_q3_home: int | None,
        score_q4_home: int | None,
        score_q1_out: int | None,
        score_q2_out: int | None,
        score_q3_out: int | None,
        score_q4_out: int | None,
        score_ot1_home: int | None,
        score_ot2_home: int | None,
        score_ot1_out: int | None,
        score_ot2_out: int | None,
        score_home: int | None,
        score_out: int | None,
        clock: Clock,
        competition_name: str | None,
        current_status: None,
        current_period: None,
        match_status: str | None,
        team_name_home: str | None,
        team_name_out: str | None,
        external_id: ExternalID | None,
        team_engagement_home: TeamEngagement | None,
        team_engagement_out: TeamEngagement | None,
    ) -> None:
        self.match_id = match_id
        self.match_time = match_time
        self.competition_abg_name = competition_abg_name
        self.score_q1_home = score_q1_home
        self.score_q2_home = score_q2_home
        self.score_q3_home = score_q3_home
        self.score_q4_home = score_q4_home
        self.score_q1_out = score_q1_out
        self.score_q2_out = score_q2_out
        self.score_q3_out = score_q3_out
        self.score_q4_out = score_q4_out
        self.score_ot1_home = score_ot1_home
        self.score_ot2_home = score_ot2_home
        self.score_ot1_out = score_ot1_out
        self.score_ot2_out = score_ot2_out
        self.score_home = score_home
        self.score_out = score_out
        self.clock = clock
        self.competition_name = competition_name
        self.current_status = current_status
        self.current_period = current_period
        self.match_status = match_status
        self.team_name_home = team_name_home
        self.team_name_out = team_name_out
        self.external_id = external_id
        self.team_engagement_home = team_engagement_home
        self.team_engagement_out = team_engagement_out

    @staticmethod
    def from_dict(obj: Any) -> Live:
        """
        Construct a Live object from a dictionary.

        Args:
            obj (Any): The dictionary containing the Live object data.

        Returns:
            Live: The constructed Live object.
        """
        assert isinstance(obj, dict)
        match_id = from_union(
            [lambda x: int(from_str(x)), from_none], obj.get("matchId")
        )
        match_time = from_union([from_datetime, from_none], obj.get("matchTime"))
        competition_abg_name = from_union(
            [from_str, from_none], obj.get("competitionAbgName")
        )
        score_q1_home = from_union([from_int, from_none], obj.get("score_q1_home"))
        score_q2_home = from_union([from_int, from_none], obj.get("score_q2_home"))
        score_q3_home = from_union([from_int, from_none], obj.get("score_q3_home"))
        score_q4_home = from_union([from_int, from_none], obj.get("score_q4_home"))
        score_q1_out = from_union([from_int, from_none], obj.get("score_q1_out"))
        score_q2_out = from_union([from_int, from_none], obj.get("score_q2_out"))
        score_q3_out = from_union([from_int, from_none], obj.get("score_q3_out"))
        score_q4_out = from_union([from_int, from_none], obj.get("score_q4_out"))
        score_ot1_home = from_union([from_int, from_none], obj.get("score_ot1_home"))
        score_ot2_home = from_union([from_int, from_none], obj.get("score_ot2_home"))
        score_ot1_out = from_union([from_int, from_none], obj.get("score_ot1_out"))
        score_ot2_out = from_union([from_int, from_none], obj.get("score_ot2_out"))
        score_home = from_union([from_int, from_none], obj.get("score_home"))
        score_out = from_union([from_int, from_none], obj.get("score_out"))
        clock = from_union([Clock.from_str, from_none], obj.get("clock"))
        competition_name = from_union([from_str, from_none], obj.get("competitionName"))
        current_status = from_union([from_str, from_none], obj.get("currentStatus"))
        current_period = from_union([from_str, from_none], obj.get("currentPeriod"))
        match_status = from_union([from_str, from_none], obj.get("matchStatus"))
        team_name_home = from_union([from_str, from_none], obj.get("teamName_home"))
        team_name_out = from_union([from_str, from_none], obj.get("teamName_out"))
        external_id = from_union(
            [ExternalID.from_dict, from_none], obj.get("externalId")
        )
        team_engagement_home = from_union(
            [TeamEngagement.from_dict, from_none], obj.get("teamEngagement_home")
        )
        team_engagement_out = from_union(
            [TeamEngagement.from_dict, from_none], obj.get("teamEngagement_out")
        )
        return Live(
            match_id,
            match_time,
            competition_abg_name,
            score_q1_home,
            score_q2_home,
            score_q3_home,
            score_q4_home,
            score_q1_out,
            score_q2_out,
            score_q3_out,
            score_q4_out,
            score_ot1_home,
            score_ot2_home,
            score_ot1_out,
            score_ot2_out,
            score_home,
            score_out,
            clock,
            competition_name,
            current_status,
            current_period,
            match_status,
            team_name_home,
            team_name_out,
            external_id,
            team_engagement_home,
            team_engagement_out,
        )

    def to_dict(self) -> dict:
        """
        Convert the Live object to a dictionary.

        Returns:
            dict: The Live object as a dictionary.
        """
        result: dict = {}
        if self.match_id is not None:
            result["matchId"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.match_id,
            )
        if self.match_time is not None:
            result["matchTime"] = from_union(
                [lambda x: x.isoformat(), from_none], self.match_time
            )
        if self.competition_abg_name is not None:
            result["competitionAbgName"] = from_union(
                [from_str, from_none], self.competition_abg_name
            )
        if self.score_q1_home is not None:
            result["score_q1_home"] = from_union(
                [from_int, from_none], self.score_q1_home
            )
        if self.score_q2_home is not None:
            result["score_q2_home"] = from_union(
                [from_int, from_none], self.score_q2_home
            )
        if self.score_q3_home is not None:
            result["score_q3_home"] = from_union(
                [from_int, from_none], self.score_q3_home
            )
        if self.score_q4_home is not None:
            result["score_q4_home"] = from_union(
                [from_int, from_none], self.score_q4_home
            )
        if self.score_q1_out is not None:
            result["score_q1_out"] = from_union(
                [from_int, from_none], self.score_q1_out
            )
        if self.score_q2_out is not None:
            result["score_q2_out"] = from_union(
                [from_int, from_none], self.score_q2_out
            )
        if self.score_q3_out is not None:
            result["score_q3_out"] = from_union(
                [from_int, from_none], self.score_q3_out
            )
        if self.score_q4_out is not None:
            result["score_q4_out"] = from_union(
                [from_int, from_none], self.score_q4_out
            )
        if self.score_ot1_home is not None:
            result["score_ot1_home"] = from_union(
                [from_int, from_none], self.score_ot1_home
            )
        if self.score_ot2_home is not None:
            result["score_ot2_home"] = from_union(
                [from_int, from_none], self.score_ot2_home
            )
        if self.score_ot1_out is not None:
            result["score_ot1_out"] = from_union(
                [from_int, from_none], self.score_ot1_out
            )
        if self.score_ot2_out is not None:
            result["score_ot2_out"] = from_union(
                [from_int, from_none], self.score_ot2_out
            )
        if self.score_home is not None:
            result["score_home"] = from_union([from_int, from_none], self.score_home)
        if self.score_out is not None:
            result["score_out"] = from_union([from_int, from_none], self.score_out)
        if self.clock is not None:
            result["clock"] = from_union([Clock.to_str, from_none], self.clock)
        if self.competition_name is not None:
            result["competitionName"] = from_union(
                [from_str, from_none], self.competition_name
            )
        if self.current_status is not None:
            result["currentStatus"] = from_union(
                [from_str, from_none], self.current_status
            )
        if self.current_period is not None:
            result["currentPeriod"] = from_union(
                [from_str, from_none], self.current_period
            )
        if self.match_status is not None:
            result["matchStatus"] = from_union([from_str, from_none], self.match_status)
        if self.team_name_home is not None:
            result["teamName_home"] = from_union(
                [from_str, from_none], self.team_name_home
            )
        if self.team_name_out is not None:
            result["teamName_out"] = from_union(
                [from_str, from_none], self.team_name_out
            )
        if self.external_id is not None:
            result["externalId"] = from_union(
                [lambda x: to_class(ExternalID, x), from_none], self.external_id
            )
        if self.team_engagement_home is not None:
            result["teamEngagement_home"] = from_union(
                [lambda x: to_class(TeamEngagement, x), from_none],
                self.team_engagement_home,
            )
        if self.team_engagement_out is not None:
            result["teamEngagement_out"] = from_union(
                [lambda x: to_class(TeamEngagement, x), from_none],
                self.team_engagement_out,
            )
        return result


def lives_from_dict(s: Any) -> list[Live]:
    """
    Convert a list of dictionaries to a list of Live objects.

    Args:
        s (Any): The list of dictionaries.

    Returns:
        List[Live]: The list of Live objects.
    """
    return from_list(Live.from_dict, s)


def lives_to_dict(x: list[Live]) -> Any:
    """
    Convert a list of Live objects to a list of dictionaries.

    Args:
        x (List[Live]): The list of Live objects.

    Returns:
        Any: The list of dictionaries.
    """
    return from_list(lambda x: to_class(Live, x), x)
