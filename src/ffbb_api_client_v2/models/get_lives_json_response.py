from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from ..utils.converters import (
    from_datetime,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
    to_enum,
)
from .competition_id import CompetitionID
from .id_organisme_equipe import IDOrganismeEquipe
from .salle import Salle


class CompetitionAbgName(Enum):
    LBWL = "LBWL"
    LF2 = "LF2"
    NM1 = "NM1"


class Sexe(Enum):
    F = "F"
    M = "M"


class TypeCompetition(Enum):
    COUPE = "COUPE"
    DIV = "DIV"


class IDEngagementEquipe1:
    id: str

    def __init__(self, id: str) -> None:
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> "IDEngagementEquipe1":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        return IDEngagementEquipe1(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        return result


class Nom(Enum):
    GROUPE_A = "Groupe A"
    GROUPE_B = "Groupe B"
    POULE_A = "Poule A"


class IDPoule:
    id: str
    nom: Nom

    def __init__(self, id: str, nom: Nom) -> None:
        self.id = id
        self.nom = nom

    @staticmethod
    def from_dict(obj: Any) -> "IDPoule":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        nom = Nom(obj.get("nom"))
        return IDPoule(id, nom)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["nom"] = to_enum(Nom, self.nom)
        return result


class ExternalID:
    competition_id: CompetitionID
    id_engagement_equipe1: IDEngagementEquipe1
    id_engagement_equipe2: IDEngagementEquipe1
    id_organisme_equipe1: IDOrganismeEquipe
    id_organisme_equipe2: IDOrganismeEquipe
    id_poule: IDPoule
    nom_equipe1: str
    nom_equipe2: str
    numero_journee: int
    salle: Salle

    def __init__(
        self,
        competition_id: CompetitionID,
        id_engagement_equipe1: IDEngagementEquipe1,
        id_engagement_equipe2: IDEngagementEquipe1,
        id_organisme_equipe1: IDOrganismeEquipe,
        id_organisme_equipe2: IDOrganismeEquipe,
        id_poule: IDPoule,
        nom_equipe1: str,
        nom_equipe2: str,
        numero_journee: int,
        salle: Salle,
    ) -> None:
        self.competition_id = competition_id
        self.id_engagement_equipe1 = id_engagement_equipe1
        self.id_engagement_equipe2 = id_engagement_equipe2
        self.id_organisme_equipe1 = id_organisme_equipe1
        self.id_organisme_equipe2 = id_organisme_equipe2
        self.id_poule = id_poule
        self.nom_equipe1 = nom_equipe1
        self.nom_equipe2 = nom_equipe2
        self.numero_journee = numero_journee
        self.salle = salle

    @staticmethod
    def from_dict(obj: Any) -> "ExternalID":
        assert isinstance(obj, dict)
        competition_id = CompetitionID.from_dict(obj.get("competitionId"))
        id_engagement_equipe1 = IDEngagementEquipe1.from_dict(
            obj.get("idEngagementEquipe1")
        )
        id_engagement_equipe2 = IDEngagementEquipe1.from_dict(
            obj.get("idEngagementEquipe2")
        )
        id_organisme_equipe1 = IDOrganismeEquipe.from_dict(
            obj.get("idOrganismeEquipe1")
        )
        id_organisme_equipe2 = IDOrganismeEquipe.from_dict(
            obj.get("idOrganismeEquipe2")
        )
        id_poule = IDPoule.from_dict(obj.get("idPoule"))
        nom_equipe1 = from_str(obj.get("nomEquipe1"))
        nom_equipe2 = from_str(obj.get("nomEquipe2"))
        numero_journee = int(from_str(obj.get("numeroJournee")))
        salle = Salle.from_dict(obj.get("salle"))
        return ExternalID(
            competition_id,
            id_engagement_equipe1,
            id_engagement_equipe2,
            id_organisme_equipe1,
            id_organisme_equipe2,
            id_poule,
            nom_equipe1,
            nom_equipe2,
            numero_journee,
            salle,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["competitionId"] = to_class(CompetitionID, self.competition_id)
        result["idEngagementEquipe1"] = to_class(
            IDEngagementEquipe1, self.id_engagement_equipe1
        )
        result["idEngagementEquipe2"] = to_class(
            IDEngagementEquipe1, self.id_engagement_equipe2
        )
        result["idOrganismeEquipe1"] = to_class(
            IDOrganismeEquipe, self.id_organisme_equipe1
        )
        result["idOrganismeEquipe2"] = to_class(
            IDOrganismeEquipe, self.id_organisme_equipe2
        )
        result["idPoule"] = to_class(IDPoule, self.id_poule)
        result["nomEquipe1"] = from_str(self.nom_equipe1)
        result["nomEquipe2"] = from_str(self.nom_equipe2)
        result["numeroJournee"] = from_str(str(self.numero_journee))
        result["salle"] = to_class(Salle, self.salle)
        return result


class MatchStatus(Enum):
    COMPLETE = "COMPLETE"
    SCHEDULED = "SCHEDULED"


class TeamEngagement:
    code_abrege: str
    id: str
    logo: IDEngagementEquipe1
    nom_officiel: str
    nom_usuel: str

    def __init__(
        self,
        code_abrege: str,
        id: str,
        logo: IDEngagementEquipe1,
        nom_officiel: str,
        nom_usuel: str,
    ) -> None:
        self.code_abrege = code_abrege
        self.id = id
        self.logo = logo
        self.nom_officiel = nom_officiel
        self.nom_usuel = nom_usuel

    @staticmethod
    def from_dict(obj: Any) -> "TeamEngagement":
        assert isinstance(obj, dict)
        code_abrege = from_str(obj.get("codeAbrege"))
        id = from_str(obj.get("id"))
        logo = IDEngagementEquipe1.from_dict(obj.get("logo"))
        nom_officiel = from_str(obj.get("nomOfficiel"))
        nom_usuel = from_str(obj.get("nomUsuel"))
        return TeamEngagement(code_abrege, id, logo, nom_officiel, nom_usuel)

    def to_dict(self) -> dict:
        result: dict = {}
        result["codeAbrege"] = from_str(self.code_abrege)
        result["id"] = from_str(self.id)
        result["logo"] = to_class(IDEngagementEquipe1, self.logo)
        result["nomOfficiel"] = from_str(self.nom_officiel)
        result["nomUsuel"] = from_str(self.nom_usuel)
        return result


class Element:
    clock: Optional[datetime]
    competition_abg_name: CompetitionAbgName
    competition_name: str
    current_period: Optional[int]
    current_status: Optional[str]
    external_id: ExternalID
    match_id: int
    match_status: MatchStatus
    match_time: datetime
    score_home: int
    score_ot1_home: int
    score_ot1_out: int
    score_ot2_home: int
    score_ot2_out: int
    score_out: int
    score_q1_home: int
    score_q1_out: int
    score_q2_home: int
    score_q2_out: int
    score_q3_home: int
    score_q3_out: int
    score_q4_home: int
    score_q4_out: int
    team_engagement_home: TeamEngagement
    team_engagement_out: TeamEngagement
    team_name_home: str
    team_name_out: str
    venue_name: str

    def __init__(
        self,
        clock: Optional[datetime],
        competition_abg_name: CompetitionAbgName,
        competition_name: str,
        current_period: Optional[int],
        current_status: Optional[str],
        external_id: ExternalID,
        match_id: int,
        match_status: MatchStatus,
        match_time: datetime,
        score_home: int,
        score_ot1_home: int,
        score_ot1_out: int,
        score_ot2_home: int,
        score_ot2_out: int,
        score_out: int,
        score_q1_home: int,
        score_q1_out: int,
        score_q2_home: int,
        score_q2_out: int,
        score_q3_home: int,
        score_q3_out: int,
        score_q4_home: int,
        score_q4_out: int,
        team_engagement_home: TeamEngagement,
        team_engagement_out: TeamEngagement,
        team_name_home: str,
        team_name_out: str,
        venue_name: str,
    ) -> None:
        self.clock = clock
        self.competition_abg_name = competition_abg_name
        self.competition_name = competition_name
        self.current_period = current_period
        self.current_status = current_status
        self.external_id = external_id
        self.match_id = match_id
        self.match_status = match_status
        self.match_time = match_time
        self.score_home = score_home
        self.score_ot1_home = score_ot1_home
        self.score_ot1_out = score_ot1_out
        self.score_ot2_home = score_ot2_home
        self.score_ot2_out = score_ot2_out
        self.score_out = score_out
        self.score_q1_home = score_q1_home
        self.score_q1_out = score_q1_out
        self.score_q2_home = score_q2_home
        self.score_q2_out = score_q2_out
        self.score_q3_home = score_q3_home
        self.score_q3_out = score_q3_out
        self.score_q4_home = score_q4_home
        self.score_q4_out = score_q4_out
        self.team_engagement_home = team_engagement_home
        self.team_engagement_out = team_engagement_out
        self.team_name_home = team_name_home
        self.team_name_out = team_name_out
        self.venue_name = venue_name

    @staticmethod
    def from_dict(obj: Any) -> "Element":
        assert isinstance(obj, dict)
        clock = from_union([from_none, from_datetime], obj.get("clock"))
        competition_abg_name = CompetitionAbgName(obj.get("competitionAbgName"))
        competition_name = from_str(obj.get("competitionName"))
        current_period = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("currentPeriod")
        )
        current_status = from_union([from_none, from_str], obj.get("currentStatus"))
        external_id = ExternalID.from_dict(obj.get("externalId"))
        match_id = int(from_str(obj.get("matchId")))
        match_status = MatchStatus(obj.get("matchStatus"))
        match_time = from_datetime(obj.get("matchTime"))
        score_home = from_int(obj.get("score_home"))
        score_ot1_home = from_int(obj.get("score_ot1_home"))
        score_ot1_out = from_int(obj.get("score_ot1_out"))
        score_ot2_home = from_int(obj.get("score_ot2_home"))
        score_ot2_out = from_int(obj.get("score_ot2_out"))
        score_out = from_int(obj.get("score_out"))
        score_q1_home = from_int(obj.get("score_q1_home"))
        score_q1_out = from_int(obj.get("score_q1_out"))
        score_q2_home = from_int(obj.get("score_q2_home"))
        score_q2_out = from_int(obj.get("score_q2_out"))
        score_q3_home = from_int(obj.get("score_q3_home"))
        score_q3_out = from_int(obj.get("score_q3_out"))
        score_q4_home = from_int(obj.get("score_q4_home"))
        score_q4_out = from_int(obj.get("score_q4_out"))
        team_engagement_home = TeamEngagement.from_dict(obj.get("teamEngagement_home"))
        team_engagement_out = TeamEngagement.from_dict(obj.get("teamEngagement_out"))
        team_name_home = from_str(obj.get("teamName_home"))
        team_name_out = from_str(obj.get("teamName_out"))
        venue_name = from_str(obj.get("venueName"))
        return Element(
            clock,
            competition_abg_name,
            competition_name,
            current_period,
            current_status,
            external_id,
            match_id,
            match_status,
            match_time,
            score_home,
            score_ot1_home,
            score_ot1_out,
            score_ot2_home,
            score_ot2_out,
            score_out,
            score_q1_home,
            score_q1_out,
            score_q2_home,
            score_q2_out,
            score_q3_home,
            score_q3_out,
            score_q4_home,
            score_q4_out,
            team_engagement_home,
            team_engagement_out,
            team_name_home,
            team_name_out,
            venue_name,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["clock"] = from_union([from_none, lambda x: x.isoformat()], self.clock)
        result["competitionAbgName"] = to_enum(
            CompetitionAbgName, self.competition_abg_name
        )
        result["competitionName"] = from_str(self.competition_name)
        result["currentPeriod"] = from_union(
            [
                lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x)),
            ],
            self.current_period,
        )
        result["currentStatus"] = from_union([from_none, from_str], self.current_status)
        result["externalId"] = to_class(ExternalID, self.external_id)
        result["matchId"] = from_str(str(self.match_id))
        result["matchStatus"] = to_enum(MatchStatus, self.match_status)
        result["matchTime"] = self.match_time.isoformat()
        result["score_home"] = from_int(self.score_home)
        result["score_ot1_home"] = from_int(self.score_ot1_home)
        result["score_ot1_out"] = from_int(self.score_ot1_out)
        result["score_ot2_home"] = from_int(self.score_ot2_home)
        result["score_ot2_out"] = from_int(self.score_ot2_out)
        result["score_out"] = from_int(self.score_out)
        result["score_q1_home"] = from_int(self.score_q1_home)
        result["score_q1_out"] = from_int(self.score_q1_out)
        result["score_q2_home"] = from_int(self.score_q2_home)
        result["score_q2_out"] = from_int(self.score_q2_out)
        result["score_q3_home"] = from_int(self.score_q3_home)
        result["score_q3_out"] = from_int(self.score_q3_out)
        result["score_q4_home"] = from_int(self.score_q4_home)
        result["score_q4_out"] = from_int(self.score_q4_out)
        result["teamEngagement_home"] = to_class(
            TeamEngagement, self.team_engagement_home
        )
        result["teamEngagement_out"] = to_class(
            TeamEngagement, self.team_engagement_out
        )
        result["teamName_home"] = from_str(self.team_name_home)
        result["teamName_out"] = from_str(self.team_name_out)
        result["venueName"] = from_str(self.venue_name)
        return result


class GetLivesJsonResponse:
    elements: List[Element]

    def __init__(self, elements: List[Element]) -> None:
        self.elements = elements

    @staticmethod
    def from_dict(obj: Any) -> "GetLivesJsonResponse":
        assert isinstance(obj, dict)
        elements = from_list(Element.from_dict, obj.get("elements"))
        return GetLivesJsonResponse(elements)

    def to_dict(self) -> dict:
        result: dict = {}
        result["elements"] = from_list(lambda x: to_class(Element, x), self.elements)
        return result


def get_lives_json_response_from_dict(s: Any) -> GetLivesJsonResponse:
    return GetLivesJsonResponse.from_dict(s)


def get_lives_json_response_to_dict(x: GetLivesJsonResponse) -> Any:
    return to_class(GetLivesJsonResponse, x)
