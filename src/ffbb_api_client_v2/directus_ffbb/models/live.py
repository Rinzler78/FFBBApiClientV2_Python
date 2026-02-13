from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ...models.clock import Clock
from ...models.external_id import ExternalID
from ...models.team_engagement import TeamEngagement
from ...utils.converter_utils import (
    from_datetime,
    from_int,
    from_obj,
    from_str,
)


@dataclass
class Live:
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
    clock: Clock | None = None
    competition_name: str | None = None
    current_status: str | None = None
    current_period: str | None = None
    match_status: str | None = None
    team_name_home: str | None = None
    team_name_out: str | None = None
    external_id: ExternalID | None = None
    team_engagement_home: TeamEngagement | None = None
    team_engagement_out: TeamEngagement | None = None

    @staticmethod
    def from_dict(obj: Any) -> Live:
        assert isinstance(obj, dict)
        match_id = from_int(obj, "matchId")
        match_time = from_datetime(obj, "matchTime")
        competition_abg_name = from_str(obj, "competitionAbgName")
        score_q1_home = from_int(obj, "score_q1_home")
        score_q2_home = from_int(obj, "score_q2_home")
        score_q3_home = from_int(obj, "score_q3_home")
        score_q4_home = from_int(obj, "score_q4_home")
        score_q1_out = from_int(obj, "score_q1_out")
        score_q2_out = from_int(obj, "score_q2_out")
        score_q3_out = from_int(obj, "score_q3_out")
        score_q4_out = from_int(obj, "score_q4_out")
        score_ot1_home = from_int(obj, "score_ot1_home")
        score_ot2_home = from_int(obj, "score_ot2_home")
        score_ot1_out = from_int(obj, "score_ot1_out")
        score_ot2_out = from_int(obj, "score_ot2_out")
        score_home = from_int(obj, "score_home")
        score_out = from_int(obj, "score_out")
        clock_val = obj.get("clock")
        clock = Clock.from_str(clock_val) if clock_val is not None else None
        competition_name = from_str(obj, "competitionName")
        current_status = from_str(obj, "currentStatus")
        current_period = from_str(obj, "currentPeriod")
        match_status = from_str(obj, "matchStatus")
        team_name_home = from_str(obj, "teamName_home")
        team_name_out = from_str(obj, "teamName_out")
        external_id = from_obj(ExternalID.from_dict, obj, "externalId")
        team_engagement_home = from_obj(
            TeamEngagement.from_dict, obj, "teamEngagement_home"
        )
        team_engagement_out = from_obj(
            TeamEngagement.from_dict, obj, "teamEngagement_out"
        )
        return Live(
            match_id=match_id,
            match_time=match_time,
            competition_abg_name=competition_abg_name,
            score_q1_home=score_q1_home,
            score_q2_home=score_q2_home,
            score_q3_home=score_q3_home,
            score_q4_home=score_q4_home,
            score_q1_out=score_q1_out,
            score_q2_out=score_q2_out,
            score_q3_out=score_q3_out,
            score_q4_out=score_q4_out,
            score_ot1_home=score_ot1_home,
            score_ot2_home=score_ot2_home,
            score_ot1_out=score_ot1_out,
            score_ot2_out=score_ot2_out,
            score_home=score_home,
            score_out=score_out,
            clock=clock,
            competition_name=competition_name,
            current_status=current_status,
            current_period=current_period,
            match_status=match_status,
            team_name_home=team_name_home,
            team_name_out=team_name_out,
            external_id=external_id,
            team_engagement_home=team_engagement_home,
            team_engagement_out=team_engagement_out,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.match_id is not None:
            result["matchId"] = str(self.match_id)
        if self.match_time is not None:
            result["matchTime"] = self.match_time.isoformat()
        if self.competition_abg_name is not None:
            result["competitionAbgName"] = self.competition_abg_name
        if self.score_q1_home is not None:
            result["score_q1_home"] = self.score_q1_home
        if self.score_q2_home is not None:
            result["score_q2_home"] = self.score_q2_home
        if self.score_q3_home is not None:
            result["score_q3_home"] = self.score_q3_home
        if self.score_q4_home is not None:
            result["score_q4_home"] = self.score_q4_home
        if self.score_q1_out is not None:
            result["score_q1_out"] = self.score_q1_out
        if self.score_q2_out is not None:
            result["score_q2_out"] = self.score_q2_out
        if self.score_q3_out is not None:
            result["score_q3_out"] = self.score_q3_out
        if self.score_q4_out is not None:
            result["score_q4_out"] = self.score_q4_out
        if self.score_ot1_home is not None:
            result["score_ot1_home"] = self.score_ot1_home
        if self.score_ot2_home is not None:
            result["score_ot2_home"] = self.score_ot2_home
        if self.score_ot1_out is not None:
            result["score_ot1_out"] = self.score_ot1_out
        if self.score_ot2_out is not None:
            result["score_ot2_out"] = self.score_ot2_out
        if self.score_home is not None:
            result["score_home"] = self.score_home
        if self.score_out is not None:
            result["score_out"] = self.score_out
        if self.clock is not None:
            result["clock"] = self.clock.to_str()
        if self.competition_name is not None:
            result["competitionName"] = self.competition_name
        if self.current_status is not None:
            result["currentStatus"] = self.current_status
        if self.current_period is not None:
            result["currentPeriod"] = self.current_period
        if self.match_status is not None:
            result["matchStatus"] = self.match_status
        if self.team_name_home is not None:
            result["teamName_home"] = self.team_name_home
        if self.team_name_out is not None:
            result["teamName_out"] = self.team_name_out
        if self.external_id is not None:
            result["externalId"] = self.external_id.to_dict()
        if self.team_engagement_home is not None:
            result["teamEngagement_home"] = self.team_engagement_home.to_dict()
        if self.team_engagement_out is not None:
            result["teamEngagement_out"] = self.team_engagement_out.to_dict()
        return result


def lives_from_dict(s: Any) -> list[Live]:
    return [Live.from_dict(item) for item in s]
